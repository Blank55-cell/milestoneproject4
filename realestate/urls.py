from django.contrib import admin
from django.urls import path, include, get_resolver
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# Quick debug to check if URLs are loading
def show_all_urls(request):
    url_list = [str(p) for p in get_resolver().url_patterns]
    return HttpResponse("<br>".join(url_list))

urlpatterns = [
    # Django Admin site
    path('admin/', admin.site.urls),

    # Debug route to see what's registered
    path('debug-urls/', show_all_urls),

    # App routing
    path('account/', include('accounts.urls')),    # Custom user profile and accounts section
    path('accounts/', include('allauth.urls')),    # Django-allauth signup/login routes
    path('', include('listings.urls')),            # Property list, details, and stripe checkout
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)