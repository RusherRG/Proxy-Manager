import os
import unittest
import threading

# import test modules
from .mockapi_server import app
from . import mockapi
from . import secrets_config
from . import request_middleware

from request_middleware.rate_limit_utils import update_secrets


def setup():
    # start mockapi_server

    thread = threading.Thread(target=app.run, args=("localhost", 5555))
    thread.daemon = True
    thread.start()
    # update_secrets()


def run():
    # initialize the test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(mockapi))
    suite.addTests(loader.loadTestsFromModule(request_middleware))

    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
