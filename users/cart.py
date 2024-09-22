from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        """
        Inicializace košíku.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Uložení prázdného košíku do relace
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Přidání produktu do košíku nebo aktualizace jeho množství.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Odebrání produktu z košíku.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # Označení relace jako modifikované, aby se uložila
        self.session.modified = True

    def __iter__(self):
        """
        Iterace přes položky v košíku a získání produktů z databáze.
        """
        product_ids = self.cart.keys()
        # Získání objektů produktů a jejich přidání do košíku
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Spočítání všech položek v košíku.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Spočítání celkové ceny všech položek v košíku.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Vyčištění košíku.
        """
        del self.session['cart']
        self.save()
