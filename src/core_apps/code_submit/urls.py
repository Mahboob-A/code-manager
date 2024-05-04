

from django.urls import path
from core_apps.code_submit.views import TestAPI

urlpatterns = [
    path('test/', TestAPI.as_view()), 
]
