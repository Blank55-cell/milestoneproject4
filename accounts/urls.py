from django.urls import path
from . import views

urlpatterns = [
    # My main profile dashboard view when I'm logged in
    path('', views.account_dashboard, name='account_dashboard'),
    
    # URL for toggling a property to my wishlist
    path('toggle-save/<int:listing_id>/', views.toggle_save_property, name='toggle_save'),
]