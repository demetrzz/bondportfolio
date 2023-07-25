from rest_framework import serializers
from .models import *


class BondsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonds
        fields = "__all__"


class BondsRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class BondsSerializerByRating(serializers.ModelSerializer):
    bonds_rating = BondsRatingSerializer(read_only=True)

    class Meta:
        model = Bonds
        fields = ['name', 'yield_date', 'price', 'duration', 'effective_yield', 'g_spread', 'volume', 'bonds_rating']
