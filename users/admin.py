from django.contrib import admin
from .models import Profile, Category, Product, Order, OrderItem


# Registrace modelu Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'address', 'role', 'communication_channel']
    search_fields = ['user__username', 'city', 'address']


# Registrace modelu Category s vlastním Admin třídou
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']
    search_fields = ['name']
    list_filter = ['parent_category']


# Registrace modelu Product s vlastním Admin třídou
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'availability', 'author']  # Přidáno 'stock'
    search_fields = ['name', 'category__name']
    list_filter = ['availability', 'category', 'author']
    list_editable = ['price', 'stock', 'availability']  # Přidáno 'stock' do 'list_editable'
    raw_id_fields = ['author']  # Zlepšení výkonu při výběru autora

    # Přidání API pole pro správu produktů
    readonly_fields = ['api_field']

    def api_field(self, obj):
        return f"/api/products/{obj.id}/"

    api_field.short_description = "API Endpoint"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created', 'updated', 'paid']
    list_filter = ['status', 'paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)

    mark_as_paid.short_description = "Označit vybrané objednávky jako zaplacené"
