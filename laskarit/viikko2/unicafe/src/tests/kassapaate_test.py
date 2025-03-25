import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_kassa_luotu_oikein(self):
        self.assertEqual(
            (self.kassapaate.kassassa_rahaa, self.kassapaate.edulliset + self.kassapaate.maukkaat), (100000, 0))

    def test_edullinen_kateinen_riittava_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(250), 10)

    def test_edullinen_kateinen_riittava_kassa_oikein(self):
        self.kassapaate.syo_edullisesti_kateisella(250)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_maukas_kateinen_riittava_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(410), 10)

    def test_maukas_kateinen_riittava_kassa_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(410)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_edullinen_kateinen_riittava_lounaat_oikein(self):
        self.kassapaate.syo_edullisesti_kateisella(250)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_kateinen_riittava_lounaat_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(410)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edullinen_kateinen_ei_riittava_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(230), 230)

    def test_edullinen_kateinen_ei_riittava_kassa_oikein(self):
        self.kassapaate.syo_edullisesti_kateisella(230)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukas_kateinen_ei_riittava_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(390), 390)

    def test_maukas_kateinen_ei_riittava_kassa_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(390)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullinen_kateinen_ei_riittava_lounaat_oikein(self):
        self.kassapaate.syo_edullisesti_kateisella(230)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukas_kateinen_riittava_lounaat_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(390)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_edullinen_kortti_riittava_true(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(
            self.maksukortti), True)

    def test_edullinen_kortti_riittava_kassa_oikein(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukas_kortti_riittava_true(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(
            self.maksukortti), True)

    def test_maukas_kortti_riittava_kassa_oikein(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullinen_kortti_riittava_lounaat_oikein(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_kortti_riittava_lounaat_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat(), 1)

    def test_edullinen_kortti_ei_riittava_false(self):
        self.maksukortti = Maksukortti(10)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(
            self.maksukortti), False)

    def test_edullinen_kortti_ei_riittava_kortti_oikein(self):
        self.maksukortti = Maksukortti(10)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 0.1)

    def test_maukas_kortti_ei_riittava_false(self):
        self.maksukortti = Maksukortti(10)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(
            self.maksukortti), False)

    def test_maukas_kortti_ei_riittava_kortti_oikein(self):
        self.maksukortti = Maksukortti(10)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 0.1)

    def test_edullinen_kortti_ei_riittava_lounaat_oikein(self):
        self.maksukortti = Maksukortti(10)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maukas_kortti_riittava_lounaat_oikein(self):
        self.maksukortti = Maksukortti(10)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_lataa_rahaa_kassasta_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual((self.maksukortti.saldo_euroina(),
                         self.kassapaate.kassassa_rahaa), (11.0, 100100))

    def test_lataa_rahaa_kassasta_kortille_summa_neg(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1)
        self.assertEqual((self.maksukortti.saldo_euroina(),
                         self.kassapaate.kassassa_rahaa), (10.0, 100000))

    def test_kassa_rahat_nakyy_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
