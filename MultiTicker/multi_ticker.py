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
        """Override base class method to show all cryptocurrency prices."""
        for crypto in self.crypto_types:
            price_info = self._parse_price_data(
                self.fetch_current_price(),
                instrument_key=crypto.instrument_key
            )
            formatted_string = (
                f"As of {price_info['pretty_est_time']} EST:\n"
                f"\t1 {crypto.value} = {price_info['price_str']}"
            )

            if self.use_colorizer:
                color = self.get_color_for_crypto(crypto)
                formatted_string = self.colorizer.colorize(
                    text=formatted_string,
                    color=color
                )
            print(formatted_string)

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
        """Returns formatted string of current prices for all cryptocurrencies."""
        price_data = self.fetch_current_price()
        result = []

        for crypto in self.crypto_types:
            parsed_data = self._parse_price_data(
                price_data,
                instrument_key=crypto.instrument_key
            )
            line = (
                f"1 {crypto.value} = {parsed_data['price_str']} "
                f"({parsed_data['pretty_est_time']} EST)"
            )
            if self.use_colorizer:
                line = self.colorizer.colorize(
                    text=line,
                    color=self.get_color_for_crypto(crypto)
                )
            result.append(line)

        return "\n".join(result)


# Usage example:
if __name__ == '__main__':
    # Create MultiTicker with all supported cryptocurrencies
    multi_ticker = MultiTicker()
    multi_ticker.continuous_check()