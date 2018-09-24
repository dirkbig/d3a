from d3a.exceptions import MarketException
from d3a.models.strategy.base import BaseStrategy
from d3a.models.state import LoadState


class PermanentLoadStrategy(BaseStrategy):
    parameters = ('energy', 'pre_buy_range')

    def __init__(self, energy=100, pre_buy_range=4):
        if energy <= 0 or pre_buy_range <= 1:
            raise ValueError("Incorrect parameter values for PermanentLoad.")
        super().__init__()
        self.energy = energy
        self.pre_buy_range = pre_buy_range
        self.state = LoadState()
        self.bought_in_market = set()

    def event_tick(self, *, area_id):
        area = self.get_area_from_area_id(area_id)
        try:
            for i, market in enumerate(area.markets.values()):
                if i + 1 > self.pre_buy_range:
                    break
                if market in self.bought_in_market:
                    continue
                for offer in market.sorted_offers:
                    if offer.energy < self.energy / 1000:
                        continue
                    try:
                        self.accept_offer(market, offer)
                        self.bought_in_market.add(market)
                        break
                    except MarketException:
                        # Offer already gone etc., use next one.
                        continue
        except IndexError:
            pass

    def _update_energy_requirement(self):
        self.state.record_desired_energy(self.area, self.energy)

    def event_market_cycle(self):
        self._update_energy_requirement()
