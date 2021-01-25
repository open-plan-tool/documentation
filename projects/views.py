from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.decorators import login_required
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseForbidden, JsonResponse
from django.http.response import Http404
from django.shortcuts import *
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.contrib import messages
from jsonview.decorators import json_view
from crispy_forms.templatetags import crispy_forms_filters
from datetime import datetime

from .forms import *
from .requests import mvs_simulation_request, mvs_simulation_check, check_mvs_simulation
from .models import *
from .scenario_topology_helpers import create_node_interconnection_links, load_scenario_topology_from_db, NodeObject, \
    update_deleted_objects_from_database, duplicate_scenario_objects, duplicate_scenario_connections, get_topology_json


class HomeView(TemplateView):
    template_name = 'home.html'


# region Project

@login_required
@require_http_methods(["GET"])
def project_detail(request, proj_id):
    project = get_object_or_404(Project, pk=proj_id)
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
            # economic_data.annuity_factor = form.cleaned_data['annuity_factor']
            # economic_data.crf = form.cleaned_data['crf']

            economic_data.save()

            project.economic_data = economic_data

            project.save()

            request.session['project_id'] = project.id

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('scenario_search', args=[project.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectCreateForm()

    return render(request, 'project/project_create.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def project_update(request, proj_id):
    project = get_object_or_404(Project, pk=proj_id)
    economic_data = EconomicData.objects.get(project=project)

    if project.user != request.user:
        return HttpResponseForbidden()

    project_form = ProjectUpdateForm(request.POST or None, instance=project)
    economic_data_form = EconomicDataUpdateForm(request.POST or None, instance=economic_data)

    if request.method == "POST" and project_form.is_valid() and economic_data_form.is_valid():
        project_form.save()
        economic_data_form.save()
        # Save was successful, so send message
        messages.success(request, 'Project Info updated successfully!')
        return HttpResponseRedirect(reverse('project_search'))

    return render(request, 'project/project_update.html',
                  {'project_form': project_form, 'economic_data_form': economic_data_form})


@login_required
@require_http_methods(["POST"])
def project_delete(request, proj_id):
    project = get_object_or_404(Project, pk=proj_id)

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
            
            #  return JsonResponse({"success":True}, status=201)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('scenario_search', args=[request.session['project_id'], 1]))
        # return JsonResponse({"success":False, "forms_errors":form.errors}, status=400)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()

    return render(request, 'comment/comment_create.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def comment_update(request, com_id):
    comment = get_object_or_404(Comment, pk=com_id)

    if comment.project.user != request.user:
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

            comment.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('scenario_search', args=[comment.project.id, 1]))

        # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comment/comment_update.html', {'form': form})


@login_required
@require_http_methods(["POST"])
def comment_delete(request, com_id):
    comment = get_object_or_404(Comment, pk=com_id)

    if comment.project.user != request.user:
        return HttpResponseForbidden()

    if request.POST:
        comment.delete()
        messages.success(request, 'Comment successfully deleted!')
        return HttpResponseRedirect(reverse('scenario_search', args=[comment.project.id, 1]))


# endregion Comment


# region Scenario

@login_required
@require_http_methods(["GET"])
def scenario_search(request, proj_id, show_comments=0):
    """
    This view renders the scenarios and comments search html template.

    args: proj_id, show_comments
    proj_id: The Project id the user requests to observe associated scenarios and comments.
    show_comments: An integer flag to indicate wether the page will open on scenarios tab or comments tab.
    If show_comments==1 the html page will load and following a click event will change the active tab to comments.
    Otherwise the default scenarios tab will be presented to the user.

    Returns: A rendered html template.
    """
    project = get_object_or_404(Project, pk=proj_id)
    request.session['project_id'] = proj_id  # set the session according to current project
    comment_list = Comment.objects.filter(project=project)

    simulations_list = Simulation.objects.filter(scenario__project=project)
    # update the simulation status from MVS
    [check_mvs_simulation(simulation) for simulation in simulations_list]

    scenarios_list = Scenario.objects.filter(project=project)

    # TODO: In case of MVS DONE with errors handle accordingly
    return render(request, 'scenario/scenario_search.html',
                  {'comment_list': comment_list,
                   'scenarios_list': scenarios_list,
                   'project_name': project.name,
                   'show_comments':show_comments
                   })


@login_required
@require_http_methods(["GET"])
def scenario_create(request):
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
@require_http_methods(["POST"])
def scenario_update(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    if request.POST:
        form = ScenarioUpdateForm(request.POST)

        if form.is_valid():
            [setattr(scenario, name, value) for name, value in form.cleaned_data.items()]

            scenario.save(update_fields=form.cleaned_data.keys())
            return HttpResponseRedirect(reverse('scenario_search', args=[scenario.project.id]))

    else:
        raise Http404("An error occurred while updating the Scenario.")


@login_required
@require_http_methods(["GET"])
def scenario_view(request, scen_id):
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    scenario_form = ScenarioUpdateForm(None, instance=scenario)
    return render(request, 'scenario/scenario_info.html', 
        {
            'scenario_form': scenario_form, 
            'scenario_id': scen_id,
            'project_id': scenario.project.id
        })


@login_required
@require_http_methods(["GET"])
def scenario_duplicate(request, scen_id):
    """ duplicates the selected scenario and all of its associated components (topology data included) """
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project.user != request.user:
        return HttpResponseForbidden()

    # We need to iterate over all the objects related to this scenario and duplicate them
    # and associate them with the new scenario id.
    asset_list = Asset.objects.filter(scenario=scenario)
    bus_list = Bus.objects.filter(scenario=scenario)
    connections_list = ConnectionLink.objects.filter(scenario=scenario)
    # simulation_list = Simulation.objects.filter(scenario=scenario)

    # first duplicate the scenario
    scenario.pk = None
    scenario.save()
    # from now on we are working with the duplicated scenario, not the original
    old2new_asset_ids_map = duplicate_scenario_objects(asset_list, scenario)
    old2new_bus_ids_map = duplicate_scenario_objects(bus_list, scenario, old2new_asset_ids_map)
    duplicate_scenario_connections(connections_list, scenario, old2new_asset_ids_map, old2new_bus_ids_map)
    # duplicate_scenario_objects(simulation_list, scenario)

    return HttpResponseRedirect(reverse('scenario_search', args=[request.session['project_id']]))


@login_required
@require_http_methods(["POST"])
def scenario_delete(request, scen_id):
    project = get_object_or_404(Project, pk=request.session['project_id'])
    scenario = get_object_or_404(Scenario, pk=scen_id)

    if scenario.project != project:
        return HttpResponseForbidden()

    if request.POST:
        scenario.delete()
        messages.success(request, 'scenario successfully deleted!')
        return HttpResponseRedirect(reverse('scenario_search', args=[request.session['project_id']]))


class LoadScenarioFromFileView(BSModalCreateView):
    template_name = 'scenario/load_scenario_from_file.html'
    form_class = LoadScenarioFromFileForm
    success_message = 'Success: Scenario Uploaded.'

    def get_success_url(self):
        proj_id = self.request.session['project_id']
        return reverse_lazy('scenario_search', args=[proj_id])

# endregion Scenario


# region Asset

@login_required
@require_http_methods(["GET"])
def get_asset_create_form(request, asset_type_name):
    """
    This view is responsible to serve the appropriate form for each asset.
    Utilized in the 'create_asset_topology.html' template and retrieves 
    form data from the backend.
    """
    form = AssetCreateForm()
    # Retrieve asset type
    asset_type = get_object_or_404(AssetType, asset_type=asset_type_name)
    request.session['asset_type_name'] = asset_type_name

    form_fields = list(form.fields)
    # Remove form fields that do not correspond to the model
    [form.fields.pop(field) for field in form_fields if field not in asset_type.asset_fields]
    
    return render(request, 'asset/asset_create_form.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def scenario_topology_view(request, scen_id):
    if request.method == "GET" and request.is_ajax():
        # Approach: send assets, busses and connection links to the front end and let it do the work
        topology_data_list = load_scenario_topology_from_db(scen_id)
        return JsonResponse(topology_data_list, status=200)

    if request.method == "GET":
        request.session['scenario_id'] = scen_id  # we need to set the session since asset creation relies on it.
        return render(request, 'asset/create_asset_topology.html',
                      {'scenario_id': scen_id, 'project_id': request.session['project_id']})

    elif request.method == "POST" and request.is_ajax():
        topology = json.loads(request.body)['drawflow']['Home']['data']
        node_list = list()

        # get and clear topology data
        for node in topology:
            del topology[node]['html'], topology[node]['typenode'], topology[node]['class']
            node_list.append(NodeObject(topology[node]))

        # delete objects from database which were deleted by the user
        update_deleted_objects_from_database(scen_id, node_list)

        # map topology nodes to database objects during the process of database objects insertion
        node_to_db_mapping_dict = dict()
        for node_obj in node_list:
            if node_obj.name == 'bus':
                successful_bus_insertion = node_obj.create_or_update_bus(scen_id)
                if not successful_bus_insertion["success"]:
                    return JsonResponse(successful_bus_insertion, status=400)
            else:
                successful_asset_insertion = node_obj.create_or_update_asset(scen_id)
                if not successful_asset_insertion["success"]:
                    return JsonResponse(successful_asset_insertion, status=400)

            node_to_db_mapping_dict[node_obj.obj_id] = {
                'db_obj_id': node_obj.db_obj_id,
                'node_type': node_obj.node_obj_type,
                'input_connections': node_obj.inputs,
                'output_connections': node_obj.outputs,
            }

        # Make sure there are no connections in the Database to prevent inserting the same connections upon updating.
        ConnectionLink.objects.filter(scenario_id=scen_id).delete()
        for node_obj in node_list:
            create_node_interconnection_links(node_obj, node_to_db_mapping_dict, scen_id)
            node_obj.assign_asset_to_proper_group(node_to_db_mapping_dict)

        ''' return a dictionary as a response to the front end, containing the node_ids along with their
        # associated database_ids. This information will help the front end to identify whether the submitted
        # nodes are new or existing ones and thus discriminate if they need to be updated or created. '''
        topo2db_id_map = dict()
        for key, value in node_to_db_mapping_dict.items():
            topo2db_id_map[key] = value['db_obj_id']
        response_dict = {"success": True, "data": topo2db_id_map}
        return JsonResponse(response_dict, status=200)
    else:
        return JsonResponse({"success": False, "request": "bad request type. couldn't respond."}, status=400)

# endregion Asset


# region MVS JSON Related

# End-point to send MVS simulation request
@json_view
@login_required
@require_http_methods(["GET", "POST"])
def request_mvs_simulation(request, scenario_id=0):
    if scenario_id == 0:
        return JsonResponse({"status": "error", "error": "No scenario id provided"},
                            status=500, content_type='application/json')
    # Load scenario
    scenario = Scenario.objects.get(pk=scenario_id)
    data_clean = get_topology_json(scenario)

    # delete existing simulation
    Simulation.objects.filter(scenario_id=scenario_id).delete()
    # Create empty Simulation model object
    simulation = Simulation(start_date=datetime.now(), scenario_id=scenario_id)
    # Make simulation request to MVS
    results = mvs_simulation_request(data_clean)

    simulation.mvs_token = results['id'] if results['id'] else None

    if 'status' in results.keys() and (results['status'] == 'DONE' or results['status'] == 'FAILED'):
        simulation.status = results['status']
        simulation.results = results['results']
        simulation.end_date = datetime.now()
    else:  # PENDING
        simulation.status = results['status']

    simulation.elapsed_seconds = (datetime.now() - simulation.start_date).seconds
    simulation.save()

    return JsonResponse({'status': simulation.status,
                         'secondsElapsed': simulation.elapsed_seconds,
                         'rating': simulation.user_rating,
                         "mvs_request_json": data_clean
                         },
                        status=200, content_type='application/json')


@json_view
@login_required
@require_http_methods(["POST"])
def update_simulation_rating(request):
    try:
        simulation = Simulation.objects.filter(scenario_id=request.POST['scen_id']).first()
        simulation.user_rating = request.POST['user_rating']
        simulation.save()
        return JsonResponse({'success': True}, status=200, content_type='application/json')
    except Exception as e:
        return JsonResponse({'success': False, 'cause': str(e)}, status=200, content_type='application/json')

# endregion MVS JSON Related
