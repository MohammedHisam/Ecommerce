from django.contrib import admin
from .models import *


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']


admin.site.register(Categories, CategoryAdmin)


class FruitsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', 'price', 'category', 'stock', 'available', 'img']
    list_editable = ['price', 'category', 'stock', 'available', 'img']


admin.site.register(Fruits, FruitsAdmin)
