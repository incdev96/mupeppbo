from . import views
from django.urls import path

app_name = 'message'

urlpatterns = [
    path('index/', views.index, name='index')
]
