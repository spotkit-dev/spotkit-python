import unittest
from unittest.mock import patch
from requests.auth import HTTPBasicAuth
from spotkit.api import spotkitAPI

class TestspotkitAPI(unittest.TestCase):

    @patch('requests.get')
    def test_get_current_user(self, mock_get):
        # Mock the response to simulate the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": "12345",
            "name": "Test User",
            "email": "testuser@example.com"
        }

        # Initialize the API client
        api = spotkitAPI(client_id="dummy_id", client_secret="dummy_secret", use_basic_auth=True)

        # Call the method being tested
        result = api.get_current_user()

        # Assertions
        self.assertEqual(result['id'], "12345")
        self.assertEqual(result['name'], "Test User")
        self.assertEqual(result['email'], "testuser@example.com")
        mock_get.assert_called_once_with(
            "https://api.latest.highspot.com/v1.0/me",
            headers={
                'Authorization': '',
                'Content-Type': 'application/json',
            },
            params=None,
            auth=HTTPBasicAuth("dummy_id", "dummy_secret")
        )

if __name__ == '__main__':
    unittest.main()