
from rest_framework.response import Response
from rest_framework import status
from api.models import Categories, Products, SubVariants, Variants,LandingImage,CaroualImage
from .serializers import LandingImageSerializers,CaroualImageSerializers

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q

from api.products.serializers import ProductDetailSerializer
@api_view(["GET"])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic

def get_landing_image(request):
    ins = LandingImage.objects.filter().order_by("-id").first()
    serialized = LandingImageSerializers(ins).data

    carousal_ins = CaroualImage.objects.filter().order_by("-id")[:3]
    carousal_serialized = CaroualImageSerializers(carousal_ins,many=True).data
    
    latestProducts = Products.objects.filter().order_by("-id")[:4]
    product_serialized = ProductDetailSerializer(latestProducts,many=True).data
    response_data = {
        'status_code':6000,
        'message':'success',
        'data':serialized,
        "data2":carousal_serialized,
        "data3":product_serialized
    }
    return Response(response_data, status=status.HTTP_200_OK)
