from .cart import Cart
from .forms import ProductSearchForm
from .models import Category


def search_form(request):
    return {'search_form': ProductSearchForm()}


def cart(request):
    return {'cart': Cart(request)}


def categories(request):
    return {'categories': Category.objects.all()}
