from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^regis_process$', views.process),
    url(r'^login_process$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^addpage$', views.addpage),
    url(r'^add_process$', views.add_process),
    url(r'^', views.error)
    # url(r'^regis_process/(?P<id>\d+)$', views.process)
]
