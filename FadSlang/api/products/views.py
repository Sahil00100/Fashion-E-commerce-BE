
from rest_framework.response import Response
from rest_framework import status
from api.models import Categories, Products, SubVariants, Variants
from api.products.serializers import ProductDetailSerializer, SubVariantDetailSerializer, VariantDetailSerializer

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

@api_view(["POST"])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def create_product(request):
    data = request.data
    response_data = {
        'Null'
    }
   
    name = data.get('name')
    description = data.get('description')
    product_code = data.get('product_code')
    category = data.get('category')
    price = data.get('price')
    variants_data = data.get('variants', [])
    sub_variants_data = data.get('sub_variants', [])

    category = Categories.objects.create(name='Dress')
    # Create the product
    product = Products.objects.create(
        name=name,
        description=description,
        product_code=product_code,
        category=category,
        price=price
    )
    print("variants_data==>",variants_data)
    print("sub_variants_data==>",sub_variants_data)
    # Create colors
    variants = [Variants.objects.get_or_create(name=variants['name'])[0] for variants in variants_data]
    product.variants.set(variants)

    # Create sizes
    sub_variants = [SubVariants.objects.get_or_create(name=sub_variant['name'])[0] for sub_variant in sub_variants_data]
    product.sub_variants.set(sub_variants)
    response_data = {
        'status_code':6000,
        'message':'success',
        'category':category.id
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["POST", "GET"])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic
def product(request):
    data = request.data
    count = 0
    if request.method == 'POST': # single product details
        pk = data['id']
        if Products.objects.filter(pk=pk).exists():
            instance = Products.objects.get(pk=pk)
            serializer = ProductDetailSerializer(instance)
        else:
            return Response({'status_code':6001, 'message':'No Product found!'}, status=status.HTTP_200_OK)
    else: # all product list with filter
        search = data.get('search')
        categories = data.get('categories', [])
        variants = data.get('variants', [])
        sub_variants = data.get('sub_variants', [])
        price_from = data.get('price_from')
        price_to = data.get('price_to')
        page_no = data.get('page_no')
        items_per_page = data.get('items_per_page')

        query = Q(is_active=True)
        if search:
            query |= Q(name__icontains=search) | Q(product_code__icontains=search)
        if categories:
            query |= Q(category__in=categories)
        if variants:
            query |= Q(variants__id__in=variants)
        if sub_variants:
            query |= Q(sub_variants__id__in=sub_variants)
        if price_from:
            query |= Q(price__gte=price_from)
        if price_to:
            query |= Q(price_to__lte=price_to)

        instance = Products.objects.filter(query)
        count = instance.count()
        if page_no and items_per_page:
            paginator = Paginator(instance, items_per_page)
            try:
                paginated_instance = paginator.page(page_no)
            except PageNotAnInteger:
                paginated_instance = paginator.page(1)
            except EmptyPage:
                paginated_instance = paginator.page(paginator.num_pages)
        else:
            paginated_instance = instance

        serializer = ProductDetailSerializer(paginated_instance, many=True)



    response_data = {
        'status_code':6000,
        'message':'Successfully listed products',
        'data':serializer.data,
        'count':count
    }
    return Response(response_data, status=status.HTTP_200_OK)