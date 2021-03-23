from django.contrib import admin
from .models.product import Product
from .models.categories import Category
from .models.customers import Customer
from .models.orders import Orders

class AdminProducts(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.
admin.site.register(Product, AdminProducts)
admin.site.register(Category, AdminCategory)
admin.site.register(Customer)
admin.site.register(Orders)
