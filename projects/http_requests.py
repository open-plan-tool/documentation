import requests
import json
from requests.exceptions import HTTPError

from epa.settings import PROXY_CONFIG, MVS_URL


def mvs_simulation_request(data: dict):

    headers = {'content-type': 'application/json'}
    payload = json.dumps(data)

    try:
        response = requests.get(MVS_URL, data=payload, headers=headers, proxies=PROXY_CONFIG)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None
    else:
        print('Success!')
        return json.loads(response.text)
