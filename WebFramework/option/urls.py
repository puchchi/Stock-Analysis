
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django.conf.urls import url
import views

urlpatterns = [
    # Examples:
#    url(r'^$', views.arView, name='arView'),
#    url(r'^$', views.indesignARView, name='arView'),
    url(r'^$', views.indesignVRView, name='vrView'),
    url(r'^pk/(?P<value>\d+)$', views.pktrial, name='pktrial'),
    url(r'^ar$', views.arIndex, name="AR Index"),
    url(r'^arvideoplayer(?P<path>.*)$', views.arVideoPlayer, name="AR Video Player"),
    url(r'^ar2$', views.arView2, name="arView"),
    url(r'^ar3$', views.ar3, name="arView"),
    url(r'^ar4$', views.ar4, name="arView"),
    url(r'^index/$', views.index, name='index'),
    url(r'^home$', views.optionHome, name="optionHome"),
    url(r'^image', views.imageColorEditing, name="imageColorEditing"),
]