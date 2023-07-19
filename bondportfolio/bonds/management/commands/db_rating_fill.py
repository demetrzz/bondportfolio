from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from ...models import *


class Command(BaseCommand):
    def handle(self, **options):
        print("clearing db ...")
        BondsRating.objects.all().delete()  # clear all database entries
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [BondsRating])  # resetting PK to 0
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        ratings = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-',
                   'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'BB-', 'B+', 'B', 'B-']

        print('filling in ratings')
        for rating in ratings:
            BondsRating.objects.update_or_create(
                rating=rating
            )

        print('done')
