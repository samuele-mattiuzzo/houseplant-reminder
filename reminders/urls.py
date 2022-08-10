from django.urls import path

from . import views

app_name = 'reminders'
urlpatterns = [
    path('', views.list, name='list'),
    path('<int:id>/', views.details, name='details'),
    path('<int:id>/complete', views.complete, name='complete'),
    path('<int:id>/delete', views.delete, name='delete'),
    #path('create', views.create, name='create'),
    #path('<int:id>/reschedule', views.reschedule, name='reschedule'),
]
