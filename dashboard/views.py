from dashboard.models import KPICostsMatrixResults, KPIScalarResults
import json
import random
from random import randrange, randint
from itertools import groupby
from operator import itemgetter
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from jsonview.decorators import json_view
# from pandas.io.json import json_normalize
# import pandas as pd

from projects.models import Scenario, Asset


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_available_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    with open('static/tempFiles/json_with_results.json') as json_file:
        dict_values = json.load(json_file)

    asset_category_list = [
        'energyProviders', 'energyConsumption', 'energyConversion', 'energyStorage', 'energyProduction']

    # Generate available asset category JSON
    asset_category_json = [
        {
            'assetCategory': asset_category
        }
        for asset_category in asset_category_list
    ]

    # Generate available asset type JSON
    try:
        asset_name_json = [
            [
                {
                    'assetCategory': asset_category,
                    'assetName': asset_name
                }
                for asset_name in dict_values[asset_category].keys()
                # show only assets of a certain Energy Vector
                if dict_values[asset_category][asset_name]['energyVector'] == request.GET['energy_vector']
            ]
            for asset_category in asset_category_list
        ]
    except KeyError:
        return JsonResponse({"error": "energyVector field missing from asset"},
                            status=400, content_type='application/json')

    response_json = {'options': asset_name_json, 'optgroups': asset_category_json}

    return JsonResponse(response_json, status=200, content_type='application/json')


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_request_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    with open('static/tempFiles/json_with_results.json') as json_file:
        dict_values = json.load(json_file)

    asset_name_list = request.GET.get('assetNameList').split(',')

    asset_category_list = [
        'energyProviders', 'energyConsumption', 'energyConversion', 'energyStorage', 'energyProduction']

    # Asset category to asset type
    asset_name_to_category = {
            asset_name: asset_category
            for asset_category in asset_category_list
            for asset_name in dict_values[asset_category]
        }

    # Generate results JSON per asset name
    results_json = [
        {
            'xAxis':
                {
                    'values': dict_values[asset_name_to_category[asset_name]][asset_name]['flow']['index'],
                    'label': 'Time'
                },
            'yAxis':
                {
                    'values': dict_values[asset_name_to_category[asset_name]][asset_name]['flow']['data'],
                    'label': 'Power'
                },
            'title': asset_name
        }
        for asset_name in asset_name_list
    ]

    return JsonResponse(results_json, status=200, content_type='application/json', safe=False)


@login_required
@require_http_methods(["GET"])
def scenario_visualize_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    # TODO: Handle the MVS file results and show to user
    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    return render(request, 'scenario/scenario_visualize_results.html',
                  {'scenario_id': scen_id})


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_economic_results(request, scen_id):
    """
    This view gather all simulation specific cost matrix KPI results
    and send them to the clent for representation.
    """
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()
    
    try:
        kpi_cost_results_obj = KPICostsMatrixResults.objects.get(simulation=scenario.simulation)
        kpi_cost_values_dict = json.loads(kpi_cost_results_obj.cost_values)

        new_dict = dict()
        for asset_name in kpi_cost_values_dict.keys():
            for category,v in kpi_cost_values_dict[asset_name].items():
                new_dict.setdefault(category, {})[asset_name] = v
        
        # non-dummy data
        results_json = [
            {
                'values': list(new_dict[category].values()),
                'labels': list(new_dict[category].keys()),
                'type': 'pie',
                'title': category
            }
            for category in new_dict.keys()
            if sum(new_dict[category].values()) > 0.0  # there is at least one non zero value
            and len(list(filter(lambda asset_name: new_dict[category][asset_name] > 0.0 ,new_dict[category]))) > 1.0
            # there are more than one assets with value > 0
        ]
    except:
        pass
    """
    # dummy data
    """
    dummy_title_list = ["Annuity Costs", "Upfront Investment Costs", "Operation and Maintenance Costs"]
    dummy_asset_list = ["PV Plant", "Transformer Station", "Wind Plant", "Electricity Grid Consumption"]
    # results_json = [
    #     {
    #         'values': [randint(30, 70) for j in range(4)],
    #         'labels': random.choices(dummy_asset_list, k=3),
    #         'type': 'pie',
    #         'title': dummy_title_list[i]
    #     }
    #     for i in range(3)
    # ]

    return JsonResponse(results_json, status=200, content_type='application/json', safe=False)


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_scalar_kpi_results(request, scen_id):
    """
    This view gather scalar KPI Results from the database and sends them
    in JSON format to the front end for representation.
    # TODO: Integrate to scenario_visualize_results view and render data in for loop template
    """
    scenario = get_object_or_404(Scenario, pk=scen_id)
    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    try:
        kpi_scalar_results_obj = KPIScalarResults.objects.get(simulation=scenario.simulation)
        kpi_scalar_values_dict = json.loads(kpi_scalar_results_obj.scalar_values)

        results_json = [
            {
                'kpi': key.replace('_',' '),
                'value': val,
                'unit': 'currency' if 'cost' in key else ('energy' if 'electricity' or 'energy' in key else None) 
            }
            for key, val in kpi_scalar_values_dict.items()
        ]

        return JsonResponse(results_json, status=200, content_type='application/json', safe=False)
    except:
        return JsonResponse({'error'}, status=404, content_type='application/json', safe=False)
