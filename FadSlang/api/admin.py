from django.contrib import admin

from api.models import CaroualImage,LandingImage,Addresses, Categories, Customers, ProductImages, ProductStock, Products, SalesDetails, SalesMaster, SubVariants, Variants

# Register your models here.

admin.site.register(LandingImage)
admin.site.register(CaroualImage)


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 1  

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


admin.site.register(Categories)
admin.site.register(Variants, ColorAdmin)
admin.site.register(SubVariants, SizeAdmin)
admin.site.register(Products, ProductAdmin)


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    search_fields = ['product__name','variant__name', 'sub_variant__name'] 
    

class SalesDetailsInline(admin.TabularInline):  
    model = SalesDetails
    extra = 1  
    autocomplete_fields = ['product']


@admin.register(SalesMaster)
class SalesMasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'total_qty', 'total', 'status')
    fields = ('name', 'email', 'phone', 'address', 'status') 
    search_fields = ['name', 'email', 'phone', 'address', 'status']
    list_filter = ['email', 'phone', 'status']
    inlines = [SalesDetailsInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        self.update_totals(form, formsets)

    def delete_model(self, request, obj):
        # Revert ProductStock quantities and SalesMaster totals
        for detail in obj.salesdetails_set.all():
            product_stock = detail.product
            product_stock.qty += detail.qty
            product_stock.save()

        obj.delete()

    def update_totals(self, form, formsets):
        total_qty = 0
        total_amount = 0

        for detail_formset in formsets:
            for detail_form in detail_formset:
                if detail_form.cleaned_data and 'qty' in detail_form.cleaned_data:
                    product_stock = detail_form.cleaned_data['product']
                    product_stock.qty -= detail_form.cleaned_data['qty']
                    product_stock.save()

                    total_qty += detail_form.cleaned_data['qty']
                    total_amount += detail_form.cleaned_data['qty'] * detail_form.cleaned_data['price']

        form.instance.total_qty = total_qty
        form.instance.total = total_amount
        form.instance.save()



admin.site.site_header = 'FadSlang Admin Panel'
admin.site.site_title = 'Admin Portal'
admin.site.index_title = 'Welcome to FadSlang Admin Panel'

