# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Zenginleştirilmiş Rastgele Olaylar ve Dönüm Noktaları Motoru
"""

import random
from typing import Optional
from .models import Character, ActiveEvent, EventChoice, LifeLog, Person, Pet
from .data import FIRST_NAMES_MALE, FIRST_NAMES_FEMALE, LAST_NAMES

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
        "id": "teen_bad_habit",
        "min_age": 14,
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

RANDOM_EVENTS_POOL = [
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
        "id": "dating_blind_date",
        "min_age": 18,
        "max_age": 55,
        "title": "Sürpriz Tanışma Fırsatı",
        "description": "Yakın bir arkadaşın seni çok kafa dengi biriyle tanıştırmak için akşam yemeği organize etti.",
        "image_emoji": "🌹",
        "choices": [
            {"id": "accept_date", "text": "Şık giyinip yemeğe katıl."},
            {"id": "refuse_date", "text": "Kibarca teşekkür edip evde kal."}
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

def check_for_annual_event(char: Character) -> Optional[ActiveEvent]:
    """Her yıl için uygun bir dönüm noktası veya rastgele ikilem seçer."""
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
    
    # 2. Rastgele Olay Şansı (%65 ihtimalle her yaşta bir olay tetiklenir)
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
                category="random"
            )
            
    return None

def resolve_event_choice(char: Character, event_id: str, choice_id: str) -> str:
    """Kullanıcının yaptığı seçime göre istatistikleri ve hikayeyi günceller."""
    result_text = ""
    
    if event_id == "school_start":
        char.job_history.append("milestone_school_start")
        if choice_id == "study_hard":
            char.smarts = min(100, char.smarts + 8)
            char.school_performance = 90
            result_text = "Ön sıraya geçip dersi can kulağıyla dinledin. Öğretmenin seni çok sevdi! (Zeka +8)"
        elif choice_id == "cry_loud":
            char.happiness = max(0, char.happiness - 8)
            result_text = "Koridorda ortalığı birbirine kattın. Müdür yardımcısı sana çikolata vererek sakinleştirdi."
        else:
            char.happiness = min(100, char.happiness + 12)
            # Yeni okul arkadaşı ekle
            friend_gender = random.choice(["Erkek", "Kadın"])
            f_names = FIRST_NAMES_MALE if friend_gender == "Erkek" else FIRST_NAMES_FEMALE
            f_name = f"{random.choice(f_names)} {random.choice(LAST_NAMES)}"
            char.relationships.append(Person(
                id=f"friend_{len(char.relationships)+1}",
                name=f_name,
                relation="Arkadaş",
                gender=friend_gender,
                age=char.age,
                relationship_level=85
            ))
            result_text = f"Elmanı paylaştığın {f_name} ile en yakın okul arkadaşı oldunuz! (Mutluluk +12)"

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
            Severance = 450000 if char.current_job else 120000
            char.money += Severance
            char.current_job = None
            char.happiness = min(100, char.happiness + 25)
            result_text = f"Emekli oldun! {Severance:,} TL emeklilik ikramiyeni alıp huzurlu günlere adım attın."
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
                result_text = "Anons микрофonunda adın yankılandı: 'Çeyrek altın!' Tüm salon seni alkışladı!"
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

    elif event_id == "dating_blind_date":
        if choice_id == "accept_date":
            partner_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
            p_names = FIRST_NAMES_FEMALE if partner_gender == "Kadın" else FIRST_NAMES_MALE
            p_name = f"{random.choice(p_names)} {random.choice(LAST_NAMES)}"
            existing = next((p for p in char.relationships if p.relation in ["Sevgili", "Eş"]), None)
            if not existing:
                new_lover = Person(
                    id=f"person_lover_{len(char.relationships)+1}",
                    name=p_name,
                    relation="Sevgili",
                    gender=partner_gender,
                    age=char.age,
                    relationship_level=85,
                    job="Mimar"
                )
                char.relationships.append(new_lover)
                if "first_love" not in char.achievements:
                    char.achievements.append("first_love")
                char.happiness = min(100, char.happiness + 20)
                result_text = f"Randevu muhteşem geçti! {p_name} ile yeni bir aşka yelken açtınız! 💘"
            else:
                char.happiness = min(100, char.happiness + 8)
                result_text = f"Keyifli bir akşam yemeği oldu ve {p_name} ile iyi birer dost oldunuz."
        else:
            result_text = "Evde kalıp dinlenmeyi tercih ettin."

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
        category="event",
        icon="⚖️"
    ))
    
    char.active_event = None
    return result_text
