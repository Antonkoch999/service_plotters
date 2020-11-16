#!/usr/bin/env python
#encoding: utf-8
from django.urls import path
from .views import dashboard, timeline, index

app_name = "acra"
urlpatterns = [
    #url(r'^$', 'acra.views.dashboard', name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('timeline/', timeline, name='timeline'),
    path('_design/acra-storage/_update/report/', index, name='submit'),
]
