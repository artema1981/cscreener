from django.urls import path
from .views import *

urlpatterns = [
    path('', Density.as_view(), name='density'),
]