import os
import sqlite3

DB_YOLU = os.path.join(os.path.dirname(__file__), "haberler.db")


def baglan():
    return sqlite3.connect(DB_YOLU)


def tablo_olustur():
    with baglan() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS haberler (
                id INTEGER PRIMARY KEY,
                baslik TEXT NOT NULL,
                link TEXT UNIQUE,
                kaynak TEXT,
                tarih TEXT,
                kategori TEXT,
                sehir TEXT
            )
        """)


# Aynı linke sahip haber varsa eklenmez, eklenirse True döner
def haber_kaydet(haber):
    with baglan() as db:
        sonuc = db.execute(
            """INSERT OR IGNORE INTO haberler (baslik, link, kaynak, tarih, kategori, sehir)
               VALUES (:baslik, :link, :kaynak, :tarih, :kategori, :sehir)""",
            haber,
        )
        return sonuc.rowcount == 1
