from datetime import datetime
from collections import deque


class Stock:
    '''Manage stock state through events.'''

    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = deque(maxlen=3)
        self.last_updated = datetime.utcnow()

    def update(self, cur_update, price):
        if price < 0:
            raise ValueError('Price must not be negative.')

        self.last_updated = cur_update
        self.price_history.append(price)
    @property
    def price(self):
        return self.price_history[-1] if self.price_history else None

    @property
    def increasing_trend_is(self):
        return all(self.price_history[i] < self.price_history[i + 1] for i in range(len(self.price_history) - 1))

