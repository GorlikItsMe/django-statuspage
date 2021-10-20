from django.db import models
from django.views.generic import DetailView
from django.http import JsonResponse
from django.utils import timezone
from .models import Service, ServiceCheck
from datetime import datetime, timedelta


class UptimeChartApiView(DetailView):
    model = Service

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # chartdata = self.chart_data()
        chartdata = self.chart_round()
        return JsonResponse({
            'servicename': self.object.name,
            'data': chartdata
        }, safe=False)

    def chart_data(self, metadata=False):
        service = self.object
        sc_list = ServiceCheck.objects.filter(
            service=service,
            datetime__gt=timezone.now() - timedelta(days=1)
        )
        data = []
        for sc in sc_list:
            sc: ServiceCheck
            if metadata:
                data.append({
                    'dt': sc.datetime,
                    'x': f'{sc.datetime.isoformat("T", "milliseconds")}Z',  # '2016-01-11T23:00:00.000Z',
                    'y': sc.latency
                })
            else:
                data.append({
                    'x': f'{sc.datetime.isoformat("T", "milliseconds")}Z',  # '2016-01-11T23:00:00.000Z',
                    'y': sc.latency
                })
        return data

    def chart_round(self):

        def create_dt_syganture(dt: datetime):
            dt = dt.replace(minute=(dt.minute - (dt.minute % 5)))  # 5min bloki czasowe
            return dt.strftime("%Y-%m-%d %H:%M")

        cd = self.chart_data(metadata=True)
        date_start: datetime = cd[0]['dt']
        thesame_hash = create_dt_syganture(date_start)
        bucket = []
        bucket_list = []

        # grupowanie
        for data in cd:
            dt: datetime = data['dt']
            if thesame_hash == create_dt_syganture(dt):
                # ta sama sygnatura czasu, dodaj do grupy
                bucket.append(data)
            else:
                # inna sygnatura
                bucket_list.append(bucket)
                bucket = [data]
                thesame_hash = create_dt_syganture(dt)
        bucket_list.append(bucket)  # ostatni bucket dodaje

        # usrednianie
        out = []
        for bucket in bucket_list:
            dt: datetime = bucket[0]['dt']
            dt_round = dt.replace(second=0, microsecond=0)
            dt_round = dt_round.replace(minute=(dt_round.minute - (dt_round.minute % 5)))  # 5min bloki czasowe

            latency_sum = 0
            is_offline = False
            for d in bucket:
                latency_sum += d['y']
                if d['y'] == 0:
                    is_offline = True

            latency_avg = round(latency_sum / len(bucket))
            if is_offline:
                latency_avg = 0

            out.append({
                'x': f'{dt_round.isoformat("T", "milliseconds")}Z',
                'y': latency_avg,
            })
        return out
