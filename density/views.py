from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from .binance_ws import start_api_ws
from .chart_of_dencitys import ChartOfDencitys, INST_LIST
import json
from .redis_db import *

# Create your views here.

# def Density(request):
#     return HttpResponse('Density')


class Density(ListView):
    template_name = 'index.html'
    context_object_name = 'density'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['INST_LIST'] = INST_LIST



        return context

    def get_queryset(self):
        return 'density'