from django.urls import path
from . import views

urlpatterns = [
    # Main profile dashboard
    path('', views.account_dashboard, name='account_dashboard'),

    # Toggle save/unsave from listings or detail page
    path('toggle-save/<int:listing_id>/', views.toggle_save_property, name='toggle_save'),

    # Remove a saved property directly from dashboard
    path('remove-saved/<int:saved_id>/', views.remove_saved_property, name='remove_saved'),
]