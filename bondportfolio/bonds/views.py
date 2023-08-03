from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated


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


class BondsDeals(generics.ListCreateAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    permission_classes = (IsAuthenticated, )


class DealsByUser(generics.ListCreateAPIView):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializerByUser
    permission_classes = (IsAuthenticated, )


class BondsImage(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_id = self.request.user.id                                                                                                  
        image = Images.generate_and_send(user_id, (1, 2))
        return image
