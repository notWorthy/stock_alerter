from datetime import datetime, timedelta
import pytest

from stock_alerter.stock import Stock
# def pytest_itemcollected(item):
#     par = item.parent.obj
#     node = item.obj
#     pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
#     suf = node.__doc__.strip() if node.__doc__ else node.__name__
#     if pref or suf:
#         item._nodeid = ' '.join((pref, suf))
@pytest.fixture()
def stock():
    return Stock("GOOG")

@pytest.fixture()
def timestamp():
    return datetime.now()

@pytest.fixture()
def timestamp_list():
    def create_timestamps(length=1, step=1):
        return [datetime.now() + i*timedelta(days=1) for i in range(0,length,step)]
    return create_timestamps





