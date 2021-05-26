from django.urls import path
from .views import *

urlpatterns = [
    path('test_connection/',test_connection),
    path('get_all_instances/<model_name>/',get_all_instances),
    path('set_new_poll/',set_new_poll),
    path('set_new_choice/<int:poll_id>/',set_new_choice),
    path('get_poll_options/<int:poll_id>/',get_poll_options),
    path('set_new_vote/<int:poll_id>/<int:choice_id>/',set_new_vote),
    path('get_poll_results/<int:poll_id>/',get_poll_results),
]
