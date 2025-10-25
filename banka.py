import pyodbc


def veritabanina_baglan(): # Database  e baglanmaya yarayan fonksiyondur
    try:
        baglan = pyodbc.connect(# MSSQL Database baglantısı geriye baglantı nesnesini döndürür hata var ise geriye bir şey döndürmez ve hata mesajı verir
    #        "Driver={SQL Server};"
     #       "Server=
     #       "Database=Bankadb;"
    #   "Trusted_Connection=True;"
        )
        return baglan
    except Exception as e:
        print("Bağlantı hatası:", e)
        return None




def kayit_ol(baglan):  # Bankaya kayıt olmaya yarayan fonksiyondur Baglantı nesnesini parametre olarak alır
    cursor = baglan.cursor() #ilk olarak veritabanında işlem yapmak için  cursor oluşturur
    try:
        print("\n--- Kayıt Ol ---")  #Kullanıcıdan  Kayıt olması için Kullanıcı adı ve şifre ister
        kullanici_adi = input("Kullanıcı Adı:").strip()
        sifre = input("Şifre: ").strip()

        if(sifre.strip()=="" or kullanici_adi==""):
            print("sifre veya kullanıcı adı boş olamaz")
            return
        cursor.execute("SELECT id FROM musteriler WHERE kullanici_ad=?", (kullanici_adi,)) #Girilen kullanıcı adını alarak veritabanındaki musteriler tablosuyla karşılaştırır
        if cursor.fetchone():                                                              #eğer  musteriler tablosunda kayıtlı kullanıcı varsa yakalar ve mesaj göndererek false döndürür
            print("Bankamıza kayıtlı kullanıcı vardır")
            return False
        cursor.execute( #kullanıcı kayıtlı değilse INSERT INTO ile kullanıcı adı,şifre ve otomatik olarak bakiyeyi 0 olarak tabloya ekler ve return olarak  true döner
            "INSERT INTO musteriler (kullanici_ad, sifre, bakiye) VALUES (?, ?, ?)",
            (kullanici_adi, sifre, 0.0)
        )
        baglan.commit()# Insert işlemini yaptırır
        print("Başarıyla kayıt olunmuştur. Giriş yapabilirsiniz.")
        return True
    except ValueError as e:  # Değer hataları
        print(f"Değer hatası: {e}")
        return False
    except IndexError as e:  # Liste indeks hataları
        print(f"İndeks hatası: {e}")
        return False
    except ConnectionError as e:  # Bağlantı hataları
        print(f"Bağlantı hatası: {e}")
        return False
    except Exception as e:  # Diğer hatalar
        print(f"Beklenmeyen bir hata oluştu: {e}")
        return False









def giris_yap(baglan):#Bankaya giriş yapmaya yarayan fonksiyondur paramete olarak baglantı nesnesini alır
    print("\n--- Giriş Yap ---")

    cursor = baglan.cursor()
    kullanici_adi = input("Kullanıcı adınızı giriniz: ").strip() #kullanıcıdan kullanıcı adını ve şifre ister strip ile sağ ve solda boşluk bıraktıysa siler
    sifre = input("Şifrenizi giriniz: ").strip()

    if (sifre.strip() == "" or kullanici_adi == ""):
        print("sifre veya kullanıcı adı boş olamaz")
        return

    try:
        cursor.execute(
            "SELECT id, bakiye FROM musteriler WHERE kullanici_ad=? AND sifre=?",
            (kullanici_adi, sifre)
        )
        kullanici = cursor.fetchone() #kullanıcının bankaya kayıtlı olup olmadığı bakılır ve kayıtlıysa kullanıcı varsa bilgileri alınır.
        if kullanici:  #kullanıcı varsa if e girer ve kullanıcı adı ile mesaj verilir ve return ile kullanıcı bilgilerini döndürür
            print(f"İnal Bankasına Hoş geldin {kullanici_adi}.")
            return kullanici
        else: #kullanıcın kaydı yoksa mesaj gönderir ve geriye hiçbir şey döndürmez
            print("Yanlış kullanıcı adı veya şifre.")
            return None
    except ValueError as e:  # Değer hatası
        print(f"Değer hatası: {e}")
        return None
    except IndexError as e:  # Liste indeks hataları
        print(f"İndeks hatası: {e}")
        return None
    except ConnectionError as e:  # Bağlantı hataları
        print(f"Bağlantı hatası: {e}")
        return None
    except Exception as e:  # Diğer tüm hatalar
        print(f"Giriş sırasında beklenmeyen bir hata oluştu: {e}")
        return None








