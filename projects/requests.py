from datetime import datetime

import requests
import json
from requests.exceptions import HTTPError

from epa.settings import PROXY_CONFIG, MVS_POST_URL, MVS_GET_URL
from dashboard.models import KPIResults


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
    DONE = 'DONE'
    FAILED = 'FAILED'
    if simulation.status not in ['3']:  #[FAILED, DONE]:
        response = mvs_simulation_check(token=simulation.mvs_token)
        simulation.status = response['status']

        try:
            simulation.results = parse_mvs_results(simulation, response['results']) if simulation.status == DONE else None
        except:
            simulation.results = None

        simulation.elapsed_seconds = (datetime.now() - simulation.start_date).seconds
        simulation.end_date = datetime.now() if response['status'] in [FAILED, DONE] else None
        simulation.save()


def parse_mvs_results(simulation, response_results):
    with open('../static/tempFiles/json_with_results.json', 'r') as expected_file:
        expected_json = json.load(expected_file)

    # keys for json_with_results.json
    asset_key_list = ['energyProviders', 'energyConsumption', 'energyConversion',
                      'energyProduction', 'energyStorage', 'kpi']

    # keys for 3aea5991-324b-41fc-99d8-0c1856a4279a(MVS API OUTPUT).json
    asset_key_list = ['energyProviders', 'energyConsumption', 'energyConversion',
                      'energyProduction', 'energyStorage', 'kpi']

    if not set(asset_key_list).issubset(expected_json.keys()):
        return "ERROR"

    # write the scalar results to db
    kpi_results = KPIResults(simulation=simulation, attributed_costsElectricity=0.3)



    gather_all_objects = [expected_json[item] for item in asset_key_list]

    print(expected_json.keys())

