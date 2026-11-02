# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Zenginleştirilmiş Rastgele Olaylar, Aşk/İlişki Dramaları ve Dönüm Noktaları Motoru
"""

import random
from typing import Optional
from .models import Character, ActiveEvent, EventChoice, LifeLog, Person, Pet
from .data import (
    FIRST_NAMES_MALE, FIRST_NAMES_FEMALE, LAST_NAMES,
    ZODIAC_SIGNS, PERSONALITIES, INTERESTS_POOL
)

MILESTONE_EVENTS = [
    {
        "id": "school_start",
        "min_age": 6,
        "max_age": 6,
        "title": "İlkokula Başlama Günü",
        "description": "Bugün ilkokuldaki ilk günün! Sınıfta herkes ağlıyor ve annen kapıda el sallıyor. Ne yapacaksın?",
        "image_emoji": "🎒",
        "category": "school",
        "choices": [
            {"id": "study_hard", "text": "Hemen ön sıraya oturup defterimi açarım."},
            {"id": "cry_loud", "text": "Annemi bırakmamak için koridorda avazım çıktığı kadar ağlarım."},
            {"id": "make_friend", "text": "Yanımdaki çocuğa beslenme çantamdaki elmayı teklif ederim."}
        ]
    },
    {
        "id": "bayram_pocket_money",
        "min_age": 8,
        "max_age": 10,
        "title": "Bayram Ziyareti ve Harçlık Taktikleri",
        "description": "Bayram sabahı bütün sülale dedenin evinde toplandı! El öpme sırası sana geldi.",
        "image_emoji": "🍬",
        "category": "milestone",
        "choices": [
            {"id": "kiss_all", "text": "Herkesin elini tek tek öpüp hal hatır sorarım."},
            {"id": "eat_baklava", "text": "Harçlığı boş verip mutfakta iki tepsi baklavaya gömülürüm."},
            {"id": "bargain_uncle", "text": "Zengin amcamın yanına oturup harçlık pazarlığı yaparım."}
        ]
    },
    {
        "id": "middle_school_bully",
        "min_age": 11,
        "max_age": 13,
        "title": "Okul Koridorunda Zorba!",
        "description": "Ortaokulda senden iki yaş büyük bir çocuk teneffüste önüne geçip kantin tostunu zorla almaya çalışıyor!",
        "image_emoji": "👊",
        "category": "school",
        "choices": [
            {"id": "fight_back", "text": "Tostumu kimseye vermem! Yumruğumu sıkarım."},
            {"id": "tell_teacher", "text": "Hemen nöbetçi öğretmene şikayet ederim."},
            {"id": "give_toast", "text": "Tostu verir, sessizce uzaklaşırım."}
        ]
    },
    {
        "id": "first_school_crush",
        "min_age": 14,
        "max_age": 15,
        "title": "Lisede İlk Kalp Çarpıntısı 💓",
        "description": "Sınıfın en popüler ve sempatik öğrencisi teneffüste yanına gelip ders notlarını istedi ve sana tatlı tatlı gülümsedi!",
        "image_emoji": "💌",
        "category": "love",
        "choices": [
            {"id": "confess_crush", "text": "Cesaretimi toplayıp okul çıkışı birlikte çay/kahve içmeyi teklif ederim!"},
            {"id": "write_love_note", "text": "Defterin arasına romantik ve gizemli bir şiir/not bırakırım."},
            {"id": "shy_away", "text": "Yüzüm kıpkırmızı olur, notları verip heyecanla kaçarım."}
        ]
    },
    {
        "id": "teen_bad_habit",
        "min_age": 15,
        "max_age": 16,
        "title": "Okul Arkası Teklifi",
        "description": "Lisede havalı görünen bir grup seni okul bahçesinin arkasına çağırdı: 'Al bir nefes çek, korkak mısın yoksa?' dediler.",
        "image_emoji": "🚬",
        "category": "teen",
        "choices": [
            {"id": "refuse_smoke", "text": "'Sağlığıma değer veriyorum' deyip yanlarından ayrılırım."},
            {"id": "accept_smoke", "text": "Gruba girmek için teklifi kabul ederim."},
            {"id": "mock_them", "text": "'Ciğerlerinize yazık gençler' diye espri yapıp geçerim."}
        ]
    },
    {
        "id": "driving_license_age",
        "min_age": 18,
        "max_age": 18,
        "title": "18 Yaş: Reşit Oldun ve Ehliyet Sınavı!",
        "description": "Artık 18 yaşındasın! Sürücü kursuna yazılıp ehliyet sınavına girmek ister misin? (Kurs ücreti: 15.000 TL - Ailen destek olabilir)",
        "image_emoji": "🚗",
        "category": "milestone",
        "choices": [
            {"id": "take_driving_test", "text": "Evet, direksiyon sınavına gir ve ehliyet al."},
            {"id": "skip_license", "text": "Şimdilik ehliyet almayı ertele."}
        ]
    },
    {
        "id": "university_choice",
        "min_age": 18,
        "max_age": 19,
        "title": "YKS Üniversite Sınavı Sonuçları!",
        "description": "Liseden mezun oldun ve YKS sınav sonuçları açıklandı! Geleceğin için nasıl bir yol çizmek istiyorsun?",
        "image_emoji": "🎓",
        "category": "education",
        "choices": [
            {"id": "go_university", "text": "Üniversiteye kayıt ol ve kampüs hayatına başla."},
            {"id": "start_working", "text": "Üniversiteyi boş ver, doğrudan iş hayatına atıl."},
            {"id": "gap_year", "text": "Bir yıl mezuna kalıp kafa dinle ve ders çalış."}
        ]
    },
    {
        "id": "military_call",
        "min_age": 20,
        "max_age": 21,
        "title": "Askerlik Yoklama Tebligatı!",
        "description": "e-Devlet üzerinden askerlik yoklama mesajın geldi! Vatan borcu kapıda. Ne yapacaksın?",
        "image_emoji": "🪖",
        "category": "milestone",
        "gender_only": "Erkek",
        "choices": [
            {"id": "regular_service", "text": "Kışlaya teslim olup 6 ay er olarak askerliğimi yaparım."},
            {"id": "paid_service", "text": "Bedelli askerlik ücretini (180.000 TL) ödeyip 1 ayda tamamlarım."},
            {"id": "postpone_service", "text": "Eğitim/sağlık gerekçesiyle tecil ettiririm."}
        ]
    },
    {
        "id": "midlife_crisis",
        "min_age": 42,
        "max_age": 46,
        "title": "Orta Yaş Bunalımı",
        "description": "Aynaya baktığında şakaklarındaki beyazları ve geçen yılları fark ettin. İçinde garip bir huzursuzluk var.",
        "image_emoji": "🧘",
        "category": "general",
        "choices": [
            {"id": "sport_hobbies", "text": "Kendimi spora ve yeni bir hobiye veririm."},
            {"id": "luxury_buy", "text": "Birikimimle çılgın bir tatile çıkarım (40.000 TL)."},
            {"id": "therapy", "text": "Bir psikoterapiste gidip iç dünyamı keşfederim."}
        ]
    },
    {
        "id": "retirement_choice",
        "min_age": 65,
        "max_age": 68,
        "title": "Emeklilik Çağı",
        "description": "Yılların emeğinin ardından yasal emeklilik yaşına ulaştın. Çalışmaya devam mı, yoksa emekli olup dinlenmek mi?",
        "image_emoji": "🏖️",
        "category": "career",
        "choices": [
            {"id": "retire_now", "text": "Emekli ol, kıdem tazminatını al ve huzura çekil."},
            {"id": "keep_working", "text": "İşimi seviyorum, çalışmaya devam edeceğim."}
        ]
    }
]

PARTNER_EVENTS_POOL = [
    {
        "id": "partner_phone_msg",
        "title": "Gece Yarısı Gelen Şüpheli Mesaj 📱",
        "description": "Saat gece 01:30... Partnerinin başucundaki telefon titredi ve ekranda 'Uyudun mu? Seni düşündüm 😊' mesajı belirdi!",
        "image_emoji": "📱",
        "category": "love",
        "choices": [
            {"id": "snoop_phone", "text": "Gizlice parmak iziyle telefonu açıp tüm mesajları oku!"},
            {"id": "ask_calmly", "text": "Sabah kahvaltıda sakin ama net bir şekilde kim olduğunu sor."},
            {"id": "make_scene", "text": "Hemen uyandırıp hesap sor ve kıyameti kopar!"}
        ]
    },
    {
        "id": "partner_anniversary",
        "title": "Yıl Dönümü Sürprizi Beklentisi 🥂",
        "description": "Bugün partnerinle ilişkinizin yıl dönümü! Sabah uyanır uyanmaz sana 'Bugün günlerden ne biliyor musun aşkım?' diye sordu.",
        "image_emoji": "💝",
        "category": "love",
        "choices": [
            {"id": "luxury_celebration", "text": "'Unutur muyum hiç!' deyip Boğaz'da lüks yemeğe götür (6.000 TL)."},
            {"id": "homemade_romance", "text": "Mum ışığında kendi ellerinle romantik bir akşam yemeği hazırla."},
            {"id": "admit_forgot", "text": "Unuttuğunu itiraf edip gönlünü almaya çalış."}
        ]
    },
    {
        "id": "partner_inlaws_dinner",
        "title": "Kayınvalide & Aile Tanışma Yemeği 🍲",
        "description": "Partnerinin ailesi bu akşam yemeğe geliyor! Annesi kapıdan girer girmez evi ve seni tepeden tırnağa süzmeye başladı.",
        "image_emoji": "👵",
        "category": "love",
        "choices": [
            {"id": "charm_inlaws", "text": "En leziz ikramları sunup tatlı dille kalplerini fethet (2.500 TL)."},
            {"id": "be_natural", "text": "Kendin gibi davran, samimi bir sohbet aç."},
            {"id": "argue_inlaws", "text": "İğneleyici laflarına dayanamayıp lafı gediğine oturt!"}
        ]
    },
    {
        "id": "partner_jealousy_crisis",
        "title": "Kıskançlık Krizi! 🔥",
        "description": "Sosyal medyada eski bir okul arkadaşının fotoğrafını beğendiğini gören partnerin küplere bindi: 'Kim bu?! Hemen açıkla!' diyor.",
        "image_emoji": "😤",
        "category": "love",
        "choices": [
            {"id": "reassure_love", "text": "Sarılarak tek sevdiğinin o olduğunu söyle ve takipten çık."},
            {"id": "defend_freedom", "text": "'Özel alanıma karışamazsın, sadece eski bir arkadaş!' de."},
            {"id": "turn_tables", "text": "'Asıl senin geçen gün konuştuğun kişi kimdi?!' diyerek üste çık."}
        ]
    }
]

RANDOM_EVENTS_POOL = [
    {
        "id": "secret_admirer",
        "min_age": 16,
        "max_age": 55,
        "title": "Gizli Hayrandan Aşk İtirafı! 💌",
        "description": "Sosyal çevrenden uzun süredir seni uzaktan beğenen çok hoş biri yanına yaklaştı ve gözlerinin içine bakarak duygularını açtı!",
        "image_emoji": "💘",
        "category": "love",
        "choices": [
            {"id": "give_chance", "text": "Heyecanla karşılık ver ve ilk randevuya çık!"},
            {"id": "friendzone", "text": "'Seni çok seviyorum ama arkadaş olarak kalalım' de."},
            {"id": "reject_coldly", "text": "İlgilenmediğini söyleyip hızla uzaklaş."}
        ]
    },
    {
        "id": "friend_asks_loan",
        "min_age": 18,
        "max_age": 70,
        "title": "Dosttan Borç Talebi 🤝",
        "description": "Yakın bir arkadaşın çok sıkıştığını söyleyerek senden 15.000 TL borç istedi: 'Kanka söz 2 aya kuruşu kuruşuna ödeyeceğim!'",
        "image_emoji": "💸",
        "category": "general",
        "choices": [
            {"id": "lend_money", "text": "Dost kara günde belli olur, 15.000 TL borç ver."},
            {"id": "gift_small", "text": "'Borç olmasın, benden sana 3.000 TL destek olsun' de."},
            {"id": "refuse_loan", "text": "'Para alışverişi dostluğu bozar' diyerek kibarca reddet."}
        ]
    },
    {
        "id": "family_reunion",
        "min_age": 15,
        "max_age": 80,
        "title": "Büyük Pazar Aile Kahvaltısı 🥐",
        "description": "Annen ve baban hafta sonu tüm aileyi bir araya getirmek için büyük bir kahvaltı sofrası kurdu.",
        "image_emoji": "👨‍👩‍👧‍👦",
        "category": "general",
        "choices": [
            {"id": "go_with_gifts", "text": "En sevdiği pastaneden su böreği ve tatlı alıp git (1.000 TL)."},
            {"id": "attend_happily", "text": "Keyifle katılıp aile büyüklerinin gönlünü al."},
            {"id": "skip_reunion", "text": "Bahane uydurup evde uyu."}
        ]
    },
    {
        "id": "found_wallet",
        "min_age": 10,
        "max_age": 80,
        "title": "Yolda Bulunan Cüzdan",
        "description": "Sokakta yürürken yerde şişkin bir deri cüzdan buldun. İçinde 25.000 TL nakit para ve kimlik kartı var!",
        "image_emoji": "👛",
        "choices": [
            {"id": "return_wallet", "text": "Kimlik sahibine ulaşıp kuruşuna dokunmadan teslim et."},
            {"id": "keep_money", "text": "Parayı cebine at, cüzdanı kenara bırak."},
            {"id": "police_station", "text": "Doğrudan en yakın polis karakoluna götür."}
        ]
    },
    {
        "id": "astroturf_match",
        "min_age": 15,
        "max_age": 50,
        "title": "Gece 11-12 Halı Saha Maçı",
        "description": "Arkadaşlar aradı: 'Kadroda son 1 kişi eksik, kaleye veya forvete gelir misin? Maç başlamak üzere!'",
        "image_emoji": "⚽",
        "choices": [
            {"id": "play_striker", "text": "Kramponları giyip forvete geçerim, gol kralı olurum!"},
            {"id": "play_goalie", "text": "Eldivenleri takıp kaleye geçerim."},
            {"id": "decline_match", "text": "'Sakatlanmak istemiyorum' deyip evde dizi izlerim."}
        ]
    },
    {
        "id": "landlord_rent_hike",
        "min_age": 22,
        "max_age": 65,
        "title": "Ev Sahibinden Telefon!",
        "description": "Ev sahibin aradı: 'Almanya'dan oğlum gelecek, ya kirayı iki katına çıkarırsın ya da evi tahliye edersin!' diyor.",
        "image_emoji": "🏠",
        "choices": [
            {"id": "know_rights", "text": "Yasal kira artış oranını hatırlatıp hakkımı savunurum."},
            {"id": "accept_hike", "text": "Tatsızlık çıkmasın diye istediği zammı öderim (-30.000 TL)."},
            {"id": "argue_landlord", "text": "Telefonda sert tartışıp mahkemeye veririm."}
        ]
    },
    {
        "id": "relative_wedding_gold",
        "min_age": 20,
        "max_age": 75,
        "title": "Uzak Akraba Düğünü ve Takı Merasimi",
        "description": "Kuzeninin düğününe davetlisin. Takı anonsu başladı, herkes sıraya girdi ve tüm gözler senin üzerinde!",
        "image_emoji": "🪙",
        "choices": [
            {"id": "pin_quarter_gold", "text": "Şanımız yürüsün! Çeyrek altın takarım (8.000 TL)."},
            {"id": "pin_cash", "text": "Zarfa 1.000 TL koyup hızlıca sandığa atarım."},
            {"id": "fake_ribbon", "text": "Kalabalıkta sadece kurdele tokalaşıp tebrik ederim (0 TL)."}
        ]
    },
    {
        "id": "stranger_crypto_tip",
        "min_age": 18,
        "max_age": 70,
        "title": "Gizemli Yatırım Tüyosu",
        "description": "Bir kafede yan masadaki takım elbiseli adam fısıldadı: 'Yeni bir teknoloji tokenı çıkıyor, 10 katı garanti!'",
        "image_emoji": "📈",
        "choices": [
            {"id": "invest_crypto", "text": "Fırsatı kaçırma! 20.000 TL yatır."},
            {"id": "ignore_crypto", "text": "'Dolandırıcılarla işim olmaz' deyip kahveni iç."},
            {"id": "research_crypto", "text": "Eve gidip finansal raporlarını detaylıca incele."}
        ]
    },
    {
        "id": "work_office_rumor",
        "min_age": 20,
        "max_age": 64,
        "title": "Ofis Dedikodusu ve Rekabet",
        "description": "İş yerinde bir çalışma arkadaşının senin projenin başarısını kendi üstüne almaya çalıştığını fark ettin!",
        "image_emoji": "🗣️",
        "choices": [
            {"id": "prove_with_data", "text": "Toplantıda tüm e-posta ve belgelerle projeyi senin yaptığını kanıtla."},
            {"id": "confront_person", "text": "Mutfakta yakalayıp sertçe yüzleş."},
            {"id": "stay_silent", "text": "Tatsızlık çıkmasın diye sineye çek."}
        ]
    },
    {
        "id": "street_fight",
        "min_age": 16,
        "max_age": 60,
        "title": "Trafikte Yol Verme Kavgası",
        "description": "Trafikte bir sürücü aniden önüne kırdı, kornaya bastığında ise öfkeyle araçtan inip üzerine yürüdü!",
        "image_emoji": "🚙",
        "choices": [
            {"id": "lock_doors", "text": "Kapıları kilitleyip araç kamerası kaydıyla polise bildir."},
            {"id": "step_out_fight", "text": "Sen de araçtan inip göğüs göğüse kavgaya tutuş!"},
            {"id": "apologize_leave", "text": "Manevra yapıp olay yerinden uzaklaş."}
        ]
    },
    {
        "id": "lottery_vendor",
        "min_age": 18,
        "max_age": 85,
        "title": "Yılbaşı Özel Çekiliş Bileti",
        "description": "Köşe başındaki seyyar bayi seslendi: 'Son şanslı biletler! Büyük ikramiye 50 Milyon TL!' (Bilet: 500 TL)",
        "image_emoji": "🎟️",
        "choices": [
            {"id": "buy_ticket", "text": "Şansımı deneyeyim, bir bilet çek!"},
            {"id": "decline_ticket", "text": "'Şans oyunlarıyla işim olmaz' deyip geç."}
        ]
    },
    {
        "id": "illegal_offer",
        "min_age": 18,
        "max_age": 60,
        "title": "Karanlık Sevkiyat Teklifi",
        "description": "Eski bir tanıdık yanına yaklaştı: 'Gümrükten birkaç gizli koli geçireceğiz, bir gecede 120.000 TL nakit. Var mısın?'",
        "image_emoji": "📦",
        "choices": [
            {"id": "accept_illegal", "text": "Risk olmadan kazanç olmaz, kabul et!"},
            {"id": "reject_illegal", "text": "Yasa dışı işlere bulaşmam, reddet."},
            {"id": "snitch_police", "text": "Emniyet kaçakçılık şubesine ihbar et."}
        ]
    },
    {
        "id": "homeless_animal",
        "min_age": 6,
        "max_age": 85,
        "title": "Yağmur Altında Yavru Kedi",
        "description": "Soğuk ve yağmurlu bir akşamda minik bir kedi yavrusu apartman girişinde titreyerek sana bakıyor.",
        "image_emoji": "🐱",
        "choices": [
            {"id": "adopt_cat", "text": "Eve alıp ısıt, veterinere götür ve sahiplen."},
            {"id": "feed_only", "text": "Mama ve su kabı koyup karnını doyur."},
            {"id": "ignore_animal", "text": "İçeri girip kapıyı kapat."}
        ]
    },
    {
        "id": "inheritance_distant_relative",
        "min_age": 25,
        "max_age": 75,
        "title": "Beklenmedik Miras Mektubu!",
        "description": "İsviçre'de yaşayan uzak bir akraban vefat etmiş. Hukuk bürosu sana ulaştı ve yüklü bir miras kaldığını bildirdi!",
        "image_emoji": "📜",
        "choices": [
            {"id": "claim_inheritance", "text": "İmzaları at ve mirası banka hesabına aktar."},
            {"id": "donate_inheritance", "text": "Tüm mirası eğitim vakfına bağışla."}
        ]
    }
]

def _create_romantic_person(char: Character, relation_type: str = "Sevgili") -> Person:
    partner_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
    p_names = FIRST_NAMES_FEMALE if partner_gender == "Kadın" else FIRST_NAMES_MALE
    p_name = f"{random.choice(p_names)} {random.choice(LAST_NAMES)}"
    p_spec = random.choice(PERSONALITIES)
    p_interests = random.sample(INTERESTS_POOL, 3)
    return Person(
        id=f"person_lover_{len(char.relationships)+1}_{random.randint(10,99)}",
        name=p_name,
        relation=relation_type,
        gender=partner_gender,
        age=max(14, char.age + random.randint(-1, 2)),
        relationship_level=85,
        job="Öğrenci" if char.age < 21 else random.choice(["Mimar", "Avukat", "Doktor", "Tasarımcı", "Mühendis"]),
        personality=p_spec["id"],
        zodiac=random.choice(ZODIAC_SIGNS),
        looks=random.randint(65, 98),
        smarts=random.randint(60, 95),
        craziness=max(10, min(95, p_spec["crazy_bias"] + random.randint(-10, 10))),
        loyalty=max(20, min(100, p_spec["loyalty_bias"] + random.randint(-10, 10))),
        wealth=random.randint(40, 90),
        interests=p_interests,
        memories=[f"{char.age} yaşındayken romantik bir şekilde tanıştınız."]
    )

def check_for_annual_event(char: Character) -> Optional[ActiveEvent]:
    """Her yıl için uygun bir dönüm noktası, ilişki draması veya rastgele ikilem seçer."""
    if not char.is_alive or char.is_in_prison:
        return None
    
    # 1. Milestone kontrolü
    for m in MILESTONE_EVENTS:
        if m["min_age"] <= char.age <= m["max_age"]:
            if "gender_only" in m and m["gender_only"] != char.gender:
                continue
            done_key = f"milestone_{m['id']}"
            if done_key not in char.job_history:
                choices = [EventChoice(id=c["id"], text=c["text"]) for c in m["choices"]]
                return ActiveEvent(
                    id=m["id"],
                    title=m["title"],
                    description=m["description"],
                    image_emoji=m["image_emoji"],
                    choices=choices,
                    category=m.get("category", "milestone")
                )
    
    # 2. Aktif Partner / Eş Varsa Özel İlişki Olayı (%35 İhtimal)
    partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive), None)
    if partner and random.random() < 0.35:
        pev = random.choice(PARTNER_EVENTS_POOL)
        choices = [EventChoice(id=c["id"], text=c["text"]) for c in pev["choices"]]
        return ActiveEvent(
            id=pev["id"],
            title=f"{pev['title']} ({partner.name})",
            description=pev["description"],
            image_emoji=pev["image_emoji"],
            choices=choices,
            category="love"
        )

    # 3. Genel Rastgele Olay Şansı (%65 ihtimal)
    if random.random() < 0.65:
        eligible_events = [e for e in RANDOM_EVENTS_POOL if e["min_age"] <= char.age <= e["max_age"]]
        if eligible_events:
            ev = random.choice(eligible_events)
            choices = [EventChoice(id=c["id"], text=c["text"]) for c in ev["choices"]]
            return ActiveEvent(
                id=ev["id"],
                title=ev["title"],
                description=ev["description"],
                image_emoji=ev.get("image_emoji", "⚡"),
                choices=choices,
                category=ev.get("category", "random")
            )
            
    return None

def resolve_event_choice(char: Character, event_id: str, choice_id: str) -> str:
    """Kullanıcının yaptığı seçime göre istatistikleri, ilişkileri ve hikayeyi günceller."""
    result_text = ""
    log_cat = "event"
    log_icon = "⚖️"
    partner = next((p for p in char.relationships if p.relation in ["Flört", "Sevgili", "Nişanlı", "Eş"] and p.is_alive), None)
    
    if event_id == "school_start":
        char.job_history.append("milestone_school_start")
        log_cat = "school"
        if choice_id == "study_hard":
            char.smarts = min(100, char.smarts + 8)
            char.school_performance = 90
            result_text = "Ön sıraya geçip dersi can kulağıyla dinledin. Öğretmenin seni çok sevdi! (Zeka +8)"
        elif choice_id == "cry_loud":
            char.happiness = max(0, char.happiness - 8)
            result_text = "Koridorda ortalığı birbirine kattın. Müdür yardımcısı sana çikolata vererek sakinleştirdi."
        else:
            char.happiness = min(100, char.happiness + 12)
            friend_gender = random.choice(["Erkek", "Kadın"])
            f_names = FIRST_NAMES_MALE if friend_gender == "Erkek" else FIRST_NAMES_FEMALE
            f_name = f"{random.choice(f_names)} {random.choice(LAST_NAMES)}"
            char.relationships.append(Person(
                id=f"friend_{len(char.relationships)+1}",
                name=f_name,
                relation="Arkadaş",
                gender=friend_gender,
                age=char.age,
                relationship_level=85,
                personality="Sadık & Aileci",
                zodiac=random.choice(ZODIAC_SIGNS),
                interests=random.sample(INTERESTS_POOL, 2),
                memories=["İlkokulun ilk gününde elmanı paylaştığın çocukluk arkadaşın."]
            ))
            result_text = f"Elmanı paylaştığın {f_name} ile en yakın okul arkadaşı oldunuz! (Mutluluk +12)"

    elif event_id == "first_school_crush":
        char.job_history.append("milestone_first_school_crush")
        log_cat = "love"
        log_icon = "💘"
        if choice_id in ["confess_crush", "write_love_note"]:
            new_lover = _create_romantic_person(char, "Sevgili")
            char.relationships.append(new_lover)
            char.dating_partner_id = new_lover.id
            if "first_love" not in char.achievements:
                char.achievements.append("first_love")
            char.happiness = min(100, char.happiness + 22)
            result_text = f"Kalbin yerinden çıkacak gibiydi ama {new_lover.name} teklifini gülümseyerek kabul etti! İlk gençlik aşkın başladı! 💘"
        else:
            char.happiness = max(0, char.happiness - 5)
            result_text = "Utangaçlığından dolayı fırsatı kaçırdın ama tatlı bir anı olarak kaldı."

    elif event_id == "partner_phone_msg":
        log_cat = "love"
        log_icon = "📱"
        if not partner:
            result_text = "Mesaj yanlış numaraymış."
        elif choice_id == "snoop_phone":
            if partner.loyalty >= 65:
                partner.relationship_level = max(10, partner.relationship_level - 20)
                partner.memories.append("Telefonunu gizlice karıştırdığın için sana kırıldı.")
                result_text = f"Telefonu karıştırdın; mesaj kuzenindenmiş! Ama {partner.name} uyandığında telefonunu karıştırdığını fark etti ve güveni sarsıldı! (İlişki -20)"
            else:
                partner.relationship_level = max(5, partner.relationship_level - 45)
                char.happiness = max(0, char.happiness - 30)
                partner.memories.append("Gizli flört mesajlarını yakaladın!")
                result_text = f"ŞOK! {partner.name}'in gizlice başkasıyla flörtleştiğini yakaladın! Büyük bir kavga çıktı! (İlişki -45)"
        elif choice_id == "ask_calmly":
            partner.relationship_level = min(100, partner.relationship_level + 10)
            result_text = f"Sabah sakince sordun. {partner.name} iş arkadaşının nöbet mesajı olduğunu gösterip olgun yaklaşımın için sana sarıldı. (İlişki +10)"
        else:
            partner.relationship_level = max(10, partner.relationship_level - 25)
            char.happiness = max(0, char.happiness - 15)
            result_text = f"Gece yarısı bağırıp çağırdın! Oysa mesaj operatörden/kuzeninden gelmiş. {partner.name} aşırı kıskançlığından bunaldı. (İlişki -25)"

    elif event_id == "partner_anniversary":
        log_cat = "love"
        log_icon = "💝"
        if not partner:
            result_text = "Güzel bir gün geçti."
        elif choice_id == "luxury_celebration":
            if char.money >= 6000:
                char.money -= 6000
                partner.relationship_level = 100
                char.happiness = min(100, char.happiness + 20)
                partner.memories.append("Yıl dönümünüzü Boğaz'da muhteşem bir yemekle kutladınız.")
                result_text = f"Boğaz'da harika bir kutlama yaptınız! {partner.name} sana bir kez daha aşık oldu! (İlişki %100)"
            else:
                partner.relationship_level = min(100, partner.relationship_level + 10)
                result_text = f"Bütçen lüks restorana yetmese de sahilde yürüyüp romantik bir akşam geçirdiniz."
        elif choice_id == "homemade_romance":
            partner.relationship_level = min(100, partner.relationship_level + 18)
            char.happiness = min(100, char.happiness + 15)
            partner.memories.append("Yıl dönümünde ellerinle yemek hazırladın.")
            result_text = f"Kendi ellerinle hazırladığın mum ışığı sofrası {partner.name}'i çok duygulandırdı! (İlişki +18)"
        else:
            partner.relationship_level = max(5, partner.relationship_level - 30)
            char.happiness = max(0, char.happiness - 15)
            result_text = f"Yıl dönümünü unuttuğun için {partner.name} bütün hafta seninle küstü! (İlişki -30)"

    elif event_id == "partner_inlaws_dinner":
        log_cat = "love"
        log_icon = "🍲"
        if not partner:
            result_text = "Misafirler ağırlandı."
        elif choice_id == "charm_inlaws":
            char.money = max(0, char.money - 2500)
            partner.relationship_level = min(100, partner.relationship_level + 20)
            char.karma = min(100, char.karma + 10)
            partner.memories.append("Ailesini evinizde krallar gibi ağırladın.")
            result_text = f"Kayınvaliden ve kayınpederin sana bayıldı! '{partner.name} çok şanslıymış!' diyerek övgüler yağdırdılar. (İlişki +20)"
        elif choice_id == "be_natural":
            partner.relationship_level = min(100, partner.relationship_level + 10)
            result_text = "Samimi ve doğal tavrınla akşam yemeği gayet huzurlu geçti. (İlişki +10)"
        else:
            partner.relationship_level = max(10, partner.relationship_level - 25)
            char.happiness = max(0, char.happiness - 15)
            result_text = f"Masada soğuk rüzgarlar esti! Ailesi gidince {partner.name} ile tartıştınız. (İlişki -25)"

    elif event_id == "partner_jealousy_crisis":
        log_cat = "love"
        log_icon = "🔥"
        if not partner:
            result_text = "Tartışma kapandı."
        elif choice_id == "reassure_love":
            partner.relationship_level = min(100, partner.relationship_level + 12)
            result_text = f"Gönlünü aldın ve aranızdaki buzlar eridi. {partner.name} sana sıkıca sarıldı. (İlişki +12)"
        elif choice_id == "defend_freedom":
            if partner.craziness > 60:
                partner.relationship_level = max(10, partner.relationship_level - 22)
                result_text = f"{partner.name} kıskançlıktan köpürdü ve kapıyı çarpıp çıktı! (İlişki -22)"
            else:
                partner.relationship_level = min(100, partner.relationship_level + 5)
                result_text = f"{partner.name} haklı olduğunu kabul edip gereksiz kıskançlık yaptığı için özür diledi."
        else:
            partner.relationship_level = max(5, partner.relationship_level - 28)
            result_text = "İkiniz de birbirinize bağırıp küstünüz! (İlişki -28)"

    elif event_id == "secret_admirer":
        log_cat = "love"
        log_icon = "💌"
        if choice_id == "give_chance":
            if partner:
                # Mevcut partner varken şans verirse aldatma riski!
                new_crush = _create_romantic_person(char, "Flört")
                char.relationships.append(new_crush)
                if random.random() < 0.5:
                    partner.relationship_level = max(5, partner.relationship_level - 40)
                    result_text = f"Gizli hayranın {new_crush.name} ile buluştun ama {partner.name} bunu duydu ve ortalık karıştı!"
                else:
                    result_text = f"{new_crush.name} ile gizli bir flörte başladın! Kalbin iki kişi arasında kaldı..."
            else:
                new_lover = _create_romantic_person(char, "Sevgili")
                char.relationships.append(new_lover)
                char.dating_partner_id = new_lover.id
                if "first_love" not in char.achievements:
                    char.achievements.append("first_love")
                char.happiness = min(100, char.happiness + 25)
                result_text = f"Gizli hayranın {new_lover.name} ({new_lover.job}) ile harika bir ilişkiye başladınız! 💘"
        elif choice_id == "friendzone":
            new_friend = _create_romantic_person(char, "Arkadaş")
            char.relationships.append(new_friend)
            char.happiness = min(100, char.happiness + 8)
            result_text = f"{new_friend.name} kararını saygıyla karşıladı ve yakın arkadaş oldunuz."
        else:
            result_text = "Teklifi geri çevirip yoluna devam ettin."

    elif event_id == "friend_asks_loan":
        if choice_id == "lend_money":
            if char.money >= 15000:
                char.money -= 15000
                char.karma = min(100, char.karma + 15)
                for p in char.relationships:
                    if p.relation == "Arkadaş":
                        p.relationship_level = 100
                if random.random() < 0.65:
                    char.money += 18000
                    result_text = "Arkadaşın sözünde durdu ve borcunu fazlasıyla (18.000 TL) geri ödedi! Dostluğunuz perçinlendi."
                else:
                    result_text = "15.000 TL borç verdin. Arkadaşın minnettar kaldı (Karma +15)."
            else:
                result_text = "15.000 TL nakdin olmadığı için veremedin."
        elif choice_id == "gift_small":
            if char.money >= 3000:
                char.money -= 3000
                char.karma = min(100, char.karma + 12)
                result_text = "Arkadaşına 3.000 TL karşılıksız destek oldun, gözleri doldu."
            else:
                result_text = "Bütçen yetmedi ama manevi destek verdin."
        else:
            result_text = "Borç vermeyi kibarca reddettin."

    elif event_id == "family_reunion":
        if choice_id == "go_with_gifts":
            char.money = max(0, char.money - 1000)
            for p in char.relationships:
                if p.relation in ["Anne", "Baba", "Ağabey", "Abla", "Kardeş"]:
                    p.relationship_level = min(100, p.relationship_level + 18)
            char.happiness = min(100, char.happiness + 15)
            result_text = "Aldığın börekler ve tatlılarla kahvaltının yıldızı oldun! Tüm aileyle ilişkin güçlendi."
        elif choice_id == "attend_happily":
            for p in char.relationships:
                if p.relation in ["Anne", "Baba", "Ağabey", "Abla", "Kardeş"]:
                    p.relationship_level = min(100, p.relationship_level + 10)
            char.happiness = min(100, char.happiness + 10)
            result_text = "Ailenle sıcacık bir pazar kahvaltısı yaptınız."
        else:
            for p in char.relationships:
                if p.relation in ["Anne", "Baba"]:
                    p.relationship_level = max(0, p.relationship_level - 12)
            result_text = "Kahvaltıya gitmediğin için annen telefonda sitem etti."

    elif event_id == "bayram_pocket_money":
        char.job_history.append("milestone_bayram_pocket_money")
        if choice_id == "kiss_all":
            harclik = random.randint(2500, 6000)
            char.money += harclik
            char.happiness = min(100, char.happiness + 12)
            char.karma = min(100, char.karma + 8)
            result_text = f"Bütün büyüklerin elini öptün ve toplam {harclik:,} TL bayram harçlığı topladın!"
        elif choice_id == "eat_baklava":
            char.happiness = min(100, char.happiness + 15)
            char.health = max(10, char.health - 5)
            result_text = "Tepsi tepsi baklava yedin! Şeker komasına girsen de çok mutlu oldun."
        else:
            harclik = random.randint(4000, 10000)
            char.money += harclik
            char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + 10)
            result_text = f"Zengin amcan pazarlık yeteneğine hayran kaldı ve sana {harclik:,} TL harçlık verdi!"

    elif event_id == "middle_school_bully":
        char.job_history.append("milestone_middle_school_bully")
        if choice_id == "fight_back":
            char.skills["martial_arts"] = min(100, char.skills.get("martial_arts", 5) + 12)
            if random.random() < 0.55:
                char.happiness = min(100, char.happiness + 15)
                result_text = "Zorbaya sağlam bir karşılık verdin! Bir daha kimse senin tostuna yan gözle bakamadı."
            else:
                char.health = max(10, char.health - 12)
                result_text = "Kavgada dudağın patladı ama cesaretinle okulda saygı kazandın."
        elif choice_id == "tell_teacher":
            char.smarts = min(100, char.smarts + 4)
            result_text = "Öğretmen zorbaya disiplin cezası verdi ve tostunu kurtardın."
        else:
            char.happiness = max(0, char.happiness - 15)
            result_text = "Tostunu kaptırdın ve aç kaldın. Moralin bozuldu."

    elif event_id == "teen_bad_habit":
        char.job_history.append("milestone_teen_bad_habit")
        if choice_id == "refuse_smoke":
            char.health = min(100, char.health + 6)
            char.smarts = min(100, char.smarts + 5)
            result_text = "İradeni korudun ve teklifi reddettin. (Sağlık +6, Zeka +5)"
        elif choice_id == "accept_smoke":
            char.health = max(10, char.health - 12)
            char.looks = max(10, char.looks - 5)
            result_text = "Dumanı çekince öksürük krizine girdin! Sağlığın olumsuz etkilendi."
        else:
            char.happiness = min(100, char.happiness + 10)
            result_text = "Esprinle ortamı yumuşattın ve sana saygı duydular."

    elif event_id == "driving_license_age":
        char.job_history.append("milestone_driving_license_age")
        if choice_id == "take_driving_test":
            has_parent_support = any(p.relation in ["Anne", "Baba"] and p.is_alive and p.relationship_level > 55 for p in char.relationships)
            if char.money >= 15000:
                char.money -= 15000
                paid = True
            elif has_parent_support:
                paid = True
            else:
                paid = False

            if paid:
                if char.smarts >= 35:
                    char.has_drivers_license = True
                    if "driver" not in char.achievements:
                        char.achievements.append("driver")
                    char.happiness = min(100, char.happiness + 15)
                    result_text = "Tebrikler! Direksiyon sınavını başarıyla geçtin ve B Sınıfı Ehliyetini aldın! 🚗"
                else:
                    result_text = "L-park yaparken dubaları devirdin! Sınavdan kaldın."
            else:
                result_text = "Kurs ücretini (15.000 TL) ödeyecek paran yoktu, ehliyet alamadın."
        else:
            result_text = "Ehliyet almayı daha sonraya bıraktın."

    elif event_id == "university_choice":
        char.job_history.append("milestone_university_choice")
        if choice_id == "go_university":
            char.education_level = "Üniversite"
            char.current_school = "Üniversite (Lisans)"
            char.school_years_left = 4
            char.smarts = min(100, char.smarts + 10)
            if "graduate" not in char.achievements:
                char.achievements.append("graduate")
            result_text = "Üniversiteye yerleşerek akademik hayatına adım attın! (Zeka +10)"
        elif choice_id == "start_working":
            char.education_level = "Lise"
            char.money += 45000
            result_text = "Doğrudan iş hayatına atıldın ve ilk 45.000 TL birikimini yaptın!"
        else:
            char.happiness = min(100, char.happiness + 15)
            char.smarts = min(100, char.smarts + 6)
            result_text = "Mezuna kalıp hem dinlendin hem de kendini geliştirdin."

    elif event_id == "military_call":
        char.job_history.append("milestone_military_call")
        if choice_id == "regular_service":
            char.military_status = "Tamamlandı"
            char.health = min(100, char.health + 8)
            char.skills["athletics"] = min(100, char.skills.get("athletics", 15) + 15)
            result_text = "6 ay boyunca kışlada vatani görevini başarıyla yerine getirdin ve terhis oldun! 🪖"
        elif choice_id == "paid_service":
            if char.money >= 180000:
                char.money -= 180000
                char.military_status = "Bedelli Tamamlandı"
                result_text = "180.000 TL bedelli ücretini yatırıp 28 günlük temel askerlik eğitimini tamamladın."
            else:
                char.military_status = "Tecilli"
                result_text = "Bedelli parası çıkışmadığı için askerliği 2 yıl tecil ettirdin."
        else:
            char.military_status = "Tecilli"
            result_text = "Askerliğini tecil ettirdin."

    elif event_id == "midlife_crisis":
        char.job_history.append("milestone_midlife_crisis")
        if choice_id == "sport_hobbies":
            char.health = min(100, char.health + 12)
            char.happiness = min(100, char.happiness + 12)
            result_text = "Yüzmeye ve doğa yürüyüşlerine başladın, kendini 20 yaşında gibi hissediyorsun!"
        elif choice_id == "luxury_buy":
            if char.money >= 40000:
                char.money -= 40000
                char.happiness = min(100, char.happiness + 25)
                result_text = "Harika bir dünya turuna çıktın, orta yaş krizinden eser kalmadı!"
            else:
                result_text = "Bütçen lüks tatile yetmedi, sahilde çay içip denizi izledin."
        else:
            char.happiness = min(100, char.happiness + 18)
            char.smarts = min(100, char.smarts + 5)
            result_text = "Terapi seansları sayesinde hayatındaki öncelikleri yeniden keşfettin."

    elif event_id == "retirement_choice":
        char.job_history.append("milestone_retirement_choice")
        if choice_id == "retire_now":
            severance = 450000 if char.current_job else 120000
            char.money += severance
            char.current_job = None
            char.happiness = min(100, char.happiness + 25)
            result_text = f"Emekli oldun! {severance:,} TL emeklilik ikramiyeni alıp huzurlu günlere adım attın."
        else:
            char.happiness = min(100, char.happiness + 8)
            result_text = "Çalışmayı bırakmadın! Tecrübenle gençlere örnek olmaya devam ediyorsun."

    elif event_id == "astroturf_match":
        if choice_id == "play_striker":
            if random.random() < 0.75:
                char.happiness = min(100, char.happiness + 15)
                char.health = min(100, char.health + 6)
                result_text = "Halı sahada 4 gol atıp maçın yıldızı oldun! Maç sonu baklavalar senden soruldu! ⚽"
            else:
                char.health = max(15, char.health - 12)
                result_text = "Röveşata denerken bileğini burktun! Bir hafta topalladın."
        elif choice_id == "play_goalie":
            char.happiness = min(100, char.happiness + 10)
            result_text = "Kalede devleştin, doksandan toplar çıkardın!"
        else:
            result_text = "Evde dinlenmeyi seçtin."

    elif event_id == "landlord_rent_hike":
        if choice_id == "know_rights":
            char.smarts = min(100, char.smarts + 5)
            char.happiness = min(100, char.happiness + 8)
            result_text = "Kira kontratını ve kanun maddesini gösterince ev sahibi geri adım attı!"
        elif choice_id == "accept_hike":
            char.money = max(0, char.money - 30000)
            char.happiness = max(0, char.happiness - 10)
            result_text = "Ekstra 30.000 TL kira farkı ödedin, bütçen sarsıldı."
        else:
            char.happiness = max(0, char.happiness - 8)
            result_text = "Ev sahibiyle arabuluculukta anlaştınız."

    elif event_id == "relative_wedding_gold":
        if choice_id == "pin_quarter_gold":
            if char.money >= 8000:
                char.money -= 8000
                char.karma = min(100, char.karma + 15)
                char.happiness = min(100, char.happiness + 12)
                result_text = "Anons mikrofonunda adın yankılandı: 'Çeyrek altın!' Tüm salon seni alkışladı!"
            else:
                result_text = "Cebinde çeyrek altın parası yoktu, zarfla geçiştirdin."
        elif choice_id == "pin_cash":
            char.money = max(0, char.money - 1000)
            char.karma = min(100, char.karma + 5)
            result_text = "1.000 TL zarf bıraktın, düğün pastasını afiyetle yedin."
        else:
            char.karma = max(0, char.karma - 10)
            result_text = "Boş kurdele taktığın anlaşılınca akrabalar arkandan fısıldaştı!"

    elif event_id == "work_office_rumor":
        if choice_id == "prove_with_data":
            char.smarts = min(100, char.smarts + 6)
            char.happiness = min(100, char.happiness + 15)
            if char.current_job:
                char.current_job.performance = min(100, char.current_job.performance + 20)
            result_text = "Belgelerle gerçeği ortaya koydun! Yöneticin seni tebrik etti ve performans puanın fırladı!"
        elif choice_id == "confront_person":
            char.happiness = min(100, char.happiness + 5)
            result_text = "İş arkadaşın özür diledi ve bir daha senin işine karışamadı."
        else:
            char.happiness = max(0, char.happiness - 15)
            result_text = "Hakkını aramadığın için bütün övgüyü başkası topladı."

    elif event_id == "found_wallet":
        if choice_id == "return_wallet":
            char.karma = min(100, char.karma + 20)
            char.happiness = min(100, char.happiness + 15)
            char.money += 5000
            result_text = "Cüzdanı sahibine verdin. Sahibi minnettarlıktan sana 5.000 TL ödül verdi! (Karma +20)"
        elif choice_id == "keep_money":
            char.karma = max(0, char.karma - 25)
            char.money += 25000
            result_text = "25.000 TL'yi cebine indirdin! (Para +25.000 TL, Karma -25)"
        else:
            char.karma = min(100, char.karma + 12)
            result_text = "Cüzdanı polise teslim ettin. Örnek davranışın takdir topladı."

    elif event_id == "stranger_crypto_tip":
        if choice_id == "invest_crypto":
            if char.money >= 20000:
                char.money -= 20000
                if random.random() < 0.40:
                    win = 160000
                    char.money += win
                    char.happiness = min(100, char.happiness + 25)
                    result_text = f"İnanılmaz! Kripto token patladı ve {win:,} TL kazandın!"
                else:
                    char.happiness = max(0, char.happiness - 18)
                    result_text = "Proje çöktü! Yatırım yaptığın 20.000 TL buhar oldu..."
            else:
                result_text = "Yatırım yapacak 20.000 TL nakdin yoktu."
        elif choice_id == "ignore_crypto":
            result_text = "Riskli tüyolara kulak asmadın."
        else:
            char.smarts = min(100, char.smarts + 5)
            result_text = "Projeyi inceleyip sahte olduğunu anladın ve paranı korudun! (Zeka +5)"

    elif event_id == "street_fight":
        if choice_id == "lock_doors":
            char.smarts = min(100, char.smarts + 5)
            result_text = "Kayıt aldığını görünce saldırgan panikleyip kaçtı."
        elif choice_id == "step_out_fight":
            if random.random() < 0.5 + (char.skills.get("martial_arts", 5) / 200):
                char.happiness = min(100, char.happiness + 15)
                result_text = "Savunma hamlenle saldırganı etkisiz hale getirdin!"
            else:
                char.health = max(10, char.health - 20)
                result_text = "Kavgada darbe aldın ve acillik oldun! (Sağlık -20)"
        else:
            result_text = "Soğukkanlılıkla uzaklaştın."

    elif event_id == "lottery_vendor":
        if choice_id == "buy_ticket":
            if char.money >= 500:
                char.money -= 500
                roll = random.random()
                if roll < 0.01:
                    jackpot = 50000000
                    char.money += jackpot
                    char.happiness = 100
                    result_text = "MUCİZE GERÇEK OLDU! BÜYÜK İKRAMİYE VURDU: 50.000.000 TL KAZANDIN! 🎉"
                elif roll < 0.15:
                    win = 10000
                    char.money += win
                    result_text = "Tebrikler! Biletine 10.000 TL ikramiye isabet etti!"
                else:
                    result_text = "Biletine ikramiye çıkmadı."
            else:
                result_text = "Cebinde 500 TL yoktu."
        else:
            result_text = "Piyango bileti almadın."

    elif event_id == "illegal_offer":
        if choice_id == "accept_illegal":
            if "criminal" not in char.achievements:
                char.achievements.append("criminal")
            if random.random() < 0.50:
                char.money += 120000
                char.karma = max(0, char.karma - 30)
                result_text = "Sevkiyat sorunsuz bitti ve 120.000 TL kazandın!"
            else:
                char.is_in_prison = True
                char.prison_years_left = 4
                char.prison_sentence = 4
                char.criminal_record.append("Gümrük Kaçakçılığı")
                char.happiness = max(0, char.happiness - 40)
                result_text = "Polis baskın yaptı! Yakalandın ve 4 Yıl Hapis cezasına çarptırıldın!"
        elif choice_id == "reject_illegal":
            char.karma = min(100, char.karma + 10)
            result_text = "Teklifi reddettin ve temiz sicilini korudun."
        else:
            char.karma = min(100, char.karma + 25)
            char.money += 25000
            result_text = "Emniyete ihbar ettin ve 25.000 TL muhbir ödülü aldın!"

    elif event_id == "homeless_animal":
        if choice_id == "adopt_cat":
            new_pet = Pet(
                id=f"pet_{len(char.pets)+1}",
                name="Şanslı",
                species="Kedi",
                breed="Tekir",
                age=1,
                relationship_level=100
            )
            char.pets.append(new_pet)
            char.happiness = min(100, char.happiness + 20)
            char.karma = min(100, char.karma + 20)
            result_text = "Yavru kediyi sahiplendin ve adını 'Şanslı' koydun! (Mutluluk +20, Karma +20)"
        elif choice_id == "feed_only":
            char.happiness = min(100, char.happiness + 6)
            char.karma = min(100, char.karma + 8)
            result_text = "Kediye mama verdin, karnını doyurup mırıldandı."
        else:
            char.karma = max(0, char.karma - 10)
            result_text = "İçeri girip kapıyı kapattın."

    elif event_id == "inheritance_distant_relative":
        inheritance_amount = random.randint(350000, 2000000)
        if choice_id == "claim_inheritance":
            char.money += inheritance_amount
            char.happiness = min(100, char.happiness + 25)
            result_text = f"Miras hesabına geçti! Tam {inheritance_amount:,} TL servetine eklendi!"
        else:
            char.karma = 100
            char.happiness = min(100, char.happiness + 25)
            char.fame = min(100, char.fame + 20)
            result_text = f"Tüm mirası ({inheritance_amount:,} TL) eğitim vakfına bağışladın. Gazetelere çıktın!"

    else:
        result_text = "Bir karar verdin ve hayat akmaya devam etti."
        
    char.logs.append(LifeLog(
        age=char.age,
        year=char.current_year,
        text=result_text,
        category=log_cat,
        icon=log_icon
    ))
    
    char.active_event = None
    return result_text
