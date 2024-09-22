from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProductSearchForm
from .models import Category, Product
from django.conf import settings


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


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Tvé údaje byly aktualizovány!')
            return redirect('profile')  # Přesměrování na profilovou stránku
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile_update.html', context)


def category_list(request):
    categories = Category.objects.all()
    print("Načtené kategorie:", categories)  # Ladicí výpis
    return render(request, 'users/category_list.html', {'categories': categories})


def home(request):
    print("Database NAME in view:", settings.DATABASES['default']['NAME'])
    categories = Category.objects.all()
    products = Product.objects.all()
    search_form = ProductSearchForm()  # Vytvoření instance formuláře
    print("Categories in view:", categories)
    print("Products in view:", products)
    return render(request, 'users/home.html', {
        'categories': categories,
        'products': products,
        'search_form': search_form  # Přidání formuláře do kontextu
    })

def product_search(request):
    form = ProductSearchForm()
    results = []

    print("Accessing product_search view")  # Ladicí výpis

    if 'query' in request.GET:
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(name__icontains=query) | Product.objects.filter(
                description__icontains=query)
            print(f"Search query: {query}, results found: {results.count()}")  # Ladicí výpis
        else:
            print("Form is not valid")  # Ladicí výpis
    else:
        print("No query parameter in GET request")  # Ladicí výpis

    return render(request, 'users/product_search.html', {'form': form, 'results': results})
