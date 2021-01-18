from dashboard.models import AssetsResults, KPICostsMatrixResults, KPIScalarResults
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from jsonview.decorators import json_view
from projects.models import Scenario
import json


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_available_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)
    if scenario.project.user != request.user:
        return HttpResponseForbidden()
    
    try:
        assets_results_obj = AssetsResults.objects.get(simulation=scenario.simulation)
        assets_results_json = json.loads(assets_results_obj.assets_list)

        # Generate available asset category JSON
        asset_category_json = [{'assetCategory': asset_category} for asset_category in assets_results_json.keys()]
        # Generate available asset type JSON
        assets_names_json = [
            [
                {
                    'assetCategory': asset_category,
                    'assetName': asset['label']
                }
                for asset in assets_results_json[asset_category]
                # show only assets of a certain Energy Vector
                if asset['energy_vector'] == request.GET['energy_vector']
            ]
            for asset_category in assets_results_json.keys()
        ]
        response_json = {'options': assets_names_json, 'optgroups': asset_category_json}
        return JsonResponse(response_json, status=200, content_type='application/json')
    except:
        return JsonResponse({"error": "Could not retrieve asset names and categories."},
                            status=404, content_type='application/json')


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
                'title': category.replace('_',' ')
            }
            for category in new_dict.keys()
            if sum(new_dict[category].values()) > 0.0  # there is at least one non zero value
            and len(list(filter(lambda asset_name: new_dict[category][asset_name] > 0.0 ,new_dict[category]))) > 1.0
            # there are more than one assets with value > 0
        ]
        return JsonResponse(results_json, status=200, content_type='application/json', safe=False)
    except:
        return JsonResponse({"error":"Could not retrieve kpi cost data."}, status=404, content_type='application/json', safe=False)
    """
    # dummy data
    """
    # dummy_title_list = ["Annuity Costs", "Upfront Investment Costs", "Operation and Maintenance Costs"]
    # dummy_asset_list = ["PV Plant", "Transformer Station", "Wind Plant", "Electricity Grid Consumption"]
    # results_json = [
    #     {
    #         'values': [randint(30, 70) for j in range(4)],
    #         'labels': random.choices(dummy_asset_list, k=3),
    #         'type': 'pie',
    #         'title': dummy_title_list[i]
    #     }
    #     for i in range(3)
    # ]


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
