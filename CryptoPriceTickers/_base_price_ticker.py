from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from requests import get as r_get
from CryptoPriceTickers._version import __version__

from Backend.err import CoinDeskApiError
from Backend.helpers import CryptoColorizer, CryptoType


class BasePriceTicker:
    BASE_URL: str = 'https://data-api.coindesk.com'
    ENDPOINT: str = '/index/cc/v1/latest/tick'
    EST_TIMEZONE_OFFSET: int = -4

    # API response keys
    KEY_DATA: str = 'Data'
    KEY_BTC_USD: str = 'BTC-USD'
    KEY_ETH_USD: str = 'ETH-USD'
    KEY_LTC_USD: str = 'LTC-USD'
    KEY_XRP_USD: str = 'XRP-USD'
    KEY_DOGE_USD: str = 'DOGE-USD'

    KEY_VALUE: str = 'VALUE'
    KEY_TIMESTAMP: str = 'VALUE_LAST_UPDATE_TS'

    REQUIRED_PARAMS = [
        "market",
        "instruments"
    ]
    DEFAULT_PARAMS: Dict[str, str] = {
        "market": "cadli",
        #"instruments": "BTC-USD",
        "apply_mapping": "true",
        "groups": "VALUE"
    }

    INSTRUMENT_KEY = None

    CONTINUOUS_CHECK_INTERVAL_SECONDS: int = 120

    def __init__(self, params: Dict[str, str] = None, base_url: str = None, **kwargs) -> None:
        """
        Initialize the Bitcoin Price Ticker.

        Args:
            params: Optional API request parameters
            base_url: Optional base URL for the API
        """
        print(f"{'-'* 10} Initializing {self} {'-'* 10}")
        self._params = None
        self.params = params or BasePriceTicker.DEFAULT_PARAMS
        self.url = base_url or f"{BasePriceTicker.BASE_URL}{BasePriceTicker.ENDPOINT}"
        self.currency_shorthand = None
        self._colorizer = None
        self.use_colorizer = kwargs.get('use_colorizer', True)

    def __str__(self):
        return f'{self.__class__.__name__} v{__version__}'

    @classmethod
    def get_color(cls):
        if cls.INSTRUMENT_KEY == cls.KEY_BTC_USD:
            return 'GOLD'
        elif cls.INSTRUMENT_KEY == cls.KEY_ETH_USD:
            return 'PURPLE'
        elif cls.INSTRUMENT_KEY == cls.KEY_LTC_USD:
            return 'GRAY'
        elif cls.INSTRUMENT_KEY == cls.KEY_XRP_USD:
            return 'RED'
        else:
            return 'WHITE'

    @property
    def colorizer(self):
        if not self._colorizer:
            if self.use_colorizer:
                self._colorizer = CryptoColorizer()
        return self._colorizer

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value: dict[str, str]) -> None:
        if not isinstance(value, dict):
            raise TypeError("Params must be a dictionary")
            # Check if all required parameters are present in the dictionary keys
        if not all(param in value.keys() for param in BasePriceTicker.REQUIRED_PARAMS):
            raise ValueError(
            "Params must contain at least the following keys: "
            f"{', '.join(BasePriceTicker.REQUIRED_PARAMS)}"
        )
        self._params = value

    @classmethod
    def _format_minutes_seconds(cls) -> str:
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
        minutes, seconds = divmod(cls.CONTINUOUS_CHECK_INTERVAL_SECONDS, 60)
        if seconds > 0:
            return f"{minutes} minutes and {seconds} seconds"
        return f"{minutes} minutes"

    @property
    def formatted_price(self) -> str:
        """Returns a formatted string of the current Bitcoin price."""
        price_info = self._parse_price_data(self.fetch_current_price())
        formatted_string = f"As of {price_info['pretty_est_time']} EST:\n\t1 {self.currency_shorthand} = {price_info['price_str']}"
        if self.use_colorizer:
            # TODO: use something like the below to avoid having to have a separate get_color() method
            #  CryptoType.get_color_for_crypto(CryptoType.from_string()
            formatted_string = self.colorizer.colorize(text=formatted_string, color=self.__class__.get_color())
        return formatted_string

    @classmethod
    def get_continuous_check_interval(cls) -> str:
        """Returns a human-readable string of the check interval."""
        if cls.CONTINUOUS_CHECK_INTERVAL_SECONDS > 60:
            return cls._format_minutes_seconds()
        else:
            return f"{cls.CONTINUOUS_CHECK_INTERVAL_SECONDS} seconds"

    def fetch_current_price(self) -> Dict[str, Any]:
        """Fetches and returns current Bitcoin price information."""
        response = r_get(self.url, params=self.params)

        if not response.ok:
            raise CoinDeskApiError(f'API request failed: {response.status_code} - {response.reason}')

        return response.json()

    @classmethod
    def _convert_to_est_time(cls, timestamp: float) -> datetime:
        """Converts Unix timestamp to EST timezone."""
        return datetime.fromtimestamp(timestamp).astimezone(
            timezone(timedelta(hours=cls.EST_TIMEZONE_OFFSET))
        )

    @classmethod
    def get_currency_data(cls, data: Dict[str, Any], instrument_key=None) -> tuple:
        if instrument_key is None:
            instrument_key = cls.INSTRUMENT_KEY
        instrument_data = data[cls.KEY_DATA][instrument_key]
        timestamp = instrument_data[cls.KEY_TIMESTAMP]
        return instrument_data, timestamp

    def _continuous_check_process(self):
        """
        Performs a continuous check process.

        This method executes a continuous checking process by printing the formatted price
        attribute of the instance. The method is primarily designed for internal use and can
        be part of background operations.

        """
        print(self.formatted_price)

    @classmethod
    def should_update_continuous(cls, last_update: Optional[datetime]) -> bool:
        """Check if enough time has passed since the last update."""
        check_interval = cls.CONTINUOUS_CHECK_INTERVAL_SECONDS
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
              f"{self.__class__.get_continuous_check_interval()} "
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

    @classmethod
    def _parse_price_data(cls, data: Dict[str, Any], instrument_key=None) -> Dict[str, Any]:
        """
        Parses raw API response into structured price data.

        Args:
            data: Raw API response data

        Returns:
            Dictionary containing formatted price and time information

        Raises:
            CoinDeskApiError: If required data is missing
        """
        if instrument_key is None:
            instrument_key = cls.INSTRUMENT_KEY
        try:
            btc_data, timestamp = cls.get_currency_data(data, instrument_key)
            return {
                'price_str': f'${btc_data[cls.KEY_VALUE]:,.2f}',
                'datetime_from_ts': datetime.fromtimestamp(timestamp),
                'pretty_est_time': cls._convert_to_est_time(timestamp).ctime()
            }
        except KeyError as e:
            raise CoinDeskApiError(f"Missing required data field: {e}")