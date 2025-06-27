from typing import Optional

from MultiTicker.multi_ticker import MultiTicker
from Backend.factory import TickerFactory
from Backend.helpers import CryptoType


class Ticker:
    MULTI_MODE = 'multi'
    FACTORY_MODE = 'factory'
    VALID_MODES = [MULTI_MODE, FACTORY_MODE]
    def __init__(self,  mode, factory: Optional[TickerFactory]=None, **kwargs):
        self._mode = None

        self.factory = factory or TickerFactory()
        self.crypto_type: Optional[CryptoType | str] = kwargs.get('crypto_type', None)

        if isinstance(self.crypto_type, str):
            self.crypto_type = CryptoType.from_string(self.crypto_type)

        self.params = kwargs.get('params', None)
        self.base_url = kwargs.get('base_url', None)
        self.mode = mode
        self.use_colorizer = kwargs.get('use_colorizer', True)
        self.ticker = self._initialize_ticker()

    def _initialize_ticker(self):
        if self.mode == self.__class__.MULTI_MODE:
            initialized_ticker = MultiTicker(self.factory,
                                             crypto_types=self.crypto_type,
                                             params=self.params,
                                             use_colorizer=self.use_colorizer)
        elif self.mode == self.__class__.FACTORY_MODE and self.crypto_type is not None:
            initialized_ticker = self.factory.create_ticker(self.crypto_type, self.params)
        else:
            raise AttributeError('Invalid mode or crypto_type')

        return initialized_ticker

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value.lower() if value in self.__class__.VALID_MODES else 'err'
        if self._mode == 'err':
            raise AttributeError('Invalid mode')

    def run(self):
        self.ticker.continuous_check()


if __name__ == '__main__':
    tk_factory = TickerFactory()
    # mt = Ticker(mode='multi')
    mt = Ticker(mode='factory', factory=tk_factory, crypto_type='bitcoin')
    mt.run()