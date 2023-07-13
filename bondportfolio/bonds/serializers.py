from rest_framework import serializers
from .models import *

class BondsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonds
        fields = ("__all__")
