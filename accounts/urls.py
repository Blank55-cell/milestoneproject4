from django.urls import path
from . import views

urlpatterns = [
    # My main profile dashboard view when I'm logged in
    path('', views.account_dashboard, name='account_dashboard'),
]