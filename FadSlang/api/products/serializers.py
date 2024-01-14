from rest_framework import serializers

from api.models import Categories, ProductImages, ProductStock, Products, SubVariants, Variants

class VariantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variants
        exclude = ('created_date',)

class SubVariantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVariants
        exclude = ('created_date',)

class ProductStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductStock
        exclude = ('created_date',)
        # fields = '__all__'
    

class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        exclude = ('created_date',)
    

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = VariantDetailSerializer(many=True)
    sub_variants = SubVariantDetailSerializer(many=True)
    product_stock = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ('__all__')

    def get_product_stock(self, instance):
        stock_inst = ProductStock.objects.filter(product=instance)
        serialized = ProductStockSerializer(stock_inst, many=True)
        return serialized.data

    def get_images(self, instance):
        image_inst = ProductImages.objects.filter(product=instance)
        serialized = ProductImagesSerializer(image_inst, many=True)
        return serialized.data
class CategoriesHomeSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Categories
        fields = ('id','name','description','images')

    def get_images(self, instance):
        image=None
        image_inst = Products.objects.filter(category=instance).first()
        if ProductImages.objects.filter(product=image_inst).exists():
            image = ProductImages.objects.filter(product=image_inst).first()
            image = ProductImagesSerializer(image).data
        return image
class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'
class SubVariantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubVariants
        fields = '__all__'
    