def kayit_sil(baglan,kullanici_id): #kullanıcın kendi kaydını silmesini sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        sil = input("Hesabınızı silmek istediğinizden eminseniz (Evet) yazınız:") # ilk olarak kullanıcıdan onay ister ve kullanıcı evet yazarsa kaydı silinir

        if sil.strip().lower() == "evet": # kullanıcı evet yazarsa if e girer
            cursor.execute("DELETE FROM hesap_hareketleri where musteri_id=?", (kullanici_id,))#kullanıcının id'sine göre hesap hareketleri tablosundan DELETE FROM ile verileri silinir
            cursor.execute("DELETE FROM vadeli_hesaplar where musteri_id=?", (kullanici_id,))#kullanıcının id'sine göre hesap vadeli_hesaplar tablosundan DELETE FROM ile verileri silinir
            cursor.execute("DELETE FROM musteriler where id=?", (kullanici_id,))#kullanıcının id'sinegöre  hesap  musteriler tablosundan DELETE FROM ile verileri silinir
            baglan.commit()
            print("Hesabınız Başarıyla Silinmiştir...")#eğer işlem başarılı olduysa  mesaj gösterir işlem başarılı olmadığında tekrardan menüye  geri döner
        else:
            print("Menüye Geri dönülüyor...")
    except ValueError as e:  # Değer hataları
        print(f"Değer hatası: {e}")
    except IndexError as e:  # Liste indeks hataları
        print(f"İndeks hatası: {e}")
    except ConnectionError as e:  # Bağlantı hataları
        print(f"Bağlantı hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Kayit silinirken beklenmeyen bir hata oluştu: {e}")











def bakiye_goruntule(baglan, kullanici_id):#kullanıcının bakiyesini görmesini sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        cursor.execute("SELECT bakiye FROM musteriler WHERE id=?", (kullanici_id,)) # kullanıcı id'sine göre Select From ile  musteriler tablosundan bakiyesi alınır
        bakiye = cursor.fetchone()[0] #kullanıcın bakiyesini alır ve yazdırır
        print(f"Mevcut bakiyeniz: {bakiye} TL")
    except ValueError as e:  # Değer hataları
        print(f"Değer hatası: {e}")
    except IndexError as e:  # Liste indeks hataları
        print(f"İndeks hatası: {e}")
    except ConnectionError as e:  # Bağlantı hataları
        print(f"Bağlantı hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Bakiye görüntülerken beklenmeyen bir hata oluştu: {e}")









def para_yatir(baglan, kullanici_id):#kullanıcının hesaba para yatırtmasını sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        miktar = float(input("Yatırmak istediğiniz tutar: ").strip()) #kullanıcıya yatırmak istediği miktarı sorarak yatırmak istediği tutarı float olarak alır
        if miktar > 0 :#miktarı 0 dan büyük ise Update SET ile  kullanıcı id'sine göre bakiyesini günceller
            cursor.execute("UPDATE musteriler SET bakiye = bakiye + ? WHERE id=?", (miktar, kullanici_id))
            cursor.execute( #para yatırdıktan sonra hesap_hareketleri tablosuna INSERT INTO ile  kullanıcın İd'sine göre veri eklenir
                "INSERT INTO hesap_hareketleri (para_akisi, musteri_id) VALUES (?, ?)",
                (miktar, kullanici_id)
            )
            baglan.commit()
            print(f"{miktar} TL başarıyla yatırıldı.")#işlem başarıyla gerçekleştiyse para yatırdığı miktarı gösterek mesaj gösterilir
        else:
            print("Geçersiz tutar.")#eğer geçersiz miktar girdiyse mesaj olarak gösterili
    except ValueError as e:  # Kullanıcı geçersiz bir değer girdiğinde (örn. sayı olmayan bir değer)
        print(f"Geçersiz tutar: {e}")
    except IndexError as e:  # Liste indeks hataları
        print(f"İndeks hatası: {e}")
    except ConnectionError as e:  # Bağlantı hataları
        print(f"Bağlantı hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Para yatırılırken beklenmeyen bir hata oluştu: {e}")










