from django.http import request
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .permissions import *
from .models import *
from rest_framework import generics


class BondsAPIList(generics.ListCreateAPIView):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    permission_classes = (IsAdminOrReadOnly, )


class BondsAPIListByRating(generics.ListCreateAPIView):
    serializer_class = BondsSerializerByRating
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        bonds_rating_id = self.kwargs.get('bonds_rating_id', None)
        start = self.kwargs.get('start', None)
        end = self.kwargs.get('end', None)
        print('kek')

        if bonds_rating_id:
            bonds_by_id = Bonds.objects.filter(bonds_rating_id=bonds_rating_id)
            if bonds_by_id:
                return bonds_by_id
            else:
                raise NotFound()
        elif start and end:
            bonds_range = Bonds.objects.filter(bonds_rating_id__gte=start, bonds_rating_id__lte=end)
            if bonds_range:
                return bonds_range
            else:
                raise NotFound()


class BondsByParameters(generics.ListCreateAPIView):
    serializer_class = BondsSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        #self.request.GET.items()
        startdur = self.request.GET.get('startdur')
        enddur = self.request.GET.get('enddur')
        qs = Bonds.objects.filter(duration__range=(startdur, enddur))
        return qs


class BondsDeals(generics.CreateAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    permission_classes = (IsAuthenticated, )
