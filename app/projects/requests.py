from datetime import datetime

import requests
import json
from requests.exceptions import HTTPError

from epa.settings import PROXY_CONFIG, MVS_POST_URL, MVS_GET_URL


def mvs_simulation_request(data: dict):

    headers = {'content-type': 'application/json'}
    payload = json.dumps(data)

    try:
        response = requests.post(MVS_POST_URL, data=payload, headers=headers, proxies=PROXY_CONFIG, verify=False)

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


def mvs_simulation_check(token):
    try:
        response = requests.get(MVS_GET_URL+token, proxies=PROXY_CONFIG, verify=False)
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


def check_mvs_simulation(simulation):
    if simulation.status not in ['FAILED', 'DONE']:
        response = mvs_simulation_check(token=simulation.mvs_token)
        simulation.results = response['results']
        simulation.status = response['status']
        simulation.elapsed_seconds = (datetime.now() - simulation.start_date).seconds
        simulation.end_date = datetime.now() if response['status'] == 'DONE' else None
        simulation.save()
