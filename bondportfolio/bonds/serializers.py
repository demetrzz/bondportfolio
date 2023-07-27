from rest_framework import serializers
from .models import *


class BondsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonds
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class BondsSerializerByRating(serializers.ModelSerializer):
    bonds_rating = RatingSerializer(read_only=True)

    class Meta:
        model = Bonds
        fields = ['name', 'yield_date', 'price', 'duration', 'effective_yield', 'g_spread', 'volume', 'bonds_rating']


class DealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deals
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    image_base64 = serializers.SerializerMethodField()

    class Meta:
        model = Images
        fields = "__all__"

    def get_image_base64(self, obj):
        print('kek2')
        print(type(bytes(obj.image_base64).decode()))
        return bytes(obj.image_base64).decode()

    class Meta:
        model = Images
        fields = "__all__"
