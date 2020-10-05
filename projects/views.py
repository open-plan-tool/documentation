from django.contrib.auth.decorators import login_required
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import *
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.contrib import messages
from jsonview.decorators import json_view
from crispy_forms.templatetags import crispy_forms_filters

from .dtos import convert_to_dto
from .forms import *
from .models import *
from .scenario_topology_helpers import create_node_interconnection_links, load_scenario_topology_from_db, NodeObject, \
    update_deleted_objects_from_database


class HomeView(TemplateView):
    template_name = 'home.html'


# region Project

@login_required
@require_http_methods(["GET"])
def project_detail(request, id):
    project = get_object_or_404(Project, pk=id)
    economic_data = EconomicData.objects.get(project=project)

    if project.user != request.user:
        return HttpResponseForbidden()

    project_form = ProjectDetailForm(None, instance=project)
    economic_data_form = EconomicDataDetailForm(None, instance=economic_data)

    return render(request, 'project/project_detail.html',
                  {'project_form': project_form, 'economic_data_form': economic_data_form})


@login_required
@require_http_methods(["GET", "POST"])
def project_create(request):
    # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = ProjectCreateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            project = Project()
            economic_data = EconomicData()

            project.name = form.cleaned_data['name']
            project.description = form.cleaned_data['description']
            project.country = form.cleaned_data['country']
            project.longitude = form.cleaned_data['longitude']
            project.latitude = form.cleaned_data['latitude']

            project.user = request.user

            economic_data.duration = form.cleaned_data['duration']
            economic_data.currency = form.cleaned_data['currency']
            economic_data.discount = form.cleaned_data['discount']
            economic_data.tax = form.cleaned_data['tax']
            economic_data.annuity_factor = form.cleaned_data['annuity_factor']
            economic_data.crf = form.cleaned_data['crf']

            economic_data.save()

            project.economic_data = economic_data

            project.save()

            request.session['project_id'] = project.id

            # redirect to a new URL:
            return HttpResponseRedirect('/comment/search')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectCreateForm()

    return render(request, 'project/project_create.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def project_update(request, id):
    project = get_object_or_404(Project, pk=id)
    economic_data = EconomicData.objects.get(project=project)

    if project.user != request.user:
        return HttpResponseForbidden()

    project_form = ProjectUpdateForm(request.POST or None, instance=project)
    economic_data_form = EconomicDataUpdateForm(request.POST or None, instance=economic_data)

    if request.POST and project_form.is_valid() and economic_data_form.is_valid():
        project_form.save()
        economic_data_form.save()
        # Save was successful, so send message
        messages.success(request, 'Project Info updated successfully!')

    return render(request, 'project/project_update.html',
                  {'project_form': project_form, 'economic_data_form': economic_data_form})


@login_required
@require_http_methods(["POST"])
def project_delete(request, id):
    project = get_object_or_404(Project, pk=id)

    if project.user != request.user:
        return HttpResponseForbidden()

    if request.POST:
        project.delete()
        messages.success(request, 'Project successfully deleted!')

    project_list = Project.objects.filter(user=request.user)
    return render(request, 'project/project_search.html', {'project_list': project_list})


@login_required
@require_http_methods(["GET"])
def project_search(request):
    project_list = Project.objects.filter(user=request.user)
    # project_list_json = json.dumps(list(project_list.values_list('name', 'longitude', 'latitude')),
    #                                cls=DjangoJSONEncoder)

    return render(request, 'project/project_search.html',
                  {'project_list': project_list})

# endregion Project


# region Comment

@login_required
@require_http_methods(["GET"])
def comment_search(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    comment_list = Comment.objects.filter(project=project)

    return render(request, 'comment/comment_search.html', {'comment_list': comment_list})


@login_required
@require_http_methods(["GET", "POST"])
def comment_create(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            comment = Comment()
            comment.name = form.cleaned_data['name']
            comment.body = form.cleaned_data['body']
            comment.project = project
            comment.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/scenario/search')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return render(request, 'comment/comment_create.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def comment_update(request, id):
    project = get_object_or_404(Project, pk=request.session['project_id'])
    comment = get_object_or_404(Comment, pk=id)

    if comment.project != project:
        return HttpResponseForbidden()

        # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            comment.name = form.cleaned_data['name']
            comment.body = form.cleaned_data['body']

            comment.project = project

            comment.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/scenario/search')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comment/comment_update.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def comment_delete(request, id):
    project = get_object_or_404(Project, pk=request.session['project_id'])
    comment = get_object_or_404(Comment, pk=id)

    if comment.project != project:
        return HttpResponseForbidden()

    if request.POST:
        comment.delete()
        messages.success(request, 'Comment successfully deleted!')
        return HttpResponseRedirect('/scenario/search')


# endregion Comment


# region Scenario

@login_required
@require_http_methods(["GET"])
def scenario_search(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    scenario_list = Scenario.objects.filter(project=project)

    comment_list = Comment.objects.filter(project=project)

    return render(request, 'scenario/scenario_search.html', {'scenario_list': scenario_list, 'comment_list': comment_list})


@login_required
@require_http_methods(["GET"])
def scenario_create(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    form = ScenarioCreateForm()

    return render(request, 'scenario/scenario_create.html', {'form': form})


@json_view
@login_required
@require_http_methods(["POST"])
def scenario_create_post(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])
    form = ScenarioCreateForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        scenario = Scenario()

        for name, value in form.cleaned_data.items():
            setattr(scenario, name, value)

        scenario.project = project
        scenario.save()

        request.session['scenario_id'] = scenario.id

        # redirect to a new URL:
        return {'success': True}

    form_html = crispy_forms_filters.as_crispy_form(form)

    return {'success': False, 'form_html': form_html}


@login_required
@require_http_methods(["GET", "POST"])
def scenario_update(request, id):
    project = get_object_or_404(Project, pk=request.session['project_id'])
    scenario = get_object_or_404(Scenario, pk=id)

    if scenario.project != project:
        return HttpResponseForbidden()

        # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = ScenarioUpdateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            scenario.name = form.cleaned_data['name']
            scenario.start_date = form.cleaned_data['start_date']
            scenario.period = form.cleaned_data['period']
            scenario.time_step = form.cleaned_data['time_step']
            scenario.capex_fix = form.cleaned_data['capex_fix']
            scenario.capex_var = form.cleaned_data['capex_var']
            scenario.opex_fix = form.cleaned_data['opex_fix']
            scenario.opex_var = form.cleaned_data['opex_var']
            scenario.lifetime = form.cleaned_data['lifetime']

            scenario.project = project

            scenario.save()

            # redirect to a new URL:
            return HttpResponseRedirect('scenario/search')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = ScenarioUpdateForm(instance=scenario)

    return render(request, 'comment/comment_update.html', {'form': form})


@login_required
@require_http_methods(["GET"])
def scenario_view(request, id):
    project = get_object_or_404(Project, pk=request.session['project_id'])
    scenario = get_object_or_404(Scenario, pk=id)

    if scenario.project != project or project.user != request.user:
        return HttpResponseForbidden()

    scenario_form = ScenarioUpdateForm(None, instance=scenario)
    return render(request, 'scenario/scenario_info.html', {'scenario_form': scenario_form})



@login_required
@require_http_methods(["POST"])
def scenario_delete(request, id):
    project = get_object_or_404(Project, pk=request.session['project_id'])
    scenario = get_object_or_404(Scenario, pk=id)

    if scenario.project != project:
        return HttpResponseForbidden()

    if request.POST:
        scenario.delete()
        messages.success(request, 'scenario successfully deleted!')
        return HttpResponseRedirect('/scenario/search')


# endregion Scenario


# region Asset

@login_required
@require_http_methods(["GET"])
def asset_search(request, id):
    scenario = get_object_or_404(Scenario, pk=id)
    request.session['scenario_id'] = scenario.id

    asset_list = Asset.objects.filter(scenario=scenario)

    asset_type_list = json.dumps(list(AssetType.objects.all().values()), cls=DjangoJSONEncoder)

    return render(request, 'asset_search.html', {'asset_list': asset_list, 'asset_type_list': asset_type_list})


@login_required
@require_http_methods(["GET"])
def asset_create(request, asset_type_name):
    form = AssetCreateForm()

    # Retrieve asset type
    asset_type = get_object_or_404(AssetType, asset_type=asset_type_name)
    request.session['asset_type_name'] = asset_type_name

    form_fields = list(form.fields)

    # Remove form fields that do not correspond to the model
    for field in form_fields:
        if field not in asset_type.asset_fields:
            form.fields.pop(field)

    return render(request, 'asset/asset_create_form.html', {'form': form})


@json_view
@login_required
@require_http_methods(["POST"])
def asset_create_post(request):
    form = AssetCreateForm(request.POST)
    asset_type = get_object_or_404(AssetType, asset_type=request.session['asset_type_name'])
    form_fields = list(form.fields)

    # Remove form fields that do not correspond to the model
    for field in form_fields:
        if field not in asset_type.asset_fields:
            form.fields.pop(field)

    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        asset = Asset()

        for name, value in form.cleaned_data.items():
            setattr(asset, name, value)

        asset.scenario = get_object_or_404(Scenario, pk=request.session['scenario_id'])
        asset.asset_type = get_object_or_404(AssetType, asset_type=request.session['asset_type_name'])
        asset.save()

        # redirect to a new URL:
        return {'success': True}

    form_html = crispy_forms_filters.as_crispy_form(form)


@login_required
@require_http_methods(["GET", "POST"])
def scenario_topology_view(request):
    if request.method == "GET" and request.is_ajax():
        # Approach: send assets, busses and connection links to the front end and let it do the work
        topology_data_list = load_scenario_topology_from_db(request.session['scenario_id'])
        return JsonResponse(topology_data_list, status=200)

    if request.method == "GET":
        return render(request, 'asset/create_asset_topology.html')

    elif request.method == "POST" and request.is_ajax():
        topology = json.loads(request.body)['drawflow']['Home']['data']
        node_list = list()
        # get and clear topology data
        for node in topology:
            del topology[node]['html'], topology[node]['typenode'], topology[node]['class']
            node_list.append(NodeObject(topology[node]))

        # delete objects from database which were deleted by the user
        update_deleted_objects_from_database(request.session['scenario_id'], node_list)

        node_to_db_mapping_dict = dict()
        for node_obj in node_list:
            if node_obj.name == 'bus':
                node_obj.create_or_update_bus(request.session['scenario_id'])
            else:
                node_obj.create_or_update_asset(request.session['scenario_id'])

            node_to_db_mapping_dict[node_obj.obj_id] = {
                'db_obj_id': node_obj.db_obj_id,
                'node_type': node_obj.node_obj_type,
                'output_connections': node_obj.outputs,
            }
        # Make sure there are no connections in the Database to prevent inserting the same connections upon updating.
        ConnectionLink.objects.filter(scenario_id=request.session['scenario_id']).delete()
        for node_obj in node_list:
            create_node_interconnection_links(node_obj, node_to_db_mapping_dict, request.session['scenario_id'])

        ''' return a dictionary as a response to the front end, containing the node_ids along with their
        # associated database_ids. This information will help the front end to identify whether the submitted
        # nodes are new or existing ones and thus discriminate if they need to be updated or created. '''
        topo2db_id_map = dict()
        for key, value in node_to_db_mapping_dict.items():
            topo2db_id_map[key] = value['db_obj_id']
        response_dict = {"success": True, "data": topo2db_id_map}
        return JsonResponse(response_dict, status=200)
    else:
        return JsonResponse({"success": False}, status=400)

# endregion Asset


# region MVS JSON Related

@login_required
@require_http_methods(["GET"])
def get_topology_json(request, scenario_id):
    scenario = Scenario.objects.get(pk=scenario_id)
    mvs_request_dto = convert_to_dto(scenario)

    # Create data dict from dto object
    data = json.loads(json.dumps(mvs_request_dto.__dict__, default=lambda o: o.__dict__))
    # Remove None values
    data_clean = del_none(data)

    return JsonResponse(data_clean, status=200, content_type='application/json')


# Helper method to clean data from None values


def del_none(d):
    # Copy dict in order to modify
    rez = d.copy()
    # Iterate over dict
    for key, value in d.items():
        # If null or empty delete key from dict
        if value is None or value == '':
            del rez[key]
        # Else if nested dict call method again on dict
        elif isinstance(value, dict):
            rez[key] = del_none(value)
        # Else if nested list call method again on contents
        elif isinstance(value, list):
            if not value:
                del rez[key]
        # Remove empty list entries
            for entry in value:
                value[value.index(entry)] = del_none(entry)
    return rez

# endregion
