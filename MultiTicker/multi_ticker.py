from typing import Dict, List, Optional
from bitcoin_price_ticker import BasePriceTicker
from bitcoin_price_ticker.helpers import CryptoType


class MultiTicker(BasePriceTicker):
    """A ticker that handles multiple cryptocurrencies simultaneously."""

    def __init__(self, crypto_types: Optional[List[CryptoType]] = None,
                 params: Optional[Dict[str, str]] = None,
                 base_url: str = None,
                 **kwargs) -> None:
        """
        Initialize MultiTicker with specified cryptocurrencies.

        Args:
            crypto_types: List of CryptoType to track. If None, tracks all supported types.
            params: Optional API parameters
            base_url: Optional base URL for the API
        """
        self.crypto_types = crypto_types or list(CryptoType)

        # Prepare params with all instruments
        if params is None:
            params = {
                "market": "cadli",
                "instruments": ",".join(crypto.instrument_key for crypto in self.crypto_types)
            }

        super().__init__(params=params, base_url=base_url, **kwargs)
        self.currency_shorthand = "MULTI"  # Identifier for multi-currency ticker

    def _continuous_check_process(self):
        """Override the base class method to show all cryptocurrency prices."""
        print(self.formatted_price)
        print('-'* 50)

    @staticmethod
    def get_color_for_crypto(crypto: CryptoType) -> str:
        """Get the display color for a specific cryptocurrency."""
        color_map = {
            CryptoType.BITCOIN: "GOLD",
            CryptoType.ETHEREUM: "PURPLE",
            CryptoType.LITECOIN: "GRAY",
            CryptoType.XRP: "RED"
        }
        return color_map.get(crypto, "WHITE")

    @property
    def formatted_price(self) -> str:
        """Returns a formatted string of current prices for all cryptocurrencies."""
        price_data = self.fetch_current_price()
        result = []
        not_first_line = False

        for crypto in self.crypto_types:
            parsed_data = self._parse_price_data(price_data,
                instrument_key=crypto.instrument_key)

            if not_first_line:
                line = f"1 {crypto.value} = {parsed_data['price_str']}"
            else:
                line = (f"As of {parsed_data['pretty_est_time']} EST:\n"
                    f"1 {crypto.value} = {parsed_data['price_str']} ")

            if self.use_colorizer:
                line = self.colorizer.colorize(
                    text=line,
                    color=self.get_color_for_crypto(crypto)
                )

            result.append(line)

            not_first_line = True

        return "\n".join(result)


# Usage example:
if __name__ == '__main__':
    # Create MultiTicker with all supported cryptocurrencies
    multi_ticker = MultiTicker()
    multi_ticker.continuous_check()