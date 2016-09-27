from datetime import datetime, timedelta
import pytest


class TestStock:
    """Stock's """

    def test_price_of_a_new_stock_class_should_be_None(self, stock):
        """price should initialize with None."""
        assert stock.price is None

    def test_stock_update(self, stock, timestamp):
        """update should set the price."""
        stock.update(timestamp, price = 10)
        assert stock.price == 10

    def test_update_price_should_be_not_negative(self, stock, timestamp):
        """update should throw an error if price is negative."""
        with pytest.raises(ValueError) as excinfo:
            stock.update(timestamp, price=-10)
        assert 'negative' in str(excinfo.value)

    def test_price_should_give_latest_price_by_timestamp(self, stock, timestamp):
        """price should return the latest price added."""

        stock.update(timestamp, price = 8.4)
        stock.update(timestamp - timedelta(days=1), price = 10)
        assert stock.price == pytest.approx(8.4)

    trend_data = [ ([8,10,12],True), ([8,12,10],False), ([8,10,10],False), ]
    trend_ids = ["increasing numbers are True", "decreasing numbers are False", "same numbers are False"]

    @pytest.mark.parametrize("prices,expected", trend_data, ids=trend_ids)
    def test_increasing_trend_is(self, stock, timestamp_list, prices, expected):
        """increasing_trend_is should be True if the previous three price updates were increases, else False."""
        timestamps = timestamp_list(3)
        for timestamp, price in zip(timestamps, prices):
            stock.update(timestamp, price)
        assert stock.increasing_trend_is is expected


