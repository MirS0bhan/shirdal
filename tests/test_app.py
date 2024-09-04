import unittest
from unittest.mock import Mock

# Assuming the Application and Container classes are defined in a module named 'app_module'
from shirdal import Application


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application()
        self.mock_service = Mock()
        self.mock_dt = Mock()

    def test_service_registration(self):
        # Register the mock service
        self.app.service(self.mock_service)

        # Check if the service is registered in the container
        self.assertIn(self.mock_service, self.app.container)

    def test_operate(self):
        # Register a mock service that we can call
        def mock_endpoint(dt):
            dt.result = 6985
            return "Service called with data: {}".format(dt)

        # Register the mock endpoint
        self.app.service(mock_endpoint)

        # Set up the mock data transfer object (dt)
        self.mock_dt.endpoint = 'mock_endpoint'
        self.mock_dt.some_data = "test data"

        # Call the operate method
        result = self.app.operate(self.mock_dt)

        # Check if the result is as expected
        self.assertEqual(6985, self.mock_dt.result)


if __name__ == '__main__':
    unittest.main()
