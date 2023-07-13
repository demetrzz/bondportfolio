from .serializers import BondsSerializer
from .permissions import *
from .models import *
from rest_framework import generics


class BondsAPIList(generics.ListCreateAPIView):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    permission_classes = (IsAdminOrReadOnly, )


class BondsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrReadOnly, )


class BondsAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Bonds.objects.all()
    serializer_class = BondsSerializer
    permission_classes = (IsAdminOrReadOnly, )
