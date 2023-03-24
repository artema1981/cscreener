from django.urls import path
from .views import *

urlpatterns = [
    path('density/', Density.as_view(), name='density'),
]