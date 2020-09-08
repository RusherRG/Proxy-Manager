import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from utils import get_logger
from .rate_limit_utils import get_secret, update_count
from .elasticsearch_utils import get_cached_response, cache_response, \
    log_request

logger = get_logger(__name__)


class Request:
    def __init__(self, secret_type=None, endpoint=None, cache=True):
        self.source_type = secret_type
        self.endpoint = endpoint
        self.cache = cache
        self.secret = None
        self.session = None
        self.user_agent_rotator = None
        self.count = 0
        self.create_session()

    def create_session(self):
        """
        Initializes the variables and creates a requests Session
        """
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value]
        self.user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems,
            limit=100)

        self.session = requests.Session()
        return

    def close_session(self):
        """
        Closes the session and updates the count for the current secret
        """
        logger.info("Closing session")
        if self.secret is not None and self.count > 0:
            update_count(self.source_type, self.endpoint,
                         self.secret, self.count)

    def add_user_agent(self, headers={}):
        headers['User-Agent'] = self.user_agent_rotator.get_random_user_agent()
        return

    def get_key_proxy(self):
        if self.secret is not None and self.count > 0:
            update_count(self.source_type, self.endpoint,
                         self.secret, self.count)
        self.count = 0
        self.secret = get_secret(self.source_type, self.endpoint)
        return self.secret

    def send(self, method, url, proxies=None, **kwargs):
        """
        Sends the request as per the provided config. Checks the cache if
        self.cache==True. Logs the requests and caches the response
        """
        request = requests.Request(method, url, **kwargs)
        if self.cache:
            response = self.check_cache(method=method, url=url,
                                        data=request.data,
                                        params=request.params)
            if response is not None:
                return response
        logger.debug("Sending request: {}".format(request))
        self.count += 1
        response = self.session.send(request.prepare(), proxies=proxies)
        if self.cache:
            cache_response(method=method, url=url,
                           data=request.data, params=request.params,
                           response=response)
        log_request(method=method, url=url, endpoint=self.endpoint,
                    secret_type=self.source_type, secret=self.secret)
        return response

    def run(self):
        """
        Run multiple requests async
        """
        pass

    def check_cache(self, method, url, data=None, params=None):
        """
        Check for already existing request
        """
        request_query = {
            "method": method,
            "url": url,
            "data": data,
            "params": params
        }
        cached_response = get_cached_response(request_query)
        return cached_response
