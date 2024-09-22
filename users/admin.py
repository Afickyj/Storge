from django.contrib import admin
from .models import Profile, Category, Product

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
    list_display = ['name', 'category', 'price', 'availability', 'author']
    search_fields = ['name', 'category__name']
    list_filter = ['availability', 'category', 'author']
    list_editable = ['price', 'availability']
    raw_id_fields = ['author']  # Zlepšení výkonu při výběru autora
