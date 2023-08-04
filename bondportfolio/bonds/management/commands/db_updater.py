from concurrent import futures

from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection

from ...models import *
import requests
import datetime


class Command(BaseCommand):
    def handle(self, **options):
        print("clearing db ...")
        Bonds.objects.all().delete()  # clear all database entries
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Bonds])  # resetting PK to 0
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        print("sending request")
        response = requests.get(
            'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off')

        securities = response.json()['securities']
        marketdata_yields = response.json()['marketdata_yields']

        print("filling in market data")
        marketdata_yields_data = []

        for data in marketdata_yields['data']:
            a = list(zip(marketdata_yields['columns'], data))  # filling in market data
            marketdata_yields_data.append(a)

        # here we check if data exists, if it doesn't or exceeds reasonable numbers then we don't add
        for bond in marketdata_yields_data:
            if bond[6][1] and bond[6][1] < 40:
                effective_yield = round(bond[6][1], 2)
            else:
                continue

            if bond[9][1] and (20 > bond[9][1] / 100 > -20):
                g_spread = round(bond[9][1] / 100, 2)
            else:
                continue

            if bond[8][1] and (20 > bond[8][1] / 100 > -20):
                z_spread = round(bond[8][1] / 100, 2)
            else:
                continue

            if bond[2][1] and bond[7][1] and bond[3][1]:
                pass
            else:
                continue

            if bond[0][1].startswith('RU'):
                pass
            else:
                continue

            Bonds.objects.update_or_create(
                isin=bond[0][1],
                price=bond[2][1],
                duration=bond[7][1],
                effective_yield=effective_yield,
                g_spread=g_spread,
                z_spread=z_spread,
                yield_date=bond[3][1]
            )

        print("filling in isin and name")
        securities_data = []
        for data in securities['data']:
            a = list(zip(securities['columns'], data))  # filling in isin and name fields
            securities_data.append(a)

        for bond in securities_data:
            try:
                obj = Bonds.objects.get(isin=bond[0][1])
                obj.name = bond[2][1]
                obj.save()
            except Bonds.DoesNotExist:
                continue

        print('filling in volume')
        # creating url list
        url_list = []
        date_14_days_ago = datetime.date.today() - datetime.timedelta(days=14)
        objs = Bonds.objects.all()
        for item in objs:
            isin = item.isin
            url_list.append('https://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/TQCB/securities/'
                            f'{isin}.json')

        def getdata(url):
            res = requests.get(url, params={'iss.meta': 'off','from': date_14_days_ago})
            return res.json()['history']

        with futures.ThreadPoolExecutor() as executor:  # concurrent requests
            res = executor.map(getdata, url_list)

        responses = list(res)

        for history in responses:
            isin = history['data'][0][3]
            print(f'trying to write {isin}')
            history_data = []
            for data in history['data']:
                if data[14]:
                    history_data.append(data[14])
                else:
                    continue
            if history_data:
                obj = Bonds.objects.get(isin=isin)
                avg_volume = int((sum(history_data) / len(history_data)) * 1000)
                print(f'writing volume for {isin}')
                obj.volume = avg_volume
                obj.save()

        print('done')
