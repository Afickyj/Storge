# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    ProductSearchForm,
    ProductForm,
    OrderCreateForm
)
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse

import random
from django.utils import timezone


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
    return render(request, 'users/category_list.html', {'categories': categories})


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Seed the random number generator with the current date to change products every 24 hours
    seed = timezone.now().date().toordinal()
    random.seed(seed)

    # Randomly select 5 products
    trending_products = random.sample(list(products), min(len(products), 5))

    context = {
        'categories': categories,
        'trending_products': trending_products,
    }
    return render(request, 'users/home.html', context)


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Zpracování filtru kategorie
    category_id = request.GET.get('category')
    current_category = None
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category_id=category_id)

    # Zpracování vyhledávání
    search_query = request.GET.get('query', '')
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)

    paginator = Paginator(products.order_by('id'), 6)  # Počet produktů na stránku (nastaveno na 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query
    }

    # Zpracování AJAX požadavků
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'users/product_list_partial.html', context)
    else:
        return render(request, 'users/product_list.html', context)


def product_search(request):
    form = ProductSearchForm()
    results = Product.objects.all()

    # Zpracování filtru kategorie
    category_id = request.GET.get('category')
    current_category = None
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        results = results.filter(category_id=category_id)

    # Zpracování vyhledávání
    search_query = request.GET.get('query', '')
    if search_query:
        results = results.filter(name__icontains=search_query) | results.filter(description__icontains=search_query)

    paginator = Paginator(results.order_by('id'), 6)  # Počet produktů na stránku (nastaveno na 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'search_query': search_query,
        'current_category': current_category,
    }

    # Zpracování AJAX požadavků
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'users/product_list_partial.html', context)
    else:
        return render(request, 'users/product_search.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'users/product_detail.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def update_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        stock = request.POST.get('stock')
        if stock.isdigit() and int(stock) >= 0:
            product.stock = int(stock)
            product.save()
            messages.success(request, 'Skladová zásoba byla aktualizována.')
        else:
            messages.error(request, 'Zadejte platné množství.')
    return redirect('product_detail', product_id=product.id)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form_quantity = int(request.POST.get('quantity', 1))

    if form_quantity > product.stock:
        messages.error(request, f'Na skladě je pouze {product.stock} ks tohoto produktu.')
        return redirect('product_detail', product_id=product.id)

    cart.add(product=product, quantity=form_quantity, update_quantity=False)
    messages.success(request, 'Produkt byl přidán do košíku.')
    return redirect('cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity > product.stock:
        messages.error(request, f'Na skladě je pouze {product.stock} ks tohoto produktu.')
        return redirect('cart_detail')

    cart.add(product=product, quantity=quantity, update_quantity=True)
    messages.success(request, 'Košík byl aktualizován.')
    return redirect('cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, 'Produkt byl odstraněn z košíku.')
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
                product = item['product']
                if item['quantity'] > product.stock:
                    messages.error(request, f'Produkt {product.name} nemá dostatečnou skladovou zásobu.')
                    return redirect('cart_detail')
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']
                )
                # Aktualizace skladové zásoby
                product.stock -= item['quantity']
                product.save()
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


# Přehled stromu kategorií
def category_tree(request):
    query = request.GET.get('q')
    if query:
        categories = Category.objects.filter(name__icontains=query)
    else:
        categories = Category.objects.all()

    parent_categories = Category.objects.filter(parent_category__isnull=True)

    context = {
        'categories': categories,
        'parent_categories': parent_categories,
        'query': query
    }
    return render(request, 'users/category_tree.html', context)


# Přemístění kategorie
def move_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        new_parent_id = request.POST.get('parent_category')
        if new_parent_id:
            new_parent = get_object_or_404(Category, id=new_parent_id)
            category.parent_category = new_parent
        else:
            category.parent_category = None
        category.save()
        return redirect('category_tree')

    parent_categories = Category.objects.filter(parent_category__isnull=True).exclude(id=category_id)
    return render(request, 'users/move_category.html', {'category': category, 'parent_categories': parent_categories})


# API endpoint pro seznam produktů
@csrf_exempt
def api_product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = serializers.serialize('json', products)
        return JsonResponse({'products': data}, safe=False)


# API endpoint pro detail produktu
@csrf_exempt
def api_product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = serializers.serialize('json', [product])
        return JsonResponse({'product': data}, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produkt nenalezen'}, status=404)
