"""
BitcoinPriceTicker.py

gets the current btc price from coindesk and parses the resulting JSON
"""


from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from requests import get as r_get
from _version import __version__

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
    CONTINUOUS_CHECK_INTERVAL_SECONDS: int = 120

    def __init__(self, params: Dict[str, str] = None, base_url: str = None) -> None:
        """
        Initialize the Bitcoin Price Ticker.

        Args:
            params: Optional API request parameters
            base_url: Optional base URL for the API
        """
        print(f"Initializing {self}")
        self.params = params or BitcoinPriceTicker.DEFAULT_PARAMS
        self.url = base_url or f"{BitcoinPriceTicker.BASE_URL}{BitcoinPriceTicker.ENDPOINT}"

    def __str__(self):
        return f'Bitcoin Price Ticker v{__version__}'

    @staticmethod
    def _format_minutes_seconds() -> str:
        """
        Formats a duration given in seconds to a string representing the duration
        in minutes and seconds.

        Returns a human-readable string representation of the duration, where the
        format varies based on whether the duration has a non-zero value for
        seconds. This method assumes the duration is derived from the
        CONTINUOUS_CHECK_INTERVAL_SECONDS constant.

        Returns:
            str: Formatted duration in minutes and seconds.
        """
        minutes, seconds = divmod(BitcoinPriceTicker.CONTINUOUS_CHECK_INTERVAL_SECONDS, 60)
        if seconds > 0:
            return f"{minutes} minutes and {seconds} seconds"
        return f"{minutes} minutes"

    @classmethod
    def get_continuous_check_interval(cls) -> str:
        """Returns a human-readable string of the check interval."""
        if cls.CONTINUOUS_CHECK_INTERVAL_SECONDS > 60:
            return cls._format_minutes_seconds()
        else:
            return f"{cls.CONTINUOUS_CHECK_INTERVAL_SECONDS} seconds"

    @property
    def formatted_price(self) -> str:
        """Returns a formatted string of the current Bitcoin price."""
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

    def _continuous_check_process(self):
        """
        Performs a continuous check process.

        This method executes a continuous checking process by printing the formatted price
        attribute of the instance. The method is primarily designed for internal use and can
        be part of background operations.

        """
        print(self.formatted_price)

    @staticmethod
    def should_update_continuous(last_update: Optional[datetime]) -> bool:
        """Check if enough time has passed since the last update."""
        check_interval = BitcoinPriceTicker.CONTINUOUS_CHECK_INTERVAL_SECONDS
        if last_update is None:
            return True
        return datetime.now() - last_update >= timedelta(seconds=check_interval)

    def continuous_check(self) -> None:
        """
        Performs a continuous check process in a loop, updating and re-evaluating based on
        specific conditions, until interrupted by the user.

        Attributes:
            last_checked (Optional[datetime]): Stores the last checked datetime. Initialized
            to None.

        Methods:
            This method does not contain individual methods.

        Raises:
            This method does not raise any specific exception internally, but captures the
            KeyboardInterrupt to terminate the loop gracefully.

        """
        last_checked: Optional[datetime] = None
        print(f"Starting continuous check every "
              f"{BitcoinPriceTicker.get_continuous_check_interval()} "
              f"press Ctrl+C to exit.")
        while True:
            try:
                if not self.should_update_continuous(last_checked):
                    continue
                self._continuous_check_process()
                last_checked = datetime.now()
            except KeyboardInterrupt:
                print("Exiting...")
                break

            #print(f"As of {price_info['pretty_est_time']} EST:\n\t1 BTC = {price_info['price_str']}")
            # print()
            # input("Press Enter to check again or Ctrl+C to exit...")
            # print()


if __name__ == '__main__':
    btc_ticker = BitcoinPriceTicker()
    btc_ticker.continuous_check()
    #print(btc_ticker.formatted_price)
    #info = btc_ticker.get_current_info()
    #print(f"As of {info['pretty_est_time']} EST:\n\t1 BTC = {info['price_str']}")
