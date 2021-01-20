from django.urls import path
from .views import *

urlpatterns = [
    path('', project_search, name='home'),
    # Project
    path('project/create/', project_create, name='project_create'),
    path('project/search/', project_search, name='project_search'),
    path('project/update/<int:proj_id>', project_update, name='project_update'),
    path('project/detail/<int:proj_id>', project_detail, name='project_detail'),
    path('project/delete/<int:proj_id>', project_delete, name='project_delete'),
    # Comment
    path('comment/search/', comment_search, name='comment_search'),
    path('comment/create/', comment_create, name='comment_create'),
    path('comment/update/<int:com_id>', comment_update, name='comment_update'),
    path('comment/delete/<int:com_id>', comment_delete, name='comment_delete'),
    # Scenario
    path('scenario/search/<int:proj_id>', scenario_search, name='scenario_search'),
    path('scenario/create/', scenario_create, name='scenario_create'),
    path('scenario/create_post/', scenario_create_post, name='scenario_create_post'),
    path('scenario/update/<int:scen_id>', scenario_update, name='scenario_update'),
    path('scenario/delete/<int:scen_id>', scenario_delete, name='scenario_delete'),
    path('scenario/view/<int:scen_id>', scenario_view, name='scenario_view'),
    path('scenario/duplicate/<int:scen_id>', scenario_duplicate, name='scenario_duplicate'),
    path('scenario/upload/', LoadScenarioFromFileView.as_view(), name='scenario_upload'),
    # Grid Model (Assets Creation)
    path('asset/assets_topology/<int:scen_id>', scenario_topology_view, name='new_assets_topology'),
    path('asset/create/<str:asset_type_name>', get_asset_create_form, name='get_asset_create_form'),
    # MVS Simulation
    path('topology/mvs_simulation/<int:scenario_id>', request_mvs_simulation, name='request_mvs_simulation'),
    path('topology/update_simulation_rating/', update_simulation_rating, name='update_simulation_rating'),
]
