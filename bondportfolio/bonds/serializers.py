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
