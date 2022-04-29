from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:state>/<str:year>/', views.election, name='election'),
]
