from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import (
    Category,
    Product,
    ProductImage,
)

# class InLineProduct(admin.StackedInline):
#     model = Product
#     extra = 1
class InLineProduct(admin.TabularInline):
    model = Product
    extra = 1
    max_num = 10

class CategoryAdmin(admin.ModelAdmin):
    inlines=[InLineProduct]
    fieldsets = (
        ('Category Info', {
            "fields": (
                'name',
            ),
        }),
    )


class InLineImage(admin.TabularInline):
    model=ProductImage
    extra=1
    max_num=10

class ProductAdmin(admin.ModelAdmin):
    inlines=[InLineImage]

    list_display=(
        'category',
        'name',
        # 'description',
        'image',
        'price',
        'currency',
        'published_at',
        'updated_at',        
    )
    ordering=(
        'category',
        'name',
        'image',
        'price',
        'currency',
        'published_at',
        'updated_at',        
    )
    list_editable=(
        'category',
        # 'description',
        'price',
        'currency',
    )
    list_display_links=(
        # 'category',
        'name',
        # 'image',
        'published_at',
        'updated_at',        
    )
    search_fields=(
        'category',
        'name',
        'price',
        'published_at',
        'updated_at',        
    )
    list_filter=(
        'category',
        'name',
        'price',
        'currency',
        'published_at',
        'updated_at',        
    )
    fieldsets = (
        ('Product Info', {
            "fields": (
                'category',
                'name',
                'description',
                'image',
                'price',
                'currency',
            ),
        }),
    )
    formfield_overrides={
        models.TextField : {'widget' : TinyMCE},
    }
    
class ProductImageAdmin(admin.ModelAdmin):
    fieldsets=(
        ('Image', {
            'fields':(
                'product',
                'short_caption',
                'image',
            )
        }),
    )
# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)