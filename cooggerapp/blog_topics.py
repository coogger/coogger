class Category: 
    "kategoriler eylence/ders/"
    def __init__(self):
        list_category = (
            ("ders","Ders"),
            ("oyun","oyun"),
            ("seyahat","seyahat"),
            ("giyim","giyim"),
            ("makyaj_ve_cilt_bakım","makyaj ve cilt bakım"),
            ("sağlık","sağlık"),
            ("yiyecek_ve_içecek","yiyecek ve içecek"),
            ("medya","medya"),
            ("ürün_eşya","ürün - eşya"),
            ("taşıtlar","taşıtlar"),
            ("tanınmış_kişi","tanınmış kişi"),
            ("hayvanlar","hayvanlar"),
            ("inanç","inanç"),
            ("dil","dil"),
            ("metafizik","metafizik"),
            ("aşk_arkadaşlık","aşk - arkadaşlık"),
            ("erotik","erotik"),
        )
        self.category = []
        for i in list_category:
            self.category.append((i[0].lower().replace(" ","_"),i[1].lower())) 
    

class Subcategory:
    "alt kategori"
    def ders():
        faculties = (
            # fakülteler
            ("Mühendislik", 'Mühendislik'),
            ("Tıp","Tıp"),
            ("Fen-edebiyat","Fen-edebiyat"),
            ("İktisadi ve idari bilimleri","İktisadi ve idari bilimleri"),
            ("Eğitim","Eğitim"),
            ("Diş hekimliği","Diş hekimliği"),
            ("Mimarlık","Mimarlık"),
            ("İslahiye iktisadi ve idari bilimleri","İslahiye iktisadi ve idari bilimleri"),
            ("Güzel sanatlar","Güzel sanatlar"),
            ("Sağlık bilimleri","Sağlık bilimleri"),
            ("Hukuk","Hukuk"),
            ("İlahiyat","İlahiyat"),
            ("İletişim","İletişim"),
            ("Havacılık ve uzay mühendisliği","Havacılık ve uzay mühendisliği"),
            ("Turizm","Turizm")
        )
        yüksekokul = (
            # yüksekokular
            ("Turkish_music_conservatory","Türk musıkisi devlet konservatuarı"),
            ("Physical_education_and_sports","Beden eğitimi ve spor"),
            ("Foreign_languages","Yabancı diller"),
            ("Civil_Aviation","Sivil havacılık")
        )
        meslek_yüksekokul = (
            # meslek yüksek okullar
            ("Technical_sciences","Teknik bilimler"),
            ("Liberal_arts","Sosyal bilimler"),
            ("Health_care","Sağlık hizmetleri"),
            ("Tourism_and_Hotel_Management","Turizm ve Otelcilik"),
            ("Islahiye","Islahiye"),
            ("OFFICE_DEPARTMENT_OF_SERVICES_AND_SECRETARITY","BÜRO HİZMETLERİ VE SEKRETERLİK BÖLÜMÜ"),
            ("COMPUTER_TECHNOLOGY_DEPARTMENT","BİLGİSAYAR TEKNOLOJİLERİ BÖLÜMÜ"),
            ("DEPARTMENT OF VEGETABLE_AND_ANIMAL_PRODUCTION","BİTKİSEL VE HAYVANSAL ÜRETİMİ BÖLÜMÜ"),
            ("DEPARTMENT OF FINANCE AND BANKING","FİNANS VE BANKACILIK BÖLÜMÜ"),
            ("DEPARTMENT OF FOOD PROCESSING","GIDA İŞLEMLERİ BÖLÜMÜ"),
            ("FOREIGN TRADE DEPARTMENT","DIŞ TİCARET BÖLÜMÜ"),
            ("DEPARTMENT OF MANAGEMENT AND ORGANIZATION","YÖNETİM VE ORGANİZASYON BÖLÜMÜ"),
            ("DEPARTMENT OF MARKETING AND ADVERTISING","PAZARLAMA VE REKLAMCILIK BÖLÜMÜ"),
            ("DEPARTMENT OF THERAPY AND REHABILITATION","TERAPİ VE REHABİLİTASYON BÖLÜMÜ"),
            ("DEPARTMENT OF HEALTH CARE SERVICES","SAĞLIK BAKIM HİZMETLERİ BÖLÜMÜ"),
            ("DENTAL SERVICES DEPARTMENT","DİŞÇİLİK HİZMETLERİ BÖLÜMÜ"),
            ("HOTEL, RESTAURANT AND CATERING SERVICES DEPARTMENT","OTEL, LOKANTA VE İKRAM HİZMETLERİ BÖLÜMÜ"),
            ("DEPARTMENT OF TRAVEL TOURISM AND ENTERTAINMENT SERVICES","SEYAHAT-TURİZM VE EĞLENCE HİZMETLERİ BÖLÜMÜ"),
            ("Justice","Adalet"),
            ("Logistics","Lojistik"),
            ("Business Administration","İşletme Yönetimi"),
            ("Occupational health and Safety","İş Sağlığı ve Güvenliği"),
            ("Computer programming","Bilgisayar Programcılığı"),
            ("Private Security and Protection","Özel Güvenlik ve Koruma"),
            ("Civil Defense and Firefighting","Sivil Savunma ve İtfaiyecilik"),
            ("Social Security","Sosyal Güvenlik"),
            ("PROTECTION AND SECURITY DEPARTMENT OF PROPERTY","MÜLKİYETİ KORUMA VE GÜVENLİK BÖLÜMÜ"),
            ("VETERINARY DEPARTMENT","VETERİNERLİK BÖLÜMÜ"),
            ("ACCOUNTING AND TAX DEPARTMENT","MUHASEBE VE VERGİ BÖLÜMÜ"),
            ("Foreign trade","Dış ticaret"),
            ("Management and organization","Yönetim ve organizasyon"),
            ("Plant and animal production","Bitkisel ve hayvansal üretim"),
            ("handicrafts","el sanatları"),
            ("food processing","gıda işleme"),
            ("material and material processing","malzeme ve malzeme işleme"),
            ("textiles, clothing, footwear, leather","tekstil,giyim,ayakkabı,deri"),
            ("property protection and security","mülkiyet koruma ve güvenlik"),
            ("machine and metal technology","makine ve metal teknolojileri"),
            ("chemical and chemical processing technologies","kimya ve kimyasal işleme teknolojileri"),
            ("DEPARTMENT OF MEDICAL SERVICES AND TECHNIQUES","TIBBİ HİZMETLER VE TEKNİKLER BÖLÜMÜ"),
            ("DEPARTMENT OF VEGETABLE AND ANIMAL PRODUCTION","BİTKİSEL VE HAYVANSAL ÜRETİM BÖLÜMÜ"),
        )
        list_faculties = []
        for i in faculties:
            list_faculties.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_faculties
    def oyun():
        pc_games = (
            ("grand theft auto","grand theft auto"),
            ("counter strike global offensive","counter strike global offensive"),
            ("euro truck simulator","euro truck simulator"),
            ("minecraft","minecraft"),
            ("fifa","fifa"),
            ("battlefield","battlefield"),
            ("call of duty","call of duty"),
            ("prey","prey"),
            ("watch dogs","watch dogs"),
            ("fallout","fallout"),
            ("far cry","far cry"),
            ("half-life","half-life"),
            ("assassin's creed","assassin's creed"),
            ("league of legends","league of legends"),
            ("destiny","destiny"),
            ("rise of the tomb raider","rise of the tomb raider"),
        )
        mobile_games = (
            ("clash of clans","clash of clans"),
        )
        games = pc_games + mobile_games
        list_games = []
        for i in games:
            list_games.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_games

    def seyahat():
        name_of_cities = (
            ("adana","adana"),
            ("adıyaman","adıyaman"),
            ("afyon","afyon"),
            ("ağrı","ağrı"),
            ("amasya","amasya"),
            ("ankara","ankara"),
            ("antalya","antalya"),
            ("artvin","artvin"),
            ("aydın","aydın"),
            ("balıkesir","balıkesir"),
            ("bilecik","bilecik"),
            ("bingöl","bingöl"),
            ("bitlis","bitlis"),
            ("bolu","bolu"),
            ("burdur","burdur"),
            ("bursa","bursa"),
            ("çanakkale","çanakkale"),
            ("çankırı","çankırı"),
            ("çorum","çorum"),
            ("denizli","denizli"),
            ("diyarbakır","diyarbakır"),
            ("edirne","edirne"),
            ("elazığ","elazığ"),
            ("erzincan","erzincan"),
            ("erzurum","erzurum"),
            ("eskişehir","eskişehir"),
            ("gaziantep","gaziantep"),
            ("giresun","giresun"),
            ("gümüşhane","gümüşhane"),
            ("hakkari","hakkari"),
            ("hatay","hatay"),
            ("ısparta","ısparta"),
            ("mersin","mersin"),
            ("istanbul","istanbul"),
            ("izmir","izmir"),
            ("kars","kars"),
            ("kastamonu","kastamonu"),
            ("kayseri","kayseri"),
            ("Kırklareli","Kırklareli"),
            ("kırşehir","kırşehir"),
            ("kocaeli","kocaeli"),
            ("konya","konya"),
            ("kütahya","kütahya"),
            ("malatya","malatya"),
            ("manisa","manisa"),
            ("kahramanmaraş","kahramanmaraş"),
            ("mardin","mardin"),
            ("muğla","muğla"),
            ("muş","muş"),
            ("nevşehir","nevşehir"),
            ("niğde","niğde"),
            ("ordu","ordu"),
            ("rize","rize"),
            ("sakarya","sakarya"),
            ("samsun","samsun"),
            ("siirt","siirt"),
            ("sinop","sinop"),
            ("sivas","sivas"),
            ("tekirdağ","tekirdağ"),
            ("tokat","tokat"),
            ("trabzon","trabzon"),
            ("tunceli","tunceli"),
            ("şanlıurfa","şanlıurfa"),
            ("uşak","uşak"),
            ("van","van"),
            ("yozgat","yozgat"),
            ("zonguldak","zonguldak"),
            ("aksaray","aksaray"),
            ("bayburt","bayburt"),
            ("karaman","karaman"),
            ("kırıkkale","kırıkkale"),
            ("batman","batman"),
            ("şırnak","şırnak"),
            ("bartın","bartın"),
            ("ardahan","ardahan"),
            ("ığdır","ığdır"),
            ("yalova","yalova"),
            ("karabuk","karabuk"),
            ("kilis","kilis"),
            ("osmaniye","osmaniye"),
            ("düzce","düzce"),
        )
        list_name_of_cities = []
        for i in name_of_cities:
            list_name_of_cities.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_name_of_cities

    def giyim():
        clot = (
            ("yazlık","yazlık"),
            ("kışlık","kışlık"),
            ("mevsimlik","mevsimlik"),
            ("aksesuar","aksesuar"),
        )
        list_ = []
        for i in clot:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_
    def makyaj_ve_cilt_bakım():
        make = (
            ("gunluk","Günlük Makyaj"),
            ("pormak","Porselen Makyaj"),
            ("showm","Show Makyajı"),
            ("kalmak","Kalıcı Makyaj"),
            ("gecemak","Gece Makyajı"),
            ("ciltb","cilt bakımı"),
        )
        list_ = []
        for i in make:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def yiyecek_ve_içecek():
        food = (
            ("sulu","sulu"),
            ("çorbalar","çorbalar"),
            ("etli","etli"),
            ("fastfood","fastfood"),
            ("soğuk","soğuk"),
            ("sıcak","sıcak"),
            ("alkollu","alkollu"),
            ("tatlılar","tatlılar"),
            ("tuzlu","tuzlu"),
            ("restorant","restorant"),
            ("pasta","pasta"),
            ("ev yemekleri","ev yemekleri"),
        )
        list_food = []
        for i in food:
            list_food.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_food

    def medya():
        med = (
            ("televiyon-programr","televiyon - program"),
            ("radyo","radyo"),
            ("sinema","sinema"),
            ("müzik","müzik"),
            ("video","video"),
            ("ses","ses"),
        )
        list_ = []
        for i in med:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def ürün_eşya():
        pro = (
            ("ev","ev eşyaları"),
            ("teknolojik","teknolojik eşyalar"),
        )
        list_ = []
        for i in pro:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_ 

    def taşıtlar():
        ve = (
            ("kara","kara"),
            ("hava","hava"),
            ("deniz","deniz"),
        )
        list_ = []
        for i in ve:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def tanınmış_kişi():
        person = (
            ("Bilim insanı","Bilim insanı"),
            ("siyaset insanı","siyaset insanı"),
            ("din insanı","din insanı"),
            ("felsefe insanı","felsefe insanı"),
            ("sinema-oyuncusu","sinema-oyuncusu"),
            ("müzisyen","müzisyen"),
            ("oyuncu - gamer","oyuncu - gamer"),
            ("yazar","yazar"),
            ("şarkıcı","şarkıcı"),
            ("sporcu","sporcu"),
            ("girişimci","girişimci"),
            ("diger","diğer"),
        )
        list_person = []
        for i in person:
            list_person.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_person

    def hayvanlar():
        anim = (
            ("sokak","sokak"),
            ("evcil","evcil"),
            ("vahşi","vahşi"),
        )
        list_ = []
        for i in anim:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def inanç():
        fa = (
            ("dini","dini"),
            ("kişisel","kişisel"),
        )
        list_ = []
        for i in fa:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def all(): # bütün alt kategorileri almak için
        all_ = Subcategory.ders() + Subcategory.oyun() + Subcategory.seyahat() + Subcategory.giyim() + Subcategory.makyaj_ve_cilt_bakım() \
        + Subcategory.yiyecek_ve_içecek() + Subcategory.medya() + Subcategory.ürün_eşya() + Subcategory.taşıtlar() + Subcategory.tanınmış_kişi() \
        + Subcategory.hayvanlar() + Subcategory.inanç()
        list_all = []
        for i in all_:
            list_all.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_all

