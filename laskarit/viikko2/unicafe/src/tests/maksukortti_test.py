import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_luotu_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_rahaa_lisatty_oikein(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 20.0)

    def test_raha_vahenee_kun_tarpeeksi_rahaa(self):
        self.maksukortti.ota_rahaa(100)
        self.assertNotEqual(self.maksukortti.saldo_euroina, 9.0)

    def test_raha_ei_vahene_kun_ei_tarpeeksi_rahaa(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertNotEqual(self.maksukortti.saldo_euroina, 10.0)

    def test_true_kun_tarpeeksi_rahaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(100), True)

    def test_false_kun_ei_tarpeeksi_rahaa(self):
        self.assertEqual(self.maksukortti.ota_rahaa(10000), False)

    def test_print_toimii_oikein(self):
        self.assertEqual(str(self.maksukortti),
                         "Kortilla on rahaa 10.00 euroa")
