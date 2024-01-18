from rest_framework import serializers
from api.models import LandingImage,CaroualImage

class LandingImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = LandingImage
        fields = ("image",)
class CaroualImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = CaroualImage
        fields = ("image",)
