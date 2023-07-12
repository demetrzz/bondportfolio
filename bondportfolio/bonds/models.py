from django.db import models


class Bonds(models.Model):
    name = models.CharField(max_length=20)
    yield_date = models.DateField()
    isin = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    duration = models.SmallIntegerField()
    effective_yield = models.DecimalField(max_digits=4, decimal_places=2)
    g_spread = models.DecimalField(max_digits=4, decimal_places=2)
    z_spread = models.DecimalField(max_digits=4, decimal_places=2)
    volume = models.IntegerField()
    bonds_rating = models.ForeignKey('BondsRating', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Bonds"


class BondsRating(models.Model):
    rating = models.CharField(max_length=4)

    def __str__(self):
        return self.rating
