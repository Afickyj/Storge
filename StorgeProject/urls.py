from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Toto je domovská stránka")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Uživatelské URL
    path('', home, name='home'),  # Přidání domovské stránky
]
