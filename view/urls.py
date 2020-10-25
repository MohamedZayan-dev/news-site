from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pages/<str:page>/', views.subPages, name='base_page'),
    path('details/<path:id>/', views.details, name='details'),
   
    
]
