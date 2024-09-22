from .cart import Cart
from .forms import ProductSearchForm


def search_form(request):
    return {'search_form': ProductSearchForm()}


def cart(request):
    return {'cart': Cart(request)}
