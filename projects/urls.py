from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('project/create/', project_create, name='project_create'),
    path('project/search/', project_search, name='project_search'),
    path('project/update/<int:id>', project_update, name='project_update'),
    path('project/detail/<int:id>', project_detail, name='project_detail'),
    path('project/delete/<int:id>', project_delete, name='project_delete'),

    path('comment/search/', comment_search, name='comment_search'),
    path('comment/create/', comment_create, name='comment_create'),
    path('comment/update/<int:id>', comment_update, name='comment_update'),
    path('comment/delete/<int:id>', comment_delete, name='comment_delete'),

    path('scenario/search/', scenario_search, name='scenario_search'),
    path('scenario/create/', scenario_create, name='scenario_create'),
    path('scenario/create_post/', scenario_create_post, name='scenario_create_post'),
    path('scenario/update/<int:id>', scenario_update, name='scenario_update'),
    path('scenario/delete/<int:id>', scenario_delete, name='scenario_delete'),
    path('scenario/view/<int:id>', scenario_view, name='scenario_view'),
    path('scenario/upload/', BookCreateView.as_view(), name='scenario_upload'),

    path('asset/search/<int:id>', asset_search, name='asset_search'),
    path('asset/assets_topology', scenario_topology_view, name='new_assets_topology'),

    path('asset/create/<str:asset_type_name>', asset_create, name='asset_create'),
    path('asset/create_post/', asset_create, name='asset_create_post'),

    path('topology/mvs_simulation/<int:scenario_id>', request_mvs_simulation, name='request_mvs_simulation'),

]
