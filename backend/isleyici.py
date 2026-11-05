import re

from sehirler import SEHIRLER

# Başlıkta geçen kelimelere göre haberin kategorisi belirlenecek
KATEGORILER = {
    "spor": ["maç", "gol", "lig", "takım", "teknik direktör", "transfer"],
    "ekonomi": ["dolar", "euro", "faiz", "enflasyon", "borsa", "altın fiyat"],
    "siyaset": ["meclis", "bakan", "seçim", "parti", "cumhurbaşkanı"],
    "asayiş": ["kazası", "kazada", "yangın", "gözaltı", "operasyon", "saldırı"],
    "doğa": ["deprem", "sel felaketi", "fırtına", "yağmur", "kar yağışı"],
    "sağlık": ["hastane", "doktor", "salgın", "aşı", "hastalık"],
    "teknoloji": ["yapay zeka", "telefon", "internet", "uygulama", "yazılım"],
}


# Python'ın lower() fonksiyonu Türkçe I ve İ harflerini yanlış çevirir
def kucult(metin):
    return metin.replace("I", "ı").replace("İ", "i").lower()


def kelime_var_mi(kelime, metin):
    return re.search(r"\b" + re.escape(kelime), metin) is not None


def kategori_bul(baslik):
    baslik = kucult(baslik)
    for kategori, kelimeler in KATEGORILER.items():
        for kelime in kelimeler:
            if kelime_var_mi(kelime, baslik):
                return kategori
    return "genel"


def sehir_bul(baslik):
    baslik = kucult(baslik)
    for sehir in SEHIRLER:
        if kelime_var_mi(sehir, baslik):
            return sehir
    return None
