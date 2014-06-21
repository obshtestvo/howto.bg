import os
import uwsgi
import django.core.handlers.wsgi
from uwsgidecorators import timer
from django.utils import autoreload

@timer(2)
def change_code_gracefull_reload(sig):
    if autoreload.code_changed():
        uwsgi.reload()

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = django.core.handlers.wsgi.WSGIHandler()
