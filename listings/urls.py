from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),                      # Homepage
    path('listings/', views.all_listings, name='listings'),      # Show all listings page
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'), # Individual property details
    path('account/', views.account_dashboard, name='account_dashboard'), # Logged in user dashboard
]