from django.urls import path


from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('change_password/', change_password, name='change_password'),
    path('user_info/', user_info, name='user_info'),
]
