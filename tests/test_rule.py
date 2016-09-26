from datetime import datetime
import pytest
from stock_alerter.stock import Stock
from stock_alerter.rule import PriceRule

class TestRule:
    """Rule's"""


    @pytest.fixture()
    def exchange(self):
        goog = Stock("GOOG")
        goog.update(datetime(2016,9,26), 11)
        return {"GOOG": goog}

    rules_data = [
        ("GOOG", lambda stock: stock.price > 10, True),
        ("GOOG", lambda stock: stock.price < 10, False),
        ("MSFT", lambda stock: stock.price > 10, False)]
    rules_ids = ["True when condition is met.",
                 "False when condition is not met.",
                 "False when stock is not in exchange." ]

    @pytest.mark.parametrize("stock,condition,assertion", rules_data, ids=rules_ids)
    def test_matches_on_condition_not_otherwise(self,exchange, stock, condition, assertion):
        rule = PriceRule(stock,condition)
        assert rule.matches(exchange) is assertion

    def test_matches_is_false_if_stock_has_not_been_updated(self,exchange):
        exchange["AAPL"] = Stock("AAPL")
        rule = PriceRule("AAPL", lambda stock: stock.price > 10)
        assert rule.matches(exchange) is False

    def test_a_rule_depends_on_its_stock(self):
            rule = PriceRule("MSFT", lambda stock: stock.price > 10)
            assert rule.depends_on() == "MSFT"

