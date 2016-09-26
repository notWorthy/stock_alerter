from datetime import datetime
import pytest
from stock_alerter import stock


class TestStock:
    """Stock's """

    @pytest.fixture()
    def sample_stock(self):
        yield stock.Stock("Goog")

    def test_price_of_a_new_stock_class_should_be_None(self, sample_stock):
        """price should initialize with None."""
        assert sample_stock.price is None

    def test_stock_update(self, sample_stock):
        """update should set the price."""
        sample_stock.update(datetime(2016, 9, 23), price = 10)
        assert sample_stock.price == 10

    def test_update_price_should_be_nonnegative(self, sample_stock):
        """update should throw an error if price is negative."""
        with pytest.raises(ValueError) as excinfo:
            sample_stock.update(datetime(2016, 9, 23), price=-10)
        assert 'negative' in str(excinfo.value)

    def test_price_should_give_latest_price_by_timestamp(self, sample_stock):
        """price should return the latest price added."""
        sample_stock.update(datetime(2016, 9, 23), price = 8.4)
        sample_stock.update(datetime(2016, 9, 22), price = 10)
        assert sample_stock.price == pytest.approx(8.4)

    trend_data = [ ([8,10,12],True), ([8,12,10],False), ([8,10,10],False), ]
    trend_ids = ["increasing numbers are True", "decreasing numbers are False", "same numbers are False"]
    @pytest.mark.parametrize("prices,expected",trend_data, ids=trend_ids )
    def test_increasing_trend_is(self, sample_stock, prices, expected):
        """increasing_trend_is should be True if the previous three price updates were increases, else False."""
        timestamps = [datetime(2016, 9, 22), datetime(2016, 9, 23), datetime(2016, 9, 24)]
        for timestamp, price in zip(timestamps, prices):
            sample_stock.update(timestamp, price)
        assert sample_stock.increasing_trend_is is expected

