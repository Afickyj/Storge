from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Category, Product, Order, OrderItem
from .forms import UserRegisterForm, OrderCreateForm
from django.urls import reverse
from decimal import Decimal  # Přidáno pro práci s desetinnými čísly

# Testování modelu Profile
class ProfileModelTest(TestCase):
    def test_profile_creation(self):
        # Vytvoření nového uživatele
        user = User.objects.create_user(username='testuser', password='testpass')
        # Získání propojeného profilu (mělo by být vytvořeno automaticky pomocí signálů)
        profile = Profile.objects.get(user=user)
        # Kontrola, zda instance profilu existuje
        self.assertIsInstance(profile, Profile)
        # Ověření, že uživatelské jméno profilu je správné
        self.assertEqual(profile.user.username, 'testuser')

# Testování modelu Product
class ProductModelTest(TestCase):
    def test_product_creation(self):
        # Vytvoření kategorie pro produkt
        category = Category.objects.create(name='Testovací kategorie')
        # Vytvoření produktu s přiřazenou kategorií
        product = Product.objects.create(
            name='Testovací produkt',
            description='Popis produktu',
            price=Decimal('99.99'),  # Použití Decimal
            stock=10,
            category=category
        )
        # Ověření, že název produktu je správný
        self.assertEqual(product.name, 'Testovací produkt')
        # Ověření, že metoda get_absolute_url vrací správnou URL
        self.assertEqual(product.get_absolute_url(), reverse('product_detail', args=[product.id]))

# Testování modelu Order
class OrderModelTest(TestCase):
    def test_order_total_cost_with_user(self):
        # Vytvoření uživatele pro objednávku
        user = User.objects.create_user(username='testuser', password='testpass')
        # Vytvoření objednávky přiřazené k uživateli
        order = Order.objects.create(
            user=user,
            first_name='Jan',
            last_name='Novák',
            email='jan@example.com',
            address='Ulice 123',
            delivery_method='courier',
            payment_method='cash',
            delivery_price=Decimal('50.00')  # Použití Decimal
        )
        # Vytvoření kategorie a produktu
        category = Category.objects.create(name='Testovací kategorie')
        product = Product.objects.create(
            name='Testovací produkt',
            description='Popis produktu',
            price=Decimal('100.00'),  # Použití Decimal
            stock=10,
            category=category
        )
        # Vytvoření položky objednávky pro produkt
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=2
        )
        # Výpočet celkové ceny objednávky
        total_cost = order.get_total_cost()
        # Ověření, že celková cena je správná (2 * 100 + 50 za dopravu)
        self.assertEqual(total_cost, Decimal('250.00'))

    def test_order_total_cost_without_user(self):
        # Vytvoření objednávky bez uživatele (nákup bez registrace)
        order = Order.objects.create(
            user=None,  # Žádný uživatel není přiřazen
            first_name='Host',
            last_name='Uživatel',
            email='host@example.com',
            address='Hostovská 789',
            delivery_method='courier',
            payment_method='cash',
            delivery_price=Decimal('30.00')  # Použití Decimal
        )
        # Vytvoření kategorie a produktu
        category = Category.objects.create(name='Hostovská kategorie')
        product = Product.objects.create(
            name='Hostovský produkt',
            description='Popis hostovského produktu',
            price=Decimal('50.00'),  # Použití Decimal
            stock=5,
            category=category
        )
        # Vytvoření položky objednávky pro produkt
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=1
        )
        # Výpočet celkové ceny objednávky
        total_cost = order.get_total_cost()
        # Ověření, že celková cena je správná (1 * 50 + 30 za dopravu)
        self.assertEqual(total_cost, Decimal('80.00'))

# Testování registračního formuláře uživatele
class UserRegisterFormTest(TestCase):
    def test_valid_form(self):
        # Platná data pro formulář
        form_data = {
            'username': 'novyuzivatel',
            'email': 'novyuzivatel@example.com',
            'password1': 'SilneHeslo123',
            'password2': 'SilneHeslo123'
        }
        # Inicializace formuláře s daty
        form = UserRegisterForm(data=form_data)
        # Formulář by měl být platný
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Neplatná data pro formulář
        form_data = {
            'username': 'admin',  # Zakázané uživatelské jméno
            'email': 'neplatnyemail',  # Neplatný formát emailu
            'password1': 'heslo',  # Slabé heslo
            'password2': 'heslo'   # Hesla se shodují, ale jsou slabá
        }
        # Inicializace formuláře s daty
        form = UserRegisterForm(data=form_data)
        # Formulář by měl být neplatný
        self.assertFalse(form.is_valid())
        # Kontrola, zda jsou v chybách uvedena specifická pole
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)

