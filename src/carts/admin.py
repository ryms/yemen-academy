from django.contrib import admin

from .models import Cart, ProductInCart



admin.register(Cart,ProductInCart)(admin.ModelAdmin)