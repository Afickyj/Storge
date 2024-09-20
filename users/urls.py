from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),  # Registrace
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),      # Přihlášení
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),   # Odhlášení
    path('profile/', views.profile, name='profile'),     # Profilová stránka
    path('profile/update/', views.profile_update, name='profile-update'),  # Aktualizace profilu
]
