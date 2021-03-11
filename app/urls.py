from django.urls import path
from . import views
from app.views import HomeView, RegisterView, GetInfoView, StrengthWorkoutView, StepWorkoutView
from django.contrib.auth import views as auth_views

# for use with auth LoginView
LOGIN_CONTEXT = {
    'step': 'Login',
    'title': 'Sign in to ZotFit',
    'button_title': 'Sign in'
}

urlpatterns = [
    path('', views.index, name='index'),
    path('home', HomeView.as_view(), name='home'),
    path('getinfo', GetInfoView.as_view(), name='getinfo'),
    path('register', RegisterView.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(template_name='form.html', extra_context=LOGIN_CONTEXT), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('workout', StrengthWorkoutView.as_view(), name='workout'),
    path('steps', StepWorkoutView.as_view(), name='steps'),
]
