import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen

from isleyici import kategori_bul, sehir_bul
from veritabani import haber_kaydet, tablo_olustur

# Haberlerin çekileceği RSS kaynakları
KAYNAKLAR = {
    "NTV": "https://www.ntv.com.tr/gundem.rss",
    "Hürriyet": "https://www.hurriyet.com.tr/rss/anasayfa",
    "CNN Türk": "https://www.cnnturk.com/feed/rss/all/news",
    "TRT Haber": "https://www.trthaber.com/manset_articles.rss",
}


ATOM = "{http://www.w3.org/2005/Atom}"


# Kaynaklardan gelen farklı tarih biçimlerini tek biçime çevirir
def tarih_duzenle(metin):
    try:
        tarih = parsedate_to_datetime(metin)
    except ValueError:
        try:
            tarih = datetime.fromisoformat(metin)
        except ValueError:
            return ""
    return tarih.strftime("%Y-%m-%d %H:%M")


def haber_olustur(kaynak, baslik, link, tarih):
    return {
        "baslik": baslik,
        "link": link,
        "kaynak": kaynak,
        "tarih": tarih_duzenle(tarih),
        "kategori": kategori_bul(baslik),
        "sehir": sehir_bul(baslik),
    }


def rss_oku(kaynak, adres):
    istek = Request(adres, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(istek, timeout=15) as cevap:
        kok = ET.fromstring(cevap.read())

    haberler = []
    # Çoğu kaynak RSS biçiminde
    for item in kok.iter("item"):
        baslik = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        if baslik and link:
            haberler.append(haber_olustur(kaynak, baslik, link, item.findtext("pubDate", "").strip()))

    # NTV gibi bazı kaynaklar Atom biçiminde
    for entry in kok.iter(ATOM + "entry"):
        baslik = entry.findtext(ATOM + "title", "").strip()
        link = entry.find(ATOM + "link")
        if baslik and link is not None:
            haberler.append(haber_olustur(kaynak, baslik, link.get("href"), entry.findtext(ATOM + "published", "").strip()))
    return haberler


def haberleri_topla():
    tablo_olustur()
    for kaynak, adres in KAYNAKLAR.items():
        try:
            haberler = rss_oku(kaynak, adres)
        except Exception as hata:
            print(kaynak, "okunamadı:", hata)
            continue
        yeni = sum(haber_kaydet(haber) for haber in haberler)
        print(f"{kaynak}: {len(haberler)} haber, {yeni} yeni")


if __name__ == "__main__":
    haberleri_topla()
