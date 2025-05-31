from typing import Dict, Type, Optional

from bitcoin_price_ticker import BasePriceTicker, BitcoinPriceTicker, EthereumPriceTicker, LitecoinPriceTicker, \
    RipplePriceTicker

from enum import Enum, auto


class CryptoType(Enum):
    BITCOIN = "BTC"
    ETHEREUM = "ETH"
    LITECOIN = "LTC"
    XRP = "XRP"

    def __str__(self):
        return self.value

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
            raise ValueError(f"Unknown cryptocurrency: {value}. "
                             f"Valid options are: {', '.join(crypto.name for crypto in cls)}")


class TickerFactory:
    def __init__(self):
        self._ticker_instances = {}

    @classmethod
    def _get_ticker_class(cls, crypto_type: CryptoType) -> Type[BasePriceTicker]:
        """Maps CryptoType to the corresponding Ticker class"""
        ticker_map = {
            CryptoType.BITCOIN: BitcoinPriceTicker,
            CryptoType.ETHEREUM: EthereumPriceTicker,
            CryptoType.LITECOIN: LitecoinPriceTicker,
            CryptoType.XRP: RipplePriceTicker,
        }

        if crypto_type not in ticker_map:
            supported = ", ".join(str(crypto) for crypto in ticker_map.keys())
            raise ValueError(f"Unsupported cryptocurrency: {crypto_type}. "
                             f"Supported types: {supported}")
        return ticker_map[crypto_type]

    def create_ticker(self, crypto_type: CryptoType,
                      params: Optional[Dict[str, str]] = None,
                      force_new: bool = False) -> BasePriceTicker:
        """
        Creates or returns existing ticker instance

        Args:
            crypto_type: Type of cryptocurrency
            params: Optional API parameters
            force_new: If True, always creates new instance
        """
        if not force_new and crypto_type in self._ticker_instances:
            return self._ticker_instances[crypto_type]

        ticker_class = self._get_ticker_class(crypto_type)
        if params is None:
            params = {
                "market": "cadli",  # Adding the required market parameter
                "instruments": crypto_type.instrument_key
            }
        return ticker_class(params=params)

    @classmethod
    def get_supported_cryptos(cls) -> list[CryptoType]:
        """Returns list of supported cryptocurrencies"""
        return list(CryptoType)

if __name__ == '__main__':
    # Create factory
    factory = TickerFactory()

    # TODO: Create tickers using enum
    # btc_ticker = factory.create_ticker(CryptoType.BITCOIN)
    # eth_ticker = factory.create_ticker(CryptoType.ETHEREUM)
    # ltc_ticker = factory.create_ticker(CryptoType.LITECOIN)
    # xrp_ticker = factory.create_ticker(CryptoType.XRP)

    # TODO: Create multi-ticker for all supported cryptocurrencies
    all_cryptos = TickerFactory.get_supported_cryptos()
    for crypto in all_cryptos:
        ticker = factory.create_ticker(crypto)
        print(ticker.formatted_price)

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

