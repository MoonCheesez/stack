from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.maze, name='maze-maze'),
]