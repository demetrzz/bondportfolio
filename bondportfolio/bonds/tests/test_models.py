from django.test import TestCase

from bonds.models import Bonds


class BondsModelTest(TestCase):
    def setUp(self):
        Bonds.objects.create(name="Роделен1P3", yield_date="2027-11-19", isin="RU000A105M59", price=103.92,
                             duration=849, effective_yield=14.12, g_spread=4.68, z_spread=4.50, volume=711000)

    def test_fields_are_valid(self):
        bond = Bonds.objects.get(name="Роделен1P3")
        self.assertEqual(bond.name, "Роделен1P3")
