from django.db import models
from rest_framework.authtoken.admin import User


class Bonds(models.Model):
    name = models.CharField(max_length=20, null=False)
    yield_date = models.DateField(null=False)
    isin = models.CharField(max_length=20, unique=True, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    duration = models.SmallIntegerField(null=False)
    effective_yield = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    g_spread = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    z_spread = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    volume = models.IntegerField(null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    rating = models.ForeignKey('Rating', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Bonds"


class Rating(models.Model):
    rating = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.rating


class Deals(models.Model):
    buy = models.BooleanField(null=False)
    quantity = models.IntegerField(null=False)
    time_create = models.DateTimeField(auto_now_add=True)
    bonds = models.ForeignKey('Bonds', on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Deals"


class Images(models.Model):
    image_base64 = models.BinaryField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Images"
