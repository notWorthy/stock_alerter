from datetime import datetime, timedelta
from collections import deque, namedtuple


class Stock:
    """Manage state and pricing history for stock.

    Initialized with a string representing the stock market symbol for the stock.
    """

    def __init__(self, symbol):
        self.symbol = symbol
        self.price_history = deque(maxlen=3)

    def update(self, timestamp, price):
        """Inserts price into appropriate spot in price history ordered by timestamp."""
        if price < 0:
            raise ValueError('Price must not be negative.')
        self.price_history.append(PriceEvent(timestamp=timestamp, price=price))
        self.price_history = sorted(self.price_history, key=lambda update: update.timestamp)

    @property
    def price(self):
        """Return latest price for stock by timestamp."""
        return self.price_history[-1].price if self.price_history else None

    @property
    def increasing_trend_is(self):
        """Return truth of whether stock was explicitly increasing in recent history."""
        return all(self.price_history[i].price < self.price_history[i + 1].price
                   for i in range(len(self.price_history) - 1))

    def get_crossover_signal(self, on_date):
        closing_price_list = []
        for i in range(11):
            chk = on_date.date() - timedelta(i)
            for price_event in reversed(self.price_history):
                date = price_event.timestamp.date()
                if date <= chk:
                    closing_price_list.insert(0, price_event)

        # Return NEUTRAL signal
        if len(closing_price_list) < 11:
            return 0

        def get_slice_avg(slice, period):
            return sum([update.price for update in slice]) / period

        ten_day_avg_older = get_slice_avg(closing_price_list[-11:-1], 10)
        five_day_avg_older = get_slice_avg(closing_price_list[-6:-1], 5)
        ten_day_avg_newer = get_slice_avg(closing_price_list[-10:], 10)
        five_day_avg_newer = get_slice_avg(closing_price_list[-5:], 5)

        # BUY signal
        if ten_day_avg_older > five_day_avg_older and ten_day_avg_newer < five_day_avg_newer:
            return 1

        # SELL signal
        if ten_day_avg_older < five_day_avg_older and ten_day_avg_newer > five_day_avg_newer:
            return -1

        # NEUTRAL signal
        return 0

PriceEvent = namedtuple('PriceEvent', ['timestamp', 'price'])
