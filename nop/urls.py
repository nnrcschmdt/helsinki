import os

from django.conf.urls import url
from django.views.static import serve

from .views import get, get_current, nop_form

NOP_SITE_MEDIA = os.path.join(os.path.dirname(__file__), 'site_media')

urlpatterns = [
    url(r'^get_current/?$', get_current),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<hour>\d{1,2})/(?P<minute>\d{1,2})/?$', get),
    url(r'^$', nop_form),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': NOP_SITE_MEDIA}),
]
