from typing import Dict, List, Optional
from CryptoPriceTickers import BasePriceTicker
from Backend.helpers import CryptoType

from Backend.factory import TickerFactory


class MultiTicker(BasePriceTicker):
    """A ticker that handles multiple cryptocurrencies simultaneously."""

    def __init__(self, factory: 'TickerFactory',
                 crypto_types: Optional[List[CryptoType]] = None,
                 params: Optional[Dict[str, str]] = None,
                 base_url: str = None,
                 **kwargs) -> None:
        """
        Initialize MultiTicker with specified cryptocurrencies.

        Args:
            factory: TickerFactory instance to create and validate tickers
            crypto_types: List of CryptoType to track. If None, tracks all supported types.
            params: Optional API parameters
            base_url: Optional base URL for the API
        """
        self.factory = factory
        self.crypto_types = crypto_types or factory.get_supported_cryptos()

        # Validate all crypto types are supported
        for crypto in self.crypto_types:
            self.factory.get_ticker_class(crypto)  # Will raise UnsupportedCryptoError if not supported

        # Prepare params with all instruments
        if params is None:
            params = {
                "market": "cadli",
                "instruments": ",".join(crypto.instrument_key for crypto in self.crypto_types)
            }

        super().__init__(params=params, base_url=base_url, **kwargs)
        self.currency_shorthand = "MULTI"

        # Create individual tickers using factory
        self.tickers = {
            crypto: self.factory.create_ticker(crypto, params=params)
            for crypto in self.crypto_types
        }

    def _continuous_check_process(self):
        """Override the base class method to show all cryptocurrency prices."""
        print(self.formatted_price)
        print('-'* 50)

    def _format_price_line(self, price_data, crypto: CryptoType,
                           not_first_line: bool = False):
        """
        Formats a line containing price information for a specific cryptocurrency.

        The method uses provided price data and cryptocurrency information to format and
        optionally colorize a string representing the price of the cryptocurrency. It generates
        a formatted string either as an initial line with a timestamp or as a subsequent line
        without a timestamp.

        Arguments:
            price_data: The raw price data dictionary from which formatted price information
                is extracted.
            crypto: The cryptocurrency for which the price line is being formatted.
            not_first_line: Determines whether the line being formatted is the first line
                (which includes a timestamp) or a subsequent line.

        Returns:
            A string representing the formatted cryptocurrency price information.
        """
        parsed_data = self._parse_price_data(price_data,
                                             instrument_key=crypto.instrument_key)
        price_change = self._calculate_price_change(parsed_data)
        # FIXME: where to set old price per crypto?
        print(f"CURRENT: {parsed_data['price_str']} | OLD: {self.tickers[crypto]._old_price}")


        if not_first_line:
            line = f"1 {crypto.value} = {parsed_data['price_str']} ({price_change})"
        else:
            line = (f"As of {parsed_data['pretty_est_time']} EST:\n"
                    f"1 {crypto.value} = {parsed_data['price_str']} ({price_change})")

        if self.use_colorizer:
            line = self.colorizer.colorize(
                text=line,
                color=crypto.get_color_for_crypto()
            )
        return line

    @property
    def formatted_price(self) -> str:
        """Returns a formatted string of current prices for all cryptocurrencies."""
        price_data = self.fetch_current_price()
        result = []
        not_first_line = False

        for crypto, ticker in self.tickers.items():
            formatted_line = self._format_price_line(price_data, crypto, not_first_line)
            result.append(formatted_line)

            not_first_line = True

        return "\n".join(result)


# Usage example:
if __name__ == '__main__':
    # Create factory
    factory = TickerFactory()

    # Create multi-ticker with all supported cryptocurrencies
    multi_ticker = MultiTicker(factory)
    multi_ticker.continuous_check()