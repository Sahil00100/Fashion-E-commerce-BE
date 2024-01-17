from rest_framework import serializers
from api.models import LandingImage

class LandingImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = LandingImage
        fields = ("image",)
