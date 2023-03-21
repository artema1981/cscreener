from django.urls import path
from .views import *

urlpatterns = [
    path('index/', Density.as_view(), name='index'),
]