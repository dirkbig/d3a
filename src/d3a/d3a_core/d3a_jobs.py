"""
Copyright 2018 Grid Singularity
This file is part of D3A.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import logging
from os import environ, getpid
import ast

from datetime import datetime
from pendulum import now, duration, instance
from redis import StrictRedis
from rq import Connection, Worker, get_current_job
from rq.decorators import job

from d3a.models.config import SimulationConfig
from d3a.d3a_core.util import available_simulation_scenarios, update_advanced_settings
from d3a.d3a_core.simulation import run_simulation
from d3a_interface.constants_limits import GlobalConfig, ConstSettings
from d3a_interface.settings_validators import validate_global_settings


@job('d3a')
def start(scenario, settings, events):
    logging.getLogger().setLevel(logging.ERROR)

    job = get_current_job()
    job.save_meta()

    try:
        if settings is None:
            settings = {}
        else:
            settings = {k: v for k, v in settings.items() if v is not None and v != "None"}

        advanced_settings = settings.get('advanced_settings', None)
        if advanced_settings is not None:
            update_advanced_settings(ast.literal_eval(advanced_settings))

        if events is not None:
            events = ast.literal_eval(events)

        config_settings = {
            "start_date":
                instance(datetime.combine(settings.get('start_date'), datetime.min.time()))
                if 'start_date' in settings else GlobalConfig.start_date,
            "sim_duration":
                duration(days=settings['duration'].days)
                if 'duration' in settings else GlobalConfig.sim_duration,
            "slot_length":
                duration(seconds=settings['slot_length'].seconds)
                if 'slot_length' in settings else GlobalConfig.slot_length,
            "tick_length":
                duration(seconds=settings['tick_length'].seconds)
                if 'tick_length' in settings else GlobalConfig.tick_length,
            "market_maker_rate":
                settings.get('market_maker_rate',
                             str(ConstSettings.GeneralSettings.DEFAULT_MARKET_MAKER_RATE)),
            "market_count": settings.get('market_count', GlobalConfig.market_count),
            "cloud_coverage": settings.get('cloud_coverage', GlobalConfig.cloud_coverage),
            "pv_user_profile": settings.get('pv_user_profile', None),
            "iaa_fee": settings.get('iaa_fee', GlobalConfig.iaa_fee),
            "max_panel_power_W": settings.get('max_panel_power_W',
                                              ConstSettings.PVSettings.MAX_PANEL_OUTPUT_W)
        }

        validate_global_settings(config_settings)

        config = SimulationConfig(**config_settings)

        spot_market_type = settings.get('spot_market_type', None)
        if spot_market_type is not None:
            ConstSettings.IAASettings.MARKET_TYPE = spot_market_type

        if scenario is None:
            scenario_name = "default_2a"
        elif scenario in available_simulation_scenarios:
            scenario_name = scenario
        else:
            scenario_name = 'json_arg'
            config.area = scenario

        kwargs = {"no_export": True,
                  "pricing_scheme": 0,
                  "seed": settings.get('random_seed', 0)}

        run_simulation(setup_module_name=scenario_name,
                       simulation_config=config,
                       simulation_events=events,
                       slowdown=settings.get('slowdown', 0),
                       redis_job_id=job.id,
                       kwargs=kwargs)
    except Exception:
        import traceback
        from d3a.d3a_core.redis_connections.redis_communication import publish_job_error_output
        publish_job_error_output(job.id, traceback.format_exc())
        logging.getLogger().error(f"Error on jobId {job.id}: {traceback.format_exc()}")


@job('d3a')
def get_simulation_scenarios():
    return available_simulation_scenarios


def main():
    with Connection(StrictRedis.from_url(environ.get('REDIS_URL', 'redis://localhost'))):
        Worker(
            ['d3a'],
            name='simulation.{}.{:%s}'.format(getpid(), now())
        ).work()


if __name__ == "__main__":
    main()
