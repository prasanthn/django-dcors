import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = "settings_test"

from django.utils import unittest
from django.test.client import Client
from django.test.utils import override_settings


class Tests(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_default_headers(self):
        # CORS is disabled by default, but headers will be present
        r = self.client.get("/")
        self.assertEqual(r['Access-Control-Allow-Origin'], '')
        self.assertEqual(r['Access-Control-Allow-Methods'], '')
        self.assertEqual(r['Access-Control-Allow-Headers'], '')
        self.assertEqual(r['Access-Control-Allow-Credentials'], "false")
        self.assertEqual(r['Access-Control-Expose-Headers'], '')
        self.assertEqual(r['Access-Control-Max-Age'], '0')

        r = self.client.options("/")
        self.assertEqual(r['Access-Control-Allow-Origin'], '')
        self.assertEqual(r['Access-Control-Allow-Methods'], '')
        self.assertEqual(r['Access-Control-Allow-Headers'], '')
        self.assertEqual(r['Access-Control-Allow-Credentials'], "false")
        self.assertEqual(r['Access-Control-Expose-Headers'], '')
        self.assertEqual(r['Access-Control-Max-Age'], '0')

    @override_settings(CORS_ALLOW_ORIGIN="http://www.example.com",
        CORS_ALLOW_METHODS=["get", "post"])
    def test_preflight(self):
        # Pre-flight OPTIONS request
        r = self.client.options("/")
        self.assertEqual(r['Access-Control-Allow-Origin'], 'http://www.example.com')
        self.assertEqual(r['Access-Control-Allow-Methods'], 'get,post')
        self.assertEqual(r['Access-Control-Allow-Headers'], '')
        self.assertEqual(r['Access-Control-Allow-Credentials'], "false")
        self.assertEqual(r['Access-Control-Expose-Headers'], '')
        self.assertEqual(r['Access-Control-Max-Age'], '0')

    @override_settings(CORS_ALLOW_ORIGIN="*",
        CORS_ALLOW_CREDENTIALS="true", CORS_ALLOW_ALL_ORIGIN=True)
    def test_crendentials_and_origin(self):
        r = self.client.get("/", HTTP_ORIGIN="http://www.example.com")
        self.assertEqual(r['Access-Control-Allow-Origin'], 'http://www.example.com')
        self.assertEqual(r['Access-Control-Allow-Methods'], '')
        self.assertEqual(r['Access-Control-Allow-Headers'], '')
        self.assertEqual(r['Access-Control-Allow-Credentials'], "true")
        self.assertEqual(r['Access-Control-Expose-Headers'], '')
        self.assertEqual(r['Access-Control-Max-Age'], '0')


if __name__ == "__main__":
    p = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, p)  # Add dcors to path

    from django.test.simple import DjangoTestSuiteRunner
    # The tests are in this file itself. But dcors is added to path above, and
    # is also in INSTALLED_APPS in settings_test.py. So we can run the tests
    # as a Django test suite.
    DjangoTestSuiteRunner(failfast=False).run_tests([
        'dcors.Tests'
    ], verbosity=1, interactive=True)
