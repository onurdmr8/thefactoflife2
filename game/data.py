# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Zenginleştirilmiş Veri Kütüphanesi
İsimler, şehirler, meslekler, flört/aşk profilleri, randevu mekanları, düğün paketleri ve başarımlar.
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

# ----------------- İNSAN İLİŞKİLERİ & FLÖRT VERİTABANI -----------------

PERSONALITIES = [
    {"id": "Romantik", "emoji": "🌹", "loyalty_bias": 85, "crazy_bias": 25},
    {"id": "Eğlenceli", "emoji": "🎉", "loyalty_bias": 75, "crazy_bias": 45},
    {"id": "Entelektüel", "emoji": "📚", "loyalty_bias": 85, "crazy_bias": 20},
    {"id": "Sadık & Aileci", "emoji": "🏡", "loyalty_bias": 95, "crazy_bias": 15},
    {"id": "Hırslı & Kariyerist", "emoji": "💼", "loyalty_bias": 75, "crazy_bias": 30},
    {"id": "Maceracı", "emoji": "🏕️", "loyalty_bias": 70, "crazy_bias": 50},
    {"id": "Kıskanç & Tutkulu", "emoji": "🔥", "loyalty_bias": 80, "crazy_bias": 82},
    {"id": "Materyalist", "emoji": "💎", "loyalty_bias": 55, "crazy_bias": 60},
    {"id": "Çapkın & Özgür Ruhlu", "emoji": "🦋", "loyalty_bias": 40, "crazy_bias": 65}
]

INTERESTS_POOL = [
    "☕ Kahve & Kitap", "✈️ Seyahat & Kamp", "🎸 Canlı Müzik & Konser",
    "🏋️ Spor & Fitness", "🎬 Sinema & Tiyatro", "🍳 Gastronomi & Gurme",
    "💻 Teknoloji & Oyun", "📈 Borsa & Yatırım", "🐾 Hayvansever", "🪩 Gece Hayatı"
]

LOVE_LANGUAGES = [
    "Tatlı Sözler & İltifat",
    "Kaliteli Zaman",
    "Hediye & Sürprizler",
    "Romantik Temas & Tutku",
    "Güven & Sadakat"
]

COUPLE_VACATIONS = [
    {
        "id": "sapanca_bungalow",
        "name": "🌲 Sapanca Isıtmalı Havuzlu Bungalov",
        "desc": "Orman içinde şömine başında baş başa romantik hafta sonu.",
        "cost": 4500,
        "rel_boost": 18,
        "hap_boost": 16
    },
    {
        "id": "uludag_chalet",
        "name": "❄️ Uludağ Şömineli Dağ Evi Kaçamağı",
        "desc": "Karlar altında kayak ve sıcak çikolata keyfi.",
        "cost": 12000,
        "rel_boost": 25,
        "hap_boost": 22
    },
    {
        "id": "kas_yacht",
        "name": "⛵ Kaş & Göcek Özel Yat Turu",
        "desc": "Turkuaz koylarda sadece ikinize özel tekne tatili.",
        "cost": 28000,
        "rel_boost": 35,
        "hap_boost": 30
    },
    {
        "id": "paris_venice",
        "name": "🗼 Paris & Venedik Rüya Balayı Turu",
        "desc": "Eyfel Kulesi ve Venedik gondollarında unutulmaz aşk tatili.",
        "cost": 85000,
        "rel_boost": 50,
        "hap_boost": 42
    }
]

SOCIAL_HANGOUTS = [
    {
        "id": "coffee_gossip",
        "name": "☕ Kahve & Derin Dedikodu Seansı",
        "desc": "Saatlerce süren samimi sohbet ve dertleşme.",
        "cost": 400,
        "rel_boost": 15
    },
    {
        "id": "halisaha_match",
        "name": "⚽ Halı Saha / Derbi Maçı Gecesi",
        "desc": "Omuz omuza maç heyecanı ve sonrasında baklava ısmarlama.",
        "cost": 600,
        "rel_boost": 18
    },
    {
        "id": "boardgame_night",
        "name": "🎲 Kutu Oyunu & Ev Partisi",
        "desc": "Sabaha kadar kahkaha dolu oyun ve eğlence gecesi.",
        "cost": 800,
        "rel_boost": 20
    },
    {
        "id": "concert_buddy",
        "name": "🎸 Beraber Konsere & Festivale Git",
        "desc": "Favori sanatçınızı en önden birlikte dinleyin.",
        "cost": 2500,
        "rel_boost": 26
    }
]

DM_TOPICS = [
    {
        "id": "flirt_msg",
        "name": "😘 Romantik & Flörtöz Mesaj At",
        "my_text": "Bugün bütün gün aklımdan hiç çıkmadın, seni çok özledim ❤️✨",
        "partner_only": True
    },
    {
        "id": "funny_meme",
        "name": "😂 Komik Video / Esprili Caps Gönder",
        "my_text": "Şu videoya bak, tıpkı ikimiz! Gülmekten gözümden yaş geldi 😂🔥",
        "partner_only": False
    },
    {
        "id": "future_dream",
        "name": "🏡 Gelecek & Ortak Hayallerden Bahset",
        "my_text": "İleride seninle çok güzel günler göreceğimize tüm kalbimle inanıyorum 🌟",
        "partner_only": False
    },
    {
        "id": "jealous_check",
        "name": "🧐 'Neredesin, Kimlesin?' Diye Yokla",
        "my_text": "Son attığın hikayede yanındaki kimdi? Neredesin şu an? 🤨",
        "partner_only": True
    },
    {
        "id": "apology_msg",
        "name": "🕊️ Özür Dile & Gönlünü Al",
        "my_text": "Son zamanlarda seni kırdıysam özür dilerim, benim için çok değerlisin 🤍",
        "partner_only": False
    }
]

DATING_BIOS_BY_PERSONALITY = {
    "Romantik": [
        "Sahilde gün batımını izleyip şiir konuşabileceğim gerçek aşkı arıyorum 🌅",
        "Küçük sürprizlere, el ele yürüyüşlere ve samimiyete inanırım 🌹",
        "Kalbi güzel, sadık ve duygusal zekası yüksek biriyle tanışmak isterim ✨"
    ],
    "Eğlenceli": [
        "Hayat sıkılmak için çok kısa! Konserlere ve festivallere eşlik edecek suç ortağım nerede? 🎶",
        "Espri anlayışı yüksek, spontane planlara 'evet' diyen biriysen sağa kaydır 😄",
        "Komik olmayanlarla anlaşamıyorum, enerjisi yüksek olanlar yazsın ⚡"
    ],
    "Entelektüel": [
        "Üçüncü nesil kahve eşliğinde sinema, felsefe ve bilim konuşalım ☕📚",
        "Sığ sohbetlerden hoşlanmam; zeka en büyük çekiciliktir 🧠",
        "Müze gezileri, klasik müzik ve derin sohbetler arıyorum 🎻"
    ],
    "Sadık & Aileci": [
        "Ciddi düşünmeyenler zahmet etmesin. Huzurlu bir yuva ve güven arıyorum 🏡",
        "Pazar kahvaltılarını, aile sıcaklığını ve sadakati her şeyin üstünde tutarım 🤍",
        "Yalanı asla affetmem, ömürlük bir yol arkadaşı arıyorum 💍"
    ],
    "Hırslı & Kariyerist": [
        "Kariyer odaklıyım, vizyonu geniş ve başarılı insanlardan etkilenirim 🚀",
        "Birlikte imparatorluk kurabileceğim güçlü bir partner arıyorum 💼",
        "Zamanım değerli, ne istediğini bilen olgun kişiler tercihimdir ⌚"
    ],
    "Maceracı": [
        "Sırt çantamı alıp kamp yapmaya, yeni ülkeler keşfetmeye bayılırım 🏕️🌍",
        "Konfor alanından çıkabilen, adrenalin seven bir yol arkadaşı arıyorum 🪂",
        "Rutin hayattan sıkılanlar burada mı? Hadi yola çıkalım! 🚐"
    ],
    "Kıskanç & Tutkulu": [
        "Sevdiğimi sahiplenirim, gözü benden başkasını görmeyecek biri olmalı 🔥",
        "Mesajlara geç cevap verilmesinden ve ‘kanka’ ayağından nefret ederim 😤",
        "Ya tam seversin ya hiç! Tutkulu ve net bir ilişki istiyorum ❤️‍🔥"
    ],
    "Materyalist": [
        "Lüks restoranlar, şık hediyeler ve kaliteli yaşam tarzım vazgeçilmezimdir 💎💅",
        "Cimri insanlara tahammülüm yok, cömert ve centilmen/zarif olanlar gelsin 🥂",
        "Standartlarım yüksek, beni şımartacak birini arıyorum 🛍️"
    ],
    "Çapkın & Özgür Ruhlu": [
        "Kısıtlanmaya ve hesap sormalara gelemem, anın tadını çıkaralım 🦋",
        "Gece hayatı, hız ve eğlence... Fazla ciddiyet bana göre değil 🍸",
        "Bakalım beni kendine bağlayabilecek kadar etkileyici misin? 😉"
    ]
}

MEET_PLACES = [
    {
        "id": "library_cafe",
        "name": "📚 Kitapçı & Üçüncü Nesil Kahveci",
        "desc": "Entelektüel, romantik ve zeki insanlarla tanışma fırsatı.",
        "cost": 400,
        "preferred_personalities": ["Entelektüel", "Romantik", "Sadık & Aileci"]
    },
    {
        "id": "fitness_club",
        "name": "🏋️ Lüks Spor & Tenis Kulübü",
        "desc": "Fiziksel görünüşü yüksek, enerjik ve maceracı kişiler.",
        "cost": 1200,
        "preferred_personalities": ["Maceracı", "Eğlenceli", "Hırslı & Kariyerist"]
    },
    {
        "id": "night_club",
        "name": "🪩 Popüler Gece Kulübü & Lounge",
        "desc": "Eğlenceli, tutkulu veya çapkın karakterlerle hızlı flört.",
        "cost": 2500,
        "preferred_personalities": ["Eğlenceli", "Çapkın & Özgür Ruhlu", "Kıskanç & Tutkulu"]
    },
    {
        "id": "business_gala",
        "name": "🥂 VIP İş & Sanat Müzayedesi",
        "desc": "Varlıklı, kariyerist ve seçkin cemiyet üyeleri.",
        "cost": 8000,
        "preferred_personalities": ["Hırslı & Kariyerist", "Materyalist", "Entelektüel"],
        "wealth_boost": 35
    },
    {
        "id": "family_match",
        "name": "👵 Aile & Akraba Tavsiyesi (Görücü Usulü)",
        "desc": "Annenin/ailenin kefil olduğu, sadık ve evliliğe uygun kısmetler.",
        "cost": 0,
        "preferred_personalities": ["Sadık & Aileci", "Romantik", "Hırslı & Kariyerist"]
    }
]

