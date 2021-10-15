from django.shortcuts import render
from django.views.generic import TemplateView


class StatusPageView(TemplateView):
    template_name = 'statuspage.html'
