from datetime import datetime


class Stock:
    '''Manage stock state through events.'''

    def __init__(self, symbol):
        self.symbol = symbol
        self.price = None
        self.last_updated = datetime.utcnow()

    def update(self, cur_update, price):
        if price < 0:
            raise ValueError('Price must not be negative.')

        self.last_updated = cur_update
        self.price = price

