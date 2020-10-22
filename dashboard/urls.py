from django.urls import path
from .views import timeseries_chart_jsonview, scenario_visualize_results, scenario_available_results

urlpatterns = [
    path('scenario/results/get_chart/<int:scen_id>', timeseries_chart_jsonview, name='scenario_json_chart'),
    path('scenario/results/visualize/<int:scen_id>', scenario_visualize_results, name='scenario_visualize_results'),
    path('scenario/results/available/<int:scen_id>', scenario_available_results, name='scenario_available_results'),
]
