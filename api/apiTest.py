import requests

BASE_API_URL = 'https://solodit.xyz/api/'
AUTHORIZATION_HEADER = {
    'Authorization': 'Token f7cddb5d3cc4600e8e4f30e478158e71c0ca8dfb' # Replace with your actual authorization token
}

def make_authorized_request(endpoint, params=None):
    url = BASE_API_URL + endpoint
    headers = AUTHORIZATION_HEADER
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f" error status code not 200: {response.json()}"
print(make_authorized_request("auditfirms/"))