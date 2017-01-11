from d3a.models.appliance.simple import SimpleAppliance
from d3a.models.area import Area
from d3a.models.strategy.commercial_producer import CommercialStrategy
from d3a.models.strategy.fridge import FridgeStrategy
from d3a.models.strategy.permanent import PermanentLoadStrategy
from d3a.models.strategy.pv import PVStrategy
from d3a.models.strategy.storage import StorageStrategy


def get_setup(config):
    area = Area(
        'Grid',
        [
            Area(
                'Street 1',
                [
                    Area(
                        'S1 House 1',
                        [
                            Area('S1 H1 Fridge 1', strategy=FridgeStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S1 H1 Fridge 2', strategy=FridgeStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S1 H1 Load', strategy=PermanentLoadStrategy(),
                                 appliance=SimpleAppliance()),
                        ]
                    ),
                    Area(
                        'S1 House 2',
                        [
                            Area('S1 H2 PV', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S1 H2 Fridge', strategy=FridgeStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S1 H2 Load 1', strategy=PermanentLoadStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S1 H2 Load 2', strategy=PermanentLoadStrategy(80),
                                 appliance=SimpleAppliance()),
                        ]
                    ),
                    Area(
                        'S1 House 3',
                        [
                            Area('S1 H3 PV 1', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S1 H3 PV 2', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S1 H3 PV 3', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S1 H3 Storage', strategy=StorageStrategy(80),
                                 appliance=SimpleAppliance()),
                        ]
                    ),
                ]
            ),
            Area(
                'Street 2',
                [
                    Area(
                        'S2 House 1',
                        [
                            Area('S2 H1 Fridge 1', strategy=FridgeStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S2 H1 Fridge 2', strategy=FridgeStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S2 H1 Load 1', strategy=PermanentLoadStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S2 H1 Load 2', strategy=PermanentLoadStrategy(80),
                                 appliance=SimpleAppliance()),
                        ]
                    ),
                    Area(
                        'S2 House 2',
                        [
                            Area('S2 H2 PV', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S2 H2 Fridge', strategy=FridgeStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S2 H2 Load 1', strategy=PermanentLoadStrategy(50),
                                 appliance=SimpleAppliance()),
                            Area('S2 H2 Load 2', strategy=PermanentLoadStrategy(80),
                                 appliance=SimpleAppliance()),
                            Area('S2 H2 Load 3', strategy=PermanentLoadStrategy(40),
                                 appliance=SimpleAppliance()),
                            Area('S2 H2 Load 4', strategy=PermanentLoadStrategy(10),
                                 appliance=SimpleAppliance()),
                        ]
                    ),
                    Area(
                        'S2 House 3',
                        [
                            Area('S2 H3 PV 1', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S2 H3 PV 2', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S2 H3 PV 3', strategy=PVStrategy(100),
                                 appliance=SimpleAppliance()),
                            Area('S2 H3 Storage', strategy=StorageStrategy(80),
                                 appliance=SimpleAppliance()),
                        ]
                    ),
                ]
            ),
            Area('Commercial Energy Producer', strategy=CommercialStrategy(energy_price=30))
        ],
        config=config
    )
    return area