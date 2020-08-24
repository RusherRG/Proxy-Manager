import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from rate_limit_utils import get_secret, update_count


class Request:
    def __init__(self, endpoint, secret_type, cache=True):
        self.endpoint = endpoint
        self.source_type = secret_type
        self.cache = cache
        self.secret = None
        self.session = None
        self.user_agent_rotator = None
        self.count = 0
        self.create_session()

    def create_session(self):
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value]
        self.user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems,
            limit=100)

        self.session = requests.Session()
        return

    def close_session(self):
        logger.info("Closing session")
        if self.secret is not None and self.count > 0:
            update_count(self.secret, self.endpoint,
                         self.secret_type, self.count)

    def add_user_agent(self, headers={}):
        headers['User-Agent'] = user_agent_rotator.get_random_user_agent()
        return

    def get_key_proxy(self):
        if self.secret is not None and self.count > 0:
            update_count(self.secret, self.endpoint,
                         self.secret_type, self.count)
        self.count = 0
        self.secret = get_secret(self.secret_type, self.endpoint)
        return self.secret

    def send(self, method, url, **kwargs):
        request = requests.Request(method, url, **kwargs)
        if self.cache:
            self.check_cache(method, url, **kwargs)
        logger.debug("Sending request: {}".format(request))
        self.count += 1
        return self.session.send(request.prepare())

    def run(self):
        """
        Run multiple requests async
        """
        pass

    def check_cache(self, **kwargs):
        """
        Check for already existing request
        """
        print(**kwargs)
        return False
