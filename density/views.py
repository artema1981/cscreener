from django.views.generic import ListView
from .chart_of_dencitys import INST_LIST


class Density(ListView):
    template_name = 'density.html'
    context_object_name = 'density'

    def filter_empty(self, lst: list):

        res = list(filter(lambda x: any([x.get('future_bids', False),
                                         x.get('future_asks', False),
                                         x.get('spot_bids', False),
                                         x.get('spot_asks', False)]), lst))

        return res

    def get_list(self):
        pass

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('volume') == '250k':
            context['INST_LIST'] = self.filter_empty([i.nearest_density_250k for i in INST_LIST])
        elif self.request.GET.get('volume') == '500k':
            context['INST_LIST'] = self.filter_empty([i.nearest_density_500k for i in INST_LIST])
        elif self.request.GET.get('volume') == '750k':
            context['INST_LIST'] = self.filter_empty([i.nearest_density_750k for i in INST_LIST])
        elif self.request.GET.get('volume') == '1m':
            context['INST_LIST'] = self.filter_empty([i.nearest_density_1m for i in INST_LIST])

        else:
            context['INST_LIST'] = self.filter_empty([i.nearest_density_500k for i in INST_LIST])
        return context

    def get_queryset(self):
        return 'density'
