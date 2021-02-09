from django.urls import path
from . import views
from app.views import RegisterView, GetInfoView

urlpatterns = [
    path('', views.index, name='index'),
    path('getinfo', GetInfoView.as_view(), name='getinfo'),
    path('register', RegisterView.as_view(), name='register'),
    path('thanks', views.thanks, name='thanks'),
]
