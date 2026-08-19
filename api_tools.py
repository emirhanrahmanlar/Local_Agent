from fastmcp import FastMCP
import urllib.request
import json
import random
import os
import sqlite3
import string
import secrets
from datetime import datetime

mcp = FastMCP("Kale_API_Entegrasyonu")

@mcp.tool()
def get_users() -> str:
    """Veritabanindan tum kullanici listesini getirir."""
    url = "https://jsonplaceholder.typicode.com/users"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    return json.dumps(data, indent=2)

@mcp.tool()
def get_products() -> str:
    """Veritabanindan tum urunlerin listesini getirir."""
    url = "https://dummyjson.com/products"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    products = data.get("products", [])
    return json.dumps(products, indent=2)

@mcp.tool()
def get_user_by_id(kullanici_id: int) -> str:
    """Disaridan girilen ID numarasina gore spesifik bir kullanicinin detaylarini getirir."""
    url = f"https://jsonplaceholder.typicode.com/users/{kullanici_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        return json.dumps(data, indent=2)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"Hata: Sistemde {kullanici_id} numarali bir kullanici bulunamadi."
        return f"Bir hata olustu: HTTP {e.code}"


@mcp.tool()
def get_factory_status(bant_adi: str) -> str:
    """Belirtilen uretim bandinin anlik sicaklik, uretim adedi ve calisma durumunu getirir."""
    durumlar = ["Aktif - Sorunsuz", "Aktif - Dikkat!", "Bakimda", "Durdu - Hata"]
    
    secilen_durum = random.choice(durumlar)
    if "Aktif" in secilen_durum:
        sicaklik = random.randint(65, 95)
        uretim_adedi = random.randint(1000, 5000)
    else:
        sicaklik = random.randint(25, 40)
        uretim_adedi = random.randint(0, 500)
        
    zaman = datetime.now().strftime("%H:%M:%S")

    rapor = {
        "zaman": zaman,
        "bant_ismi": bant_adi,
        "anlik_durum": secilen_durum,
        "motor_sicakligi_C": sicaklik,
        "gunluk_uretim_adedi": uretim_adedi
    }
    return json.dumps(rapor, indent=2)


@mcp.tool()
def get_active_tickets(rol: str) -> str:
    """Sistemdeki acik IT destek biletlerini kullanici rolune (yonetici veya calisan) gore filtreleyip getirir."""
    
    tickets = [
        {"id": "T-101", "baslik": "Veritabani Baglanti Hatasi", "durum": "Kritik", "yetki_seviyesi": "yonetici"},
        {"id": "T-102", "baslik": "Yeni Personel Mail Acilisi", "durum": "Acik", "yetki_seviyesi": "calisan"},
        {"id": "T-103", "baslik": "Sunucu RAM Guncellemesi", "durum": "Planlandi", "yetki_seviyesi": "yonetici"},
        {"id": "T-104", "baslik": "Ofis Yazicisi Calismiyor", "durum": "Acik", "yetki_seviyesi": "calisan"}
    ]
    
    
    rol = rol.lower()
    if rol not in ["yonetici", "calisan"]:
        return "Hata: Gecersiz yetki rolu. Lutfen sadece 'yonetici' veya 'calisan' giriniz."
        
    filtrelenmis_tickets = [t for t in tickets if t["yetki_seviyesi"] == rol]
    
    sonuc = {
        "sorgulanan_portal": rol.capitalize(),
        "acik_kayit_sayisi": len(filtrelenmis_tickets),
        "kayitlar": filtrelenmis_tickets
    }
    
    return json.dumps(sonuc, indent=2)


@mcp.tool()
def read_local_file(dosya_adi: str) -> str:
    """Masaustunde bulunan metin tabanli yerel dosyalari okuyup yapay zekaya aktarir."""
    base_path = "/Users/emirhanrahmanlar/Desktop/"
    tam_yol = os.path.join(base_path, dosya_adi)
    
    if not os.path.exists(tam_yol):
        return f"Hata: Masaustunde '{dosya_adi}' adinda bir dosya bulunamadi."
        
    try:
        with open(tam_yol, 'r', encoding='utf-8') as file:
            icerik = file.read()
            return f"--- {dosya_adi} Icerigi ---\n\n{icerik}"
    except Exception as e:
        return f"Dosya okunurken bir hata olustu: {str(e)}"



