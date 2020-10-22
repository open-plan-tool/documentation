import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from jsonview.decorators import json_view
from projects.models import Scenario


@json_view
@login_required
@require_http_methods(["GET"])
def timeseries_chart_jsonview(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)
    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    if request.method == "GET" and request.is_ajax():
        return JsonResponse({"test": 1})


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
    asset_type_json = [
        [
            {
                'assetCategory': asset_category,
                'assetType': asset_type
            }
            for asset_type in dict_values[asset_category].keys()
        ]
        for asset_category in asset_category_list
    ]

    response_json = {'options': asset_type_json, 'optgroups': asset_category_json}

    return JsonResponse(response_json, status=200, content_type='application/json')


@login_required
@require_http_methods(["GET", "POST"])
def scenario_visualize_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    if request.method == "GET":
        with open('static/tempFiles/json_with_results.json') as json_file:
            dict_values = json.load(json_file)
        test_data = dict_values['energyProduction']['DSO_consumption']['flow']['data']

        # TODO: Take time from simulation settings
        test_times = dict_values['energyProduction']['DSO_consumption']['flow']['index']

        return render(request, 'scenario/scenario_visualize_results.html',
                      {'scenario_id': scen_id, 'tData': test_data, 'tTime': test_times})
    elif request.method == "POST" and request.is_ajax():
        pass
