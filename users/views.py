from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Registrace uživatele
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Účet pro {username} byl vytvořen! Nyní se můžeš přihlásit.')
            return redirect('login')  # Přesměrování na přihlášení
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Profilová stránka
@login_required
def profile(request):
    return render(request, 'users/profile.html')
