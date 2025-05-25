"""
BitcoinPriceTicker.py

gets the current btc price from coindesk and parses the resulting json
"""


from requests import get as r_get, RequestException
import datetime


class BitcoinPriceTicker:
    """
    A class to retrieve and process Bitcoin price data.

    This class interacts with the CoinDesk API to fetch the latest Bitcoin price data
    and parses it into a user-friendly format. It supports customization of API query
    parameters and base URL. The main functionality includes retrieving current price
    data and generating a formatted string representation of the Bitcoin price.

    :ivar BASE_URL: Base URL of the CoinDesk API.
    :type BASE_URL: Str
    :ivar END_POINT: Endpoint for the API to retrieve Bitcoin price information.
    :type END_POINT: Str
    :ivar DEFAULT_PARAMS: Default parameters for the API request.
    :type DEFAULT_PARAMS: Dict
    :ivar params: API request parameters, which can be overridden during initialization.
    :type params: Dict
    :ivar url: Full URL for the API request, combining the base URL and endpoint.
    :type url: Str
    """
    BASE_URL = 'https://data-api.coindesk.com'
    END_POINT = '/index/cc/v1/latest/tick'
    DEFAULT_PARAMS = {"market": "cadli",
                      "instruments": "BTC-USD",
                      "apply_mapping": "true",
                      "groups": "VALUE"}

    def __init__(self, **kwargs):
        self.params = kwargs.get('params', BitcoinPriceTicker.DEFAULT_PARAMS)
        self.url = kwargs.get('url', BitcoinPriceTicker.BASE_URL + BitcoinPriceTicker.END_POINT)

    @property
    def ticker_string(self):
        ticker_info = self.get_current_info()
        return f"As of {ticker_info['pretty_est_time']} EST:\n\t1 BTC = {ticker_info['price_str']}"

    @staticmethod
    def parse_info_dict(req_json: dict):
        """
        Parses the information from a given dictionary and extracts specific data
        related to currency value, last update timestamp, and formatted time in EST.

        This method is used to parse a nested dictionary structure and extract key
        details about currency value in USD for BTC (Bitcoin). It also converts the
        timestamp into a human-readable datetime format in EST timezone and formats
        the price as a string.

        :param req_json: A dictionary containing nested data with currency and
            timestamp information related to BTC-USD.
        :type req_json: Dict
        :return: A dictionary containing the formatted price, a datetime object
            converted from the timestamp, and a human-readable formatted string
            for the EST timezone. If the required data keys are missing, it will
            return the KeyError exception encountered during the parsing process.
        :rtype: Dict or KeyError
        """
        try:
            data = req_json['Data']['BTC-USD']
            pretty_est_time = datetime.datetime.fromtimestamp(
                    data['VALUE_LAST_UPDATE_TS']).astimezone(
                    datetime.timezone(
                        datetime.timedelta(hours=-4)
                    )
                ).ctime()
            info_dict = {
                'price_str': f'${data['VALUE']:,.2f}',
                'datetime_from_ts': datetime.datetime.fromtimestamp(data['VALUE_LAST_UPDATE_TS']),
                'pretty_est_time': pretty_est_time
            }
            return info_dict
        except KeyError as e:
            return e

    def get_current_info(self) -> dict:  # 'https://data-api.coindesk.com/v1/bpi/currentprice/usd.json') -> dict:
        r = r_get(self.url, params=self.params)
        if r.ok:
            try:
                info_dict = self.parse_info_dict(r.json())
                if isinstance(info_dict, Exception):
                    raise info_dict

            except KeyError as e:
                print(f"ERROR: {e}")
                raise e

            return info_dict
        else:
            try:
                raise RequestException(f'Something went wrong - response code: {r.status_code} - {r.reason}')
            except RequestException as e:
                print(f"ERROR: {e}")
                raise e


if __name__ == '__main__':
    btc_ticker = BitcoinPriceTicker()
    print(btc_ticker.ticker_string)
    #info = btc_ticker.get_current_info()
    #print(f"As of {info['pretty_est_time']} EST:\n\t1 BTC = {info['price_str']}")
