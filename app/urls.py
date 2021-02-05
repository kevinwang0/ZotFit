from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getinfo', views.getinfo, name='getinfo'),
    path('thanks', views.thanks, name='thanks')
    path('login/', views.login, name='login')
]