def para_cek(baglan, kullanici_id):#kullanıcının hesaptan para çekmesini sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        miktar = float(input("Çekmek istediğiniz tutar: ").strip())#kullanıcıya çekmek istediği miktarı sorarak çekmek istediği tutarı float olarak alır
        cursor.execute("SELECT bakiye FROM musteriler WHERE id=?", (kullanici_id,))
        bakiye = cursor.fetchone()[0]#kullanıcın Bakiyesi id'sine göre alınır

        if 0 < miktar <= bakiye:#çekmek istediği tutar 0 dan büyük ve  bakiyeden eşit veya küçükkse if true döner
            cursor.execute("UPDATE musteriler SET bakiye = bakiye - ? WHERE id=?", (miktar, kullanici_id))#Update Set ile musteriler tablosundaki ıd'sine göre bakiyesini günceller
            cursor.execute(
                "INSERT INTO hesap_hareketleri (para_akisi, musteri_id) VALUES (?, ?)",
                (-miktar, kullanici_id) #para çektikten sonra hesap_hareketleri tablosuna INSERT INTO ile  kullanıcın İd'sine göre veri eklenir
            )
            baglan.commit()
            print(f"{miktar} TL başarıyla çekildi.")#işlem başarıyla gerçekleştiyse  para çektiği miktarı gösterek mesaj gösterilir
        else:
            print("Yetersiz bakiye veya geçersiz tutar.")#eğer geçersiz miktar girdiyse mesaj olarak gösterilir
    except ValueError as e:  # Geçersiz bir değer
        print(f"Geçersiz tutar: {e}")
    except IndexError as e:  # Liste indeks hatası (örn. bakiye değeri bulunamadığında)
        print(f"İndeks hatası: {e}")
    except ConnectionError as e:  # Bağlantı hatası
        print(f"Bağlantı hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Para çekilirken beklenmeyen bir hata oluştu: {e}")








