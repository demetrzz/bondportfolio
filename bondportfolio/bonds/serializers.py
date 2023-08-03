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


class DealsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deals
        fields = '__all__'


class DealsSerializerByUser(serializers.ModelSerializer):
    bonds = BondsSerializer(read_only=True)

    class Meta:
        model = Deals
        fields = ['user_id', 'id', 'bonds']


class ImageSerializer(serializers.ModelSerializer):
    image_base64 = serializers.SerializerMethodField()

    def get_image_base64(self, obj):
        return bytes(obj.image_base64).decode()

    class Meta:
        model = Images
        fields = "__all__"


class BondsSerializerByRating(serializers.ModelSerializer):
    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Bonds
        fields = ['name', 'yield_date', 'price', 'duration', 'effective_yield', 'g_spread', 'volume', 'rating_id',
                  'rating']
