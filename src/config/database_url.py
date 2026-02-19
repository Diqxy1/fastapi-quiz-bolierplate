from decouple import config

class DatabaseUrl:

    def __init__(
        self, host: str = None, port: str = None, engine: str = None, driver: str = None,
        database: str = None, user: str = None, password: str = None, charset: str = None
        ):
        self._host = host or config('DB_HOST')
        self._port = port or config('DB_PORT')
        self._engine = engine or config('DB_ENGINE')
        self._driver = driver or config('DB_DRIVER')
        self._database = database or config('DB_DATABASE')
        self._user = user or config('DB_USER')
        self._password = password or config('DB_PASSWORD')
        self._charset = charset or config('DB_CHARSET')

    def get_database_url(self):
        if config('ENVIRONMENT') == 'development':
            driver = f'{self._engine}+{self._driver}'
            credential = f'{self._user}:{self._password}'
            host = f'{self._host}:{self._port}'
            database_url = f'{driver}://{credential}@{host}/{self._database}'
        if self._engine == 'sqlite':
            database_url = f'{self._engine}:///./{self._database}.db'
            return database_url
        return database_url