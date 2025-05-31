from ColorizerAJM import Colorizer
from enum import Enum

class CryptoType(Enum):
    BITCOIN = "BTC"
    ETHEREUM = "ETH"
    LITECOIN = "LTC"
    XRP = "XRP"

    def __str__(self):
        return self.value

    @property
    def instrument_key(self) -> str:
        """Returns the instrument key used in the API"""
        return f"{self.value}-USD"

    @classmethod
    def from_string(cls, value: str) -> "CryptoType":
        """Create enum from string, case-insensitive"""
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"Unknown cryptocurrency: {value}. "
                             f"Valid options are: {', '.join(crypto.name for crypto in cls)}")


class CryptoColorizer(Colorizer):
    def __init__(self):
        super().__init__(custom_colors={'PURPLE': 97, 'GOLD': 184, 'GRAY': 244})