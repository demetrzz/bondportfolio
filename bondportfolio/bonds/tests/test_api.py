from django.test import TestCase
from django.urls import reverse

from bonds.models import Bonds


class BondsAPITest(TestCase):
    def setUp(self):
        Bonds.objects.create(name="Роделен1P3", yield_date="2027-11-19", isin="RU000A105M59", price=103.92,
                             duration=849, effective_yield=14.12, g_spread=4.68, z_spread=4.50, volume=711000)
        self.create_read_url = reverse('bonds_rest_api', kwargs={'isin': 'RU000A105M59'})

    def test_list(self):
        response = self.client.get(self.create_read_url)
        self.assertContains(response, 'RU000A105M59')
