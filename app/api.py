from django.db import models
from django.views.generic import DetailView
from django.http import JsonResponse
from django.utils import timezone
from .models import Service, ServiceCheck
from datetime import timedelta


class UptimeChartApiView(DetailView):
    model = Service

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        chartdata = self.chart_data()
        return JsonResponse({
            'servicename': self.object.name,
            'data': chartdata
        }, safe=False)

    def chart_data(self):
        service = self.object
        sc_list = ServiceCheck.objects.filter(
            service=service,
            datetime__gt=timezone.now() - timedelta(days=1)
        )
        data = []
        for sc in sc_list:
            sc: ServiceCheck
            data.append({
                'x': sc.datetime.isoformat(),  # '2016-01-11T23:00:00.000Z',
                'y': sc.latency
            })
        return data
