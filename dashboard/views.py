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

    json_to_db()

    return JsonResponse(results_json, status=200, content_type='application/json', safe=False)


def json_to_db():
    with open('static/tempFiles/EPA_input.json') as json_file:
        dict_values = json.load(json_file)

    energy_types = ['energyProviders', 'energy_consumption', 'energy_conversion', 'energy_production', 'energy_storage']

    for item in energy_types:
        key_list = list()
        for obj in dict_values[item]:
            [key_list.append(key) for key, val in obj.items() if key not in key_list]
        print("{}: {}".format(item, key_list))

    energyProviders = ['connected_consumption_sources', 'connected_feedin_sink', 'development_costs', 'dispatch_price',
                      'energy_price', 'energy_vector', 'feedin_tariff', 'inflow_direction', 'installed_capacity',
                      'label', 'lifetime', 'optimize_capacity', 'outflow_direction', 'peak_demand_pricing',
                      'peak_demand_pricing_period', 'renewable_share', 'specific_costs', 'specific_costs_om',
                      'type_oemof', 'unit']
    energy_consumption= ['development_costs', 'dispatch_price', 'energy_vector', 'inflow_direction', 'input_bus_name',
                         'input_timeseries', 'installed_capacity', 'label', 'lifetime', 'optimize_capacity',
                         'specific_costs', 'specific_costs_om', 'type_oemof']
    energy_conversion= ['age_installed', 'development_costs', 'dispatch_price', 'efficiency', 'energy_vector',
                        'inflow_direction', 'input_bus_name', 'installed_capacity', 'label', 'lifetime',
                        'maximum_capacity', 'optimize_capacity', 'outflow_direction', 'output_bus_name',
                        'specific_costs', 'specific_costs_om', 'type_oemof']
    energy_production= ['age_installed', 'development_costs', 'dispatch_price', 'dispatchable', 'energy_vector',
                        'installed_capacity', 'label', 'lifetime', 'maximum_capacity', 'optimize_capacity',
                        'outflow_direction', 'output_bus_name', 'renewable_asset', 'specific_costs',
                        'specific_costs_om', 'type_oemof', 'input_timeseries']
    energy_storage= ['energy_vector', 'inflow_direction', 'input power', 'input_bus_name', 'label', 'optimize_capacity',
                     'outflow_direction', 'output power', 'output_bus_name', 'storage capacity', 'type_oemof']

    set(energy_consumption).intersection(set(energy_conversion)).intersection(set(energy_production)) \
        .intersection(set(energy_storage)).intersection(set(energyProviders))
    # {'type_oemof', 'energy_vector', 'optimize_capacity', 'label'}

    set(energy_consumption).intersection(set(energy_conversion)).intersection(set(energy_production))
    # {'energy_vector', 'label', 'dispatch_price', 'specific_costs_om', 'specific_costs', 'development_costs', 'type_oemof', 'lifetime', 'optimize_capacity', 'installed_capacity'}

    set(energy_production).symmetric_difference(set(energyProviders))

    set(energy_production).union(set(energy_consumption)).union(set(energy_conversion)).union(set(energy_storage))
    # {'age_installed', 'lifetime', 'dispatch_price', 'efficiency', 'type_oemof', 'development_costs',
    # 'optimize_capacity', 'outflow_direction', 'output_bus_name', 'input_bus_name', 'output power',
    # 'installed_capacity', 'label', 'specific_costs', 'maximum_capacity', 'inflow_direction', 'specific_costs_om',
    # 'input_timeseries', 'input power', 'storage capacity', 'renewable_asset', 'energy_vector', 'dispatchable'}

    set(energy_production).union(set(energy_consumption)).union(set(energy_conversion)).union(set(energy_storage)).union(set(energyProviders))
    # {'efficiency', 'peak_demand_pricing_period', 'output power', 'connected_feedin_sink', 'specific_costs',
    # 'connected_consumption_sources', 'maximum_capacity', 'renewable_share', 'input_timeseries', 'input power',
    # 'renewable_asset', 'energy_vector', 'dispatchable', 'age_installed', 'feedin_tariff', 'lifetime',
    # 'dispatch_price', 'type_oemof', 'development_costs', 'optimize_capacity', 'outflow_direction',
    # 'output_bus_name', 'input_bus_name', 'installed_capacity', 'label', 'inflow_direction', 'specific_costs_om',
    # 'storage capacity', 'unit', 'energy_price', 'peak_demand_pricing'}
