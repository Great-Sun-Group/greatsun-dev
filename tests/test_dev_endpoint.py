import os
import requests
import json

BASE_URL = 'http://localhost:5000/api/v1'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

def test_dev_endpoint():
    print(f"Testing Dev Endpoint: {BASE_URL}/dev/members")
    print(f"GitHub Token available: {'Yes' if GITHUB_TOKEN else 'No'}")

    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/json'
    }

    try:
        response = requests.get(
            f'{BASE_URL}/dev/members',
            params={'count': 5},
            headers=headers
        )
        
        print(f'Response status: {response.status_code}')
        print('Response headers:')
        for key, value in response.headers.items():
            print(f"{key}: {value}")
        
        print('\nRaw response content:')
        print(response.text)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print('\nParsed JSON data:')
                print(json.dumps(data, indent=2))
                if isinstance(data, list) and len(data) > 0:
                    print('\nExample member:')
                    print(f"Phone: {data[0].get('phone')}")
                    print(f"Member ID: {data[0].get('memberID')}")
                else:
                    print('No members returned or unexpected data format')
            except ValueError as e:
                print(f"Error parsing JSON: {str(e)}")
        else:
            print(f'Error: Unexpected status code {response.status_code}')
    
    except requests.RequestException as e:
        print(f'Error making request: {str(e)}')
    except Exception as e:
        print(f'Unexpected error: {str(e)}')

if __name__ == '__main__':
    test_dev_endpoint()
