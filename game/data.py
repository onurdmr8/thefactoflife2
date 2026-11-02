# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Zenginleştirilmiş Veri Kütüphanesi
İsimler, şehirler, meslekler, girişimler, kulüpler, varlıklar, hastalıklar ve başarımlar.
"""

FIRST_NAMES_MALE = [
    "Ahmet", "Mehmet", "Mustafa", "Ali", "Can", "Burak", "Emre", "Murat", "Oğuzhan", "Kerem",
    "Kaan", "Deniz", "Onur", "Barış", "Efe", "Arda", "Yusuf", "Emir", "Hakan", "Volkan",
    "Serkan", "Tolga", "Mert", "Berk", "Yiğit", "Umut", "Eren", "Kuzey", "Rüzgar", "Cem",
    "Batuhan", "Doruk", "Sinan", "Okan", "Gökhan", "Tarık", "Alper", "Selim", "Kadir", "Harun",
    "Koray", "Tuna", "Alp", "Çağlar", "Levent", "Taylan", "Bora", "Cihan", "Metin", "Furkan"
]

FIRST_NAMES_FEMALE = [
    "Zeynep", "Elif", "Ayşe", "Fatma", "Merve", "Büşra", "Ece", "Melis", "Selin", "Damla",
    "Defne", "Duru", "Derin", "Aslı", "Ezgi", "Gamze", "Seda", "Ceren", "Tuğba", "Pelin",
    "Berna", "Gizem", "İrem", "Eylül", "Yağmur", "Güneş", "Bade", "Dilek", "Sinem", "Aylin",
    "Ceyda", "Hande", "Hazal", "Özge", "Deniz", "Hilal", "Sibel", "Bahar", "Burcu", "Yasemin",
    "Nehir", "Ada", "Lara", "Nil", "Gökçe", "Simge", "Melisa", "Dilara", "Nazlı", "Çağla"
]

LAST_NAMES = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir",
    "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
    "Erdoğan", "Polat", "Korkmaz", "Özer", "Yalçın", "Güler", "Bulut", "Keskin", "Aksoy", "Tekin",
    "Güneş", "Bozkurt", "Avcı", "Taş", "Coşkun", "Köse", "Duran", "Turan", "Yavuz", "Sarı",
    "Soylu", "Karaca", "Aktaş", "Ünal", "Erdem", "Çakır", "Sezer", "Yüksel", "Mutlu", "Kalkan"
]

CITIES = [
    {"city": "İstanbul", "country": "Türkiye", "cost_mult": 1.4},
    {"city": "Ankara", "country": "Türkiye", "cost_mult": 1.1},
    {"city": "İzmir", "country": "Türkiye", "cost_mult": 1.2},
    {"city": "Bursa", "country": "Türkiye", "cost_mult": 1.0},
    {"city": "Antalya", "country": "Türkiye", "cost_mult": 1.15},
    {"city": "Eskişehir", "country": "Türkiye", "cost_mult": 0.95},
    {"city": "Trabzon", "country": "Türkiye", "cost_mult": 0.9},
    {"city": "Gaziantep", "country": "Türkiye", "cost_mult": 0.9},
    {"city": "Adana", "country": "Türkiye", "cost_mult": 0.9},
    {"city": "Muğla (Bodrum)", "country": "Türkiye", "cost_mult": 1.3},
    {"city": "Diyarbakır", "country": "Türkiye", "cost_mult": 0.85},
    {"city": "Samsun", "country": "Türkiye", "cost_mult": 0.9}
]

ZODIAC_SIGNS = [
    "Koç ♈", "Boğa ♉", "İkizler ♊", "Yengeç ♋", "Aslan ♌", "Başak ♍",
    "Terazi ♎", "Akrep ♏", "Yay ♐", "Oğlak ♑", "Kova ♒", "Balık ♓"
]

PARENT_JOBS = [
    "Öğretmen", "Mühendis", "Doktor", "Esnaf", "Memur", "Avukat", "Hemşire",
    "Banka Müdürü", "Taksici", "Muhasebeci", "Polis", "Aşçı", "Mimar", "Ev Hanımı",
    "Müteahhit", "Eczacı", "Akademisyen", "Kuaför", "Fabrika İşçisi", "Diş Hekimi"
]

SCHOOL_CLUBS = [
    {"id": "robotics", "name": "💻 Bilişim ve Robotik Kulübü", "skill": "coding", "smarts_boost": 6},
    {"id": "theater", "name": "🎭 Tiyatro ve Drama Kulübü", "skill": "charisma", "smarts_boost": 3},
    {"id": "football", "name": "⚽ Okul Futbol / Voleybol Takımı", "skill": "athletics", "smarts_boost": 1},
    {"id": "music", "name": "🎸 Okul Rock & Müzik Grubu", "skill": "music", "smarts_boost": 2},
    {"id": "debate", "name": "🗣️ Münazara ve Hitabet Kulübü", "skill": "charisma", "smarts_boost": 5}
]

ILLNESSES = [
    {"name": "Mevsimsel Grip", "health_drain": 8, "happiness_drain": 6, "cure_chance": 0.90, "cost": 400},
    {"name": "Şiddetli Migren", "health_drain": 7, "happiness_drain": 14, "cure_chance": 0.75, "cost": 900},
    {"name": "Gastrit & Mide Ağrısı", "health_drain": 6, "happiness_drain": 10, "cure_chance": 0.80, "cost": 700},
    {"name": "Kronik Depresyon", "health_drain": 10, "happiness_drain": 22, "cure_chance": 0.65, "cost": 1800},
    {"name": "Yüksek Tansiyon", "health_drain": 13, "happiness_drain": 9, "cure_chance": 0.70, "cost": 1400},
    {"name": "Bel Fıtığı", "health_drain": 12, "happiness_drain": 12, "cure_chance": 0.60, "cost": 2500},
    {"name": "Astım Krizi", "health_drain": 15, "happiness_drain": 14, "cure_chance": 0.75, "cost": 2000},
    {"name": "Gıda Zehirlenmesi", "health_drain": 14, "happiness_drain": 18, "cure_chance": 0.92, "cost": 800},
    {"name": "Tükenmişlik Sendromu", "health_drain": 9, "happiness_drain": 25, "cure_chance": 0.60, "cost": 2200}
]

UNIVERSITIES = [
    {"id": "med", "name": "Tıp Fakültesi", "tuition_annual": 0, "smarts_required": 82, "duration": 6, "unlocked_category": "Tıp"},
    {"id": "eng", "name": "Bilgisayar & Yazılım Mühendisliği", "tuition_annual": 0, "smarts_required": 72, "duration": 4, "unlocked_category": "Teknoloji"},
    {"id": "law", "name": "Hukuk Fakültesi", "tuition_annual": 0, "smarts_required": 68, "duration": 4, "unlocked_category": "Hukuk"},
    {"id": "biz", "name": "İşletme & Ekonomi", "tuition_annual": 0, "smarts_required": 52, "duration": 4, "unlocked_category": "Kurumsal"},
    {"id": "arch", "name": "Mimarlık & Tasarım", "tuition_annual": 0, "smarts_required": 64, "duration": 4, "unlocked_category": "Tasarım"},
    {"id": "art", "name": "Konservatuvar & Sinema", "tuition_annual": 0, "smarts_required": 45, "duration": 4, "unlocked_category": "Sanat"}
]

PART_TIME_JOBS = [
    {"id": "pt_barista", "title": "Hafta Sonu Baristası", "salary": 96000, "min_age": 15},
    {"id": "pt_tutor", "title": "Matematik Özel Ders Öğretmeni", "salary": 135000, "min_age": 16},
    {"id": "pt_freelance", "title": "Freelance Web & Logo Tasarımcısı", "salary": 160000, "min_age": 15},
    {"id": "pt_dogwalker", "title": "Köpek Gezdiricisi", "salary": 75000, "min_age": 14}
]

BUSINESS_TYPES = [
    {"id": "cigkofte", "name": "Adıyaman Çiğköfte & Dürüm Bayisi", "sector": "Gıda", "cost": 350000, "base_profit": 140000},
    {"id": "coffee_shop", "name": "Üçüncü Nesil Butik Kahveci", "sector": "Kafe", "cost": 950000, "base_profit": 340000},
    {"id": "ecommerce", "name": "Moda & E-Ticaret Mağazası", "sector": "E-Ticaret", "cost": 1800000, "base_profit": 620000},
    {"id": "game_studio", "name": "Bağımsız Mobil Oyun Stüdyosu", "sector": "Teknoloji", "cost": 3500000, "base_profit": 1350000},
    {"id": "ai_startup", "name": "Yapay Zeka & FinTech Girişimi", "sector": "Teknoloji", "cost": 12000000, "base_profit": 4800000}
]

JOBS_DATABASE = [
    {
        "id": "waiter",
        "title": "Kafe Garsonu",
        "category": "Hizmet",
        "salary": 280000,
        "required_education": "Yok",
        "required_smarts": 20,
        "interview_q": "Müşteri kahvesinin soğuk olduğunu söyleyip kabalık yaparsa ne yaparsın?",
        "options": ["Hemen özür diler ve sıcağını getiririm", "Yüzüne kahveyi dökerim", "Patronu çağırıp bağırırım"],
        "correct_opt": 0
    },
    {
        "id": "courier",
        "title": "Moto Kurye",
        "category": "Hizmet",
        "salary": 420000,
        "required_education": "Yok",
        "required_smarts": 25,
        "interview_q": "Siparişi yetiştirmek için kırmızı ışıkta geçer misin?",
        "options": ["Trafik kurallarına uyar, güvenliği seçerim", "Elbette, hız her şeydir", "Kaldırımdan giderim"],
        "correct_opt": 0
    },
    {
        "id": "cashier",
        "title": "Süpermarket Kasiyeri",
        "category": "Hizmet",
        "salary": 300000,
        "required_education": "Yok",
        "required_smarts": 30,
        "interview_q": "Kasa gün sonunda 500 TL fazla çıkarsa ne yaparsın?",
        "options": ["Cebime atarım", "Müdüre ve muhasebeye tutanakla bildiririm", "Sonraki müşteriye hediye ederim"],
        "correct_opt": 1
    },
    {
        "id": "security",
        "title": "Özel Güvenlik Görevlisi",
        "category": "Hizmet",
        "salary": 360000,
        "required_education": "Lise",
        "required_smarts": 35,
        "interview_q": "Şüpheli bir paket gördüğünde ilk ne yaparsın?",
        "options": ["Açıp içine bakarım", "Alanı tahliye edip emniyeti ararım", "Görmezden gelirim"],
        "correct_opt": 1
    },
    {
        "id": "sales_rep",
        "title": "Kurumsal Satış Uzmanı",
        "category": "Kurumsal",
        "salary": 520000,
        "required_education": "Lise",
        "required_smarts": 50,
        "interview_q": "Müşteriyi ikna etmek için en etkili yol nedir?",
        "options": ["İhtiyaçlarını dinleyip uygun çözümü sunmak", "Sürekli arayıp bıkana kadar ısrar etmek", "Yalan vaatlerde bulunmak"],
        "correct_opt": 0
    },
    {
        "id": "accountant",
        "title": "Mali Müşavir / Denetçi",
        "category": "Kurumsal",
        "salary": 750000,
        "required_education": "Üniversite",
        "required_smarts": 65,
        "interview_q": "Şirket bilançosunda 100.000 TL açık fark edersen ne yaparsın?",
        "options": ["Detaylı denetim yapıp kaynağını raporlarım", "Göz ardı ederim", "Evrakları imha ederim"],
        "correct_opt": 0
    },
    {
        "id": "hr_specialist",
        "title": "İnsan Kaynakları Müdürü",
        "category": "Kurumsal",
        "salary": 680000,
        "required_education": "Üniversite",
        "required_smarts": 60,
        "interview_q": "İki departman şefi arasında kriz çıkarsa yaklaşımın ne olur?",
        "options": ["Taraf tutarım", "İki tarafı dinleyip objektif çözüm ararım", "İkisini de kovarım"],
        "correct_opt": 1
    },
    {
        "id": "junior_dev",
        "title": "Yazılım Geliştirici",
        "category": "Teknoloji",
        "salary": 850000,
        "required_education": "Lise",
        "required_smarts": 65,
        "interview_q": "Kodunda bir hata bulduğunda ve teslim süresi dolduğunda ne yaparsın?",
        "options": ["Hatayı gizleyip yayına alırım", "Ekip liderine bildirip hemen düzeltmeye çalışırım", "Bilgisayarı kapatıp kaçarım"],
        "correct_opt": 1
    },
    {
        "id": "senior_dev",
        "title": "Baş Yazılım Mimarı & CTO",
        "category": "Teknoloji",
        "salary": 1850000,
        "required_education": "Üniversite",
        "required_smarts": 80,
        "interview_q": "Sistem çöktüğünde ilk adımın ne olur?",
        "options": ["Hemen logları inceleyip geri alma (rollback) planı uygularım", "Suçu stajyere atarım", "Kahve içmeye giderim"],
        "correct_opt": 0
    },
    {
        "id": "nurse",
        "title": "Uzman Klinik Hemşiresi",
        "category": "Sağlık",
        "salary": 600000,
        "required_education": "Lise",
        "required_smarts": 60,
        "interview_q": "Hastanın damar yolunu açarken hasta korkup bağırırsa:",
        "options": ["Sakinleştirici ve şefkatli bir dille güven veririm", "Ben de bağırırım", "İğneyi fırlatırım"],
        "correct_opt": 0
    },
    {
        "id": "doctor_gp",
        "title": "Uzman Doktor",
        "category": "Tıp",
        "salary": 1400000,
        "required_education": "Üniversite",
        "required_smarts": 82,
        "interview_q": "Acile gelen kritik durumdaki hastada önceliğin nedir?",
        "options": ["Hayati fonksiyonları (solunum, dolaşım) stabilize etmek", "Kimlik bilgilerini sormak", "Sigortasını sorgulamak"],
        "correct_opt": 0
    },
    {
        "id": "surgeon",
        "title": "Prof. Dr. Beyin ve Kalp Cerrahı",
        "category": "Tıp",
        "salary": 2900000,
        "required_education": "Üniversite",
        "required_smarts": 88,
        "interview_q": "Ameliyat sırasında beklenmedik bir kanama başlarsa:",
        "options": ["Soğukkanlı kalıp hemostaz sağlar ve ekibi yönlendiririm", "Panik yapıp bayılırım", "Ameliyathaneyi terk ederim"],
        "correct_opt": 0
    },
    {
        "id": "lawyer",
        "title": "Ceza ve Ticaret Avukatı",
        "category": "Hukuk",
        "salary": 1150000,
        "required_education": "Üniversite",
        "required_smarts": 72,
        "interview_q": "Müvekkilin sana dürüst davranmadığını fark ettiğinde ne yaparsın?",
        "options": ["Kendisiyle yüzleşip delilleri yasal çerçevede sunarım", "Hakime hakaret ederim", "Karşı tarafa gizlice bilgi satarım"],
        "correct_opt": 0
    },
    {
        "id": "judge",
        "title": "Yargıtay Üyesi / Başhakim",
        "category": "Hukuk",
        "salary": 1950000,
        "required_education": "Üniversite",
        "required_smarts": 85,
        "interview_q": "Hukukta bir hakimin en temel ilkesi ne olmalıdır?",
        "options": ["Tarafsızlık, vicdan ve kanun önünde eşitlik", "Kendi şahsi menfaatleri", "Sosyal medyada popüler olmak"],
        "correct_opt": 0
    },
    {
        "id": "actor",
        "title": "Dizi & Sinema Oyuncusu",
        "category": "Sanat",
        "salary": 1600000,
        "required_education": "Lise",
        "required_smarts": 45,
        "interview_q": "Sette yönetmen sahneyi 10. kez tekrar çekmek isterse nasıl tepki verirsin?",
        "options": ["Profesyonelliğimi korur ve rolün hakkını veririm", "Senaryoyu yırtıp seti terk ederim", "Kameraları kırarım"],
        "correct_opt": 0
    },
    {
        "id": "pilot",
        "title": "Kaptan Havayolu Pilotu",
        "category": "Havacılık",
        "salary": 3200000,
        "required_education": "Üniversite",
        "required_smarts": 84,
        "interview_q": "Uçuş sırasında türbülansa girildiğinde ilk yapılması gereken nedir?",
        "options": ["Kemer ikaz ışıklarını yakıp uçağı güvenli irtifada tutmak", "Paraşütle atlamak", "Kokpitte çığlık atmak"],
        "correct_opt": 0
    },
    {
        "id": "entrepreneur",
        "title": "Uluslararası Holding CEO'su",
        "category": "Kurumsal",
        "salary": 5500000,
        "required_education": "Üniversite",
        "required_smarts": 88,
        "interview_q": "Büyük bir şirket krizini yönetirken liderin tutumu nasıl olmalı?",
        "options": ["Vizyoner, şeffaf ve kriz ekibini cesaretlendiren", "Sorumluluğu alt çalışanlara atan", "Şirketi kapatıp tatile çıkan"],
        "correct_opt": 0
    }
]

REAL_ESTATE_MARKET = [
    {"name": "1+1 Öğrenci Evi Dairesi", "price": 1250000, "annual_cost": 22000, "annual_rent": 135000},
    {"name": "2+1 Aile Apartman Dairesi", "price": 2950000, "annual_cost": 45000, "annual_rent": 250000},
    {"name": "3+1 Akıllı Rezidans Dairesi", "price": 6800000, "annual_cost": 95000, "annual_rent": 540000},
    {"name": "Çeşme/Bodrum Havuzlu Yazlık Villa", "price": 18500000, "annual_cost": 210000, "annual_rent": 1400000},
    {"name": "Boğaz Manzaralı Tarihi Yalı", "price": 85000000, "annual_cost": 800000, "annual_rent": 5500000}
]

VEHICLE_MARKET = [
    {"name": "Klasik Tofaş Şahin (1996)", "price": 140000, "annual_cost": 24000, "speed": "Klasik"},
    {"name": "Fiat Egea Sedan (2021)", "price": 680000, "annual_cost": 42000, "speed": "Ekonomik"},
    {"name": "TOGG T10X Elektrikli SUV", "price": 1650000, "annual_cost": 48000, "speed": "Yerli & Akıllı"},
    {"name": "BMW M4 Competition", "price": 5400000, "annual_cost": 180000, "speed": "Yüksek Performans"},
    {"name": "Porsche 911 Turbo S", "price": 14500000, "annual_cost": 420000, "speed": "Süper Spor"},
    {"name": "Özel Süper Yat (35 Metre)", "price": 48000000, "annual_cost": 2100000, "speed": "Deniz Lüksü"}
]

INITIAL_STOCKS = [
    {"symbol": "BISTECH", "name": "Bistech Yazılım & Teknoloji", "initial_price": 145.50, "volatility": 0.20},
    {"symbol": "PETRO", "name": "Marmara Enerji & Rafineri", "initial_price": 88.20, "volatility": 0.10},
    {"symbol": "HAVACILIK", "name": "Türk Gökleri Havayolları", "initial_price": 260.00, "volatility": 0.14},
    {"symbol": "MOONCOIN", "name": "Moon Kripto Token", "initial_price": 12.40, "volatility": 0.48},
    {"symbol": "ALTIN", "name": "Gram Altın Yatırım Fonu", "initial_price": 2850.00, "volatility": 0.07}
]

PET_BREEDS = [
    {"species": "Kedi", "breed": "Tekir Sokak Kedisi (Barınak)", "cost": 0},
    {"species": "Kedi", "breed": "Scottish Fold / British", "cost": 8000},
    {"species": "Köpek", "breed": "Golden Retriever", "cost": 14000},
    {"species": "Köpek", "breed": "Sivas Kangalı", "cost": 9000},
    {"species": "Kuş", "breed": "Konuşan Muhabbet Kuşu", "cost": 600}
]

PET_NAMES = [
    "Pamuk", "Duman", "Boncuk", "Zeytin", "Tarçın", "Gofret", "Mişa", "Karamel", "Çakıl", "Badi", "Pati", "Limon"
]

ACHIEVEMENT_DEFINITIONS = [
    {"id": "born", "icon": "🍼", "title": "Hayata Merhaba", "desc": "Dünyaya gözlerini açtın."},
    {"id": "first_love", "icon": "💘", "title": "İlk Kıvılcım", "desc": "İlk kez aşık oldun ve sevgili edindin."},
    {"id": "graduate", "icon": "🎓", "title": "Diplomalı Birey", "desc": "Üniversiteden başarıyla mezun oldun."},
    {"id": "driver", "icon": "🚗", "title": "Direksiyon Başı", "desc": "Ehliyet sınavını geçip sürücü belgesi aldın."},
    {"id": "married", "icon": "💍", "title": "Bir Yastıkta", "desc": "Evlendin ve yuva kurdun."},
    {"id": "child", "icon": "👶", "title": "Geleceğe Miras", "desc": "Bir çocuk sahibi oldun."},
    {"id": "homeowner", "icon": "🏠", "title": "Tapu Sahibi", "desc": "İlk gayrimenkulünü satın aldın."},
    {"id": "boss", "icon": "🏢", "title": "Kendi İşinin Patronu", "desc": "Bir şirket veya dükkan kurdun."},
    {"id": "millionaire", "icon": "💰", "title": "Milyoner Kulübü", "desc": "Net servetin 1.000.000 TL'yi aştı."},
    {"id": "multimillionaire", "icon": "💎", "title": "Zenginler Listesi", "desc": "Net servetin 20.000.000 TL'yi aştı."},
    {"id": "billionaire", "icon": "👑", "title": "İmparator", "desc": "Net servetin 100.000.000 TL'yi aştı."},
    {"id": "criminal", "icon": "🦹", "title": "Karanlık Yol", "desc": "Yasa dışı bir suça bulaştın."},
    {"id": "escaped", "icon": "🏃", "title": "Büyük Firar", "desc": "Cezaevinden kaçmayı başardın!"},
    {"id": "famous", "icon": "🌟", "title": "Şöhret Basamakları", "desc": "Sosyal medyada 100.000 takipçiyi geçtin."},
    {"id": "centenarian", "icon": "🌳", "title": "Asırlık Çınar", "desc": "100 yaşına kadar hayatta kaldın."}
]
