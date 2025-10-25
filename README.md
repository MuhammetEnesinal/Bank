# Bank
banking system simulator in Python


# Basit Konsol Bankacılık Sistemi

Bu proje, Python ve `pyodbc` kütüphanesi kullanılarak geliştirilmiş, Microsoft SQL Server (MSSQL) veritabanına bağlanan basit bir konsol tabanlı bankacılık uygulamasıdır.

Kullanıcılar sisteme kayıt olabilir, giriş yapabilir ve temel bankacılık işlemlerini (para yatırma, çekme, transfer, vadeli hesap işlemleri vb.) gerçekleştirebilir.

## Özellikler

* **Kullanıcı Yönetimi:**
    * Yeni kullanıcı kaydı oluşturma (`kayit_ol`)
    * Güvenli kullanıcı girişi (`giris_yap`)
    * Kullanıcı hesabını silme (`kayit_sil`)
* **Temel Bankacılık:**
    * Bakiye görüntüleme (`bakiye_goruntule`)
    * Hesaba para yatırma (`para_yatir`)
    * Hesaptan para çekme (bakiye kontrollü) (`para_cek`)
    * Kayıtlı başka bir kullanıcıya para gönderme (`para_gonder`)
* **Hesap Hareketleri:**
    * Tüm para giriş/çıkış işlemlerini tarihleriyle birlikte listeleme (`hesap_hareketlerini_goruntule`)
* **Vadeli Hesap İşlemleri:**
    * Mevcut bakiyeden vadeli hesap oluşturma (`vadeli_hesap_olustur`)
    * Tüm vadeli hesapları listeleme (`vadeli_hesaplari_goruntule`)
    * Mevcut vadeli hesaba para yatırma (`vadeli_hesaba_para_yatir`)
    * Vadeli hesaptan ana hesaba para çekme (`vadeli_hesaptan_para_cek`)
* **Finansal Araçlar:**
    * Anapara ve vade süresine göre basit faiz geliri hesaplama (`faiz_hesapla`)

## Gereksinimler

* Python 3.x
* Microsoft SQL Server
* `pyodbc` kütüphanesi

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### 1. Python Kütüphanesini Yükleyin


Gerekli olan `pyodbc` kütüphanesini yükleyin:

```bash
pip install pyodbc


### 1. Python Kütüphanesini Yükleyin

Microsoft SQL Server Management Studio (SSMS) veya benzeri bir araç kullanarak Bankadb adında (veya istediğiniz başka bir ad) bir veritabanı oluşturun. Ardından, bu veritabanında aşağıdaki SQL sorgularını çalıştırarak gerekli tabloları oluşturun:

/* Musteri bilgilerini ve ana bakiyeyi tutar */
CREATE TABLE musteriler (
    id INT PRIMARY KEY IDENTITY(1,1),
    kullanici_ad NVARCHAR(100) UNIQUE NOT NULL,
    sifre NVARCHAR(100) NOT NULL,
    bakiye DECIMAL(18, 2) NOT NULL DEFAULT 0.0
);

/* Para giriş/çıkışlarını log'lar (ana hesap) */
CREATE TABLE hesap_hareketleri (
    id INT PRIMARY KEY IDENTITY(1,1),
    musteri_id INT FOREIGN KEY REFERENCES musteriler(id) ON DELETE CASCADE,
    para_akisi DECIMAL(18, 2) NOT NULL,
    tarih DATETIME DEFAULT GETDATE()
);

/* Vadeli hesap bilgilerini tutar */
CREATE TABLE vadeli_hesaplar (
    id INT PRIMARY KEY IDENTITY(1,1),
    musteri_id INT FOREIGN KEY REFERENCES musteriler(id) ON DELETE CASCADE,
    bakiye DECIMAL(18, 2) NOT NULL,
    vade_suresi INT NOT NULL,
    faiz_orani DECIMAL(5, 2) NOT NULL,
    olusturma_tarihi DATETIME DEFAULT GETDATE()
);

3. Bağlantı Dizesini (Connection String) Güncelleyin
banka.py dosyasını açın ve veritabanina_baglan fonksiyonu içindeki yorum satırı olarak görünen pyodbc.connect bölümünü kendi SQL Server bilgilerinize göre düzenleyin ve yorum satırlarını kaldırın.

def veritabanina_baglan(): # Database  e baglanmaya yarayan fonksiyondur
    try:
        baglan = pyodbc.connect(
           "Driver={SQL Server};"
           "Server=SUNUCU_ADINIZ;"  # Örn: DESKTOP-ABC\SQLEXPRESS veya localhost
           "Database=Bankadb;"      # Oluşturduğunuz veritabanının adı
           "Trusted_Connection=True;" # Windows Authentication kullanıyorsanız


Markdown

# Basit Konsol Bankacılık Sistemi

Bu proje, Python ve `pyodbc` kütüphanesi kullanılarak geliştirilmiş, Microsoft SQL Server (MSSQL) veritabanına bağlanan basit bir konsol tabanlı bankacılık uygulamasıdır.

Kullanıcılar sisteme kayıt olabilir, giriş yapabilir ve temel bankacılık işlemlerini (para yatırma, çekme, transfer, vadeli hesap işlemleri vb.) gerçekleştirebilir.

## Özellikler

* **Kullanıcı Yönetimi:**
    * Yeni kullanıcı kaydı oluşturma (`kayit_ol`)
    * Güvenli kullanıcı girişi (`giris_yap`)
    * Kullanıcı hesabını silme (`kayit_sil`)
* **Temel Bankacılık:**
    * Bakiye görüntüleme (`bakiye_goruntule`)
    * Hesaba para yatırma (`para_yatir`)
    * Hesaptan para çekme (bakiye kontrollü) (`para_cek`)
    * Kayıtlı başka bir kullanıcıya para gönderme (`para_gonder`)
* **Hesap Hareketleri:**
    * Tüm para giriş/çıkış işlemlerini tarihleriyle birlikte listeleme (`hesap_hareketlerini_goruntule`)
* **Vadeli Hesap İşlemleri:**
    * Mevcut bakiyeden vadeli hesap oluşturma (`vadeli_hesap_olustur`)
    * Tüm vadeli hesapları listeleme (`vadeli_hesaplari_goruntule`)
    * Mevcut vadeli hesaba para yatırma (`vadeli_hesaba_para_yatir`)
    * Vadeli hesaptan ana hesaba para çekme (`vadeli_hesaptan_para_cek`)
* **Finansal Araçlar:**
    * Anapara ve vade süresine göre basit faiz geliri hesaplama (`faiz_hesapla`)

## Gereksinimler

* Python 3.x
* Microsoft SQL Server
* `pyodbc` kütüphanesi

## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### 1. Python Kütüphanesini Yükleyin

Gerekli olan `pyodbc` kütüphanesini yükleyin:

```bash
pip install pyodbc
2. Veritabanı ve Tabloları Oluşturun
Microsoft SQL Server Management Studio (SSMS) veya benzeri bir araç kullanarak Bankadb adında (veya istediğiniz başka bir ad) bir veritabanı oluşturun. Ardından, bu veritabanında aşağıdaki SQL sorgularını çalıştırarak gerekli tabloları oluşturun:

