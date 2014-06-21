from django.conf.urls import patterns, url, include
from django.http import  HttpResponse
import settings

urlpatterns = patterns('',
    (r'^robots.txt$',  lambda r: HttpResponse(settings.ROBOTS_FILE.value, content_type='text/plain')),
)
