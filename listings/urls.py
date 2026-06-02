from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),                      # Homepage
    path('listings/', views.all_listings, name='listings'),      # Show all listings page
]