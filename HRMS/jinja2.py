from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime as django_naturaltime
from django.conf import settings
from django.apps import apps
from django_middleware_global_request.middleware import get_request
from datetime import datetime


def naturaltime(value):
    """return the human readable time format"""
    return django_naturaltime(value)

def naturaldateyear(value):
    try:
        dt = datetime.strptime(value, "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except:
        return "---"


def htmldate(value):
    try:
        return value.strftime("%Y-%m-%d")
    except:
        return value

def get_base_url():
    try:
        request = get_request()
        return request.META['HTTP_HOST']
    except Exception as e:
        print(e)
        return settings.BASE_URL
    


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'get_base_url':get_base_url,
        'filter': getter_multiple_obj,

    })
    env.filters['naturaltime'] = naturaltime
    env.filters['htmldate']=htmldate
    env.filters['naturaldateyear']=naturaldateyear
    
    return env

def getter_multiple_obj(app_name, model_name, **kwargs):
    """function to get the single model object based on the filter"""
    __class = apps.get_model(app_label=app_name, model_name=model_name)
    return __class.objects.filter(**kwargs)


