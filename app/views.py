from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Service


class StatusPageView(ListView):
    template_name = 'statuspage.html'
    queryset = Service.objects.all().order_by('pos')