class Category2:
    def mühendislik():
        en = ( # mühendislik dalları
            ("Makine","Makine"),
            ("Elektrik ve elektronik","Elektrik ve elektronik"),
            ("Gıda","Gıda"),
            ("Fizik","Fizik"),
            ("İnşaat","İnşaat"),
            ("Tekstil","Tekstil"),
            ("Endüstri","Endüstri"),
            ("Bigisayar","Bigisayar"),
            ("Yazılım","Yazılım"),
            ("Metalurji ve malzeme","Metalurji ve malzeme"),
            ("Enerji sistemleri","Enerji sistemleri"),
            ("Biyoproses ve kimya","Biyoproses ve kimya"),
            ("Optik ve akustik","Optik ve akustik"),
        )
        list_ = []
        for i in en:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def tıp():
        me = ( # tıpın dalları
            ("Dahili tıp birimleri","Dahili tıp birimleri"),
            ("Cerrahi tıp birimleri","Cerrahi tıp birimleri"),
            ("Temel tıp birimleri","Temel tıp birimleri"),
        )
        list_ = []
        for i in me:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def fen_edebiyat():
        sl = ( # fen edebiyat
            ("Tarih","Tarih"),
            ("Matematik","Matematik"),
            ("Türk dili ve edebiyat","Türk dili ve edebiyat"),
            ("Biyoloji","Biyoloji"),
            ("Batı dilleri ve edebiyat","Batı dilleri ve edebiyat"),
            ("Kimya","Kimya"),
            ("Arkeoloji","Arkeoloji"),
            ("Sosyoloji","Sosyoloji"),
            ("Kültür varlıklarını koruma ve onarım","Kültür varlıklarını koruma ve onarım"),
            ("İstatislik","İstatislik"),
            ("Psikoloji","Psikoloji"),
            ("Çoğrafya","Çoğrafya"),
            ("Felsefe","Felsefe"),
            ("Doğu dilleri ve edebiyatı","Doğu dilleri ve edebiyatı"),
        )
        list_ = []
        for i in sl:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_ 
    
    def iktisadi_ve_idari_bilimleri():
        eaas = ( # iktisadi ve  idari
            ("İktisat","İktisat"),
            ("İşletme","İşletme"),
            ("Uluslar arası ticaret ve lojistik","Uluslar arası ticaret ve lojistik"),
            ("Kamu yönetim","Kamu yönetim"),
            ("Maliye","Maliye"),
            ("Küresel siyaset ve uluslararası ilişkiler","Küresel siyaset ve uluslararası ilişkiler"),
        )
        list_ = []
        for i in eaas:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def eğitim():
        ed = ( # eğitim
            ("Matematik ve fen bilimleri","Matematik ve fen bilimleri"),
            ("Güzel sanatlar","Güzel sanatlar"),
            ("Türkçe ve sosyal bilimler","Türkçe ve sosyal bilimler"),
            ("Yabancı diller","Yabancı diller"),
            ("Eğitim yönetimi anabilim dalı","Eğitim yönetimi anabilim dalı"),
            ("Eğitim programları ve öğretim adabilim dalı","Eğitim programları ve öğretim adabilim dalı"),
            ("Rehberlik ve psikojik danışma anabilim dalı","Rehberlik ve psikojik danışma anabilim dalı"),
            ("Eğitimin felsefesi,sosyal ve tarihi temelleri anabilim dalı","Eğitimin felsefesi,sosyal ve tarihi temelleri anabilim dalı"),
            ("Hayat boyu öğrenme ve yetişkin eğitimi anabilim dalı","Hayat boyu öğrenme ve yetişkin eğitimi anabilim dalı"),
            ("Öğretim teknolojileri anabilim dalı","Öğretim teknolojileri anabilim dalı"),
            ("Eğitimde ölçme ve değerlendirme anabilim dalı","Eğitimde ölçme ve değerlendirme anabilim dalı"),
            ("Bilgisayar ve öğretim teknolojileri","Bilgisayar ve öğretim teknolojileri"),
            ("Okul öncesi eğitimi anabilim dalı","Okul öncesi eğitimi anabilim dalı"),
            ("Sınıf eğitimi anabilim dalı","Sınıf eğitimi anabilim dalı"),
            ("Özel yetenekliler eğitimi anabilim dalı","Özel yetenekliler eğitimi anabilim dalı"),
            ("Zihinsel engelliler eğitimi anabilim dalı","Zihinsel engelliler eğitimi anabilim dalı"),
            ("Görme engelliler eğitimi anabilim dalı","Görme engelliler eğitimi anabilim dalı"),
            ("İşitme engelliler eğitimi anabilim dalı","İşitme engelliler eğitimi anabilim dalı"),
            ("eğitimi anabilim dalı","eğitimi anabilim dalı"),
        )
        list_ = []
        for i in ed:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_ 

    def diş_hekimliği():
        de = ( # diş 
            ("Ağız Diş ve Çene Cerrahisi AD.","Ağız Diş ve Çene Cerrahisi AD."),
            ("Endodonti AD.","Endodonti AD."),
            ("Oral Diagnoz ve Radyoloji AD.","Oral Diagnoz ve Radyoloji AD."),
            ("Ortodonti AD.","Ortodonti AD."),
            ("Pedodonti AD.","Pedodonti AD."),
            ("Periodontoloji AD.","Periodontoloji AD."),
            ("Protetik Diş Tedavisi AD.","Protetik Diş Tedavisi AD."),
            ("Restoratif Diş Tedavisi AD.","Restoratif Diş Tedavisi AD."),
        )
        list_ = []
        for i in de:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def mimarlık():
        arc = ( # mimar
            ("ŞEHİR VE BÖLGE PLANLAMA BÖLÜMÜ","ŞEHİR VE BÖLGE PLANLAMA BÖLÜMÜ"),
            ("ENDÜSTRİ ÜRÜNLERİ TASARIMI BÖLÜMÜ","ENDÜSTRİ ÜRÜNLERİ TASARIMI BÖLÜMÜ"),
            ("MİMARLIK BÖLÜMÜ","MİMARLIK BÖLÜMÜ"),
            ("İÇ MİMARLIK BÖLÜMÜ","İÇ MİMARLIK BÖLÜMÜ")
        )
        list_ = []
        for i in arc:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def islahiye_iktisadi_ve_idari_bilimleri():
        ieaas = ( # İslahiye İktisadi ve İdari Bilimler Fakültesi
            ("EKONOMETRİ","EKONOMETRİ"),
            ("ULUSLARARASI İLİŞKİLER","ULUSLARARASI İLİŞKİLER"),
            ("MALİYE","MALİYE"),
            ("KAMU YÖNETİMİ","KAMU YÖNETİMİ"),
            ("İKTİSAT","İKTİSAT"),
            ("İŞLETME","İŞLETME")
        )
        list_ = []
        for i in ieaas:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_ 

    def güzel_sanatlar():
        fi = ( # güzel sanatlar
            ("GASTRONOMİ VE MUTFAK SANATLARI BÖLÜMÜ","GASTRONOMİ VE MUTFAK SANATLARI BÖLÜMÜ"),
            ("MODA VE TEKSTİL TASARIMI BÖLÜMÜ","MODA VE TEKSTİL TASARIMI BÖLÜMÜ"),
            ("SAHNE VE GÖSTERİ SANATLARI BÖLÜMÜ","SAHNE VE GÖSTERİ SANATLARI BÖLÜMÜ"),
            ("GELENEKSEL TÜRK EL SANATLARI BÖLÜMÜ","GELENEKSEL TÜRK EL SANATLARI BÖLÜMÜ"),
            ("SİNEMA VE TELEVİZYON BÖLÜMÜ","SİNEMA VE TELEVİZYON BÖLÜMÜ"),
            ("FOTOĞRAF BÖLÜMÜ","FOTOĞRAF BÖLÜMÜ"),
            ("SERAMİK VE CAM BÖLÜMÜ","SERAMİK VE CAM BÖLÜMÜ"),
            ("RESİM BÖLÜMÜ","RESİM BÖLÜMÜ"),
            ("HEYKEL BÖLÜMÜ","HEYKEL BÖLÜMÜ"),
            ("GRAFİK BÖLÜMÜ","GRAFİK BÖLÜMÜ"),
        )
        list_ = []
        for i in fi:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def sağlık_bilimleri():
        he = ( #sağlık
            ("FİZYOTERAPİ VE REHABİLİTASYON","FİZYOTERAPİ VE REHABİLİTASYON"),
            ("DİL VE KONUŞMA TERAPİSİ","DİL VE KONUŞMA TERAPİSİ"),
            ("ODYOLOJİ","ODYOLOJİ"),
            ("BESLENME VE DİYETETİK","BESLENME VE DİYETETİK"),
            ("SAĞLIK YÖNETİMİ","SAĞLIK YÖNETİMİ"),
            ("SOLUNUM TERAPİSTLİĞİ","SOLUNUM TERAPİSTLİĞİ"),
            ("EBELİK","EBELİK"),
            ("HEMŞİRELİK","HEMŞİRELİK"),
        )
        list_ = []
        for i in he:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_ 

    def hukuk():
        la = ( # hukuk 
            ("HUKUK FAKÜLTESİ","HUKUK FAKÜLTESİ"), 
            ("ANAYASA HUKUKU ANABİLİM DALI","ANAYASA HUKUKU ANABİLİM DALI"), 
            ("CEZA VE CEZA MUHAKEMESİ HUKUKU ANABİLİM DALI","CEZA VE CEZA MUHAKEMESİ HUKUKU ANABİLİM DALI"), 
            ("GENEL KAMU HUKUKU ANABİLİM DALI","GENEL KAMU HUKUKU ANABİLİM DALI"), 
            ("HUKUK FELSEFESİ VE SOSYOLOJİSİ ANABİLİM DALI","HUKUK FELSEFESİ VE SOSYOLOJİSİ ANABİLİM DALI"), 
            ("HUKUK TARİHİ ANABİLİM DALI","HUKUK TARİHİ ANABİLİM DALI"), 
            ("MALİ HUKUK ANABİLİM DALI","MALİ HUKUK ANABİLİM DALI"), 
            ("MİLLETLERARASI HUKUK ANABİLİM DALI","MİLLETLERARASI HUKUK ANABİLİM DALI"), 
            ("İDARE HUKUKU ANABİLİM DALI","İDARE HUKUKU ANABİLİM DALI"), 
            ("İNSAN HAKLARI ANABİLİM DALI","İNSAN HAKLARI ANABİLİM DALI"), 
            ("İSLAM HUKUKU ANABİLİM DALI","İSLAM HUKUKU ANABİLİM DALI"), 
            ("TİCARET HUKUKU ANABİLİM DALI","TİCARET HUKUKU ANABİLİM DALI"), 
            ("AVRUPA BİRLİĞİ HUKUKU ANABİLİM DALI","AVRUPA BİRLİĞİ HUKUKU ANABİLİM DALI"), 
            ("DENİZ HUKUKU ANABİLİM DALI","DENİZ HUKUKU ANABİLİM DALI"), 
            ("KARŞILAŞTIRMALI HUKUK ANABİLİM DALI","KARŞILAŞTIRMALI HUKUK ANABİLİM DALI"), 
            ("MEDENİ HUKUK ANABİLİM DALI","MEDENİ HUKUK ANABİLİM DALI"), 
            ("MEDENİ USUL VE İCRA İFLAS HUKUKU ANABİLİM DALI","MEDENİ USUL VE İCRA İFLAS HUKUKU ANABİLİM DALI"),
            ("MİLLETLERARASI ÖZEL HUKUK ANABİLİM DALI","MİLLETLERARASI ÖZEL HUKUK ANABİLİM DALI"), 
            ("ROMA HUKUKU ANABİLİM DALI","ROMA HUKUKU ANABİLİM DALI"), 
            ("İŞ VE SOSYAL GÜVENLİK HUKUKU ANABİLİM DALI","İŞ VE SOSYAL GÜVENLİK HUKUKU ANABİLİM DALI"),
        )
        list_ = []
        for i in la:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def ilahiyat():
        th = ( # ilahiyat
            ("Tefsir","Tefsir"),
            ("Hadis","Hadis"),
            ("Kelam","Kelam"),
            ("İslam Hukuku","İslam Hukuku"),
            ("İslam Mezhepleri Tarihi","İslam Mezhepleri Tarihi"),
            ("Tasavvuf","Tasavvuf"),
            ("Arap Dili ve Belagatı","Arap Dili ve Belagatı"),
            ("Kuranı Kerim Okuma ve Kıraat İlmi","Kuranı Kerim Okuma ve Kıraat İlmi"),
            ("Din Eğitimi","Din Eğitimi"),
            ("Dinler Tarihi","Dinler Tarihi"),
            ("İslam Felsefesi","İslam Felsefesi"),
            ("Din Sosyolojisi","Din Sosyolojisi"),
            ("Din Psikolojisi","Din Psikolojisi"),
            ("Felsefe Tarihi","Felsefe Tarihi"),
            ("Mantık","Mantık"),
            ("İslam Tarihi","İslam Tarihi"),
            ("Türk İslam Edebiyatı","Türk İslam Edebiyatı"),
            ("Türk İslam Sanatları Tarihi","Türk İslam Sanatları Tarihi"),
            ("Türk Din Musikisi","Türk Din Musikisi"),
        )
        list_ = []
        for i in th:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def iletişim():
        co = ( # iletişim
            ("Gazetecilik","Gazetecilik"),
            ("Halkla ilişkiler ve tanıtım","Halkla ilişkiler ve tanıtım"),
            ("Radyo, tv ve sinema","Radyo, tv ve sinema"),
            ("İletişim enformatiği","İletişim enformatiği"),
            ("Reklamcılık","Reklamcılık"),
        )
        list_ = []
        for i in co:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_

    def havacılık_ve_uzay_mühendisliği():
        ae = ( # HAVACILIK VE UZAY BİLİMLERİ FAKÜLTESİ
            ("HAVACILIK YÖNETİMİ BÖLÜMÜ","HAVACILIK YÖNETİMİ BÖLÜMÜ"),
            ("UÇAK VE UZAY MÜHENDİSLİĞİ BÖLÜMÜ","UÇAK VE UZAY MÜHENDİSLİĞİ BÖLÜMÜ"),
            ("PİLOTAJ BÖLÜMÜ","PİLOTAJ BÖLÜMÜ"),
        )
        list_ = []
        for i in ae:
            list_.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_
    def all():
        all_ = Category2.mühendislik() + Category2.tıp() + Category2.fen_edebiyat() + Category2.iktisadi_ve_idari_bilimleri()\
         + Category2.eğitim() + Category2.diş_hekimliği() + Category2.mimarlık() + Category2.islahiye_iktisadi_ve_idari_bilimleri() \
         + Category2.güzel_sanatlar() + Category2.sağlık_bilimleri() + Category2.hukuk() +Category2.ilahiyat() + Category2.iletişim() \
         + Category2.havacılık_ve_uzay_mühendisliği()
        list_all = []
        for i in all_:
            list_all.append((i[0].lower().replace(" ","_"),i[1].lower())) 
        return list_all

