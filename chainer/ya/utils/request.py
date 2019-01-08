import requests
from chainer.training import extension


class FinalRequest(extension.Extension):
    def __init__(self, url, method="GET", **kwargs):
        self.url = url
        self.method = method
        self.kwargs = kwargs

    def finalize(self):
        requests.request(self.method, self.url, **self.kwargs)
