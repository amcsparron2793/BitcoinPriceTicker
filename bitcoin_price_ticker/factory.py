from typing import Dict, Type, Optional

from bitcoin_price_ticker import (BasePriceTicker, BitcoinPriceTicker,
                                  EthereumPriceTicker, LitecoinPriceTicker,
                                  RipplePriceTicker)

from bitcoin_price_ticker.err import UnsupportedCryptoError
from bitcoin_price_ticker.helpers import CryptoType


class TickerFactory:
    TICKER_MAP = {
        CryptoType.BITCOIN: BitcoinPriceTicker,
        CryptoType.ETHEREUM: EthereumPriceTicker,
        CryptoType.LITECOIN: LitecoinPriceTicker,
        CryptoType.XRP: RipplePriceTicker,
    }
    SUPPORTED_CRYPTO_TYPES = [crypto for crypto in TICKER_MAP.keys() if isinstance(crypto, CryptoType)]
    STRING_SUPPORTED_CRYPTO_TYPES = [str(x) for x in SUPPORTED_CRYPTO_TYPES]

    def __init__(self):
        self._ticker_instances = {}

    @classmethod
    def get_supported_cryptos(cls) -> list[CryptoType]:
        """Returns list of supported cryptocurrencies"""
        return list(CryptoType)

    @classmethod
    def get_ticker_class(cls, crypto_type: CryptoType) -> Type[BasePriceTicker]:
        """Maps CryptoType to the corresponding Ticker class"""
        if crypto_type not in cls.TICKER_MAP:
            raise UnsupportedCryptoError(crypto_type, cls.STRING_SUPPORTED_CRYPTO_TYPES)
        return cls.TICKER_MAP[crypto_type]

    def create_ticker(self, crypto_type: CryptoType,
                      params: Optional[Dict[str, str]] = None,
                      force_new: bool = False) -> BasePriceTicker:
        """
        Creates or returns an existing ticker instance

        Args:
            crypto_type: Type of cryptocurrency
            params: Optional API parameters
            force_new: If True, always creates new instance
        """
        if not force_new and crypto_type in self._ticker_instances:
            return self._ticker_instances[crypto_type]

        ticker_class = self.get_ticker_class(crypto_type)
        if params is None:
            params = {
                "market": "cadli",  # Adding the required market parameter
                "instruments": crypto_type.instrument_key
            }
        return ticker_class(params=params)

    def print_all_crypto_formatted_price(self):
        all_cryptos = self.__class__.get_supported_cryptos()
        for crypto in all_cryptos:
            ticker = self.create_ticker(crypto)
            print(ticker.formatted_price)

    def ticker_from_string_input(self, ticker_name):
        try:
            crypto_type = CryptoType.from_string(ticker_name)#user_input)
            ticker = self.create_ticker(crypto_type)
        except ValueError as e:
            print(f"Error: {e}")
            return e
        return ticker


if __name__ == '__main__':
    # Create factory
    factory = TickerFactory()
    factory.print_all_crypto_formatted_price()

    # TODO: Create tickers using enum
    # btc_ticker = factory.create_ticker(CryptoType.BITCOIN)
    # eth_ticker = factory.create_ticker(CryptoType.ETHEREUM)
    # ltc_ticker = factory.create_ticker(CryptoType.LITECOIN)
    # xrp_ticker = factory.create_ticker(CryptoType.XRP)

    # TODO: Create multi-ticker for all supported cryptocurrencies

    # TODO:  Create from string input (useful for command line arguments)
    # try:
    #     user_input = "bitcoin"
    #     crypto_type = CryptoType.from_string(user_input)
    #     ticker = factory.create_ticker(crypto_type)
    # except ValueError as e:
    #     print(f"Error: {e}")

    # TODO: integrate these as options?
    # Check if a crypto type is supported
    # def is_supported(crypto_type: CryptoType) -> bool:
    #     return crypto_type in CryptoType
    #
    #
    # # Pattern matching with crypto types
    # def get_color_for_crypto(crypto: CryptoType) -> str:
    #     match crypto:
    #         case CryptoType.BITCOIN:
    #             return "gold"
    #         case CryptoType.ETHEREUM:
    #             return "purple"
    #         case CryptoType.LITECOIN:
    #             return "silver"
    #         case CryptoType.XRP:
    #             return "blue"
    #     return None