def para_gonder(baglan, kullanici_id):#Bankaya kayıtlı kullanıcılara para göndermeye yarayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        hedef_kullanici_id = int(input("Göndermek istediğiniz kullanıcının ID'si: ").strip()) #ilk olarak göndermek istediğimiz kullanıcın id'si istenir ve int olarak input ile alınır
        miktar = float(input("Göndermek istediğiniz tutar: ").strip()) #kullanıcın göndermek istediği miktarı float olarak alınır

        cursor.execute("SELECT bakiye FROM musteriler WHERE id=?", (kullanici_id,)) #para göndermek isteyen kullanıcının id'sine göre bakiyesi alınır
        gonderici_bakiye = cursor.fetchone()[0]

        if 0 < miktar <= gonderici_bakiye: #göndermek istediğini bakiye 0 dan büyük ve bakiyesine eşit veya küçükse if true döner
            cursor.execute("SELECT id FROM musteriler WHERE id=?", (hedef_kullanici_id,))#para göndermek istenen kullanıcının bilgileri girilen id'ye göre çekilir
            if cursor.fetchone():#eğer bankada kayıtlı kullanıcı varsa if true döner
                cursor.execute("UPDATE musteriler SET bakiye = bakiye - ? WHERE id=?", (miktar, kullanici_id))#para gönderen kullanıcının bakiyesi UPDATE SET ile güncellenir
                cursor.execute("UPDATE musteriler SET bakiye = bakiye + ? WHERE id=?", (miktar, hedef_kullanici_id))#para alan kullanıcının bakiyesi UPDATE SET ile güncellenir
                cursor.execute( #para gönderen kullanıcının hesap_hareketleri tablosunda id'sine göre gönderdiği miktarı - olarak ekler
                    "INSERT INTO hesap_hareketleri (para_akisi, musteri_id) VALUES (?, ?)",
                    (-miktar, kullanici_id)
                )
                cursor.execute( #para alankullanıcının hesap_hareketleri tablosunda id'sine göre  gönderdiği miktarı + olarak ekler
                    "INSERT INTO hesap_hareketleri (para_akisi, musteri_id) VALUES (?, ?)",
                    (miktar, hedef_kullanici_id)
                )
                baglan.commit() #commit ile veritabanı işlemleri gerçekleştirilir ve kullanıcının ne kadar para gönderdiği gösterilerek mesaj gösterilir
                print(f"{miktar} TL başarıyla gönderildi.")
            else:
                print("Kullanıcı bulunamadı.") #kullanıcı göndermek istediği diğer banka müşterisinin id'sini girdiği zaman  kullanıcı bulunmaz ise  mesaj gösterilir
        else:
            print("Yetersiz bakiye veya geçersiz tutar.") #kullanıcın göndermek istediği tutar geçersiz bir tutar ise  mesaj gösterilir
    except ValueError as e:  # Geçersiz bir değer
        print(f"Geçersiz tutar: {e}")
    except IndexError as e:  # Liste indeks hatası
        print(f"İndeks hatası: {e}")
    except ConnectionError as e:  # Bağlantı hatası
        print(f"Bağlantı hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Para çekilirken beklenmeyen bir hata oluştu: {e}")








def hesap_hareketlerini_goruntule(baglan, kullanici_id):#Bankaya kayıtlı kullanıcıların hesap hareketlerini görmesini
    cursor = baglan.cursor()                            # yarayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    try:
        cursor.execute("SELECT para_akisi, tarih FROM hesap_hareketleri WHERE musteri_id=?", (kullanici_id,))
        hareketler = cursor.fetchall()#kullanıcın id'sine göre SELECT FROM ile hesap_hareketleri tablosundan hesabındaki hareketleri ve gerçekleşen tarihi çeker
        if hareketler: #eğer true döner ise for döngüsüyle  tarihi ve hareket tutarı yazdırılarak kullanıcıya bilgi verir
            print("\n--- Hesap Hareketleri ---")
            for hareket in hareketler:
                print(f"Tarih: {hareket[1]}, Tutar: {hareket[0]} TL")
        else:#kullanıcın hesabında para girişi veya çıkışı olmadığı zaman mesaj gösterilir
            print("Hesap hareketi bulunamadı.")
    except IndexError as e:
        print(f"Veri hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Hesap hareketleri görüntülenirken hata oluştu: {e}")









