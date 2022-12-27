import requests
from ..conf import CF_ACCOUNT_ID, cf_headers

URL = "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/images/v1"


def cf_image(url):
    data = {
        'url': url,
    }
    response = requests.post(URL.format(ACCOUNT_ID=CF_ACCOUNT_ID),
                             data=data,
                             headers=cf_headers)
    response.raise_for_status()
    response_data = response.json()
    return response_data['result']['variants']
