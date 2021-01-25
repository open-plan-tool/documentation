from django.http.response import Http404
from dashboard.helpers import storage_asset_to_list
from dashboard.models import AssetsResults, KPICostsMatrixResults, KPIScalarResults, KPI_COSTS_TOOLTIPS, KPI_SCALAR_UNITS
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from jsonview.decorators import json_view
from projects.models import Scenario
import json
import datetime


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

        # bring all storage subasset one level up to show their flows.
        storage_asset_to_list(assets_results_json)

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
                and any(key in ['flow','timeseries_soc'] for key in asset.keys())
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
    
    # real data
    try:
        asset_name_list = request.GET.get('assetNameList').split(',')
        assets_results_obj = AssetsResults.objects.get(simulation=scenario.simulation)
        assets_results_json = json.loads(assets_results_obj.assets_list)

        # Generate available asset category list
        asset_category_list = [asset_category for asset_category in assets_results_json.keys()]
        
        # bring all storage subasset one level up to show their flows.
        storage_asset_to_list(assets_results_json)

        # Asset category to asset type
        asset_name_to_category = {
                asset_name['label']: asset_category
                for asset_category in asset_category_list
                for asset_name in assets_results_json[asset_category]
            }

        # Create the datetimes index. Constrains: step in minutes and evaluated_period in days
        base_date = scenario.start_date
        datetime_list = [
            datetime.datetime.timestamp(base_date + datetime.timedelta(minutes=step)) 
            for step in range(0, 24*scenario.evaluated_period*scenario.time_step, scenario.time_step)
            ]

        # Generate results JSON per asset name
        results_json = [
            {
                'xAxis':
                    {
                        'values': datetime_list,
                        'label': 'Time'
                    },
                'yAxis':
                    {
                        'values': asset['flow']['value'] if 'flow' in asset else asset['timeseries_soc']['value'],
                        'label': asset['flow']['unit'] if 'flow' in asset else asset['timeseries_soc']['unit'],  # 'Power'
                    },
                'title': asset_name
            }
            for asset_name in asset_name_list
            for asset in assets_results_json[asset_name_to_category[asset_name]]
            if asset['label'] == asset_name
        ]

        return JsonResponse(results_json, status=200, content_type='application/json', safe=False)
    except:
        return JsonResponse({"Error":"Could not retrieve timeseries data."}, status=404, content_type='application/json', safe=False)


@login_required
@require_http_methods(["GET"])
def scenario_visualize_results(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)
    if scenario.project.user != request.user:
        return HttpResponseForbidden()
    
    try:
        kpi_scalar_results_obj = KPIScalarResults.objects.get(simulation=scenario.simulation)
        kpi_scalar_values_dict = json.loads(kpi_scalar_results_obj.scalar_values)

        scalar_kpis_json = [
            {
                'kpi': key.replace('_',' '),
                'value': round(val, 3),
                'unit': KPI_SCALAR_UNITS[key]
            }
            for key, val in kpi_scalar_values_dict.items()
        ]

        return render(request, 'scenario/scenario_visualize_results.html',
        {'scenario_id': scen_id, 'scalar_kpis': scalar_kpis_json, 'project_id': scenario.project.id})
    except:
        raise Http404("Could not retrieve simulation results.")


@login_required
@json_view
@require_http_methods(["GET"])
def scenario_economic_results(request, scen_id):
    """
    This view gathers all simulation specific cost matrix KPI results
    and sends them to the client for representation.
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
                'labels': [asset.replace('_',' ').upper() for asset in new_dict[category].keys()],
                'type': 'pie',
                'title': category.replace('_',' ').upper(),
                'titleTooltip': KPI_COSTS_TOOLTIPS[category]
            }
            for category in new_dict.keys()
            if sum(new_dict[category].values()) > 0.0  # there is at least one non zero value
            and len(list(filter(lambda asset_name: new_dict[category][asset_name] > 0.0 ,new_dict[category]))) > 1.0
            # there are more than one assets with value > 0
        ]
        return JsonResponse(results_json, status=200, content_type='application/json', safe=False)
    except:
        return JsonResponse({"error":"Could not retrieve kpi cost data."}, status=404, content_type='application/json', safe=False)

