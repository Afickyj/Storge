from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ProductSearchForm,
    ProductForm,
    OrderCreateForm  # Přidáno
)
from .models import Category, Product, Order, OrderItem  # Přidáno Order a OrderItem
from django.conf import settings
from .cart import Cart
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden

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
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
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

def product_list(request):
    """
    View pro zobrazení seznamu produktů jako mřížka nebo seznam.
    """
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    current_category = None
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category_id=category_id)

    paginator = Paginator(products.order_by('id'), 12)  # Přidáno order_by pro eliminaci varování
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': current_category,  # Přidání aktuální kategorie do kontextu
    }
    return render(request, 'users/product_list.html', context)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form_quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=form_quantity, update_quantity=False)
    return redirect('cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect('cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'users/cart_detail.html', {'cart': cart})

class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'users/product_edit.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'users.can_edit_product'

class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'users/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'users.can_delete_product'

@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        messages.error(request, "Váš košík je prázdný.")
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            messages.success(request, f'Objednávka {order.id} byla úspěšně vytvořena.')
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'users/order_create.html', {'cart': cart, 'form': form})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Uživatel může vidět pouze své objednávky nebo je administrátor
    if order.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Nemáte oprávnění zobrazit tuto objednávku.")
    return render(request, 'users/order_detail.html', {'order': order})

@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, 'users/order_list.html', {'orders': orders})
