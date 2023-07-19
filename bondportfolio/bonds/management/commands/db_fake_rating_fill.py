from django.core.management.base import BaseCommand

from ...models import *


class Command(BaseCommand):
    def handle(self, **options):
        print('filling db with fake ratings')
        # made up ratings:    AAA  	9%
        #                     AA+	9.5%
        #                     AA	10%
        #                     AA-  	10.5%
        #                     A+  	11%
        #                     A	    11.5%
        #                     A-  	12%
        #                     BBB+	12.5%
        #                     BBB	13%
        #                     BBB-  13.5%
        #                     BB+	14%
        #                     BB	14.5%
        #                     BB-	15%
        #                     B+	15.5%
        #                     B	    16%
        #                     B-	16.5%
        qs = Bonds.objects.filter(g_spread__range=(0.1, 1.4))
        qs.update(bonds_rating_id=1)

        start_range = 8.75
        finish_range = 9.25
        for rating in range(1, 17):
            qs = Bonds.objects.filter(effective_yield__range=(start_range, finish_range))
            qs.update(bonds_rating_id=rating)
            start_range = finish_range + 0.01
            finish_range = finish_range + 0.5
