from django.urls import path
from .views import *

urlpatterns = [
    path('scenario/results/visualize/<int:scen_id>', scenario_visualize_results, name='scenario_visualize_results'),
    path('scenario/results/request/<int:scen_id>', scenario_request_results, name='scenario_request_results'),
    path('scenario/results/available/<int:scen_id>', scenario_available_results, name='scenario_available_results'),
    path('scenario/results/request_economic_data/<int:scen_id>', scenario_economic_results, name='scenario_economic_results'),
]
