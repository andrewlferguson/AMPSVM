from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.seq, name='seq'),
    url(r'^result/$', views.result, name='result'),
]