def faiz_hesapla(baglan, kullanici_id):#kullanıcın faiz hesaplamasını sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        cursor.execute("SELECT bakiye FROM musteriler WHERE id=?", (kullanici_id) )#kullanıcın kullanıcı id'sine göre  bakiyesi alınır
        bakiye = float(cursor.fetchone()[0]) #bakiyesi veritabanında decimal olarak kayıtlı olduğu için * işlemininde hata çıkmaması için float türüne çevrilir

        faiz_orani =0.10  # %10 yıllık faiz oranı
        vade_suresi = int(input("Faiz hesaplamak istediğiniz vade süresini (ay olarak) giriniz: ").strip())#kullanıcıdan ay olarak  vade süresi istenir ve int türüne çevrilir
        if vade_suresi <= 0: #vade süresi 0 eşit veya 0 dan küçükse hata mesajı gönderir ve gerriye bir şey döndürmez
            print("Geçerli bir vade süresi giriniz.")
            return None

        faiz_geliri = (bakiye * faiz_orani * vade_suresi) / 12 #yıllık faiz oranı bakiye ve vade süresi hesaplanır
        toplam_bakiye = bakiye + faiz_geliri  #hesaplanan faiz geliri bakiyeye eklenir

        print(f"\nMevcut Bakiyeniz: {bakiye:.2f} TL") #kullanıcın kendi bakiyesi gösterilir
        print(f"{vade_suresi} aylık faiz geliri: {faiz_geliri:.2f} TL") #faiz geliri gösterilir
        print(f"Vade sonunda toplam bakiye: {toplam_bakiye:.2f} TL") #vade sonunda toplam bakiyesi gösterilir
    except ValueError as e:  # Kullanıcıdan alınan veri hatası
        print(f"Giriş hatası: {e}. Lütfen geçerli bir sayı giriniz.")
    except Exception as e:  # Diğer hatalar
        print(f"Faiz hesaplama sırasında hata oluştu: {e}")









def vadeli_hesap_olustur(baglan, kullanici_id):#kullanıcın vadeli hesap oluşturmasını sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        miktar = float(input("Vadeli hesaba aktarmak istediğiniz tutar: ").strip())#vadeli hesaba aktarmak istediği miktarı sorarak girilmesi istenir ve folat türüne çevrilir
        vade_suresi = int(input("Vade süresini (ay olarak) giriniz: ").strip())#vade süresini ay olarak ister ve int türüne çevirir
        faiz_orani = 0.10#yıllık faiz oranu

        cursor.execute("SELECT bakiye FROM musteriler WHERE id=?", (kullanici_id,))#kullanıcının kullanıcı id'sine göre bakiyesi alınır
        mevcut_bakiye = cursor.fetchone()[0]

        if miktar > 0 and miktar <= mevcut_bakiye and vade_suresi > 0:#vadeli hesaba yatırmak istediği miktar 0 dan büyük  kendi bakiyesinden küçük veya eşit ve vade süresi
                                                                      #0 dan büyük ise if true döner
            cursor.execute("UPDATE musteriler SET bakiye = bakiye - ? WHERE id=?", (miktar, kullanici_id))#kullanıcın id'sine göre musteriler tablosundaki bakiyesi güncellenir
            cursor.execute(
                "INSERT INTO hesap_hareketleri (para_akisi, musteri_id) VALUES (?, ?)",# kullanıcı id'sine göre hesap_hareketleri tablosuna - olarak veriyi ekler
                (-miktar, kullanici_id)
            )
            cursor.execute(
                "INSERT INTO vadeli_hesaplar (musteri_id, bakiye, vade_suresi, faiz_orani) VALUES (?, ?, ?, ?)",## kullanıcı id'sine göre vadeli_hesaplar tablosuna veriyi ekler
                (kullanici_id, miktar, vade_suresi, faiz_orani)
            )
            baglan.commit()
            print(f"{miktar} TL vadeli hesaba aktarılmıştır. Vade süresi: {vade_suresi} ay.")# eğer işlem gerçekleştiyse miktarı ve vade süresini yazdırır
        else:
            print("Geçersiz tutar veya vade süresi.")#eğer kullanıcı yatırmak istediği tutarı veya vade süresini yanlış veya geçersiz girerse hata mesajı gösterir
    except ValueError as e:  # Kullanıcıdan alınan veri hatası
        print(f"Giriş hatası: {e}. Lütfen geçerli bir sayı giriniz.")
    except Exception as e:  # Diğer hatalar
        print(f"Vadeli hesap oluştururken hata oluştu: {e}")









