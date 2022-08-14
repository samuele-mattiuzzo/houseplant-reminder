from django.urls import path

from . import views

app_name = 'reminders'
urlpatterns = [
    path('', views.list, name='list'),
    path('<int:id>/mark-water', views.mark_water, name='mark-water'),
    path('<int:id>/mark-feed', views.mark_feed, name='mark-feed'),
]