# Testování pohledu na seznam produktů
class ProductListViewTest(TestCase):
    def setUp(self):
        # Vytvoření kategorie a produktů pro testování
        self.category = Category.objects.create(name='Testovací kategorie')
        self.product1 = Product.objects.create(
            name='Produkt 1',
            description='Popis 1',
            price=Decimal('10.00'),  # Použití Decimal
            stock=5,
            category=self.category
        )
        self.product2 = Product.objects.create(
            name='Produkt 2',
            description='Popis 2',
            price=Decimal('20.00'),  # Použití Decimal
            stock=3,
            category=self.category
        )

    def test_product_list_view(self):
        # Odeslání GET požadavku na pohled seznamu produktů
        response = self.client.get(reverse('product_list'))
        # Kontrola, že odpověď má status 200 OK
        self.assertEqual(response.status_code, 200)
        # Kontrola, že byla použita správná šablona
        self.assertTemplateUsed(response, 'users/product_list.html')
        # Ověření, že produkty jsou v kontextu
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

    def test_product_list_view_with_search(self):
        # Odeslání GET požadavku s vyhledávacím dotazem
        response = self.client.get(reverse('product_list') + '?query=Produkt 1')
        # Kontrola, že pouze hledaný produkt je v kontextu
        self.assertIn(self.product1, response.context['products'])
        self.assertNotIn(self.product2, response.context['products'])

    def test_product_list_view_with_category_filter(self):
        # Odeslání GET požadavku s filtrem kategorie
        response = self.client.get(reverse('product_list') + f'?category={self.category.id}')
        # Ověření, že oba produkty jsou v kontextu
        self.assertIn(self.product1, response.context['products'])
        self.assertIn(self.product2, response.context['products'])

# Testování pohledů pro košík
class CartViewTest(TestCase):
    def setUp(self):
        # Vytvoření produktu pro přidání do košíku
        self.category = Category.objects.create(name='Košíková kategorie')
        self.product = Product.objects.create(
            name='Košíkový produkt',
            description='Popis košíkového produktu',
            price=Decimal('15.00'),  # Použití Decimal
            stock=10,
            category=self.category
        )

    def test_cart_detail_view(self):
        # Odeslání GET požadavku na detail košíku
        response = self.client.get(reverse('cart_detail'))
        # Kontrola, že odpověď má status 200 OK
        self.assertEqual(response.status_code, 200)
        # Ověření, že byla použita správná šablona
        self.assertTemplateUsed(response, 'users/cart_detail.html')

    def test_cart_add_view(self):
        # Odeslání POST požadavku pro přidání produktu do košíku
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 2})
        # Kontrola, že odpověď přesměruje na detail košíku
        self.assertRedirects(response, reverse('cart_detail'))
        # Přístup k session pro ověření obsahu košíku
        session = self.client.session
        cart = session.get('cart')
        self.assertIsNotNone(cart)
        # Ověření, že produkt byl přidán do košíku se správným množstvím
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]['quantity'], 2)

    def test_cart_update_view(self):
        # Nejprve přidat produkt do košíku
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 1})
        # Odeslání POST požadavku pro aktualizaci množství produktu v košíku
        response = self.client.post(reverse('cart_update', args=[self.product.id]), {'quantity': 5})
        # Kontrola, že odpověď přesměruje na detail košíku
        self.assertRedirects(response, reverse('cart_detail'))
        # Přístup k session pro ověření obsahu košíku
        session = self.client.session
        cart = session.get('cart')
        # Ověření, že množství produktu bylo aktualizováno
        self.assertEqual(cart[str(self.product.id)]['quantity'], 5)

    def test_cart_remove_view(self):
        # Nejprve přidat produkt do košíku
        self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 1})
        # Odeslání POST požadavku pro odstranění produktu z košíku
        response = self.client.post(reverse('cart_remove', args=[self.product.id]))
        # Kontrola, že odpověď přesměruje na detail košíku
        self.assertRedirects(response, reverse('cart_detail'))
        # Přístup k session pro ověření obsahu košíku
        session = self.client.session
        cart = session.get('cart')
        # Ověření, že produkt byl odstraněn z košíku
        self.assertNotIn(str(self.product.id), cart)
