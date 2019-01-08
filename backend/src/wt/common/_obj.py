from decimal import Decimal
from enum import Enum


class Currency(Enum):
    czk = "CZK"
    eur = "EUR"
    usd = "USD"


class Money:
    def __init__(self, amount: Decimal, currency: Currency):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other):
        if isinstance(other, Money):
            return self.__dict__ == other.__dict__
        return NotImplemented