def vadeli_hesaplari_goruntule(baglan, kullanici_id):#kullanıcın vadeli hesapları görmesini sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        cursor.execute(
            "SELECT id, bakiye, vade_suresi, faiz_orani, olusturma_tarihi FROM vadeli_hesaplar WHERE musteri_id=?",
            (kullanici_id,)
        )
        vadeli_hesaplar = cursor.fetchall()  # Kullanıcının id'sine göre vadeli_hesaplar tablosundan verileri çekilir
        if vadeli_hesaplar:  # Eğer veri varsa true döner
            print("\n--- Vadeli Hesaplar ---")
            for hesap in vadeli_hesaplar:  # Vadeli hesaplar listesinde gezinilir
                print(
                    f"Hesap ID: {hesap[0]}, Tutar: {hesap[1]:.2f} TL, Vade Süresi: {hesap[2]} ay, Faiz Oranı: {hesap[3] * 100:.1f}%, Oluşturma Tarihi: {hesap[4]}")
        else:
            print("Henüz vadeli hesabınız yok.")  # Vadeli hesap yoksa kullanıcıya mesaj gösterilir
    except Exception as e:
        print("Vadeli hesabı görüntülerken hata oluştu...")








def vadeli_hesaptan_para_cek(baglan, kullanici_id):#kullanıcının vadeli hesaptan para çekmesini sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:

        vadeli_hesap = int(input("Vadeli hesabın ID'sini giriniz: ").strip())#kullanıcıdan vadeli hesabın id'si istenir ve int türne dönüştürülür


        cursor.execute(
            "SELECT bakiye FROM vadeli_hesaplar WHERE id=? AND musteri_id=?",
            (vadeli_hesap, kullanici_id)
        )
        vadeli_hesap_bilgi = cursor.fetchone()#kullanıcının id'sine ve vadeli hesabın id'sine göre vadeli_hesaplar tablosundan vadeli hesabın bilgileri alınır

        if vadeli_hesap_bilgi:  # Vadeli hesap var ise true döner
            vadeli_hesap_bakiye = vadeli_hesap_bilgi[0] # vadeli hesabın bakiyesi alınır


            miktar = float(input("Vadeli hesaptan çekmek istediğiniz tutar: ").strip())#kullanıcıdan vadeli hesaptan ne kadar çekileceği istenir ve float türüne dönüştürülür

            if miktar > 0 and miktar <= vadeli_hesap_bakiye:# çekilecek tutar 0 dan büyük ve vadeli hesabın bakiyesinden küçük veya eşit ise true döner

                cursor.execute(
                    "UPDATE vadeli_hesaplar SET bakiye = bakiye - ? WHERE id=? AND musteri_id=?",
                    (miktar, vadeli_hesap, kullanici_id)
                ) #vadeli hesabın vadeli_hesaplar tablosundan bakiyesi güncellenir
                cursor.execute("UPDATE musteriler SET bakiye = bakiye + ? WHERE id=?", (miktar, kullanici_id))#kullanıcının musteriler tablosundan bakiyesi güncellenir
                cursor.execute(
                    "INSERT INTO hesap_hareketleri (para_akisi, musteri_id) VALUES (?, ?)",
                    (miktar, kullanici_id) #kullanıcının id sine göre hesap_hareketleri tablosuna  veri eklenir
                )
                baglan.commit()
                print(f"{miktar:.2f} TL başarıyla vadeli hesaptan çekildi.")#para çekme işlemi tamamlandıysa kullanıcıya ne kadar çektiği mesajı verilir
            else:
                print("Yetersiz bakiye veya geçersiz tutar.")  # eğer geçersiz miktar girdiyse mesaj olarak gösterilir
        else:
            print("Vadeli hesap bulunamadı...")#eğer vadeli hesap bulunamazsa mesaj olarak gösterilir
    except ValueError as e:  # Kullanıcıdan alınan veri hatası
        print(f"Geçersiz tutar: {e}")
    except IndexError as e:  # Liste indeks hataları
        print(f"İndeks hatası: {e}")
    except ConnectionError as e:  # Bağlantı hataları
        print(f"Bağlantı hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Para çekilirken beklenmeyen bir hata oluştu: {e}")








