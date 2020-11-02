import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from jsonview.decorators import json_view
from pandas.io.json import json_normalize
# import pandas as pd

from projects.models import Scenario


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

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    return render(request, 'scenario/scenario_visualize_results.html',
                  {'scenario_id': scen_id})


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_economic_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    with open('static/tempFiles/json_with_results.json') as json_file:
        dict_values = json.load(json_file)
    # TODO: Fix this

    # energy_type_keys = ['energyConsumption', 'energyConversion', 'energyProduction', 'energyProviders', 'energyStorage']
    kpi_economic_data_list = ["costs_total", "annuity_total", "costs_upfront_in_year_zero", "annuity_om", "levelized_cost_of_energy_of_asset"]
    cost_matrix_cols = dict_values["kpi"]["cost_matrix"]
    # df = json_normalize(cost_matrix_cols)
    # df = pd.DataFrame(cost_matrix_cols["data"], index=cost_matrix_cols["index"], columns=cost_matrix_cols["columns"])
    results = list()

    results_json = [
        {
            'values': dict_values['kpi']['cost_matrix']["data"][i][1:4],
            'labels': ['Cost Total', 'Cost OM Total', 'Cost investment over Time'],
            'type': 'pie',
            'title': dict_values['kpi']['cost_matrix']["data"][i][0]
        }
        for i in [3, 8, 10]
    ]

    return JsonResponse(results_json, status=200, content_type='application/json', safe=False)


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_scalar_kpi_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    with open('static/tempFiles/json_with_results.json') as json_file:
        dict_values = json.load(json_file)
    # TODO: Fix this

    results_json = [
        {
            'kpi': key,
            'value': val,
        }
        for key, val in dict_values['kpi']['scalars'].items()
    ]

    return JsonResponse(results_json, status=200, content_type='application/json', safe=False)
