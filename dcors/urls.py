import django

if django.get_version() >= '1.5':
    from django.conf.urls import *
else:
    from django.conf.urls.defaults import *

from django.http import HttpResponse

urlpatterns = patterns('',
    url(r'^$', lambda r: HttpResponse("", status=200), name='dummy'),
)
