from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin site
    path('admin/', admin.site.urls),

    # App routing
    path('', include('listings.urls')),            # Property list, details, and stripe checkout
    path('account/', include('accounts.urls')),    # Custom user profile and accounts section
    path('accounts/', include('allauth.urls')),    # Django-allauth signup/login routes
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)