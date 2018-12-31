
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django.conf.urls import url
from fno import view

urlpatterns = [
    # Examples:
#    url(r'^$', views.arView, name='arView'),
    #url(r'^pk/(?P<value>\d+)$', views.pktrial, name='pktrial'),
    #url(r'^arvideoplayer(?P<path>.*)$', views.arVideoPlayer, name="AR Video Player"),

    url(r'^$', view.index, name='index'),
    url(r'^index/$', view.index, name='index'),
    url(r'^stockoiview$', view.stockView, name="stockoiview$"),

]