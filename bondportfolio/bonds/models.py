from django.db import models


class Bonds(models.Model):
    name = models.CharField(max_length=30, null=False)
    #yield_date = models.DateField()
    isin = models.CharField(max_length=30, unique=True, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    duration = models.SmallIntegerField(null=False)
    effective_yield = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    g_spread = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    z_spread = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    volume = models.IntegerField(null=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    bonds_rating = models.ForeignKey('BondsRating', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Bonds"


class BondsRating(models.Model):
    rating = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.rating
