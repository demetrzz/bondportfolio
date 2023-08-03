from django.urls import path
from bonds.views import*

urlpatterns = [
    path("deals/", BondsDeals.as_view()),
    path("deals/user", DealsByUser.as_view()),
    path("image/", BondsImage.as_view()),
    path("instrument/", BondsByParameters.as_view()),
    path('bonds/<int:rating_id>/', BondsAPIListByRating.as_view()),
    path('bonds/', BondsAPIList.as_view(), name='all_bonds'),
]
