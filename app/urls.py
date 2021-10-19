from django.contrib import admin
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path("", views.StatusPageView.as_view(), name="statuspage"),
    path('detail/<str:slug>/', views.DetailServerView.as_view(), name="detailServer"),

    path("api/uptimechart/<str:slug>/", api.UptimeChartApiView.as_view(), name="api-uptimechart"),
]
