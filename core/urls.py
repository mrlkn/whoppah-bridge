from django.urls import path
from .views import admin_dashboard

app_name = 'core'

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
]
