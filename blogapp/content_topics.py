"issue dalların konusu anlatacağı konu ör:mühendislik -> yazılım -> python"
"title konunun başlığı ör:django ile veri tabanı ayarı"
"content belirlenen özelliklerin içerik kısmı"
"tag içeriği tarif eden kelimeler ör:python-django veri tabanı ayarı,veri tabanı,python-django,yazılım"

class Fields:
    "field mesleki alanlar ör:mühendislik,sağlık"
    faculties = (
        # fakülteler
        ("EN", 'Mühendislik'),
        ("ME","Tıp"),
        ("SL","Fen-edebiyat"),
        ("EAAS","İktisadi ve idari bilimleri"),
        ("ED","Eğitim"),
        ("DE","Diş hekimliği"),
        ("ARC","Mimarlık"),
        ("IEAAS","İslahiye iktisadi ve idari bilimleri"),
        ("FI","Güzel sanatlar"),
        ("HE","Sağlık bilimleri"),
        ("LA","Hukuk"),
        ("TH","İlahiyat"),
        ("CO","İletişim"),
        ("AE","Havacılık ve uzay mühendisliği"),
        ("TO","Turizm")
    )
    yüksekokul = (
        # yüksekokular
        ("TMC","Türk musıkisi devlet konservatuarı"),
        ("PES","Beden eğitimi ve spor"),
        ("FL","Yabancı diller"),
        ("CA","Sivil havacılık")
    )
    meslek_yüksekokul = (
        # meslek yüksek okullar
        ("TS","Teknik bilimler"),
        ("LA","Sosyal bilimler"),
        ("HC","Sağlık hizmetleri"),
        ("THM","Turizm ve Otelcilik"),
        ("IS","Islahiye")
    )
    fields = faculties+yüksekokul+meslek_yüksekokul


