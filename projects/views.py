from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from .models import Project, Location


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('name', 'details','electricity', 'heat', 'gas', 'ev')
    template_name = 'project_edit.html'


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_delete.html'
    success_url = reverse_lazy('project_list')


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project_new.html'
    fields = ('name', 'details','electricity', 'heat', 'gas', 'ev','location','author')

class LocationCreateView(CreateView):
    model = Location
    fields = ('name', 'country', 'lat','lon',)

