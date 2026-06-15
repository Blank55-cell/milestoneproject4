from django.urls import path
from . import views

urlpatterns = [
    # Main dashboard view for authenticated users
    path('', views.account_dashboard, name='account_dashboard'),
]