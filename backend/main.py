import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from toplayici import haberleri_topla
from veritabani import baglan

FRONTEND = os.path.join(os.path.dirname(__file__), "..", "frontend")
ALANLAR = ["baslik", "link", "kaynak", "tarih", "kategori", "sehir"]


def haberleri_getir(filtre):
    sorgu = "SELECT baslik, link, kaynak, tarih, kategori, sehir FROM haberler WHERE 1=1"
    degerler = []
    if filtre.get("kategori"):
        sorgu += " AND kategori = ?"
        degerler.append(filtre["kategori"])
    if filtre.get("sehir"):
        sorgu += " AND sehir = ?"
        degerler.append(filtre["sehir"])
    if filtre.get("baslangic"):
        sorgu += " AND tarih >= ?"
        degerler.append(filtre["baslangic"])
    if filtre.get("bitis"):
        sorgu += " AND tarih <= ?"
        degerler.append(filtre["bitis"] + " 23:59")
    sorgu += " ORDER BY tarih DESC LIMIT 200"

    with baglan() as db:
        satirlar = db.execute(sorgu, degerler).fetchall()
    return [dict(zip(ALANLAR, satir)) for satir in satirlar]


class Sunucu(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND, **kwargs)

    def do_GET(self):
        adres = urlparse(self.path)
        if adres.path == "/api/haberler":
            filtre = {anahtar: deger[0] for anahtar, deger in parse_qs(adres.query).items()}
            self.json_gonder(haberleri_getir(filtre))
        else:
            super().do_GET()

    def json_gonder(self, veri):
        govde = json.dumps(veri, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(govde)))
        self.end_headers()
        self.wfile.write(govde)


if __name__ == "__main__":
    haberleri_topla()
    print("Sunucu çalışıyor: http://localhost:8000")
    ThreadingHTTPServer(("localhost", 8000), Sunucu).serve_forever()