DATE_VENUES = [
    {
        "id": "tea_simit",
        "name": "☕ Sahilde Çay, Simit ve Gün Batımı",
        "desc": "Sıcak, samimi ve mütevazı bir sahil yürüyüşü.",
        "cost": 500,
        "rel_boost": 10,
        "best_for": ["Romantik", "Sadık & Aileci", "Entelektüel"],
        "disliked_by": ["Materyalist"]
    },
    {
        "id": "cinema",
        "name": "🎬 Sinema & Kahve Randevusu",
        "desc": "Vizyon filmi sonrası üçüncü nesil kahvecide derin sohbet.",
        "cost": 1500,
        "rel_boost": 14,
        "best_for": ["Entelektüel", "Eğlenceli", "Romantik"],
        "disliked_by": []
    },
    {
        "id": "concert",
        "name": "🎸 Canlı Konser & Festival Gecesi",
        "desc": "Yüksek enerji, müzik ve dans dolu unutulmaz bir gece.",
        "cost": 3500,
        "rel_boost": 18,
        "best_for": ["Eğlenceli", "Maceracı", "Çapkın & Özgür Ruhlu"],
        "disliked_by": []
    },
    {
        "id": "bosphorus_dinner",
        "name": "🕯️ Boğaz'da Mum Işığında Lüks Restoran",
        "desc": "Boğaz manzarasında keman eşliğinde romantik akşam yemeği.",
        "cost": 8000,
        "rel_boost": 24,
        "best_for": ["Romantik", "Materyalist", "Hırslı & Kariyerist", "Kıskanç & Tutkulu"],
        "disliked_by": []
    },
    {
        "id": "camping_trip",
        "name": "🏕️ Doğa & Yıldızlar Altında Glamping",
        "desc": "Şehirden uzakta kamp ateşi başında yıldızları izleme.",
        "cost": 12000,
        "rel_boost": 26,
        "best_for": ["Maceracı", "Romantik", "Eğlenceli"],
        "disliked_by": ["Materyalist"]
    },
    {
        "id": "cappadocia",
        "name": "🎈 Kapadokya Balon Turu & VIP Suit",
        "desc": "Gün doğumunda sıcak hava balonu ve taş konakta masalsı hafta sonu.",
        "cost": 35000,
        "rel_boost": 38,
        "best_for": ["Romantik", "Materyalist", "Maceracı", "Kıskanç & Tutkulu", "Sadık & Aileci"],
        "disliked_by": []
    }
]

ROMANTIC_GIFTS = [
    {"id": "roses", "name": "🌹 Kırmızı Gül Buketi & Şiir Kartı", "cost": 1000, "rel_boost": 12},
    {"id": "perfume", "name": "🍫 Belçika Çikolatası & Özel Parfüm", "cost": 4500, "rel_boost": 18},
    {"id": "smartphone", "name": "📱 Son Model Akıllı Telefon", "cost": 45000, "rel_boost": 28},
    {"id": "diamond_set", "name": "💎 Pırlanta Kolye & Lüks Saat", "cost": 120000, "rel_boost": 40},
    {"id": "luxury_car_gift", "name": "🚗 Kurdeleli Spor Otomobil Sürprizi", "cost": 850000, "rel_boost": 65}
]

ENGAGEMENT_RINGS = [
    {"id": "silver_ring", "name": "🥈 Zarif Gümüş Alyans", "cost": 5000, "bonus_chance": 0.05},
    {"id": "gold_solitaire", "name": "💍 Klasik Altın Tektaş Yüzük", "cost": 35000, "bonus_chance": 0.25},
    {"id": "emerald_platinum", "name": "💚 Platin Zümrüt & Pırlanta Yüzük", "cost": 75000, "bonus_chance": 0.38},
    {"id": "royal_diamond", "name": "👑 3 Karat Kraliyet Safir & Pırlantası", "cost": 150000, "bonus_chance": 0.55}
]

WEDDING_VENUES = [
    {
        "id": "city_hall",
        "name": "🏛️ Sade Nikah Dairesi Töreni",
        "desc": "Yakın aile ve şahitler huzurunda sade ve ekonomik nikah.",
        "cost": 5000,
        "min_gifts": 10000,
        "max_gifts": 35000,
        "hap_boost": 15
    },
    {
        "id": "wedding_hall",
        "name": "💃 Geleneksel Salon Düğünü & Takı Merasimi",
        "desc": "Halaylar, altınlar ve kalabalık akrabalarla görkemli salon düğünü.",
        "cost": 60000,
        "min_gifts": 85000,
        "max_gifts": 240000,
        "hap_boost": 30
    },
    {
        "id": "country_beach",
        "name": "🌿 Bohem Kır & Sahil Düğünü",
        "desc": "Deniz kenarında gün batımında canlı orkestralı romantik düğün.",
        "cost": 140000,
        "min_gifts": 160000,
        "max_gifts": 420000,
        "hap_boost": 40
    },
    {
        "id": "palace_wedding",
        "name": "🏰 Boğaz'da Tarihi Yalı & Saray Düğünü",
        "desc": "Cemiyet hayatının konuştuğu, havai fişekli efsanevi saray düğünü.",
        "cost": 300000,
        "min_gifts": 350000,
        "max_gifts": 950000,
        "hap_boost": 50
    }
]

