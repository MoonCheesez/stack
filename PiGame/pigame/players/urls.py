from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^join/$', views.join, name="players-join"),
    url(r'^leave/([1-4])$', views.leave, name="players-leave"),
]
