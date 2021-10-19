from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Service
import json


class StatusPageView(ListView):
    template_name = 'statuspage.html'
    queryset = Service.objects.all().order_by('pos')


class DetailServerView(DetailView):
    template_name = 'detail_server.html'
    model = Service

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        c = super().get_context_data(**kwargs)
        c['online_chart_json'] = json.dumps({
            'labels': [5],
            'data': [50, 55, 12]
        })
        return c


# Chart helper funcitons
def chart_labels():
    labels = []
    for x in range(100):
        pass