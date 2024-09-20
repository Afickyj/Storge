from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static


def home(request):
    return render(request, 'home.html')  # Používáme šablonu home.html


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Uživatelské URL
    path('', home, name='home'),  # Domovská stránka
]

# Přidání cest pro media soubory
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