SQL

/* Musteri bilgilerini ve ana bakiyeyi tutar */
CREATE TABLE musteriler (
    id INT PRIMARY KEY IDENTITY(1,1),
    kullanici_ad NVARCHAR(100) UNIQUE NOT NULL,
    sifre NVARCHAR(100) NOT NULL,
    bakiye DECIMAL(18, 2) NOT NULL DEFAULT 0.0
);

/* Para giriş/çıkışlarını log'lar (ana hesap) */
CREATE TABLE hesap_hareketleri (
    id INT PRIMARY KEY IDENTITY(1,1),
    musteri_id INT FOREIGN KEY REFERENCES musteriler(id) ON DELETE CASCADE,
    para_akisi DECIMAL(18, 2) NOT NULL,
    tarih DATETIME DEFAULT GETDATE()
);

/* Vadeli hesap bilgilerini tutar */
CREATE TABLE vadeli_hesaplar (
    id INT PRIMARY KEY IDENTITY(1,1),
    musteri_id INT FOREIGN KEY REFERENCES musteriler(id) ON DELETE CASCADE,
    bakiye DECIMAL(18, 2) NOT NULL,
    vade_suresi INT NOT NULL,
    faiz_orani DECIMAL(5, 2) NOT NULL,
    olusturma_tarihi DATETIME DEFAULT GETDATE()
);
Not: ON DELETE CASCADE komutu, bir müşteri musteriler tablosundan silindiğinde, o müşteriye ait hesap_hareketleri ve vadeli_hesaplar kayıtlarının da otomatik olarak silinmesini sağlar. kayit_sil fonksiyonunuz bu şekilde daha stabil çalışacaktır.

3. Bağlantı Dizesini (Connection String) Güncelleyin
banka.py dosyasını açın ve veritabanina_baglan fonksiyonu içindeki yorum satırı olarak görünen pyodbc.connect bölümünü kendi SQL Server bilgilerinize göre düzenleyin ve yorum satırlarını kaldırın.

Örnek:

Python

def veritabanina_baglan(): # Database  e baglanmaya yarayan fonksiyondur
    try:
        baglan = pyodbc.connect(
           "Driver={SQL Server};"
           "Server=SUNUCU_ADINIZ;"  # Örn: DESKTOP-ABC\SQLEXPRESS veya localhost
           "Database=Bankadb;"      # Oluşturduğunuz veritabanının adı
           "Trusted_Connection=True;" # Windows Authentication kullanıyorsanız
           
           # Eger SQL Server Authentication (kullanıcı adı/şifre) kullanıyorsanız:
           # "UID=KULLANICI_ADINIZ;PWD=SIFRENIZ;"
        )
        return baglan
    except Exception as e:
        print("Bağlantı hatası:", e)
        return None


**Kullanım**
  Tüm kurulum adımları tamamlandıktan sonra, projeyi terminal üzerinden çalıştırabilirsiniz:
    python banka.py
