from decouple import config as decouple_config

class Env:

    def __init__(self):
        self._config = {}

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def set_item(self, key: str, value: str):
        self._config[key] = value

    def get_item(self, key: str, default: None):
        default_config = self._config[key] if self._config else default
        return decouple_config(key, default=default_config)

    def testing(self):
        return self.get_item('ENVIRONMENT') == 'testing'

    def test_or_dev(self):
        return self.get_item('ENVIRONMENT') == 'development' or self.testing()

env: Env = Env()