from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Variants(models.Model): #Color
    name = models.CharField(max_length=100)
    # description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class SubVariants(models.Model): #Size
    name = models.CharField(max_length=100)
    # description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    product_code = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    # variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, null=True)
    # sub_variant = models.ForeignKey(SubVariants, on_delete=models.SET_NULL, null=True)
    variants = models.ManyToManyField(Variants, related_name='products', blank=True)
    sub_variants = models.ManyToManyField(SubVariants, related_name='products', blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=8, default=0)



    def __str__(self):
        return self.name
    


class ProductStock(models.Model): #Size & Color
    created_date = models.DateTimeField(auto_now_add=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, null=True)
    sub_variant = models.ForeignKey(SubVariants, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    qty = models.DecimalField(max_digits=15, decimal_places=8, default=0)

    def __str__(self):
        # return self.variant.product.name
        return f"{self.product} - variant: {self.variant} - sub_variant: {self.sub_variant} - Quantity: {self.qty}"

class ProductImages(models.Model): #Color/Variants
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name


# ==================


class Customers(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Addresses(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    home = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class SalesMaster(models.Model):
    status = [
        (0, 'pending'),
        (1, 'invoiced'),
        (2, 'delivered'),
        (3, 'returned'),
    ]
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    address = models.ForeignKey(Addresses, on_delete=models.SET_NULL, null=True)
    total_qty = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    status = models.IntegerField(default=0, choices=status)

    def __str__(self):
        return self.customer.name
    
class SalesDetails(models.Model):
    master = models.ForeignKey(SalesMaster, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, null=True)
    sub_variant = models.ForeignKey(SubVariants, on_delete=models.SET_NULL, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    price = models.DecimalField(max_digits=15, decimal_places=8, default=0)

    def __str__(self):
        return self.variant.name