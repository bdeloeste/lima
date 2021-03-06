from django.conf.urls import patterns, url, include

from lima.views import IndexView, aboutView
from maps.views import maps, stats, tweets
from rest_framework_nested import routers

# TODO: add API endpoint urls

urlpatterns = patterns(
    '',
    url(r'^api/v1/maps', maps, name='maps'),
    url(r'^about/$', aboutView.as_view(), name='about'),
    # url(r'^api/v1/stats', stats, name='stats'),
    # url(r'^api/v1/tweets', tweets, name='tweets'),
    url('^.*$', IndexView.as_view(), name='index'),
)
