from django.contrib import admin

from api.models import Categories, ProductImages, ProductStock, Products, SubVariants, Variants

# Register your models here.

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 1  # Number of empty forms to display for adding new images

class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','product_code', 'price','get_category_name')
    filter_horizontal = ('variants', 'sub_variants',)
    inlines = [ProductImageInline, ProductStockInline]
    search_fields = ['name', 'product_code']
    list_filter = ['category','variants', 'sub_variants']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else ''
    get_category_name.short_description = 'Category'

    # def get_variants_names(self, obj):
    #     return ', '.join(variants.name for variants in obj.variants.all()) if obj.variants.exists() else ''
    # get_variants_names.short_description = 'Variants'

# class ProductStockAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variant', 'sub_variant', 'qty',)

admin.site.register(Variants, ColorAdmin)
admin.site.register(SubVariants, SizeAdmin)
admin.site.register(Products, ProductAdmin)
# admin.site.register(ProductStock)
admin.site.register(Categories)
# admin.site.register(ProductImages)



admin.site.site_header = 'FadSlang Admin Panel'
admin.site.site_title = 'Admin Portal'
admin.site.index_title = 'Welcome to FadSlang Admin Panel'

# admin.site.site_url = "www.google.com"