class Branches:
    "branches mesleki alanların dalları ör:mühendislik -> yazılım"
    EN = ( # mühendislik dalları
        ("MAC","Makine"),
        ("EAE","Elektrik ve elektronik"),
        ("FOOD","Gıda"),
        ("PHY","Fizik"),
        ("CIV","İnşaat"),
        ("TEX","Tekstil"),
        ("IND","Endüstri"),
        ("COM","Bigisayar"),
        ("SOF","Yazılım"),
        ("MAM","Metalurji ve malzeme"),
        ("ENS","Enerji sistemleri"),
        ("BAC","Biyoproses ve kimya"),
        ("OAA","Optik ve akustik"),
    )
    ME = ( # tıpın dalları
        ("IMU","Dahili tıp birimleri"),
        ("SMU","Cerrahi tıp birimleri"),
        ("BMU","Temel tıp birimleri"),
    )
    SL = ( # fen edebiyat
        ("HIS","Tarih"),
        ("MAT","Matematik"),
        ("TLL","Türk dili ve edebiyat"),
        ("BİO","Biyoloji"),
        ("WLL","Batı dilleri ve edebiyat"),
        ("CHE","Kimya"),
        ("ARCH","Arkeoloji"),
        ("SOCİ","Sosyoloji"),
        ("PRCA","Kültür varlıklarını koruma ve onarım"),
        ("STA","İstatislik"),
        ("PSYCH","Psikoloji"),
        ("GEO","Çoğrafya"),
        ("PHİ","Felsefe"),
        ("ELL","Doğu dilleri ve edebiyatı"),
    )
    EAAS = ( # iktisadi ve  idari
        ("","İktisat"),
        ("","İşletme"),
        ("","Uluslar arası ticaret ve lojistik"),
        ("","Kamu yönetim"),
        ("","Maliye"),
        ("","Küresel siyaset ve uluslararası ilişkiler"),
    )
    ED = ( # eğitim
        ("","Matematik ve fen bilimleri"),
        ("","Güzel sanatlar"),
        ("","Türkçe ve sosyal bilimler"),
        ("","Yabancı diller"),
        ("","Eğitim yönetimi anabilim dalı"),
        ("","Eğitim programları ve öğretim adabilim dalı"),
        ("","Rehberlik ve psikojik danışma anabilim dalı"),
        ("","Eğitimin felsefesi,sosyal ve tarihi temelleri anabilim dalı"),
        ("","Hayar boyu öğrenme ve yetişkin eğitimi anabilim dalı"),
        ("","Öğretim teknolojileri anabilim dalı"),
        ("","Eğitimde ölçme ve değerlendirme anabilim dalı"),
        ("","Bilgisayar ve öğretim teknolojileri"),
        ("","Okul öncesi eğitimi anabilim dalı"),
        ("","Sınıf eğitimi anabilim dalı"),
        ("","Özel yetenekliler eğitimi anabilim dalı"),
        ("","Zihinsel engelliler eğitimi anabilim dalı"),
        ("","Görme engelliler eğitimi anabilim dalı"),
        ("","İşitme engelliler eğitimi anabilim dalı"),
        ("","eğitimi anabilim dalı"),
    )
    DE = ( # diş 
        ("","Ağız Diş ve Çene Cerrahisi AD."),
        ("","Endodonti AD."),
        ("","Oral Diagnoz ve Radyoloji AD."),
        ("","Ortodonti AD."),
        ("","Pedodonti AD."),
        ("","Periodontoloji AD."),
        ("","Protetik Diş Tedavisi AD."),
        ("","Restoratif Diş Tedavisi AD."),
    )
    ARC = (
        ("","ŞEHİR VE BÖLGE PLANLAMA BÖLÜMÜ"),
        ("","ENDÜSTRİ ÜRÜNLERİ TASARIMI BÖLÜMÜ"),
        ("","MİMARLIK BÖLÜMÜ"),
        ("","İÇ MİMARLIK BÖLÜMÜ")
    )
    IEAAS = ( # İslahiye İktisadi ve İdari Bilimler Fakültesi
        ("","EKONOMETRİ"),
        ("","ULUSLARARASI İLİŞKİLER"),
        ("","MALİYE"),
        ("","KAMU YÖNETİMİ"),
        ("","İKTİSAT"),
        ("","İŞLETME")
    )
    FI = ( # güzel sanatlar
        ("","GASTRONOMİ VE MUTFAK SANATLARI BÖLÜMÜ"),
        ("","MODA VE TEKSTİL TASARIMI BÖLÜMÜ"),
        ("","SAHNE VE GÖSTERİ SANATLARI BÖLÜMÜ"),
        ("","GELENEKSEL TÜRK EL SANATLARI BÖLÜMÜ"),
        ("","SİNEMA VE TELEVİZYON BÖLÜMÜ"),
        ("","FOTOĞRAF BÖLÜMÜ"),
        ("","SERAMİK VE CAM BÖLÜMÜ"),
        ("","RESİM BÖLÜMÜ"),
        ("","HEYKEL BÖLÜMÜ"),
        ("","GRAFİK BÖLÜMÜ"),
    )
    HE = ( #sağlık
        ("","FİZYOTERAPİ VE REHABİLİTASYON"),
        ("","DİL VE KONUŞMA TERAPİSİ"),
        ("","ODYOLOJİ"),
        ("","BESLENME VE DİYETETİK"),
        ("","SAĞLIK YÖNETİMİ"),
        ("","SOLUNUM TERAPİSTLİĞİ"),
        ("","EBELİK"),
        ("","HEMŞİRELİK"),
    )
    LA = ( # hukuk 
        ("","HUKUK FAKÜLTESİ"), 
        ("","ANAYASA HUKUKU ANABİLİM DALI"), 
        ("","CEZA VE CEZA MUHAKEMESİ HUKUKU ANABİLİM DALI"), 
        ("","GENEL KAMU HUKUKU ANABİLİM DALI"), 
        ("","HUKUK FELSEFESİ VE SOSYOLOJİSİ ANABİLİM DALI"), 
        ("","HUKUK TARİHİ ANABİLİM DALI"), 
        ("","MALİ HUKUK ANABİLİM DALI"), 
        ("","MİLLETLERARASI HUKUK ANABİLİM DALI"), 
        ("","İDARE HUKUKU ANABİLİM DALI"), 
        ("","İNSAN HAKLARI ANABİLİM DALI"), 
        ("","İSLAM HUKUKU ANABİLİM DALI"), 
        ("","TİCARET HUKUKU ANABİLİM DALI"), 
        ("","AVRUPA BİRLİĞİ HUKUKU ANABİLİM DALI"), 
        ("","DENİZ HUKUKU ANABİLİM DALI"), 
        ("","KARŞILAŞTIRMALI HUKUK ANABİLİM DALI"), 
        ("","MEDENİ HUKUK ANABİLİM DALI"), 
        ("","MEDENİ USUL VE İCRA İFLAS HUKUKU ANABİLİM DALI"),
        ("","MİLLETLERARASI ÖZEL HUKUK ANABİLİM DALI"), 
        ("","ROMA HUKUKU ANABİLİM DALI"), 
        ("","İŞ VE SOSYAL GÜVENLİK HUKUKU ANABİLİM DALI"),
    )
    TH = ( # ilahiyat
        ("","Tefsir"),
        ("","Hadis"),
        ("","Kelam"),
        ("","İslam Hukuku"),
        ("","İslam Mezhepleri Tarihi"),
        ("","Tasavvuf"),
        ("","Arap Dili ve Belagatı"),
        ("","Kuranı Kerim Okuma ve Kıraat İlmi"),
        ("","Din Eğitimi"),
        ("","Dinler Tarihi"),
        ("","İslam Felsefesi"),
        ("","Din Sosyolojisi"),
        ("","Din Psikolojisi"),
        ("","Felsefe Tarihi"),
        ("","Mantık"),
        ("","İslam Tarihi"),
        ("","Türk İslam Edebiyatı"),
        ("","Türk İslam Sanatları Tarihi"),
        ("","Türk Din Musikisi"),
    )
    CO = ( # iletişim
        ("","Gazetecilik"),
        ("","Halkla ilişkiler ve tanıtım"),
        ("","Radyo, tv ve sinema"),
        ("","İletişim enformatiği"),
        ("","Reklamcılık"),
    )
    AE = ( # HAVACILIK VE UZAY BİLİMLERİ FAKÜLTESİ
        ("","HAVACILIK YÖNETİMİ BÖLÜMÜ"),
        ("","UÇAK VE UZAY MÜHENDİSLİĞİ BÖLÜMÜ"),
        ("","PİLOTAJ BÖLÜMÜ"),
    )
    TO = (
        ("None","Dal yok"),
    )
    branches = EN + ME + SL + EAAS + ED + DE + ARC \
    + IEAAS +FI + HE + LA + TH + CO + AE
