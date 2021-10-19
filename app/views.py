from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.utils import timezone
from datetime import timedelta
from .models import Service, ServiceCheck


class StatusPageView(ListView):
    template_name = 'statuspage.html'
    queryset = Service.objects.all().order_by('pos')


class DetailServerView(DetailView):
    template_name = 'detail_server.html'
    model = Service

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        c = super().get_context_data(**kwargs)
        return c

