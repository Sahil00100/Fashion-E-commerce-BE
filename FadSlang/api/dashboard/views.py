
from rest_framework.response import Response
from rest_framework import status
from api.models import Categories, Products, SubVariants, Variants,LandingImage
from .serializers import LandingImageSerializers

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q


@api_view(["GET"])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
@transaction.atomic

def get_landing_image(request):
    ins = LandingImage.objects.filter().first()
    serialized = LandingImageSerializers(ins).data
    response_data = {
        'status_code':6000,
        'message':'success',
        'data':serialized
    }
    return Response(response_data, status=status.HTTP_200_OK)