# ----------------- EĞİTİM, İŞ VE DİĞER VERİLER -----------------

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
        "id": "pop_singer",
        "title": "Pop & Rap Müzik Yıldızı",
        "category": "Sanat",
        "salary": 2400000,
        "required_education": "Yok",
        "required_smarts": 35,
        "interview_q": "Stüdyoda prodüktör şarkının nakaratını daha enerjik okumanı isterse ne yaparsın?",
        "options": ["Mikrofona geçip tüm ruhumla en iyi vokali kaydederim", "Mikrofonu yere atarım", "Stüdyoyu terk ederim"],
        "correct_opt": 0
    },
    {
        "id": "pro_footballer",
        "title": "Süper Lig Profesyonel Futbolcusu",
        "category": "Spor",
        "salary": 4200000,
        "required_education": "Yok",
        "required_smarts": 30,
        "interview_q": "Derbi maçının 90. dakikasında takımın penaltı kazandı, topun başına geçerken ne düşünürsün?",
        "options": ["Soğukkanlılığımı korur, köşeye sert ve net bir vuruş yaparım", "Heyecandan topu tribüne dikerim", "Hakemle tartışırım"],
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

POLITICAL_OFFICES = [
    {
        "id": "muhtar",
        "title": "🏘️ Mahalle Muhtarı",
        "min_age": 18,
        "campaign_cost": 15000,
        "salary": 320000,
        "req_edu": "Yok",
        "desc": "Mahallenin sorunlarını çöz, sosyal yardımları organize et ve siyasete ilk adımını at."
    },
    {
        "id": "district_mayor",
        "title": "🏛️ İlçe Belediye Başkanı",
        "min_age": 25,
        "campaign_cost": 150000,
        "salary": 950000,
        "req_edu": "Lise",
        "desc": "İlçenin imar, kültür, park ve altyapı bütçesini yönet."
    },
    {
        "id": "metro_mayor",
        "title": "🌆 Büyükşehir Belediye Başkanı",
        "min_age": 28,
        "campaign_cost": 850000,
        "salary": 2200000,
        "req_edu": "Üniversite",
        "desc": "Milyonluk metropolün ulaşım, metro ve dev yatırımlarını yönet."
    },
    {
        "id": "mp",
        "title": "⚖️ Milletvekili & Parti Sözcüsü",
        "min_age": 25,
        "campaign_cost": 1500000,
        "salary": 3200000,
        "req_edu": "Üniversite",
        "desc": "Meclis kürsüsünde yasaları oyla, ülke gündemini belirle."
    },
    {
        "id": "president",
        "title": "👑 Cumhurbaşkanı",
        "min_age": 35,
        "campaign_cost": 8000000,
        "salary": 7500000,
        "req_edu": "Üniversite",
        "desc": "Devletin en üst makamı! Ülke ekonomisini ve zirveyi yönet."
    }
]

AUCTION_ITEMS = [
    {
        "id": "patek_watch",
        "name": "⌚ Klasik İsviçre Patek Saat Koleksiyonu",
        "price": 650000,
        "desc": "Her yıl değer kazanan nadir üretim mekanik saat."
    },
    {
        "id": "shelby_classic",
        "name": "🏎️ 1967 Klasik Ford Mustang Shelby",
        "price": 3200000,
        "desc": "Müzayede kondisyonunda koleksiyonluk klasik spor otomobil."
    },
    {
        "id": "ottoman_painting",
        "name": "🖼️ Osman Hamdi Bey Dönemi Nadir Tablo",
        "price": 7500000,
        "desc": "Sanat tarihinin en değerli orijinal tuval eserlerinden biri."
    },
    {
        "id": "royal_dagger",
        "name": "💎 Topkapı İşi Zümrüt Hançer (Antika)",
        "price": 15000000,
        "desc": "Paha biçilemez zümrüt ve elmas işlemeli tarihi eser."
    },
    {
        "id": "mars_meteorite",
        "name": "☄️ Nadir Mars Meteoriti & Elmas Küre",
        "price": 35000000,
        "desc": "Dünyada sadece sayılı milyarderlerin kasasında bulunan uzay hazinesi."
    }
]

OUTFIT_STYLES = [
    {
        "id": "casual",
        "name": "👕 Günlük & Rahat",
        "cost": 0,
        "looks_boost": 2,
        "charisma_boost": 2,
        "desc": "Rahat, sade ve samimi bir günlük stil."
    },
    {
        "id": "streetwear",
        "name": "🧥 Sokak Stili & Sneaker (Streetwear)",
        "cost": 6500,
        "looks_boost": 7,
        "charisma_boost": 6,
        "desc": "Genç, enerjik ve sosyal medyada dikkat çeken modern kombin."
    },
    {
        "id": "bohemian",
        "name": "🎸 Bohem & Sanatçı Ruhu",
        "cost": 12000,
        "looks_boost": 9,
        "charisma_boost": 10,
        "desc": "Entelektüel ve romantik karakterlerin hayran kaldığı özgün tarz."
    },
    {
        "id": "classic_suit",
        "name": "🤵 Klasik & Kurumsal Şıklık",
        "cost": 35000,
        "looks_boost": 14,
        "charisma_boost": 15,
        "desc": "İş dünyasında, siyasette ve aile tanışmalarında tam puan kazandıran takım/abiye."
    },
    {
        "id": "luxury_designer",
        "name": "💎 Ultra Lüks İtalyan Tasarım & Saat",
        "cost": 180000,
        "looks_boost": 22,
        "charisma_boost": 22,
        "desc": "Cemiyet hayatında, KısmetApp VIP'te ve galalarda tüm gözleri üzerine çevirir!"
    }
]

EXAM_QUESTIONS = {
    "yks": [
        {
            "q": "YKS Türkçe & Paragraf Sorusu: 'Bir eserin kalıcılığı, yazıldığı çağın ruhunu aşabilmesine bağlıdır.' cümlesinde vurgulanan temel düşünce nedir?",
            "options": [
                "Gelecek kuşaklara da hitap edebilen evrensel nitelik taşıması",
                "Sadece kendi döneminin sorunlarını anlatması",
                "Çok uzun ve ağır bir dille yazılması"
            ],
            "correct": 0
        },
        {
            "q": "YKS Matematik Sorusu: Bir araç 240 km'lik yolun yarısını saatte 60 km, diğer yarısını saatte 40 km hızla giderse toplam yolculuk kaç saat sürer?",
            "options": ["4 Saat", "5 Saat", "6 Saat"],
            "correct": 1
        }
    ],
    "kpss": [
        {
            "q": "KPSS Genel Kültür & Vatandaşlık Sorusu: Türkiye Cumhuriyeti Anayasası'na göre yasama yetkisi Türk Milleti adına hangi kuruma aittir?",
            "options": [
                "Türkiye Büyük Millet Meclisi (TBMM)",
                "Merkez Bankası",
                "Belediye Meclisleri"
            ],
            "correct": 0
        },
        {
            "q": "KPSS Tarih Sorusu: Cumhuriyetin ilanından hemen önce imzalanarak Türkiye'nin bağımsızlığını tüm dünyaya kabul ettiren barış antlaşması hangisidir?",
            "options": ["Mondros Mütarekesi", "Lozan Barış Antlaşması", "Sevr Antlaşması"],
            "correct": 1
        }
    ]
}

BAND_GENRES = [
    {"id": "anadolu_rock", "name": "🎸 Anadolu Rock Grubu", "cost": 15000, "desc": "Elektro bağlama ve güçlü gitar riffleriyle stadyumları coştur."},
    {"id": "trap_rap", "name": "🎤 Trap & Rap Kolektifi", "cost": 12000, "desc": "Dijital listelerde milyonlarca dinlenen sokak ritimleri."},
    {"id": "indie_alt", "name": "🎹 Alternatif & Indie Sahnesi", "cost": 10000, "desc": "Festivallerin ve üniversite şenliklerinin vazgeçilmez grubu."},
    {"id": "pop_orchestra", "name": "🎻 Akustik Pop & Caz Orkestrası", "cost": 20000, "desc": "Seçkin kulüplerde ve dev açıkhava sahnelerinde zarif müzik."}
]

COUPLE_BUSINESS_TYPES = [
    {"id": "boutique_cafe", "name": "☕ Üçüncü Nesil Ortak Butik Kafe", "cost": 180000, "annual_profit": 95000},
    {"id": "fashion_atelier", "name": "👗 Moda & Gelinlik Tasarım Atölyesi", "cost": 350000, "annual_profit": 185000},
    {"id": "jewelry_brand", "name": "💎 E-Ticaret Takı & Kozmetik Markası", "cost": 600000, "annual_profit": 310000}
]

DIVORCE_LAWYERS = [
    {"id": "baro", "name": "⚖️ Nöbetçi Baro Avukatı", "cost": 5000, "win_bonus": 0.0, "desc": "Standart savunma yapar, hakimin takdirine kalırsın."},
    {"id": "specialist", "name": "💼 Uzman Aile & Boşanma Avukatı", "cost": 65000, "win_bonus": 0.25, "desc": "Mal paylaşımı ve nafaka pazarlığında elini güçlendirir."},
    {"id": "shark", "name": "🦈 Cemiyetin Ünlü 'Köpekbalığı' Avukatı", "cost": 250000, "win_bonus": 0.55, "desc": "En zorlu davalarda bile karşı taraftan tazminat koparır!"}
]

SPORTS_CLUBS = [
    {"id": "anadolu_fk", "name": "⚽ Anadolu Yıldızspor", "sport": "Futbol", "tier": "Süper Lig", "salary": 1850000, "req_ath": 50},
    {"id": "istanbul_dev", "name": "🦁 İstanbul Devleri SK", "sport": "Futbol", "tier": "Süper Lig Şampiyonluk Adayı", "salary": 4500000, "req_ath": 72},
    {"id": "avrupa_real", "name": "👑 Real Madrid / Avrupa Devi", "sport": "Futbol", "tier": "Şampiyonlar Ligi Devi", "salary": 14500000, "req_ath": 88},
    {"id": "euroleague_bask", "name": "🏀 İstanbul EuroLeague Basketbol", "sport": "Basketbol", "tier": "EuroLeague", "salary": 3800000, "req_ath": 70}
]

RELATIONSHIP_CONFLICTS = [
    {
        "id": "bayram_family",
        "title": "🍬 Bayramda Kimin Ailesine Gidilecek?",
        "desc": "Kurban/Ramazan bayramı sabahı partnerin kaşlarını çattı: 'Her bayram senin ailene gidiyoruz, bu bayram kesinlikle önce benim annemlere gideceğiz!'",
        "options": [
            {"id": "compromise", "text": "🤝 'Önce senin ailene gidelim, akşam da benimkilere geçeriz' diyerek uzlaş.", "style": "Uyumlu"},
            {"id": "fight_back", "text": "😤 'Benim ailem büyük, geleneklerimize saygı duy!' diyerek sesini yükselt.", "style": "Sert"},
            {"id": "sweet_gift", "text": "🎁 'İki tarafa da gideceğiz ama önce sana bayram hediyesi alalım' de (10.000 TL).", "style": "Jest"}
        ]
    },
    {
        "id": "social_media_likes",
        "title": "🔥 Sosyal Medya & Eski Sevgili Beğenisi",
        "desc": "Partnerin telefonunu önüne koydu: 'Instagram'da eski sevgilinin/okul arkadaşının tatil fotoğrafına alev (🔥) atmışsın! Bu ne rezalet?!'",
        "options": [
            {"id": "apologize_block", "text": "🕊️ 'Haklısın düşüncesizlik ettim' deyip partnerinin önünde takipten çık.", "style": "Özür"},
            {"id": "gaslight", "text": "📱 'Sadece arkadaşça bir beğeni, abartıyorsun ve bana güvenmiyorsun!' de.", "style": "Savunma"},
            {"id": "counter_attack", "text": "🔥 'Senin geçen hafta beğendiğin fitness antrenörünü konuşalım istersen!' de.", "style": "Karşı Atak"}
        ]
    },
    {
        "id": "budget_spending",
        "title": "💳 Kredi Kartı Ekstresi & Lüks Harcama Krizi",
        "desc": "Aylık hesap ekstresi geldiğinde partnerin şok oldu: 'Bu ay bütçemizi aşmışsın! Sürekli dışarıda yemek ve lüks harcamalar yapıyoruz!'",
        "options": [
            {"id": "tighten_belt", "text": "📉 'Haklısın canım, gelecek ay tasarruf planı yapalım ve bütçeyi toparlayalım.'", "style": "Mali Disiplin"},
            {"id": "my_money", "text": "💰 'Kendi kazandığım paranın hesabını sana mı vereceğim?!' diyerek çıkış.", "style": "Bireysel"},
            {"id": "spa_treat", "text": "💆 'Stresliyiz, gel bu hafta sonu ikimize güzel bir masaj/tatil ayarlayayım.' (8.000 TL)", "style": "Kaçış"}
        ]
    },
    {
        "id": "night_out",
        "title": "🌙 Arkadaşlarla Gece Gezmesi & Eve Geç Gelme",
        "desc": "Arkadaşlarınla gece 02:30'a kadar dışarıda takıldın. Eve girdiğinde partnerin ayakta kollarını bağlamış seni bekliyordu!",
        "options": [
            {"id": "warm_hug", "text": "🤗 Çiçekle sarıl, 'Arkadaşlarla muhabbet uzadı ama aklım hep sendeydi' de.", "style": "Şefkat"},
            {"id": "defend_space", "text": "🚶 'Beni bu kadar kısıtlama, bazen kafamı dağıtmaya ihtiyacım var!' de.", "style": "Özgürlük"},
            {"id": "sleep_ignore", "text": "🥱 Tartışmaya girmeden 'Çok uykum var, sabah konuşuruz' deyip uyu.", "style": "Geçiştirme"}
        ]
    }
]

COMPANY_EXPANSION_ACTIONS = [
    {"id": "marketing", "name": "📣 Viral Reklam & Influencer Kampanyası", "cost": 150000, "desc": "Yıllık kârı %35 sıçratır ve müşteri trafiğini patlatır."},
    {"id": "rd_patent", "name": "💡 AR-GE & Yeni Nesil Ürün Lansmanı", "cost": 300000, "desc": "Şirket değerlemesini %40 artırır ve sektörel patent kazandırır."},
    {"id": "employee_bonus", "name": "🎁 Çalışanlara Çift Maaş İkramiyesi & Moral Partisi", "cost": 85000, "desc": "Çalışan sadakatini ve şirket itibarını zirveye (%100) çıkarır."},
    {"id": "open_branch", "name": "🏬 Büyükşehirde Yeni Şube Açma", "cost": 500000, "desc": "Yıllık kâra doğrudan +₺220.000/yıl kalıcı katkı sağlar."}
]

CAR_CARE_ACTIONS = [
    {"id": "maintenance", "name": "🔧 Sanayi / Yetkili Servis Bakımı", "cost": 18000, "desc": "Aracın kondisyonunu %100 yapar, yolda kalma ve kaza riskini sıfırlar."},
    {"id": "insurance", "name": "🛡️ Full Kasko & Genişletilmiş Sigorta", "cost": 25000, "desc": "Aracına 1 yıllık kasko güvencesi sağlar, olası kazalarda tek kuruş ödemezsin."},
    {"id": "highway_speed", "name": "🏎️ Otobanda Gece Gazlama & Adrenalin", "cost": 2500, "desc": "Tüm stresi sıfırlar, mutluluk +25 kazandırır! (Radar veya kaza riski taşır)"}
]

TENANT_MANAGEMENT_ACTIONS = [
    {"id": "demand_letter", "name": "📜 Noterden Resmi İhtarname Çek", "cost": 3500, "desc": "Gecikmiş kirayı yasal faiziyle tahsil eder, kiracıyı hizaya sokar."},
    {"id": "friendly_talk", "name": "🤝 Yüz Yüze Görüş & Tatlıya Bağla", "cost": 0, "desc": "Ufak bir indirim veya vadeyle kiracının gönlünü alır, sorunları çözer."},
    {"id": "eviction_lawsuit", "name": "⚖️ Tahliye Davası Aç & Tahliye Ettir", "cost": 15000, "desc": "Sorunlu kiracıyı polis/icra eşliğinde tahliye eder ve yeni güvenilir kiracı bulur."}
]

WELLNESS_SERVICES = [
    {"id": "psychologist", "name": "🧠 Uzman Klinik Psikoloğu Terapi Seansı", "cost": 4500, "desc": "Tüm stresi ve tükenmişlik sendromunu sıfırlar, ruh halini tazeleyip mutluluk verir (+22)."},
    {"id": "library", "name": "📚 Şehir Kütüphanesinde Kitap Okuma & Araştırma", "cost": 0, "desc": "Zihnini dinlendirir, genel kültür ve zekanı geliştirir (+6 Zeka)."},
    {"id": "surgery", "name": "🏥 Özel Hastanede Uzman Cerrah Operasyonu", "cost": 85000, "desc": "Tedavi edilemeyen kronik ve ağır hastalıkları profesör hekimlerle ameliyat edip kalıcı iyileştirir."}
]

# ----------------- DETAYLI İLİŞKİ SİSTEMLERİ: ÖP, DATE, KAVGA -----------------

KISS_STYLES = [
    {
        "id": "forehead",
        "name": "🕊️ Alnından Şefkatle Öp",
        "desc": "Güven, huzur ve koruyucu sevgi hissettirir. Sadık ve romantik partnerler bayılır.",
        "rel_boost": 14,
        "loyalty_boost": 8,
        "stress_relief": 15,
        "preferred_personalities": ["Sadık & Aileci", "Romantik"],
        "icon": "🕊️"
    },
    {
        "id": "cheek",
        "name": "😊 Yanağından Masum Bir Buse Al",
        "desc": "Kalp atışlarını hızlandıran tatlı ve samimi bir yakınlaşma.",
        "rel_boost": 10,
        "loyalty_boost": 4,
        "stress_relief": 8,
        "preferred_personalities": ["Romantik", "Entelektüel"],
        "icon": "😊"
    },
    {
        "id": "lips_gentle",
        "name": "💋 Dudağına Masum ve Zarif Bir Öpücük Kondur",
        "desc": "Göz göze gelip kalpleri titreten romantik bir kıvılcım.",
        "rel_boost": 18,
        "loyalty_boost": 6,
        "stress_relief": 16,
        "preferred_personalities": ["Romantik", "Sadık & Aileci", "Hırslı & Kariyerist"],
        "icon": "💋"
    },
    {
        "id": "lips_passionate",
        "name": "🔥 Gözlerinin İçine Bakıp Tutkuyla Dudaklarına Yapış",
        "desc": "Nefes kesici, derin ve ateşli bir öpüşme. Karizma ve çekicilik patlaması!",
        "rel_boost": 25,
        "loyalty_boost": 8,
        "stress_relief": 22,
        "preferred_personalities": ["Çılgın & Maceracı", "Romantik", "Materyalist"],
        "icon": "🔥"
    },
    {
        "id": "neck_whisper",
        "name": "🫦 Belinden Kavrayıp Boynundan Öp & Kulağına Fısılda",
        "desc": "Tensel çekimi ve heyecanı zirveye çıkaran cesur bir hamle.",
        "rel_boost": 22,
        "loyalty_boost": 5,
        "stress_relief": 20,
        "preferred_personalities": ["Çılgın & Maceracı", "Hırslı & Kariyerist"],
        "icon": "🫦"
    },
    {
        "id": "hand_gentleman",
        "name": "✨ Elini Nazikçe Kaldırıp Avuç İçini Öp",
        "desc": "Zarafet, saygı ve hayranlık dolu asil bir jest.",
        "rel_boost": 15,
        "loyalty_boost": 7,
        "stress_relief": 12,
        "preferred_personalities": ["Entelektüel", "Romantik", "Sadık & Aileci"],
        "icon": "✨"
    }
]

DATE_OUTFITS = [
    {
        "id": "formal_glam",
        "name": "👔 / 👗 Jilet Gibi Şık (Takım Elbise / Şık Gece Elbisesi)",
        "desc": "Lüks restoranlar ve elit mekanlar için kusursuz prestij.",
        "cost": 2500,
        "style": "Lüks & Prestij",
        "suitable_venues": ["bosphorus_dinner", "cappadocia"]
    },
    {
        "id": "cool_trendy",
        "name": "🕶️ Cool & Trend Sokak Şıklığı (Deri Ceket / Özel Parfüm)",
        "desc": "Konserler, kokteyl barlar ve genç mekanlar için çekici ve havalı.",
        "cost": 1000,
        "style": "Havalı & Çekici",
        "suitable_venues": ["concert", "cinema", "bosphorus_dinner"]
    },
    {
        "id": "smart_casual",
        "name": "👕 Sade, Temiz & Doğal (Kot Pantolon, Beyaz Gömlek/Tişört)",
        "desc": "Sahil yürüyüşleri ve samimi sohbetler için abartısız şıklık.",
        "cost": 0,
        "style": "Doğal & Samimi",
        "suitable_venues": ["tea_simit", "cinema", "camping_trip"]
    },
    {
        "id": "sloppy_tracksuit",
        "name": "🩳 Özensiz & Salaş (Eski Eşofman & Terlik)",
        "desc": "Hiç özenilmemiş, partneri şoke edecek bir felaket tercihi.",
        "cost": 0,
        "style": "Özensiz / Rezalet",
        "suitable_venues": []
    }
]

DATE_GREETINGS = [
    {
        "id": "flower_chocolate",
        "name": "🌹 Kırmızı Gül & El Yapımı Çikolata ile Karşıla (850 TL)",
        "desc": "Romantik ve zarif bir karşılama jesti.",
        "cost": 850,
        "reaction": "Gözleri parıldayarak gülü kokladı: 'Çok incesin, bunu hiç beklemiyordum!' diyerek boynuna sarıldı."
    },
    {
        "id": "passionate_hug",
        "name": "🫂 Gözlerinin İçine Bakıp Sıcacık Sarıl & İltifat Et",
        "desc": "Doğal, samimi ve sımsıcak bir ilk temas.",
        "cost": 0,
        "reaction": "Sana sımsıkı sarıldı, kokunu içine çekti: 'Seni görmek o kadar iyi geldi ki...' dedi."
    },
    {
        "id": "flirty_hand_kiss",
        "name": "✨ Elini Nazikçe Öp: 'Bu Akşam Büyüleyici Görünüyorsun'",
        "desc": "Centilmen, flörtöz ve karizmatik bir hareket.",
        "cost": 0,
        "reaction": "Yanakları hafifçe kızardı ve gülümsedi: 'Sen de fena değilsin hani...' dedi."
    },
    {
        "id": "casual_smile",
        "name": "👋 Havalı Bir Gülümsemeyle 'Hoş Geldin, Hadi Geçelim' De",
        "desc": "Sakin, dengeli ve mesafeli bir merhaba.",
        "cost": 0,
        "reaction": "'Hoş bulduk!' diyerek neşeyle masaya doğru yöneldi."
    }
]

DATE_CONVERSATION_TOPICS = [
    {
        "id": "topic_destiny",
        "question": "Sence iki insanın karşılaşması sadece bir tesadüf mü, yoksa kaderin bir oyunu mu?",
        "options": [
            {
                "id": "destiny_romantic",
                "text": "Binlerce insanın arasında gözlerimizin buluşması asla tesadüf olamaz. Biz bir araya gelmeliydik.",
                "type": "Romantik",
                "favorite_personalities": ["Romantik", "Sadık & Aileci", "Kıskanç & Tutkulu"],
                "partner_reply": "Gözleri nemlendi ve gülümsedi: 'Ben de aynı şeyi hissediyordum... Kalbimi erittin.'"
            },
            {
                "id": "destiny_action",
                "text": "Tesadüf sadece kapıyı aralar; asıl önemli olan o kapıdan cesaretle geçip elini tutabilmek.",
                "type": "Karizmatik",
                "favorite_personalities": ["Hırslı & Kariyerist", "Entelektüel", "Maceracı"],
                "partner_reply": "Tebessümle kadehini kaldırdı: 'İşte tam duymak istediğim vizyoner ve cesur yanıt!'"
            },
            {
                "id": "destiny_humor",
                "text": "Bence kader 'Bu ikisi bir araya gelip sabaha kadar gülsün' dedi, gerisi teferruat!",
                "type": "Eğlenceli",
                "favorite_personalities": ["Eğlenceli", "Çapkın & Özgür Ruhlu"],
                "partner_reply": "Kahkahayı bastı: 'İlahi! Senin yanında somurtmak imkansız gerçekten :D'"
            },
            {
                "id": "destiny_cynic",
                "text": "Algoritmalar ve istatistik işte, fazla mistik anlamlar yükleyip hayal dünyasında yaşamaya gerek yok.",
                "type": "Soğuk",
                "favorite_personalities": ["Materyalist"],
                "partner_reply": "Kaşlarını kaldırdı ve biraz soğuk baktı: 'Biraz fazla duygusuz bir yaklaşım değil mi?'"
            }
        ]
    },
    {
        "id": "topic_passion",
        "question": "Eğer yarın sabah sınırsız paran ve zamanın olsa, hayatını ilk neye adardın?",
        "options": [
            {
                "id": "passion_world_travel",
                "text": "Senin elinden tutar, tek bir sırt çantasıyla tüm dünyayı ve okyanusları keşfe çıkardım.",
                "type": "Maceracı",
                "favorite_personalities": ["Maceracı", "Romantik", "Çapkın & Özgür Ruhlu"],
                "partner_reply": "Heyecanla öne doğru eğildi: 'İnanılmaz! Bu benim de en büyük çocukluk hayalim!'"
            },
            {
                "id": "passion_empire",
                "text": "Tüm sektörleri domine eden devasa bir marka kurar, gücümü ve vizyonumu kanıtlardım.",
                "type": "Hırslı",
                "favorite_personalities": ["Hırslı & Kariyerist", "Materyalist"],
                "partner_reply": "Gözlerinde saygı dolu bir ışıltı belirdi: 'Azimli ve hedefleri olan insanlara bayılıyorum.'"
            },
            {
                "id": "passion_quiet_home",
                "text": "Ege'de taş bir ev alır; sevdiğimle şömine başında kitap okur, sakin ve huzurlu yaşardım.",
                "type": "Huzurlu",
                "favorite_personalities": ["Sadık & Aileci", "Entelektüel"],
                "partner_reply": "İç çekerek elini göğsüne koydu: 'Huzur... Dünyadaki her şeyden daha kıymetli.'"
            },
            {
                "id": "passion_lazy",
                "text": "Akşama kadar yatar, televizyon izlerdim herhalde. Yorulmaya hiç niyetim yok.",
                "type": "Tembel",
                "favorite_personalities": [],
                "partner_reply": "Hafifçe gözlerini devirdi: 'Demek hiç tutkun yok... Biraz üzücü.'"
            }
        ]
    },
    {
        "id": "topic_redflag",
        "question": "Bir ilişkide senin için 'Asla affetmem, kapıyı çarpar çıkarım' dediğin kırmızı çizgi nedir?",
        "options": [
            {
                "id": "redflag_loyalty",
                "text": "Sadakatsizlik ve yalan. Güven bir kez kırıldı mı o cam bir daha birleşmez, şeffaflık şart.",
                "type": "Sadık",
                "favorite_personalities": ["Sadık & Aileci", "Kıskanç & Tutkulu", "Romantik"],
                "partner_reply": "Başını onaylayarak salladı: 'Sonuna kadar katılıyorum. Güven yoksa sevgi bir hiçtir.'"
            },
            {
                "id": "redflag_freedom",
                "text": "Beni kısıtlamaya ve değiştirmeye çalışmak. Olduğum gibi sevilmediğim yerde durmam.",
                "type": "Özgürlükçü",
                "favorite_personalities": ["Çapkın & Özgür Ruhlu", "Maceracı"],
                "partner_reply": "Göz kırptı: 'Harika bir duruş! Herkesin kendi alanı ve özgürlüğü olmalı.'"
            },
            {
                "id": "redflag_respect",
                "text": "Saygısızlık ve manipülasyon. Fikirlerime ve ruhuma saygı duymayan biriyle ömür geçmez.",
                "type": "Olgun",
                "favorite_personalities": ["Entelektüel", "Hırslı & Kariyerist"],
                "partner_reply": "Masaya eğilip elini tuttu: 'Çok olgun ve asil bir bakış açısı.'"
            },
            {
                "id": "redflag_toxic",
                "text": "Beni sosyal medyada kıskandırmaya kalkması! Öyle bir şey olursa intikamım acı olur!",
                "type": "Toksik",
                "favorite_personalities": [],
                "partner_reply": "Hafifçe geri çekilip gergince güldü: 'Vay canına... Biraz ürkütücüsün sanırım.'"
            }
        ]
    }
]

DATE_TACTILE_ACTIONS = [
    {
        "id": "hair_tuck",
        "name": "💇‍♀️ Saçını Kulağının Arkasına İt & Tenini Okşa",
        "short_desc": "Rüzgarda yüzüne düşen saç tutamını usulca kulağının arkasına iliştir.",
        "sensory_log": "Rüzgarda gözlerine düşen bir tutam saçı parmak uçlarınla alıp usulca kulağının arkasına iliştirdin. Parmakların boyun kıvrımına hafifçe değdiğinde gözleri kısıldı, teninin sıcacık ürpertisini hissettin.",
        "partner_reaction": "Nefesi bir anlığına kesildi, dudaklarını hafifçe aralayarak gözlerinin içine baktı: 'Çok naziksin...' diye fısıldadı.",
        "chemistry_boost": 20,
        "style": "Romantik & Duygusal"
    },
    {
        "id": "hand_caress_table",
        "name": "🤲 Masanın Üzerinden Elini Tut & Parmaklarını Kenetle",
        "short_desc": "Masanın üzerinden uzanıp elini sımsıkı avucunun içine al.",
        "sensory_log": "Masanın üzerinden uzanıp elini sıcacık avucunun içine aldın. Başparmağınla elinin üzerini ve bileğindeki atan nabzı yavaşça okşadın; parmakları parmaklarına sımsıkı kenetlendi.",
        "partner_reaction": "Bileğindeki nabzın heyecandan deli gibi hızlandığını hissettin. Parmaklarını hafifçe sıkarak sıcacık gülümsedi.",
        "chemistry_boost": 18,
        "style": "Güven & Samimiyet"
    },
    {
        "id": "jacket_shoulders",
        "name": "🧥 Ceketini Omuzlarına Sar & Kollarını Sıcakça Okşa",
        "short_desc": "Akşam serinliğinde ceketini çıkarıp arkasından omuzlarına bırak.",
        "sensory_log": "Hafifçe ürperdiğini fark ettiğin an ceketini çıkardın ve arkasından nazikçe omuzlarına sardın. İki elini kollarının üzerinde yukarıdan aşağıya gezdirerek tenini ısıttın; parfümünün kokusu üzerine sindi.",
        "partner_reaction": "Ceketine sıkıca sarılıp derin bir nefes aldı: 'Kokun büyüleyici... Yanında kendimi o kadar güvende hissediyorum ki' dedi.",
        "chemistry_boost": 17,
        "style": "Koruyucu & Şefkatli"
    },
    {
        "id": "whisper_ear_neck",
        "name": "👂 Kulağına Eğilip Fısılda & Ilık Nefesini Tenine Bırak",
        "short_desc": "Kulağına eğilip fısıldarken dudaklarınla boynuna yaklaş.",
        "sensory_log": "Müzik sesini bahane edip yüzünü kulağına ve boyun kıvrımına yaklaştırdın. Dudakların tenine teğet geçerken fısıldadın. Ilık nefesin boynuna çarptığında tüyleri diken diken oldu ve nabzı fırladı.",
        "partner_reaction": "Bedeninin titrediğini hissettin; gözlerini kapatıp dudaklarını ısırdı ve sana doğru bir milim daha sokuldu.",
        "chemistry_boost": 24,
        "style": "Tutkulu & Çekici"
    },
    {
        "id": "thigh_touch_secret",
        "name": "🔥 Masanın Altından Bacağını Okşa (Gizli & Cüretkar Dokunuş)",
        "short_desc": "Masa örtüsünün altında elini yavaşça dizine ve bacağına koy.",
        "sensory_log": "Masanın örtüsü altında elini yavaşça partnerinin dizine ve bacağına koydun; parmak uçlarınla tenini yukarı doğru usulca okşadın.",
        "partner_reaction": "Göz bebekleri aniden büyüdü, derin ve kesik bir nefes aldı; masadaki bardağı tutan eli hafifçe titredi ve kaçamak bir tebessümle sana baktı.",
        "chemistry_boost": 25,
        "style": "Cüretkar & Tensel"
    },
    {
        "id": "chin_lift_gaze",
        "name": "✨ Çenesinden Hafifçe Tutup Yüzünü Kendine Çevir & Dudağını Okşa",
        "short_desc": "Çenesini nazikçe kavrayıp başparmağınla alt dudağının kenarını sev.",
        "sensory_log": "İki parmağınla çenesini nazikçe kavrayıp yüzünü kendine doğru çevirdin. Başparmağınla alt dudağının kenarını yavaşça okşadın; nefesleriniz birkaç santim mesafede birbirine karıştı.",
        "partner_reaction": "Gözlerini kısıp dokunuşuna teslim oldu; parmaklarının değdiği dudakları hafifçe aralandı, adeta bir öpücük için yalvarır gibi baktı.",
        "chemistry_boost": 23,
        "style": "Ateşli & Romantik"
    }
]

DATE_MID_EVENTS = [
    {
        "id": "waiter_spill",
        "title": "🥤 Garsonun Sakarlığı & Kaza",
        "desc": "Garson acele ederken masaya çarptı ve içecek partnerinin koluna sıçradı!",
        "options": [
            {
                "id": "hero_protect",
                "text": "Hemen peçeteyi alıp partnerinin kolunu nazikçe sildin ve 'Sen iyi misin?' diyerek sarıldın.",
                "effect_score": 15,
                "note": "Partnerin koruyucu ve ilgili tavrına hayran kaldı!"
            },
            {
                "id": "laugh_ease",
                "text": "Gülümseyip garsonu teselli ettin: 'Nazar çıktı! Bu akşamın tek kusuru bu olsun' dedin.",
                "effect_score": 14,
                "note": "Pozitif ve kriz çözücü enerjine bayıldı!"
            },
            {
                "id": "angry_yell",
                "text": "Garsona bağırıp şefi masaya çağırdın, mekanı birbirine kattın.",
                "effect_score": -20,
                "note": "Partnerin yerin dibine geçti ve senden soğudu!"
            }
        ]
    },
    {
        "id": "live_music_slow",
        "title": "🕯️ Romantik Şarkı & Loş Işıklar",
        "desc": "Mekanda ışıklar kısıldı ve büyüleyici bir akustik aşk şarkısı çalmaya başladı.",
        "options": [
            {
                "id": "dance_floor",
                "text": "Elini tutup piste davet ettin; beline sarılarak gözlerinin içine baka baka dans ettiniz.",
                "effect_score": 18,
                "note": "Romantizm tavan yaptı, kalbi küt küt attı!"
            },
            {
                "id": "toast_whisper",
                "text": "Masanın altından elini sıkıca tuttun ve kadeh kaldırıp şarkıyı fısıldadın.",
                "effect_score": 14,
                "note": "Gözlerindeki tutku partnerini büyüledi!"
            },
            {
                "id": "phone_distract",
                "text": "O sırada telefonuna gelen bildirimi açıp Instagram'da gezinmeye başladın.",
                "effect_score": -22,
                "note": "Büyük saygısızlık! Yüzünü astı ve soğudu."
            }
        ]
    },
    {
        "id": "bill_settlement",
        "title": "💳 Hesap Masaya Geldi",
        "desc": "Garson deri sümen içinde hesabı masaya bıraktı. Partnerin hafifçe çantasına uzandı.",
        "options": [
            {
                "id": "stealth_paid",
                "text": "Gülümseyerek 'Tuvalete gittiğimde çoktan hallettim, bu akşam benim misafirimsin' dedin.",
                "effect_score": 16,
                "note": "Karizmatik ve cömert tavrınla gözlerini kamaştırdın!"
            },
            {
                "id": "gentle_offer",
                "text": "Elini nazikçe tuttun: 'Lütfen bırak ben ödeyeyim, seninle olmak her şeye değer' dedin.",
                "effect_score": 12,
                "note": "Zarif ve centilmen teklifin çok hoşuna gitti."
            },
            {
                "id": "split_exact",
                "text": "Hesap makinesini açıp kuruşu kuruşuna Alman usulü bölüşmeyi teklif ettin.",
                "effect_score": 4,
                "note": "Eşitlikçi davrandın ama romantik hava biraz dağıldı."
            },
            {
                "id": "forgot_wallet",
                "text": "'Aaa cüzdanımı evde unutmuşum, sen ödeyebilir misin?' dedin.",
                "effect_score": -18,
                "note": "Rezalet! Partnerin hesabı öderken utancından kızardı."
            }
        ]
    }
]

DATE_FINALES = [
    {
        "id": "passionate_kiss",
        "name": "💋 Dudaktan Tutkulu Bir Veda Busesi Kondur (Aşk Patlaması)",
        "high_text": "Gözlerini gözlerinden ayırmadan beline sarıldın ve dudaklarına unutulmaz bir öpücük kondurdun! Karşılık verdi, kalpleriniz göğüs kafesinizden fırlayacak gibiydi! 🔥",
        "low_text": "Öpmeye yeltendin ama geri çekilip yanağını çevirdi: 'Sanırım biraz hızlı gidiyoruz...' diyerek utandı.",
        "chemistry_min": 65
    },
    {
        "id": "invite_coffee",
        "name": "☕ 'Geceyi Bitirmeyelim, Yukarı Bir Kahve / Şarap İçmeye Gelir Misin?'",
        "high_text": "Gözlerinin içine bakıp muzipçe gülümsedi: 'Ben de tam bunu sormanı bekliyordum...' Elini tutup birlikte eve çıktınız! 🔥",
        "low_text": "Tebessüm etti: 'Bu akşam harikaydı ama eve gitsem iyi olur, başka sefere...' diyerek veda etti.",
        "chemistry_min": 72
    },
    {
        "id": "warm_hug_promise",
        "name": "🫂 Sımsıkı Sarıl & 'Bu Hayatımın En Güzel Gecesiydi' De",
        "high_text": "Birbirinizin kalp atışlarını duyacak kadar sımsıkı sarıldınız. 'Beni yarın yine ara' diye fısıldayıp saçlarını okşadı.",
        "low_text": "Sıcak bir sarılmayla vedalaştınız, tatlı bir anı olarak kaldı.",
        "chemistry_min": 45
    },
    {
        "id": "gentle_cheek_kiss",
        "name": "✨ Yanağına Zarif Bir Öpücük Kondurup 'İyi Geceler' De",
        "high_text": "Yanağına tatlı bir öpücük kondurdun. Gülümseyerek içeri girdi ve 5 dakika sonra 'Eve sağ salim vardın mı?' mesajı attı.",
        "low_text": "Kibar bir iyi geceler dileyip ayrıldınız.",
        "chemistry_min": 30
    }
]

DETAILED_DATE_SCENARIOS = {
    "mid_scenarios": [
        {
            "id": "bill_arrival",
            "title": "🧾 Garson Hesabı Masaya Bıraktı",
            "desc": "Mekanın şık garsonu hesabı deri sümen içinde masaya bıraktı ve hafifçe gülümsedi.",
            "options": [
                {"id": "pay_all", "name": "💳 Hesabın Tamamını Karizmatikçe Tek Başına Öde", "desc": "Cömertlik ve güç gösterisi."},
                {"id": "split_bill", "name": "🤝 'Alman Usulü Kırışalım mı?' Teklifi Yap", "desc": "Modern ve eşitlikçi bir yaklaşım."},
                {"id": "let_them_pay", "name": "😉 'Bu Seferlik Sıra Sendeydi' Diye Tatlıca Gülümse", "desc": "Flörtöz bir espriyle onun ödemesine izin ver."}
            ]
        },
        {
            "id": "romantic_music",
            "title": "🎶 Arka Planda Büyüleyici Bir Romantik Şarkı Çalmaya Başladı",
            "desc": "Işıklar hafifçe kısıldı, mekandaki herkes melodinin büyüsüne kapıldı.",
            "options": [
                {"id": "dance_slow", "name": "💃 Elinden Tutup Piste Yavaş Dansa Kaldır", "desc": "Gözlerinin içine bakarak yavaşça dans et."},
                {"id": "sing_toast", "name": "🥂 Göz Göze Kadeh Kaldırıp Şarkıya Eşlik Et", "desc": "Gülümseyerek kadeh tokuşturun ve ambiyansı kutlayın."},
                {"id": "hold_hands", "name": "🤲 Masanın Altından Elini Sıkıca Tutup Okşa", "desc": "Sessiz, samimi ve güven veren bir yakınlaşma."}
            ]
        },
        {
            "id": "deep_question",
            "title": "❓ Partnerin Gözlerinin İçine Bakarak Derin Bir Soru Sordu",
            "desc": "'Hayatta seni gerçekten en çok ne korkutur ve gelecekte kendini nerede görüyorsun?'",
            "options": [
                {"id": "vulnerable_truth", "name": "🥺 Tüm Kırılganlığınla En Büyük Hayalini Anlat", "desc": "Maskeleri indirip tüm dürüstlüğünle kalbini aç."},
                {"id": "witty_flirt", "name": "😏 Zekice ve Flörtöz Bir Espriyle Konuyu Bize Getir", "desc": "'Sensiz kalmak korkutur' diyerek havayı romantikleştir."},
                {"id": "listen_them", "name": "👂 'Asıl Sen Anlat, Senin Ruhunu Dinlemek İstiyorum' De", "desc": "İlgiyi tamamen ona vererek can kulağıyla dinle."}
            ]
        }
    ],
    "end_scenarios": [
        {"id": "kiss_goodbye", "name": "💋 Kapısının Önünde Yanağına/Dudağına Unutulmaz Bir Veda Busesi Kondur", "desc": "Ayrılırken kalbini arkanda bırakacak büyüleyici bir kapanış."},
        {"id": "invite_coffee", "name": "☕ 'Geceyi Bitirmeyelim, Yukarı Bir Kahve İçmeye Gelir Misin?' Daveti Yap", "desc": "Randevuyu daha samimi ve özel bir ortama taşıma teklifi."},
        {"id": "warm_hug_walk", "name": "🫂 Sıkıca Sarılıp 'Bu Hayatımın En Güzel Gecesiydi' Deyip Ayrıl", "desc": "İçten, sıcacık ve güven veren bir kucaklaşma."}
    ]
}

DETAILED_FIGHT_TOPICS = [
    {
        "id": "jealousy_dm",
        "name": "📱 Sosyal Medyada Gizli Takipleşmeler & Şüpheli Beğeniler",
        "desc": "Gece yarıları gelen bildirimler, hikaye stalklamaları ve eski flörtlerin fotoğraflarına bırakılan alev emojileri!"
    },
    {
        "id": "money_waste",
        "name": "💸 Sorumsuz Para Harcama & Geleceğe Dair Bütçe Kaygısı",
        "desc": "Gereksiz lüks harcamalar, birikim yapmama ve evin ortak bütçesine gereken önemi vermeme krizi!"
    },
    {
        "id": "commitment_fear",
        "name": "💍 Gelecekten Kaçma & İlişkinin Adını / Evliliği Erteleme",
        "desc": "Aylardır/yıllardır süren belirsizlik; ne zaman evlenileceğine veya nereye varacağına dair söz vermekten kaçış!"
    },
    {
        "id": "family_interference",
        "name": "👵 Eşin/Partnerin Ailesinin İlişkiye Haddinden Fazla Karışması",
        "desc": "Kayınvalide baskısı, her karara akrabaların burnunu sokması ve partnerin ailesine sınır çizememesi!"
    },
    {
        "id": "cold_neglect",
        "name": "❄️ Son Zamanlardaki Ruhsuz, İlgisiz ve Soğuk Davranışlar",
        "desc": "Eve geldiğinde telefondan kafasını kaldırmaması, sarılmaması ve sevgiyi hissettirmemesi!"
    },
    {
        "id": "secret_ex",
        "name": "💔 Eski Sevgiliyle Gizli Görüşme / Bitmeyen İletişim",
        "desc": "'Biz sadece medeni iki insanız' bahanesiyle eski sevgiliyle mesajlaşılması veya karşılaşılması!"
    }
]

DETAILED_FIGHT_ATTITUDES = [
    {
        "id": "rage_explosion",
        "name": "🤬 Kapıları Çarp & Avazın Çıktığı Kadar Bağır (Öfke Patlaması)",
        "desc": "Tüm bastırılmış duygularını bağırarak dışa vur! (Çok yüksek kavga ve ayrılık riski)",
        "intensity": 90
    },
    {
        "id": "cold_sarcasm",
        "name": "🧊 Buz Gibi İğnelemelerle Canını Acıt (Pasif Agresif)",
        "desc": "Sesini hiç yükseltmeden en hassas yerlerinden laf sokarak gururunu incit.",
        "intensity": 65
    },
    {
        "id": "emotional_tears",
        "name": "🥺 Gözyaşlarıyla Ne Kadar Çok Kırıldığını ve Tükendiğini Anlat",
        "desc": "Öfke yerine hüznü seçip dökülen gözyaşlarıyla onun vicdanına ve sevgisine hitap et.",
        "intensity": 45
    },
    {
        "id": "calm_ultimatum",
        "name": "⚖️ Masaya Oturup Somut Kanıtlarla Net Bir Rest Çek",
        "desc": "'Ya bu durumu hemen düzeltirsin ya da bavulunu topla!' ciddiyetiyle konuş.",
        "intensity": 80
    }
]

# ----------------- AİLE & DOSTLUK DERİNLEŞTİRME SİSTEMLERİ -----------------

PARENT_CARE_OPTIONS = [
    {
        "id": "take_home",
        "name": "🏡 Kendi Evine Yanına Al & Birlikte Yaşa",
        "desc": "Anne/babanı kendi evine alıp baş tacı edersin. Evin bereketi ve hayır duası artar.",
        "cost": 0,
        "status_label": "Seninle Yaşıyor"
    },
    {
        "id": "hire_caregiver",
        "name": "👩‍⚕️ Eve Özel Yatılı Bakıcı & Hemşire Tut",
        "desc": "Kendi evinde kalır, profesyonel yatılı sağlık personeli 7/24 ilgilenir.",
        "cost": 65000,
        "status_label": "Özel Bakıcılı"
    },
    {
        "id": "nursing_home",
        "name": "🏥 Seçkin Yaşlı Bakımevi / Huzurevi",
        "desc": "7/24 doktor gözetiminde nezih ve huzurlu bir bakım evine yerleştirirsin.",
        "cost": 45000,
        "status_label": "Huzurevinde"
    },
    {
        "id": "hospital_vigil",
        "name": "🤲 Hastanede Başucunda Refakatçi Kal",
        "desc": "Hastalığında gecelerce elini tutup refakatçi kalırsın; gözyaşlarıyla sana dua eder.",
        "cost": 3500,
        "status_label": "Refakat Edildi"
    }
]

SIBLING_INTERACTIONS = [
    {
        "id": "ask_bail_loan",
        "name": "💸 Kardeşin Acil 50.000 TL Borç / Kefillik İstiyor",
        "desc": "'İşim zorda, bana acil el uzatmazsan batıyorum!' diyerek kapına geldi.",
        "cost": 50000
    },
    {
        "id": "wedding_gold_gift",
        "name": "🥇 Kardeşinin Düğününde Ağır Tam Altın Tak",
        "desc": "Düğün salonunda göğsünü gere gere kardeşine beşi bir yerde ve tam altın takarsın.",
        "cost": 28000
    },
    {
        "id": "reconcile_peace",
        "name": "🕊️ Bayramda Zeytin Dalı Uzat & Barış (Kırgınlığı Bitir)",
        "desc": "Araya giren eski soğukluğu unutup sarılmak ve helalleşmek.",
        "cost": 0
    },
    {
        "id": "deep_heart_talk",
        "name": "☕ Kahve İçip Çocukluk Hatıralarını Yad Et",
        "desc": "Eski günleri, anne-babanın gençliğini ve sokakta oynadığınız günleri konuşup dertleşin.",
        "cost": 250
    }
]

PARENTING_CRISES = [
    {
        "id": "teen_rebellion",
        "title": "🚨 Ergenlik İsyanı: Okuldan Kaçış & Kötü Arkadaş Çevresi",
        "desc": "Çocuğun okuldan kaçıp tehlikeli bir arkadaş grubuyla yakalandı! Odasına kapanıp kapıyı kilitledi.",
        "options": [
            {"id": "gentle_mentor", "text": "☕ Sakince Karşına Alıp Çay İç & Nedenini Dinle", "style": "Şefkatli Dinleme", "desc": "Güven ve sevgi bağını güçlendirir (+İlişki, +Moral)."},
            {"id": "strict_discipline", "text": "📵 Telefonuna & Harçlığına 1 Ay El Koy (Sert Disiplin)", "style": "Otorite", "desc": "Disiplini sağlar ama aranızda soğuk rüzgarlar eser."},
            {"id": "family_therapy", "text": "🛋️ Ergenlik Psikoloğu & Aile Danışmanına Götür (6.000 TL)", "style": "Profesyonel Destek", "desc": "Sorunun köküne inilir, çocuk geleceğe kazanılır."}
        ]
    },
    {
        "id": "career_choice",
        "title": "🎓 Gelecek Seçimi: 'Üniversite Okumayıp Kendi Hayalimin Peşinden Gideceğim!'",
        "desc": "Çocuğun sınav sonrası karşına dikildi: 'Ben memur veya mühendis olmak istemiyorum, sanatçı/girişimci olacağım!'",
        "options": [
            {"id": "support_dream", "text": "🌟 'Hayalinin Arkasındayım' Deyip Başlangıç Sermayesi Ver (40.000 TL)", "style": "Vizyoner Destek", "desc": "Çocuğun başarısı ve özgüveni parlar, ömür boyu sana minnet duyar."},
            {"id": "push_traditional", "text": "🏛️ 'Önce Altın Bileziğin Olsun!' Deyip Zorla Hukuk/Tıp Yazdır", "style": "Geleneksel Baskı", "desc": "Garantici ama mutsuz bir kariyer yoluna girer."},
            {"id": "compromise_school", "text": "🤝 'Hem Diplomanı Al Hem Hayalini Yanında Büyüt' Uzlaşması Yap", "style": "Denge", "desc": "Orta yolda anlaşarak aranızdaki bağı korursunuz."}
        ]
    }
]

FRIEND_INTERACTIONS = [
    {
        "id": "lend_money",
        "name": "🤝 'Kiramı Ödeyemedim, 15.000 TL Borç Verir Misin?'",
        "desc": "Zor durumdaki dostuna borç verip el uzat (Sadık dostsa zamanında öder; vefasızsa kaçabilir!).",
        "cost": 15000
    },
    {
        "id": "share_secret",
        "name": "🤫 En Karanlık ve Derin Sırrını Paylaş (Güven Testi)",
        "desc": "Hayatında kimseye anlatmadığın bir sırrı ona emanet et. Sadakati %80 altındaysa ortamda laf yayılabilir!",
        "cost": 0
    },
    {
        "id": "stand_by_night",
        "name": "🚨 Gece Yarısı Karakol / Hastane İmdadına Koş",
        "desc": "Gece 03:00'te gelen imdat telefonuna hiç düşünmeden kalkıp gitmek ('Dost kara günde belli olur').",
        "cost": 2500
    },
    {
        "id": "fun_road_trip",
        "name": "🚗 Dostlarla Hafta Sonu Ege Yolculuğu & Kamp",
        "desc": "Arabaya atlayıp müzik son ses sahil rotası çizmek, dostluğu pekiştirir.",
        "cost": 6000
    }
]

ACHIEVEMENT_DEFINITIONS = [
    {"id": "born", "icon": "🍼", "title": "Hayata Merhaba", "desc": "Dünyaya gözlerini açtın."},
    {"id": "first_love", "icon": "💘", "title": "İlk Kıvılcım", "desc": "İlk kez aşık oldun ve sevgili edindin."},
    {"id": "heartbreaker", "icon": "🔥", "title": "Kalp Hırsızı", "desc": "KısmetApp veya sosyal ortamda 3 farklı kişiyle flört ettin."},
    {"id": "married", "icon": "💍", "title": "Bir Yastıkta", "desc": "Düğün yapıp dünyaevine girdin."},
    {"id": "child", "icon": "👶", "title": "Geleceğe Miras", "desc": "Bir çocuk sahibi oldun veya evlat edindin."},
    {"id": "graduate", "icon": "🎓", "title": "Diplomalı Birey", "desc": "Üniversiteden başarıyla mezun oldun."},
    {"id": "driver", "icon": "🚗", "title": "Direksiyon Başı", "desc": "Ehliyet sınavını geçip sürücü belgesi aldın."},
    {"id": "homeowner", "icon": "🏠", "title": "Tapu Sahibi", "desc": "İlk gayrimenkulünü satın aldın."},
    {"id": "boss", "icon": "🏢", "title": "Kendi İşinin Patronu", "desc": "Bir şirket veya dükkan kurdun."},
    {"id": "millionaire", "icon": "💰", "title": "Milyoner Kulübü", "desc": "Net servetin 1.000.000 TL'yi aştı."},
    {"id": "multimillionaire", "icon": "💎", "title": "Zenginler Listesi", "desc": "Net servetin 20.000.000 TL'yi aştı."},
    {"id": "billionaire", "icon": "👑", "title": "İmparator", "desc": "Net servetin 100.000.000 TL'yi aştı."},
    {"id": "criminal", "icon": "🦹", "title": "Karanlık Yol", "desc": "Yasa dışı bir suça bulaştın."},
    {"id": "escaped", "icon": "🏃", "title": "Büyük Firar", "desc": "Cezaevinden kaçmayı başardın!"},
    {"id": "famous", "icon": "🌟", "title": "Şöhret Basamakları", "desc": "Sosyal medyada 100.000 takipçiyi geçtin veya ünlü oldun."},
    {"id": "politician", "icon": "🏛️", "title": "Devlet Adamı", "desc": "Seçim kazanarak siyasi bir makama seçildin."},
    {"id": "collector", "icon": "🖼️", "title": "Sanat & Antika Koleksiyoneri", "desc": "Müzayededen nadir bir koleksiyon eseri satın aldın."},
    {"id": "military_vet", "icon": "🪖", "title": "Vatan Borcu", "desc": "Askerlik görevini başarıyla tamamlayıp terhis oldun."},
    {"id": "civil_servant", "icon": "📋", "title": "Kadrolu Atama", "desc": "KPSS sınavında derece yapıp üst düzey devlet kadrosuna atandın."},
    {"id": "fashion_icon", "icon": "👔", "title": "Stil İkonu", "desc": "Gardırobunu yenileyip lüks tarzınla göz kamaştırdın."},
    {"id": "tv_star_love", "icon": "📺", "title": "Kısmet Evi Şampiyonu", "desc": "Evlilik TV programında büyük ödülü ve aşkı kazandın."},
    {"id": "rockstar", "icon": "🎸", "title": "Sahne Efsanesi", "desc": "Kendi müzik grubunu kurup stadyum konserine çıktın."},
    {"id": "ballon_dor", "icon": "⚽", "title": "Altın Top (Ballon d'Or)", "desc": "Profesyonel spor kariyerinde zirveye çıkıp şampiyonluk kupası kaldırdın."},
    {"id": "grandparent", "icon": "👵", "title": "Çınar & Torun Sevgisi", "desc": "Çocuğunu evlendirip ilk torununu kucağına aldın."},
    {"id": "casanova_hookup", "icon": "🔥", "title": "Gecelerin Çapkını", "desc": "Gece hayatında unutulmaz tek gecelik bir kaçamak yaşadın."},
    {"id": "centenarian", "icon": "🌳", "title": "Asırlık Çınar", "desc": "100 yaşına kadar hayatta kaldın."}
]

# ----------------- GECE HAYATI, TEK GECELİK İLİŞKİ & FLÖRT DİNAMİKLERİ -----------------

HOOKUP_VENUES = [
    {
        "id": "nightclub",
        "name": "🍸 Gece Kulübü & VIP Loca",
        "desc": "Lüks kokteyller, neon ışıklar, yüksek tempo müzik ve dans pistinde anlık kıvılcım.",
        "cost": 3000,
        "min_age": 18,
        "charm_boost": 15
    },
    {
        "id": "dive_bar",
        "name": "🍻 Salaş Kokteyl Bar & Pub",
        "desc": "Barda yan yana taburelerde oturup tekila shotlar ve samimi sohbet eşliğinde yakınlaşma.",
        "cost": 1200,
        "min_age": 18,
        "charm_boost": 10
    },
    {
        "id": "kismet_casual",
        "name": "📱 KısmetApp 'Sadece Eğlence' Randevusu",
        "desc": "Uygulamada baştan 'Ciddi düşünmüyorum' diyerek eşleşilen kişiyle doğrudan otele/eve geçme.",
        "cost": 500,
        "min_age": 18,
        "charm_boost": 8
    },
    {
        "id": "beach_resort",
        "name": "🏖️ Lüks Beach Club & After Party",
        "desc": "Yaz tatilinde deniz, gün batımı partisi ve 'Burada yaşanan burada kalır' kaçamağı.",
        "cost": 5500,
        "min_age": 18,
        "charm_boost": 20
    }
]

HOOKUP_PROTECTION_CHOICES = [
    {
        "id": "protected",
        "name": "🛡️ Korumalı (Kondom & Doğum Kontrolü)",
        "desc": "Sağlığını ve geleceğini garantiye alırsın. Hastalık ve istenmeyen gebelik riski minimumdur."
    },
    {
        "id": "unprotected",
        "name": "⚡ Korumasız (Anın Büyüsüne Kapıl - Yüksek Risk!)",
        "desc": "Heyecan dorukta fakat CYBH (zührevi hastalıklar) ve sürpriz gebelik riski çok yüksektir!"
    }
]

DATING_OPENING_LINES = [
    {
        "id": "witty_smart",
        "name": "🧠 Esprili & Zeki Açılış",
        "text": "'Profilindeki kitap/film zevkine bakılırsa bu akşamın en ilginç sohbetini seninle yapacağım belli.'",
        "best_for": ["Entelektüel", "Eğlenceli", "Uyumlu"],
        "penalty_for": ["Materyalist"]
    },
    {
        "id": "confident_direct",
        "name": "🔥 Özgüvenli & Direkt Açılış",
        "text": "'Gözlerini benden alamadığını fark ettim, yanına gelip tanışarak sana bir iyilik yapayım dedim.'",
        "best_for": ["Çapkın & Özgür Ruhlu", "Hırslı & Kariyerist"],
        "penalty_for": ["Geleneksel & Muhafazakar", "Sadık & Aileci"]
    },
    {
        "id": "romantic_sweet",
        "name": "🌹 Romantik & Samimi Açılış",
        "text": "'Gülüşün o kadar içten ve güzeldi ki, selam vermeden geçseydim bütün gün aklımda kalırdın.'",
        "best_for": ["Romantik", "Sadık & Aileci", "Uyumlu"],
        "penalty_for": ["Çapkın & Özgür Ruhlu"]
    },
    {
        "id": "cheesy_meme",
        "name": "😂 Klişe & Mizahi Açılış",
        "text": "'Baban uzaylı falan mıydı? Çünkü senin gibi biri bu dünyadan olamaz ahahaha!'",
        "best_for": ["Eğlenceli"],
        "penalty_for": ["Entelektüel", "Hırslı & Kariyerist"]
    }
]

RED_FLAGS_POOL = [
    "Garsona ve vale çalışanına kaba davranıp bahşişi geri aldı",
    "Hesap gelince telefonla konuşur gibi yapıp tuvalete saklandı",
    "Tüm randevu boyunca eski sevgilisini kötüleyip durdu",
    "Telefonunu sürekli ters çevirip bildirimlerini gizledi",
    "Daha ilk günden ne giyeceğine ve kiminle görüşeceğine karışmaya kalktı",
    "Eski sevgilisiyle hâlâ her gün mesajlaştığını ağzından kaçırdı"
]

GREEN_FLAGS_POOL = [
    "Hizmet sektöründeki çalışanlara olağanüstü nazik ve cömert davrandı",
    "Seni dinlerken gözlerini ayırmadı ve anlattığın detayları unutmadı",
    "Hesabı yarı yarıya ödemekte samimiyetle ısrar etti",
    "Yolda gördüğü yaralı sokak kedisini veterinere götürdü",
    "Kendi sınırlarını ve hayattaki hedeflerini açık yüreklilikle paylaştı",
    "Ailesine ve kardeşlerine çok düşkün ve sevgi dolu"
]

# ----------------- YATAK ODASI, İNTİMİTE & ROMANTİK YAKINLAŞMA -----------------

INTIMACY_VENUES = [
    {
        "id": "bedroom_candlelight",
        "name": "🕯️ Mum Işığında Sıcak Yatak Odası & İpeksi Çarşaflar",
        "desc": "Gül yaprakları, loş aydınlatma ve sakinleştirici melodiler eşliğinde güvenli ve samimi bir atmosfer.",
        "cost": 0,
        "comfort_score": 85,
        "romance_score": 90,
        "icon": "🕯️"
    },
    {
        "id": "jacuzzi_wine",
        "name": "🛁 Köpüklü Jakuzi, Şömine Çıtırtısı & Kırmızı Şarap",
        "desc": "Sıcak suların ve şöminenin huzurunda son derece rahatlatıcı, tutkulu ve lüks bir deneyim.",
        "cost": 1800,
        "comfort_score": 95,
        "romance_score": 92,
        "icon": "🛁"
    },
    {
        "id": "balcony_night",
        "name": "🏖️ Yıldızların Altında Gece Esintisi & Spontane Tutku",
        "desc": "Gecenin sessizliğinde aniden alevlenen, heyecan ve macera dolu spontane bir yakınlaşma.",
        "cost": 0,
        "comfort_score": 75,
        "romance_score": 88,
        "icon": "🏖️"
    },
    {
        "id": "luxury_hotel_suite",
        "name": "🏨 Boutique Otelde Boğaz Manzaralı Kaçamak Süit",
        "desc": "Şehrin gürültüsünden uzak, sadece ikinize özel büyüleyici bir süit odada aşk tazeleme.",
        "cost": 4500,
        "comfort_score": 98,
        "romance_score": 98,
        "icon": "🏨"
    }
]

INTIMACY_MOODS = [
    {
        "id": "tender_romantic",
        "name": "💕 Şefkatli, Yavaş & Derin Duygusal Bağ",
        "desc": "Gözlerinin içine bakarak, sevgi sözcükleri ve sımsıkı sarılmalarla ruhunuzun birleştiği anlar.",
        "satisfaction_boost": 20,
        "emotional_boost": 25,
        "preferred_personalities": ["Romantik", "Sadık & Aileci", "Entelektüel"]
    },
    {
        "id": "wild_passionate",
        "name": "🔥 Ateşli, Heyecanlı & Spontane Tutku",
        "desc": "Kalp atışlarının ritmini hızlandıran, engellenemez bir arzu ve enerji patlaması.",
        "satisfaction_boost": 26,
        "emotional_boost": 16,
        "preferred_personalities": ["Kıskanç & Tutkulu", "Çapkın & Özgür Ruhlu", "Çılgın & Maceracı"]
    },
    {
        "id": "relaxed_cuddle",
        "name": "💆 Masaj, Mum Kokuları & Huzurlu Sımsıkı Sarılma",
        "desc": "Günün tüm yorgunluğunu unutturan, şefkatli bir masaj ve göğsüne yaslanarak huzur bulma.",
        "satisfaction_boost": 18,
        "emotional_boost": 22,
        "preferred_personalities": ["Uyumlu", "Duygusal & Kırılgan", "Hırslı & Kariyerist"]
    }
]

INTIMACY_PROTECTIONS = [
    {
        "id": "condom_safe",
        "name": "🛡️ Korunmalı (Kondom & Doğum Kontrol)",
        "desc": "Tamamen güvenli, plansız gebelik riski %0. Endişesiz ve rahat.",
        "pregnancy_chance": 0.0,
        "safety_label": "Güvenli"
    },
    {
        "id": "unprotected",
        "name": "🎲 Korunmasız & Tutkunun Akışına Bırak",
        "desc": "Hiçbir engelin olmadığı doğal tutku! Ancak sürpriz bir gebelik ihtimali taşır.",
        "pregnancy_chance": 0.22,
        "safety_label": "Riskli (%22 Gebelik)"
    },
    {
        "id": "try_baby",
        "name": "🍼 Bebek Yapma Amacıyla (Yeni Bir Can Müjdesi)",
        "desc": "Birlikte bir aile kurma veya aileyi büyütme hayaliyle aşkı taçlandırmak.",
        "pregnancy_chance": 0.70,
        "safety_label": "Bebek Denemesi (%70)"
    }
]

INTIMACY_AFTERGLOWS = [
    "Sabah güneşin ilk ışıkları odaya dolarken birbirinize sarılarak uyandınız; sana şefkatle sokulup 'Seninle olmak dünyadaki her şeyden daha güzel' diye fısıldadı.",
    "Yataktan kalkıp mutfakta birlikte kahve ve sıcak kruvasan yaptınız, kahkaha dolu sıcacık bir pazar sabahı havası esti.",
    "Göğsüne yaslanıp kalp atışlarını dinledi ve 'Kendimi yanında hiç olmadığım kadar huzurlu ve güvende hissediyorum' dedi.",
    "Gözlerini açtığında başucuna bir gül ve sıcacık bir tebessüm bırakmıştı; aranızdaki çekim tavan yaptı.",
    "Gece boyunca süren tatlı fısıldaşmalar ve şakalaşmalar sabah kahvaltısına kadar neşeyle devam etti."
]
