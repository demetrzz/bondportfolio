import base64
import io
# import uuid as uuid_lib

import numpy as np
import requests
from django.db import models
from django.urls import reverse
from matplotlib import pyplot as plt
from rest_framework.authtoken.admin import User

plt.switch_backend('agg')


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

    def get_absolute_url(self):
        return reverse('bonds_rest_api', kwargs={'isin': self.isin})

    class Meta:
        verbose_name_plural = "Bonds"


class Rating(models.Model):
    rating = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.rating

    class Meta:
        verbose_name_plural = "Ratings"


class Deals(models.Model):
    buy = models.BooleanField(null=False)
    quantity = models.IntegerField(null=False)
    price_at_the_time = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    time_create = models.DateTimeField(auto_now_add=True)
    custom_time = models.DateTimeField(blank=True, null=True)
    total_value = models.IntegerField(null=True)
    bonds = models.ForeignKey('Bonds', on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def calculate_value(cls, user_id):
        obj = Deals.objects.filter(user_id=user_id)
        total_value = obj.
        Deals.objects.update_or_create(
            user_id=user_id,
            defaults={
                'image_base64': total_value,
            }
        )

    class Meta:
        verbose_name_plural = "Deals"


class Images(models.Model):
    image_base64 = models.BinaryField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @classmethod
    def generate_and_send(cls, user_id, percents=(0,)):
        response = requests.get(
            'https://iss.moex.com/iss/engines/stock/zcyc.json?iss.only=yearyields&iss.meta=off&date=today')
        data = response.json()['yearyields']['data']
        for i in range(len(percents)):
            x_list = [item[2] for item in data]
            y_list = [item[3]+i for item in data]
            poly = np.polyfit(x_list, y_list, 5)
            poly_y = np.poly1d(poly)(x_list)
            np.interp(0.6, x_list, poly_y)
            if i != 0:
                label = f'g-curve + {i}%'
            else:
                label = 'g-curve'
            plt.plot(x_list, y_list, label=label)

        plt.xlabel("duration")
        plt.ylabel("yield")
        plt.legend()

        string_bytes = io.BytesIO()
        plt.savefig(string_bytes, format='jpg')
        string_bytes.seek(0)
        base64_jpg_data = base64.b64encode(string_bytes.read())

        Images.objects.update_or_create(
            user_id=user_id,
            defaults={
                'image_base64': base64_jpg_data,
            }
        )
        return Images.objects.filter(user=user_id)

    class Meta:
        verbose_name_plural = "Images"
