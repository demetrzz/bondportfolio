from django.core.management.base import BaseCommand
from ...models import *
import requests
import datetime

class Command(BaseCommand):
    def handle(self, **options):
        response = requests.get(
            'https://iss.moex.com/iss/engines/stock/markets/bonds/boards/TQCB/securities.json?iss.meta=off')
        securities = response.json()['securities']
        marketdata_yields = response.json()['marketdata_yields']

        securities_data = []

        for data in securities['data']:
            a = list(zip(securities['columns'], data))
            securities_data.append(a)

        for bond in securities_data:
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
            Bonds.objects.update_or_create(
                price=bond[2][1],
                duration=bond[7][1],
                effective_yield=round(bond[6][1],2),
                g_spread=bond[9][1],
                z_spread=bond[8][1],
            )


        # date_14_days_ago = datetime.date.today() - datetime.timedelta(days=14)
        #
        # response = requests.get('https://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/TQCB/securities/'
        #                         f'RU000A105ZX2.json?iss.meta=off&from={date_14_days_ago}')
        #
        # history = response.json()['history']
        #
        # history_data = []
        # for data in history['data']:
        #     history_data.append(data[14])
        # avg_volume = int((sum(history_data) / len(history_data)) * 1000)
        #
        # print(avg_volume)
        #
        # for item in Bonds.objects.all():
        #     isin = item.isin
        #     response = requests.get(
        #         'https://iss.moex.com/iss/history/engines/stock/markets/bonds/boards/TQCB/securities/'
        #         f'RU000A105ZX2.json?iss.meta=off&from={isin}')
        #     history = response.json()['history']
        #
        #     history_data = []
        #     for data in history['data']:
        #         history_data.append(data[14])
        #     avg_volume = int((sum(history_data) / len(history_data)) * 1000)
        #     item.volume = avg_volume
        #     item.save()


