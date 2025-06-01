"""
BitcoinPriceTicker.py

gets the current btc price from coindesk and parses the resulting JSON
"""


from typing import Dict
from CryptoPriceTickers._base_price_ticker import BasePriceTicker


class BitcoinPriceTicker(BasePriceTicker):
    """A class to retrieve and process Bitcoin price data from CoinDesk API."""
    INSTRUMENT_KEY = BasePriceTicker.KEY_BTC_USD

    def __init__(self, params: Dict[str, str] = None, base_url: str = None, **kwargs) -> None:
        self.__class__.DEFAULT_PARAMS.update({"instruments": BasePriceTicker.KEY_BTC_USD})
        super().__init__(params, base_url, **kwargs)
        self.currency_shorthand = BasePriceTicker.KEY_BTC_USD.split('-')[0]


class EthereumPriceTicker(BasePriceTicker):
    """A class to retrieve and process Ethereum price data from CoinDesk API."""
    INSTRUMENT_KEY = BasePriceTicker.KEY_ETH_USD

    def __init__(self, params: Dict[str, str] = None, base_url: str = None, **kwargs) -> None:
        self.__class__.DEFAULT_PARAMS.update({"instruments": BasePriceTicker.KEY_ETH_USD})
        super().__init__(params, base_url, **kwargs)
        self.currency_shorthand = BasePriceTicker.KEY_ETH_USD.split('-')[0]


class LitecoinPriceTicker(BasePriceTicker):
    """A class to retrieve and process Litecoin price data from CoinDesk API."""
    INSTRUMENT_KEY = BasePriceTicker.KEY_LTC_USD
    def __init__(self, params: Dict[str, str] = None, base_url: str = None, **kwargs) -> None:
        self.__class__.DEFAULT_PARAMS.update({"instruments": BasePriceTicker.KEY_LTC_USD})
        super().__init__(params, base_url, **kwargs)
        self.currency_shorthand = BasePriceTicker.KEY_LTC_USD.split('-')[0]


class RipplePriceTicker(BasePriceTicker):
    """A class to retrieve and process Ripple price data from CoinDesk API."""
    INSTRUMENT_KEY = BasePriceTicker.KEY_XRP_USD
    def __init__(self, params: Dict[str, str] = None, base_url: str = None, **kwargs) -> None:
        self.__class__.DEFAULT_PARAMS.update({"instruments": BasePriceTicker.KEY_XRP_USD})
        super().__init__(params, base_url, **kwargs)
        self.currency_shorthand = BasePriceTicker.KEY_XRP_USD.split('-')[0]


class DogePriceTicker(BasePriceTicker):
    INSTRUMENT_KEY = BasePriceTicker.KEY_DOGE_USD
    def __init__(self, params: Dict[str, str] = None, base_url: str = None, **kwargs) -> None:
        self.__class__.DEFAULT_PARAMS.update({"instruments": BasePriceTicker.KEY_DOGE_USD})
        super().__init__(params, base_url, **kwargs)
        self.currency_shorthand = BasePriceTicker.KEY_DOGE_USD.split('-')[0]


if __name__ == '__main__':
    BasePriceTicker.CONTINUOUS_CHECK_INTERVAL_SECONDS = 10
    # btc_ticker = BitcoinPriceTicker()
    # btc_ticker.continuous_check()
    # eth_ticker = EthereumPriceTicker()
    # eth_ticker.continuous_check()
    # ltc_ticker = LitecoinPriceTicker()
    # ltc_ticker.continuous_check()
    # xrp_ticker = RipplePriceTicker()
    # xrp_ticker.continuous_check()
