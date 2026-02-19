class BaseException(Exception):

    _status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self._message = message
        if status_code is not None:
            self._status_code = status_code
        self._payload = payload

    @property
    def message(self):
        return self._message

    @property
    def status_code(self):
        return self._status_code

    @property
    def payload(self):
        return self._payload

    def to_dict(self):
        rv = dict(self.payload or ())
        return rv