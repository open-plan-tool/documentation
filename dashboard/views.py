import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from jsonview.decorators import json_view
from pandas.io.json import json_normalize
import pandas as pd

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
    asset_name_json = [
        [
            {
                'assetCategory': asset_category,
                'assetName': asset_name
            }
            for asset_name in dict_values[asset_category].keys()
        ]
        for asset_category in asset_category_list
    ]

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
    df = pd.DataFrame(cost_matrix_cols["data"], index=cost_matrix_cols["index"], columns=cost_matrix_cols["columns"])
    results = list()

    # for column in cost_matrix_cols:
    #     pass
    # for economic_kpi in kpi_economic_data_list:
    #     values = list()
    #     labels = list()
    #     for energy_type in energy_type_keys:
    #         for asset in dict_values[energy_type].keys():
    #             if dict_values[energy_type][asset][economic_kpi] and dict_values[energy_type][asset][economic_kpi]['value'] != 0:
    #                 values.append(dict_values[energy_type][asset][economic_kpi]['value'])
    #                 labels.append(asset)
    #
    #     results.append({
    #         'values': values,
    #         'labels': labels,
    #         'type': 'pie'
    #     })
    # Generate results JSON per asset name
    results_json = [
        {
            'values': [dict_values['kpi']['cost_matrix']["data"][1]],
            'labels': ['Residential', 'Non-Residential', 'Utility'],
            'type': 'pie'
        }
        # for asset_index in asset_index_list
    ]

    return JsonResponse(results_json, status=200, content_type='application/json', safe=False)
