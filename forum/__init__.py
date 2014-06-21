import threading


class RequestHolder(object):
    _requests = threading.local()

    @property
    def request(self):
        return self._requests.request

    @request.setter
    def request(self, value):
        self._requests.request = value

REQUEST_HOLDER = RequestHolder()
