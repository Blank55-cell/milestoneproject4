from django.contrib import admin
from .models import SavedProperty

@admin.register(SavedProperty)
class SavedPropertyAdmin(admin.ModelAdmin):
    # I want to see who saved what and when
    list_display = ('user', 'property', 'added_at')
    search_fields = ('user__username', 'property__title')