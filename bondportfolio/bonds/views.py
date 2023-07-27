import base64
import io

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
        data_0 = [[0.25, 7.3482],
                  [0.50, 7.5542],
                  [0.75, 7.7532],
                  [1.00, 7.9418],
                  [2.00, 8.5998],
                  [3.00, 9.1398],
                  [5.00, 10.0335],
                  [7.00, 10.6535],
                  [10.00, 11.1882],
                  [15.00, 11.6357],
                  [20.00, 11.8698],
                  [30.00, 12.1197]]

        (x, y) = zip(*data_0)
        x_list = list(x)
        y_list = list(y)
        poly = np.polyfit(x_list, y_list, 5)
        poly_y = np.poly1d(poly)(x_list)
        np.interp(0.6, x_list, poly_y)
        plt.plot(x_list, y_list)
        string_bytes = io.BytesIO()
        plt.savefig(string_bytes, format='jpg')
        string_bytes.seek(0)
        base64_jpg_data = base64.b64encode(string_bytes.read())
        user_id = self.request.user.id
        print(base64_jpg_data)

        Images.objects.update_or_create(
            user_id=user_id,
            defaults={
                'image_base64': base64_jpg_data,
            }
        )

        return Images.objects.filter(user=user_id)
