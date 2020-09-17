from crispy_forms.utils import render_crispy_form, render_field
from django.contrib.auth.decorators import login_required
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import *
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from jsonview.decorators import json_view
from crispy_forms.templatetags import crispy_forms_filters

from .dtos import Asset
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

    return render(request, 'project_detail.html',
                  {'project_form': project_form, 'economic_data_form': economic_data_form})

    template_name = 'project_detail.html'


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

    return render(request, 'project_create.html', {'form': form})


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

    return render(request, 'project_update.html',
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
    return render(request, 'project_search.html', {'project_list': project_list})


@login_required
@require_http_methods(["GET"])
def project_search(request):
    project_list = Project.objects.filter(user=request.user)
    # project_list_json = json.dumps(list(project_list.values_list('name', 'longitude', 'latitude')),
    #                                cls=DjangoJSONEncoder)

    return render(request, 'project_search.html',
                  {'project_list': project_list})

# endregion Project


# region Comment

@login_required
@require_http_methods(["GET"])
def comment_search(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    comment_list = Comment.objects.filter(project=project)

    return render(request, 'comment_search.html', {'comment_list': comment_list})


@login_required
@require_http_methods(["GET", "POST"])
def comment_create(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    # if this is a POST request we need to process the form data
    if request.POST:
        # create a form instance and populate it with data from the request:
        form = CommentCreateForm(request.POST)
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
        form = CommentCreateForm()

    return render(request, 'comment_create.html', {'form': form})


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
        form = CommentUpdateForm(request.POST)
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
        form = CommentUpdateForm(instance=comment)

    return render(request, 'comment_update.html', {'form': form})


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

    return render(request, 'scenario_search.html', {'scenario_list': scenario_list})


@login_required
@require_http_methods(["GET"])
def scenario_create(request):
    project = get_object_or_404(Project, pk=request.session['project_id'])

    form = ScenarioCreateForm()

    return render(request, 'scenario_create.html', {'form': form})


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
        form = CommentUpdateForm(request.POST)
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
        form = CommentUpdateForm(instance=comment)

    return render(request, 'comment_update.html', {'form': form})


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
    asset_list = []

    scenario = get_object_or_404(Scenario, pk=id)
    consumption_asset_list = EnergyConsumption.objects.filter(scenario=scenario)
    production_asset_list = EnergyProduction.objects.filter(scenario=scenario)
    conversion_asset_list = EnergyConversion.objects.filter(scenario=scenario)
    storage_asset_list = EnergyStorage.objects.filter(scenario=scenario)

    for x in asset_list:
        asset = Asset(x.id, x.name, 'Electricity', )



    asset_list.extend(consumption_asset_list)
    asset_list.extend(production_asset_list)
    asset_list.extend(conversion_asset_list)
    asset_list.extend(storage_asset_list)

    return render(request, 'asset_search.html', {'asset_list': asset_list})

# endregion Asset
