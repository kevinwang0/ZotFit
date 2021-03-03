from django.urls import path
from . import views
from app.views import HomeView, RegisterView, LoginView, GetInfoView, WorkoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('home', HomeView.as_view(), name='home'),
    path('getinfo', GetInfoView.as_view(), name='getinfo'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('thanks', views.thanks, name='thanks'),
    path('workout', WorkoutView.as_view(), name='workout'),
]
