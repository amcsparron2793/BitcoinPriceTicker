"""
BitcoinPriceTicker.py

gets the current btc price from coindesk and parses the resulting json
"""


from typing import Dict, Any
from datetime import datetime, timezone, timedelta
from requests import get as r_get


class BitcoinApiError(Exception):
    """Custom exception for Bitcoin API related errors"""
    pass


class BitcoinPriceTicker:
    """A class to retrieve and process Bitcoin price data from CoinDesk API."""

    BASE_URL: str = 'https://data-api.coindesk.com'
    ENDPOINT: str = '/index/cc/v1/latest/tick'
    EST_TIMEZONE_OFFSET: int = -4

    # API response keys
    KEY_DATA: str = 'Data'
    KEY_BTC_USD: str = 'BTC-USD'
    KEY_VALUE: str = 'VALUE'
    KEY_TIMESTAMP: str = 'VALUE_LAST_UPDATE_TS'

    DEFAULT_PARAMS: Dict[str, str] = {
        "market": "cadli",
        "instruments": "BTC-USD",
        "apply_mapping": "true",
        "groups": "VALUE"
    }

    def __init__(self, params: Dict[str, str] = None, base_url: str = None) -> None:
        """
        Initialize the Bitcoin Price Ticker.

        Args:
            params: Optional API request parameters
            base_url: Optional base URL for the API
        """
        self.params = params or BitcoinPriceTicker.DEFAULT_PARAMS
        self.url = base_url or f"{BitcoinPriceTicker.BASE_URL}{BitcoinPriceTicker.ENDPOINT}"

    @property
    def formatted_price(self) -> str:
        """Returns a formatted string of current Bitcoin price."""
        price_info = self.fetch_current_price()
        return f"As of {price_info['pretty_est_time']} EST:\n\t1 BTC = {price_info['price_str']}"

    def fetch_current_price(self) -> Dict[str, Any]:
        """Fetches and returns current Bitcoin price information."""
        response = r_get(self.url, params=self.params)

        if not response.ok:
            raise BitcoinApiError(f'API request failed: {response.status_code} - {response.reason}')

        return self._parse_price_data(response.json())

    @classmethod
    def _parse_price_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses raw API response into structured price data.

        Args:
            data: Raw API response data

        Returns:
            Dictionary containing formatted price and time information

        Raises:
            BitcoinApiError: If required data is missing
        """
        try:
            btc_data = data[cls.KEY_DATA][cls.KEY_BTC_USD]
            timestamp = btc_data[cls.KEY_TIMESTAMP]

            return {
                'price_str': f'${btc_data[cls.KEY_VALUE]:,.2f}',
                'datetime_from_ts': datetime.fromtimestamp(timestamp),
                'pretty_est_time': cls._convert_to_est_time(timestamp).ctime()
            }
        except KeyError as e:
            raise BitcoinApiError(f"Missing required data field: {e}")

    @classmethod
    def _convert_to_est_time(cls, timestamp: float) -> datetime:
        """Converts Unix timestamp to EST timezone."""
        return datetime.fromtimestamp(timestamp).astimezone(
            timezone(timedelta(hours=cls.EST_TIMEZONE_OFFSET))
        )


if __name__ == '__main__':
    btc_ticker = BitcoinPriceTicker()
    print(btc_ticker.formatted_price)
    #info = btc_ticker.get_current_info()
    #print(f"As of {info['pretty_est_time']} EST:\n\t1 BTC = {info['price_str']}")