def vadeli_hesaba_para_yatir(baglan, kullanici_id):#kullanıcının vadeli hesaba para yatırmasını sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    cursor = baglan.cursor()
    try:
        vadeli_hesap = int(input("Vadeli hesabın ID'sini giriniz: ").strip())#kullanıcıdan vadeli hesabın id'si  istenir ve int türne dönüştürülür


        cursor.execute("SELECT bakiye FROM vadeli_hesaplar WHERE id=? AND musteri_id=?", (vadeli_hesap, kullanici_id))
        vadeli_hesap_bilgi = cursor.fetchone()#kullanıcının id'sine ve vadeli hesabın id'sine göre vadeli_hesaplar tablosundan vadeli hesabın bilgileri alınır

        if vadeli_hesap_bilgi:# Vadeli hesap var ise true döner
            miktar = float(input("Vadeli hesaba yatırmak istediğiniz tutar: ").strip())#kullanıcıdan vadeli hesaba ne kadar para yatırılıcağı istenir ve float türüne dönüştürülür


            cursor.execute("SELECT bakiye FROM musteriler WHERE id=?", (kullanici_id,))
            mevcut_bakiye = cursor.fetchone()# kullanıcının musteriler tablosundan id'sine göre   bakiyesi alınır

            if mevcut_bakiye[0] > miktar and miktar > 0:#yatırılıcak tutar kullanıcının bakiysinden büyük ve miktar 0 dan büyükse true döner

                cursor.execute("UPDATE musteriler SET bakiye = bakiye - ? WHERE id=?", (miktar, kullanici_id))#kullanıcın id'sine göre musteriler tablosundan bakiyesi güncellenir
                cursor.execute("INSERT INTO hesap_hareketleri (para_akisi, musteri_id) VALUES (?, ?)", (-miktar, kullanici_id))#kullanıcın id'sine göre hesap_hareketleri tablosuna veri eklenir
                cursor.execute("UPDATE vadeli_hesaplar SET bakiye = bakiye + ? WHERE id=? AND musteri_id=?",#vadeli hesabın vadeli_hesaplar tablosundan bakiyesi güncellenir
                               (miktar, vadeli_hesap, kullanici_id))
                baglan.commit()

                print(f"{miktar:.2f} TL başarıyla vadeli hesaba yatırıldı.")
            else:
                print("Yetersiz bakiye veya geçersiz tutar.")
        else:
            print("Vadeli hesap bulunamadı...")
    except ValueError as e:  # Kullanıcıdan alınan veri hatası
        print(f"Geçersiz tutar: {e}")
    except IndexError as e:  # Liste indeks hataları
        print(f"İndeks hatası: {e}")
    except ConnectionError as e:  # Bağlantı hataları
        print(f"Bağlantı hatası: {e}")
    except Exception as e:  # Diğer tüm hatalar
        print(f"Para yatırılırken beklenmeyen bir hata oluştu: {e}")










