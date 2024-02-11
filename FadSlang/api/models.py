from django.db import models
from PIL import Image
import os
class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

class Variants(models.Model): #Color
    name = models.CharField(max_length=100)
    # description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Colour"
        verbose_name_plural = "Colours"

class SubVariants(models.Model): #Size
    name = models.CharField(max_length=100)
    # description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
    
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
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    


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
    # thumbnail = ThumbnailerImageField(upload_to='product_images_thumbnails/', resize_source={'size': None, 'sharpen': True}, blank=True)

    def save(self, *args, **kwargs):

        if self.pk:
            # Fetch the current instance from the database
            old_instance = ProductImages.objects.get(pk=self.pk)
            # Check if the image has changed
            if old_instance.image != self.image:
                # Delete the old image file
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)

        super().save(*args, **kwargs)

        # Open the original image
        original_image = Image.open(self.image.path)

        # Set the quality (adjust as needed)
        quality = 30

        # Save the image with adjusted quality
        original_image.save(self.image.path, quality=quality)

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
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class SalesMaster(models.Model):
    status = [
        (0, 'Pending'),
        (1, 'Invoiced'),
        (2, 'Delivered'),
        (3, 'Returned'),
    ]
    # customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    # address = models.ForeignKey(Addresses, on_delete=models.SET_NULL, null=True)
    address = models.TextField(null=True, blank=True)
    total_qty = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    status = models.IntegerField(default=0, choices=status)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Sales Order"
        verbose_name_plural = "Sales Orderes"
    
class SalesDetails(models.Model):
    master = models.ForeignKey(SalesMaster, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductStock, on_delete=models.SET_NULL, null=True)
    qty = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    price = models.DecimalField(max_digits=15, decimal_places=8, default=0)

    def __str__(self):
        return self.product.product.name
    

class LandingImage (models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='landing_page_images/')
    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):

        if self.pk:
            # Fetch the current instance from the database
            old_instance = LandingImage.objects.get(pk=self.pk)
            # Check if the image has changed
            if old_instance.image != self.image:
                # Delete the old image file
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)

        super().save(*args, **kwargs)

        # Open the original image
        original_image = Image.open(self.image.path)

        # Set the quality (adjust as needed)
        quality = 30

        # Save the image with adjusted quality
        original_image.save(self.image.path, quality=quality)
    
    class Meta:
        verbose_name = "LandingImage"
        verbose_name_plural = "LandingImages"

class CaroualImage (models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='carosal_page_images/')
    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):


        if self.pk:
            # Fetch the current instance from the database
            old_instance = CaroualImage.objects.get(pk=self.pk)
            # Check if the image has changed
            if old_instance.image != self.image:
                # Delete the old image file
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)


        super().save(*args, **kwargs)

        # Open the original image
        original_image = Image.open(self.image.path)

        # Set the quality (adjust as needed)
        quality = 30

        # Save the image with adjusted quality
        original_image.save(self.image.path, quality=quality)
        
    class Meta:
        verbose_name = "CaroualImage"
        verbose_name_plural = "CaroualImages"