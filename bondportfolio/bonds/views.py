from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .permissions import *
from .models import *
from rest_framework import generics, request


class BondsAPIList(generics.ListCreateAPIView):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    permission_classes = (IsAdminOrReadOnly, )


class BondsAPIListByRating(generics.ListCreateAPIView):
    serializer_class = BondsSerializerByRating
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        rating_id = self.kwargs.get('rating_id', None)
        bonds_by_id = Bonds.objects.filter(rating_id=rating_id)
        if bonds_by_id:
            return bonds_by_id
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


class BondsDeals(generics.ListAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    permission_classes = (IsAuthenticated, )


class DealsByUser(generics.ListCreateAPIView):
    #queryset = Deals.objects.all()
    serializer_class = DealsSerializer  # change this
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_id = self.request.user.id
        print(Deals.calculate_value(user_id))
        qs = Deals.objects.filter(user_id=user_id)
        return qs


class DealsTotalValue(generics.ListAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsTotalValueSerializer
    permission_classes = (IsAuthenticated,)


@api_view()
@permission_classes((IsAuthenticated,))
def total_value_view(request):
    user_id = request.user.id
    total_value = Deals.calculate_value(user_id)
    my_data = {'user_id': user_id, 'total_value': total_value}
    serializer = DealsTotalValueSerializer(my_data)
    return Response(serializer.data)


class BondsImage(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_id = self.request.user.id                                                                                                  
        image = Images.generate_and_send(user_id, (0,1,2))
        return image
