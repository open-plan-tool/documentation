from crispy_forms.utils import render_crispy_form, render_field
from django.apps import AppConfig, apps

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import *
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from jsonview.decorators import json_view
from crispy_forms.templatetags import crispy_forms_filters
from django.core import serializers

from .dtos import convert_to_dto
from .forms import *
from .models import *


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
            return HttpResponseRedirect('/comment/search')

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
            return HttpResponseRedirect('/comment/search')

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
        return HttpResponseRedirect('/comment/search')


# endregion Comment


# region Scenario

@login_required
@require_http_methods(["GET"])
def scenario_search(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    scenario_list = Scenario.objects.filter(project=project)

    return render(request, 'scenario/scenario_search.html', {'scenario_list': scenario_list})


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

        scenario.project = project;
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
            return HttpResponseRedirect('/comment/search')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm(instance=comment)

    return render(request, 'comment/comment_update.html', {'form': form})


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


class AssetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    context_object_name = 'form'
    template_name = 'asset/asset_create.html'
    fields = '__all__'
    #exclude = ('scenario', 'name')
    success_url = reverse_lazy('scenario_search')

    def test_func(self):
        scenario = get_object_or_404(Scenario, pk=self.request.session['scenario_id'])
        project = get_object_or_404(Project, pk=self.request.session['project_id'])
        return self.request.user == project.user

    def dispatch(self, request, *args, **kwargs):
        # use this method along with proper url config to load parametric Asset models.
        # where 'my_asset' is the url parameter name and 'projects' is the app name to look for models
        my_asset = kwargs.get('my_asset', None)
        self.model = apps.get_model('projects', my_asset.capitalize())
        try:
            ret = super(AssetCreateView, self).dispatch(request, *args, **kwargs)
        except AttributeError:
            raise Http404("No such Asset exists.")
        return ret

    def get_form(self):
        # User this method to prepopulate form with scenario id.
        # Also use js to hide scenario selection from the from.
        form = super(AssetCreateView, self).get_form()
        form.fields.pop('scenario')
        # initial_base = self.get_initial()
        # scenario_pk = self.request.session['scenario_id']
        # initial_base['scenario'] = Scenario.objects.get(id=scenario_pk)
        # form.initial = initial_base
        #form.fields['name'].widget = forms.widgets.TextInput()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset_name'] = self.model.__str__(self)

        myval = self.request.GET.get('test1')
        context['test_val'] = myval
        return context

    def form_valid(self, form):
        scenario = get_object_or_404(Scenario, pk=self.request.session['scenario_id'])
        form.instance.scenario = scenario
        #messages.success(self.request, 'Item created successfully!')
        return super().form_valid(form)


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


def load_scenario_topology_from_db(scen_id):
    bus_nodes_list = db_bus_nodes_to_list(scen_id)
    asset_nodes_list = db_asset_nodes_to_list(scen_id)
    connection_links_list = db_connection_links_to_list(scen_id)
    return {"busses": bus_nodes_list, "assets": asset_nodes_list, "links": connection_links_list}


def db_bus_nodes_to_list(scen_id):
    all_db_busses = Bus.objects.filter(scenario_id=scen_id)
    bus_nodes_list = list()
    for db_bus in all_db_busses:
        db_bus_dict = {"name": "bus", "data": {"name": db_bus.name, "bustype": db_bus.type, "databaseId": db_bus.id},
                       "pos_x": db_bus.pos_x, "pos_y": db_bus.pos_y}
        bus_nodes_list.append(db_bus_dict)
    return bus_nodes_list


def db_asset_nodes_to_list(scen_id):
    all_db_assets = Asset.objects.filter(scenario_id=scen_id)
    asset_nodes_list = list()
    data = dict()
    for db_asset in all_db_assets:
        db_asset_to_dict = json.loads(json.dumps(db_asset.__dict__, default = lambda o: o.__dict__))
        ignored_keys = ["scenario_id", "pos_x", "pos_y", "asset_type_id"]
        for key, val in db_asset_to_dict.items():
            if not (key.startswith('_') or (key in ignored_keys) or val is None):
                if key == "id":
                    data["databaseId"] = val
                else:
                    data[key] = val

        asset_type_obj = get_object_or_404(AssetType, pk=db_asset.asset_type_id)
        db_asset_dict = {"name": asset_type_obj.asset_type, "pos_x": db_asset.pos_x, "pos_y": db_asset.pos_y, "data": data}
        asset_nodes_list.append(db_asset_dict)
    return asset_nodes_list


def db_connection_links_to_list(scen_id):
    all_db_connection_links = ConnectionLink.objects.filter(scenario_id=scen_id)
    connections_list = list()
    for db_connection in all_db_connection_links:
        db_connection_dict = {"bus_id": db_connection.bus_id, "asset_id": db_connection.asset_id, "flow_direction": db_connection.flow_direction}
        connections_list.append(db_connection_dict)
    return connections_list


class NodeObject:
    def __init__(self, node_data=None):
        self.obj_id = node_data['id']
        self.name = node_data['name']
        self.data = node_data['data']
        self.pos_x = node_data['pos_x']
        self.pos_y = node_data['pos_y']
        self.db_obj_id = (node_data['data']['databaseId'] if 'databaseId' in node_data['data'] else None)
        self.node_obj_type = ('bus' if self.name == 'bus' else 'asset')
        self.inputs = node_data['inputs']
        self.outputs = list()

        for key1 in node_data['outputs'].keys():
            for key2 in node_data['outputs'][key1]:
                self.outputs = [connected_node['node'] for connected_node in node_data['outputs'][key1][key2]]

    def create_or_update_asset(self, scen_id):
        asset = get_object_or_404(Asset, pk=self.db_obj_id) if self.db_obj_id else Asset()
        for name, value in self.data.items():
            if name == 'optimize_cap':
                value = True if value == 'on' else False
            setattr(asset, name, value)

        setattr(asset, 'pos_x', self.pos_x)
        setattr(asset, 'pos_y', self.pos_y)
        asset.scenario = get_object_or_404(Scenario, pk=scen_id)
        asset.asset_type = get_object_or_404(AssetType, asset_type=self.name)
        asset.save()
        if self.db_obj_id is None:
            self.db_obj_id = asset.id

    def create_or_update_bus(self, scen_id):
        bus = get_object_or_404(Bus, pk=self.db_obj_id) if self.db_obj_id else Bus()
        setattr(bus, 'name', self.data['name'])
        setattr(bus, 'type', self.data['bustype'])
        setattr(bus, 'pos_x', self.pos_x)
        setattr(bus, 'pos_y', self.pos_y)
        bus.scenario = get_object_or_404(Scenario, pk=scen_id)
        bus.save()
        if self.db_obj_id is None:
            self.db_obj_id = bus.id


def create_node_interconnection_links(node_obj, map_dict, scen_id):
    for output_connection in node_obj.outputs:
        connection = ConnectionLink()
        output_node = map_dict[int(output_connection)]

        if node_obj.name == 'bus' and output_node['node_type'] != 'bus':
            setattr(connection, 'bus', get_object_or_404(Bus, pk=node_obj.db_obj_id))
            setattr(connection, 'asset', get_object_or_404(Asset, pk=output_node['db_obj_id']))
            setattr(connection, 'flow_direction', 'B2A')
            setattr(connection, 'scenario', get_object_or_404(Scenario, pk=scen_id))
        elif node_obj.name != 'bus' and output_node['node_type'] == 'bus':
            setattr(connection, 'asset', get_object_or_404(Asset, pk=node_obj.db_obj_id))
            setattr(connection, 'bus', get_object_or_404(Bus, pk=output_node['db_obj_id']))
            setattr(connection, 'flow_direction', 'A2B')
            setattr(connection, 'scenario', get_object_or_404(Scenario, pk=scen_id))
        connection.save()


# endregion Asset

@login_required
@json_view
@require_http_methods(["GET"])
def get_topology_json(request):
    scenario = Scenario.objects.get(pk=1)
    mvs_request_dto = convert_to_dto(scenario)

    return HttpResponse(json.dumps(mvs_request_dto.__dict__, default=lambda o: o.__dict__),
                        status=200)
