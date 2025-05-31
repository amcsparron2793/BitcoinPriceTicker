class UnsupportedCryptoError(Exception):
    def __init__(self, crypto_type: 'CryptoType', supported_types: list[str]):
        self.crypto_type = crypto_type
        self.supported_types = supported_types
        self.supported_types_string = ", ".join(self.supported_types)
        self.message = (f"Unsupported cryptocurrency: {self.crypto_type} "
                        f"Supported types: {self.supported_types_string}")
        super().__init__(self.message)


class CoinDeskApiError(Exception):
    """Custom exception for Bitcoin API related errors"""
    pass
