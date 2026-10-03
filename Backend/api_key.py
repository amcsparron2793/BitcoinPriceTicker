from pathlib import Path
from .err import NoAPIKeyError


class ApiKey:
    DEFAULT_KEY_LOCATION = './api_key.key'
    def __init__(self, **kwargs):
        self.api_key = kwargs.get('api_key', None)
        self.api_key_location = Path(kwargs.get('api_key_location',
                                                self.__class__.DEFAULT_KEY_LOCATION))
    def get_api_key(self):
        if self.api_key:
            return self.api_key
        try:
            with open(self.api_key_location, 'r') as f:
                self.api_key = f.read().strip()
        except FileNotFoundError as e:
            raise NoAPIKeyError(e)
        return self.api_key