def menu(baglan, kullanici_id):#Kullanıcı giriş yaptıktan sonra menü açılmasını sağlayan fonksiyondur parametre olarak bağlantı nesnesi ve kullanıcı id'sini alır.
    while True: #while true dönerek kullanıcıya işlem yaptırmak için menü gösterilir
        print("\n--- Ana Menü ---")
        print("1. Bakiye Görüntüle")
        print("2. Para Yatır")
        print("3. Para Çek")
        print("4. Başka Hesaba Para Gönder")
        print("5. Hesap Hareketleri")
        print("6. Faiz Hesapla")
        print("7. Vadeli  Hesap Oluştur")
        print("8. Vadeli  Hesabları Görüntüle")
        print("9. Vadeli  Hesatan Para Yatır ")
        print("10. Vadeli  Hesaba Para Çek ")
        print("11. Kayit Sil")
        print("12. Çıkış")
        secim = input("Seçiminiz: ").strip() #kullanıcının seçtiği işlem alınır
        if secim == "1": #kullanıcı 1  seçerse bakiye_goruntule fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            bakiye_goruntule(baglan, kullanici_id)
        elif secim == "2": #kullanıcı 2  seçerse para_yatır fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            para_yatir(baglan, kullanici_id)
        elif secim == "3": #kullanıcı 3  seçerse para_cek fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            para_cek(baglan, kullanici_id)
        elif secim == "4": #kullanıcı 4 seçerse para_gönder fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            para_gonder(baglan, kullanici_id)
        elif secim == "5":  #kullanıcı 5 seçerse hesap_hareketleri_goruntule fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            hesap_hareketlerini_goruntule(baglan, kullanici_id)
        elif secim == "6":  #kullanıcı 6 seçerse faiz_heapla fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            faiz_hesapla(baglan,kullanici_id)
        elif secim == "7": #kullanıcı 7 seçerse vadeli_hesap_oluştur fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            vadeli_hesap_olustur(baglan,kullanici_id)
        elif secim == "8": #kullanıcı 8 seçerse vadeli_hesaplari_goruntule fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            vadeli_hesaplari_goruntule(baglan,kullanici_id)
        elif secim=="9":#kullanıcı 9 seçerse vadeli_hesaba_para_yatir fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            vadeli_hesaba_para_yatir(baglan,kullanici_id)
        elif secim=="10":#kullanıcı 10 seçerse vadeli_hesaptan_para_cek fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır
            vadeli_hesaptan_para_cek(baglan, kullanici_id)
        elif secim == "11":#kullanıcı 11 seçerse kayit_sil fonksiyonuna bağlantı nesnesini ve kullanıcı id'yi vererek çağırır  ve break ile döngüden çıkar
            kayit_sil(baglan, kullanici_id)
            break
        elif secim == "12":#kullanıcı 12 seçerse  hesaptan çıkıldığına dair mesaj yazdırılıp  ve break ile döngüden çıkar
            print("Çıkış yapılıyor...")
            break
        else: #kullanıcı menüde olmayan işlemi seçerse hata mesajı verir
            print("Yanlış seçim yaptınız lütfen tekrar secim yapınız...")






def ana():#Ana programdır
    baglan = veritabanina_baglan() #veritabanına_baglan fonksiyonunu çağırarak bağlan nesnesine atar
    if baglan: #bağlantı oluştuysa if true döner
        while True: #while true dönerek kullanıcıya işlem yaptırmak için menü gösterilir
            print("\nİnal Bankasına Hoş Geldiniz")
            print("1. Giriş Yap")
            print("2. Kayıt Ol")
            print("3. Çıkış")
            secim = input("Seçiminiz: ").strip()   #kullanıcının seçtiği işlem alınır

            if secim == "1": #kullanıcı 1 seçerse giriş_fonksiyonuna bağlantı  nesnesini parametre vererek çağırır
                kullanici = giris_yap(baglan)
                if kullanici: #kullanıcı bulunursa if true olur ve kullanıcı id'si alınır
                    kullanici_id = kullanici[0]#kullanıcıların giriş yaptıktan sonra menü karşısına gelmesi için menu fonksiyonuna parametre olarak
                    menu(baglan, kullanici_id)   # baglantı nesnesi ve kullanıcı id verilerek çağırılır
            elif secim == "2":  #kullanıcı 2 seçerse kayit_ol fonksiyonuna bağlantı  nesnesini parametre vererek çağırır
                kayit_ol(baglan)
            elif secim == "3": #kullanıcı 3 seçerse çıkış yapıldığına dair mesaj gösterilerek break ile döngüden çıkılıp program sonlanır
                print("Çıkış yapılıyor...")
                break
            else:#kullanıcı menüde olmayan işlemi seçerse hata mesajı verir
                print("Yanlış seçim yaptınız lütfen tekrar secim yapınız...")
        baglan.close()









if __name__ == "__main__": #dosya doğrudan çalıştırıldığında aşağıdaki ana() fonksiyonunu çağırmak için kullanılır.
    ana() # ana fonksiyonu çağırılır ve programın başlangıcıdır


