from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),             # Main home page route
    path('listings/', views.listings_view, name='listings'), # Listings page route
]