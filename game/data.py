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
    {"id": "centenarian", "icon": "🌳", "title": "Asırlık Çınar", "desc": "100 yaşına kadar hayatta kaldın."}
]
