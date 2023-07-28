import base64
import io

import requests
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
import numpy as np
import matplotlib.pyplot as plt

from .serializers import *
from .permissions import *
from .models import *
from rest_framework import generics

plt.switch_backend('agg')

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


class BondsImage(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        response = requests.get(
            'https://iss.moex.com/iss/engines/stock/zcyc.json?iss.only=yearyields&iss.meta=off&date=today')
        data = response.json()['yearyields']['data']
        
        x_list = [item[2] for item in data]
        y_list = [item[3] for item in data]
        x_list2 = [item[2] for item in data]
        y_list2 = [item[3] + 1 for item in data]
        poly = np.polyfit(x_list, y_list, 5)
        poly_y = np.poly1d(poly)(x_list)
        np.interp(0.6, x_list, poly_y)
        plt.plot(x_list, y_list, label='g-curve')
        plt.plot(x_list2, y_list2, label='g-curve + 1%')
        plt.xlabel("duration")
        plt.ylabel("yield")
        plt.legend()
        
        string_bytes = io.BytesIO()
        plt.savefig(string_bytes, format='jpg')
        string_bytes.seek(0)
        base64_jpg_data = base64.b64encode(string_bytes.read())
        user_id = self.request.user.id                                                                                                  

        Images.objects.update_or_create(
            user_id=user_id,
            defaults={
                'image_base64': base64_jpg_data,
            }
        )

        return Images.objects.filter(user=user_id)
