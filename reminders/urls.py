from django.urls import path

from . import views

app_name = 'reminders'
urlpatterns = [
    path('', views.list, name='list'),
    path('<int:id>/mark_water', views.mark_water, name='mark_water'),
    path('<int:id>/mark_feed', views.mark_feed, name='mark_feed'),
    path('<int:id>/new_schedule', views.new_schedule, name='new_schedule'),
    #path('<int:id>/delete_schedule', views.delete_schedule, name='delete_schedule'),
]