def init_dummy_db():
    """Sistemin calismasi icin sahte bir SQLite veritabani ve tablo olusturur."""
    db_path = "sirket_veritabani.db"
    
    # Sadece dosya yoksa verileri ekleyelim ki her calistiginda veriler katlanmasin
    is_new = not os.path.exists(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabloyu yarat
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personeller (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT,
            departman TEXT,
            rol TEXT,
            cihaz_durumu TEXT
        )
    ''')
    
    if is_new:
        ornek_veriler = [
            ("A, B", "IT", "Sistem Yoneticisi", "Aktif"),
            ("C, D", "IT", "Yazilim Gelistirici", "Aktif"),
            ("E, F", "IT", "Yazılım Geliştirici", "Çevrimdışı"),
            ("Emirhan Rahmanlar", "IT", "Stajyer", "Aktif")
        ]
        cursor.executemany("INSERT INTO personeller (isim, departman, rol, cihaz_durumu) VALUES (?, ?, ?, ?)", ornek_veriler)
        conn.commit()
        
    conn.close()

# Python dosyasi calistiginda once bu veritabanini hazirlasin
init_dummy_db()


@mcp.tool()
def get_department_personnel(departman_adi: str) -> str:
    """Sirket SQL veritabanina baglanarak belirtilen departmandaki personelleri getirir."""
    conn = sqlite3.connect("sirket_veritabani.db")
    # Sonuclari düz liste degil, anahtar-deger (dictionary) seklinde almak icin ayar
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Güvenli (Parametrik) SQL Sorgusu
    cursor.execute("SELECT * FROM personeller WHERE departman = ?", (departman_adi,))
    satirlar = cursor.fetchall()
    conn.close()
    
    if not satirlar:
        return f"Hata: Veritabaninda '{departman_adi}' departmanina ait kayit bulunamadi."
        
    sonuclar = [dict(satir) for satir in satirlar]
    return json.dumps(sonuclar, indent=2)


@mcp.tool()
def generate_secure_token(uzunluk: int = 16, karmasiklik: str = "yuksek") -> str:
    """
    Kriptografik olarak guvenli rastgele sifre veya API token uretir. 
    Karmasiklik secenekleri: 'dusuk', 'orta', 'yuksek'
    """
    
    # Guvenlik standartlari geregi minimum uzunluk kontrolu
    if uzunluk < 8:
        return "Hata: Kurumsal guvenlik politikalari geregi token uzunlugu en az 8 karakter olmalidir."
    
    karmasiklik = karmasiklik.lower()
    
    # Seviyeye gore kullanilacak karakter havuzunu belirliyoruz
    if karmasiklik == "dusuk":
        karakterler = string.ascii_lowercase + string.digits # Sadece kucuk harf ve sayi
    elif karmasiklik == "orta":
        karakterler = string.ascii_letters + string.digits # Buyuk/Kucuk harf ve sayi
    else:
        # Yuksek: Harf, sayi ve ozel karakterler (!,@,#,$,% vb.)
        karakterler = string.ascii_letters + string.digits + string.punctuation
        
    # 'secrets' modulu ile kriptografik olarak kirilmasi cok zor bir token uretiyoruz
    uretilen_token = ''.join(secrets.choice(karakterler) for _ in range(uzunluk))
    
    sonuc = {
        "islem_durumu": "Basarili",
        "uretilen_token": uretilen_token,
        "parametreler": {
            "uzunluk": uzunluk,
            "karmasiklik_seviyesi": karmasiklik
        },
        "guvenlik_notu": "Kriptografik 'secrets' modulu kullanilarak uretilmistir."
    }
    
    return json.dumps(sonuc, indent=2)



if __name__ == "__main__":
    mcp.run()