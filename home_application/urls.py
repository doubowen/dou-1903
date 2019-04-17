# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^search_set/$', 'search_set'),
    (r'^serch_host/$', 'serch_host'),
    (r'^history/$', 'history'),
    (r'^search_history/$', 'search_history'),
    (r'^exectue_task/$', 'exectue_task'),
)
