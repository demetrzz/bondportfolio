from django.http import request
from rest_framework.exceptions import NotFound

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


class BondsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrReadOnly, )


class BondsAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    permission_classes = (IsAdminOrReadOnly, )


class BondsByParameters(generics.ListCreateAPIView):
    serializer_class = BondsSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')
        radius = self.request.query_params.get('radius')
