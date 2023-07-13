from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from ...models import *
import requests
import datetime

class Command(BaseCommand):
    def handle(self, **options):
        Bonds.objects.all().delete()
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Bonds])
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
        print('trying to clear table')
        print(Bonds.objects.all())
        response = requests.get(
            'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off')
        securities = response.json()['securities']
        marketdata_yields = response.json()['marketdata_yields']

        securities_data = []

        for data in securities['data']:
            a = list(zip(securities['columns'], data))
            securities_data.append(a)

        for bond in securities_data:
            print(f'bond outside is {bond[3][1]}')
            if bond[3][1] and bond[0][1].startswith('RU'):
                print(f'bond is {bond[3][1]}')
                Bonds.objects.update_or_create(
                    name=bond[2][1],
                    #yield_date=bond[13],
                    isin=bond[0][1]
                )

        marketdata_yields_data = []

        for data in marketdata_yields['data']:
            a = list(zip(marketdata_yields['columns'], data))
            marketdata_yields_data.append(a)


        for bond in marketdata_yields_data:
            if bond[6][1] and bond[6][1] < 40:
                effective_yield = round(bond[6][1], 2)
                print(f'yield = {effective_yield}')
            # elif bond[6][1] and bond[6][1] > 40:
            #     continue
            else:
                continue

            if bond[9][1] and bond[9][1]/100 < 20:
                g_spread = round(bond[9][1]/100, 2)
                print(f'g = {g_spread}')
            # elif bond[9][1] and bond[9][1]/100 > 20:
            #     continue
            else:
                continue

            if bond[8][1] and bond[8][1]/100 < 20:
                z_spread = round(bond[8][1]/100, 2)
                print(f'z = {z_spread}')
            # elif bond[8][1] and bond[8][1]/100 > 20:
            #     continue
            else:
                continue

            print(bond[0][1])
            if not bond[0][1]:
                continue

            if bond[2][1] and bond[7][1]:
                try:
                    obj = Bonds.objects.get(isin=bond[0][1])
                    obj.price = bond[2][1]
                    obj.duration = bond[7][1]
                    obj.effective_yield = effective_yield
                    obj.g_spread = g_spread
                    obj.z_spread = z_spread
                    obj.save()
                except Bonds.DoesNotExist:
                    continue
            #     .update(
            #     price=bond[2][1],
            #     duration=bond[7][1],
            #     effective_yield=effective_yield,
            #     g_spread=g_spread,
            #     z_spread=z_spread,
            # )

        print('starting volume')
        date_14_days_ago = datetime.date.today() - datetime.timedelta(days=14)



        objs = Bonds.objects.all()

        for item in objs:
            if item.g_spread:
                isin = item.isin
                response = requests.get(
                    'https://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/TQCB/securities/'
                    f'{isin}.json?iss.meta=off&from={date_14_days_ago}')
                history = response.json()['history']

                history_data = []
                for data in history['data']:
                    print(data[14])
                    if data[14]:
                        history_data.append(data[14])
                    else:
                        continue
                if history_data:
                    avg_volume = int((sum(history_data) / len(history_data)) * 1000)
                    print(f'writing volume for {isin}')
                    item.volume = avg_volume
                    item.save()


