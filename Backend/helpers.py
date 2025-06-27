from ColorizerAJM import Colorizer
from enum import Enum
from Backend.err import UnsupportedCryptoError
import argparse

class CryptoType(Enum):
    BITCOIN = "BTC"
    ETHEREUM = "ETH"
    LITECOIN = "LTC"
    XRP = "XRP"
    DOGE = "DOGE"

    def __str__(self):
        return self.value

    def get_color_for_crypto(self) -> str:
        """Get the display color for a specific cryptocurrency."""
        color_map = {
            CryptoType.BITCOIN: "GOLD",
            CryptoType.ETHEREUM: "PURPLE",
            CryptoType.LITECOIN: "GRAY",
            CryptoType.XRP: "RED"
        }
        return color_map.get(self, "WHITE")

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
            raise UnsupportedCryptoError(value, [crypto.name for crypto in cls])


class CryptoColorizer(Colorizer):
    DEFAULT_COLOR_CODES = {'PURPLE': 97, 'GOLD': 184, 'GRAY': 244}
    def __init__(self,  **kwargs):
        custom_colors = kwargs.get('custom_colors', {})
        self.crypto_custom_colors = {**custom_colors, **self.__class__.DEFAULT_COLOR_CODES}
        super().__init__(custom_colors=self.crypto_custom_colors)


class TickerArgparse(argparse.ArgumentParser):
    def __init__(self):
        super().__init__()
        self.add_argument('-m', '--mode',
                          type=str, required=False,
                          help='ticker mode', default='multi')
        self.add_argument('-c', '--crypto_type',
                          type=str, required=False,
                          help='crypto type')
        self.add_argument('-p', '--params',
                          type=str, required=False,
                          help='params')
        self.add_argument('-u', '--base_url',
                          type=str, required=False,
                          help='base url')
        self.add_argument('-uc', '--use_colorizer',
                          action='store_true', required=False,
                          default=True,
                          help='enable colorizer')
