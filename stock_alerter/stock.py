from datetime import datetime
from collections import deque, namedtuple


class Stock:
    '''Manage stock state through events.'''

    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = deque(maxlen=3)

    def update(self, cur_update, price):
        if price < 0:
            raise ValueError('Price must not be negative.')
        self.price_history.append(StockUpdate(update_time=cur_update, price=price))
        self.price_history = sorted(self.price_history, key=lambda update: update.update_time)

    @property
    def price(self):
        return self.price_history[-1].price if self.price_history else None

    @property
    def increasing_trend_is(self):
        return all(self.price_history[i].price < self.price_history[i + 1].price for i in range(len(self.price_history) - 1))

StockUpdate = namedtuple('StockUpdate', ['update_time', 'price'])
