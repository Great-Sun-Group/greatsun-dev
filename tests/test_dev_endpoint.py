"""
This module contains tests for the security layer and authentication endpoints.

Test Scenarios:
1. Accessing a protected route without a token (should be rejected)
2. Accessing a protected route with an invalid token (should be rejected)
3. Accessing the `/login` route (should be allowed without a token)
4. Accessing the `/onboardMember` route (should be allowed without a token)
5. Accessing a protected route with a valid token (should be allowed)

Additional tests:
6. Successful login
7. Login with invalid phone number
"""

from dotenv import load_dotenv
import unittest
import requests
import os
import json
from requests.exceptions import RequestException, Timeout
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Load environment variables
load_dotenv()

GITHUB_TOKEN = "ghu_NlnzfFagDos7BIK8ui1VlF6BM2UgaR0Dto3Y"
BASE_URL = "https://legendary-rotary-phone-jwjj9jr9xj53g4x-3000.app.github.dev/"
API_VERSION = "api/v1"
WHATSAPP_BOT_API_KEY = os.getenv('WHATSAPP_BOT_API_KEY')


class TestSecurityLayer(unittest.TestCase):
    def make_request(self, url, method='GET', data=None, token=None):
        headers = {
            "Content-Type": "application/json",
            "WHATSAPP_BOT_API_KEY": WHATSAPP_BOT_API_KEY,
            "X-Github-Token": GITHUB_TOKEN
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        print(f"\nAttempting to connect to: {url}")
        print('Request config:', json.dumps({
            'url': url,
            'method': method,
            'headers': headers,
            'data': data
        }, indent=2))

        if method == 'GET':
            response = requests.get(
                url, headers=headers, verify=False, timeout=10)
        else:
            response = requests.post(
                url, json=data, headers=headers, verify=False, timeout=10)

        print("\nResponse status:", response.status_code)
        print("Response headers:", json.dumps(
            dict(response.headers), indent=2))
        print("Response content:", response.text)

        try:
            response_json = response.json()
            print("Response JSON:", json.dumps(response_json, indent=2))
        except json.JSONDecodeError:
            print("Response is not valid JSON")
            response_json = None

        return response, response_json

    def test_protected_route_without_token(self):
        url = f"{BASE_URL}{API_VERSION}/member/getMemberDashboardByPhone"
        try:
            response, _ = self.make_request(url)
            self.assertEqual(response.status_code, 401,
                             "Expected 401 Unauthorized for protected route without token")
            print(
                "\nTest passed: Received 401 Unauthorized for protected route without token")
        except Exception as error:
            self.fail(f"Unexpected error: {str(error)}")

    def test_protected_route_invalid_token(self):
        url = f"{BASE_URL}{API_VERSION}/member/dashboard"
        try:
            response, _ = self.make_request(url, token="invalid_token")
            self.assertEqual(response.status_code, 401,
                             "Expected 401 Unauthorized for protected route with invalid token")
            print(
                "\nTest passed: Received 401 Unauthorized for protected route with invalid token")
        except Exception as error:
            self.fail(f"Unexpected error: {str(error)}")

    def test_login_route_without_token(self):
        url = f"{BASE_URL}{API_VERSION}/member/login"
        data = {"phone": "263778177125"}
        try:
            response, response_json = self.make_request(
                url, method='POST', data=data)
            self.assertEqual(response.status_code, 200,
                             "Expected 200 OK for login route without token")
            self.assertIn('token', response_json,
                          "Response should contain a 'token' field")
            print("\nTest passed: Received 200 OK for login route without token")
        except Exception as error:
            self.fail(f"Unexpected error: {str(error)}")

    def test_onboard_member_route_without_token(self):
        url = f"{BASE_URL}{API_VERSION}/member/onboardMember"
        data = {"phone": "263778177126", "name": "Test User"}
        try:
            response, _ = self.make_request(url, method='POST', data=data)
            self.assertEqual(response.status_code, 200,
                             "Expected 200 OK for onboard member route without token")
            print("\nTest passed: Received 200 OK for onboard member route without token")
        except Exception as error:
            self.fail(f"Unexpected error: {str(error)}")

    def test_protected_route_with_valid_token(self):
        login_url = f"{BASE_URL}{API_VERSION}/member/login"
        login_data = {"phone": "263778177125"}
        try:
            login_response, login_json = self.make_request(
                login_url, method='POST', data=login_data)
            self.assertEqual(login_response.status_code, 200,
                             "Failed to obtain a valid token")
            token = login_json['token']

            protected_url = f"{BASE_URL}{API_VERSION}/member/dashboard"
            response, _ = self.make_request(protected_url, token=token)
            self.assertEqual(response.status_code, 200,
                             "Expected 200 OK for protected route with valid token")
            print("\nTest passed: Received 200 OK for protected route with valid token")
        except Exception as error:
            self.fail(f"Unexpected error: {str(error)}")

    def test_login_endpoint_success(self):
        url = f"{BASE_URL}{API_VERSION}/member/login"
        data = {"phone": "263778177125"}
        try:
            response, response_json = self.make_request(
                url, method='POST', data=data)
            self.assertEqual(response.status_code, 200,
                             "Expected 200 OK response")
            self.assertIn('token', response_json,
                          "Response should contain a 'token' field")
            self.assertIsInstance(
                response_json['token'], str, "Token should be a string")
            self.assertTrue(
                len(response_json['token']) > 0, "Token should not be empty")
            print("\nTest passed: Received 200 OK response with valid token")
        except Exception as error:
            self.fail(f"Unexpected error: {str(error)}")

    def test_login_endpoint_invalid_phone(self):
        url = f"{BASE_URL}{API_VERSION}/member/login"
        data = {"phone": "invalid_phone_number"}
        try:
            response, response_json = self.make_request(
                url, method='POST', data=data)
            self.assertEqual(response.status_code, 400,
                             "Expected 400 Bad Request for invalid phone number")
            self.assertIn('message', response_json,
                          "Response should contain an error message")
            self.assertIsInstance(
                response_json['message'], str, "Error message should be a string")
            print("\nTest passed: Received 400 Bad Request for invalid phone number")
        except Exception as error:
            self.fail(f"Unexpected error: {str(error)}")


if __name__ == '__main__':
    unittest.main()
