from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('import_data', views.import_data, name='import_data'),
]
