# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Gelişmiş Aktiviteler, Flört/Aşk Sistemi (KısmetApp), Derin İnsan İlişkileri ve Eylemler Motoru
"""

import random
import uuid
from typing import Dict, Any, List
from .models import (
    Character, Person, DatingCandidate, Pet, Asset, Job, Business, LifeLog,
    SocialMediaAccount, MusicBand, ProSportsCareer
)
from .data import (
    JOBS_DATABASE, PART_TIME_JOBS, BUSINESS_TYPES, SCHOOL_CLUBS,
    REAL_ESTATE_MARKET, VEHICLE_MARKET, UNIVERSITIES,
    FIRST_NAMES_MALE, FIRST_NAMES_FEMALE, LAST_NAMES,
    ZODIAC_SIGNS, PERSONALITIES, INTERESTS_POOL, DATING_BIOS_BY_PERSONALITY,
    MEET_PLACES, DATE_VENUES, ROMANTIC_GIFTS, ENGAGEMENT_RINGS, WEDDING_VENUES,
    LOVE_LANGUAGES, COUPLE_VACATIONS, SOCIAL_HANGOUTS, DM_TOPICS,
    PET_BREEDS, PET_NAMES, POLITICAL_OFFICES, AUCTION_ITEMS,
    OUTFIT_STYLES, EXAM_QUESTIONS, BAND_GENRES,
    COUPLE_BUSINESS_TYPES, DIVORCE_LAWYERS, SPORTS_CLUBS,
    RELATIONSHIP_CONFLICTS, COMPANY_EXPANSION_ACTIONS, CAR_CARE_ACTIONS,
    TENANT_MANAGEMENT_ACTIONS, WELLNESS_SERVICES,
    KISS_STYLES, DETAILED_DATE_SCENARIOS, DETAILED_FIGHT_TOPICS, DETAILED_FIGHT_ATTITUDES,
    PARENT_CARE_OPTIONS, SIBLING_INTERACTIONS, PARENTING_CRISES, FRIEND_INTERACTIONS,
    HOOKUP_VENUES, HOOKUP_PROTECTION_CHOICES, DATING_OPENING_LINES, RED_FLAGS_POOL, GREEN_FLAGS_POOL
)

# ----------------- SAĞLIK & KİŞİSEL BAKIM -----------------

def do_doctor_checkup(char: Character) -> Dict[str, Any]:
    cost = 1000
    if char.money < cost:
        return {"success": False, "message": "Muayene ücreti için yeterli paran yok (1.000 TL gerekli)."}
    
    char.money -= cost
    if not char.illnesses:
        char.health = min(100, char.health + 6)
        char.happiness = min(100, char.happiness + 4)
        return {"success": True, "message": "Doktor kontrollerini yaptı: 'Tahlilleriniz tertemiz, turp gibisiniz!' (Sağlık +6)"}
    
    cured_illness = char.illnesses.pop(0)
    char.health = min(100, char.health + 22)
    char.happiness = min(100, char.happiness + 15)
    char.logs.append(LifeLog(
        age=char.age,
        year=char.current_year,
        text=f"Doktor tedavisiyle '{cured_illness}' rahatsızlığından tamamen kurtuldun!",
        category="health",
        icon="🩺"
    ))
    return {"success": True, "message": f"Tedavi başarılı! '{cured_illness}' tamamen iyileşti. (Sağlık +22, Mutluluk +15)"}

def do_plastic_surgery(char: Character, procedure: str) -> Dict[str, Any]:
    cost_map = {
        "rhinoplasty": ("Burun Estetiği", 45000, 16),
        "botox": ("Botoks ve Dolgu", 15000, 9),
        "hair_transplant": ("Mikro FUE Saç Ekimi", 35000, 14),
        "gym_sculpt": ("Tam Vücut Şekillendirme", 75000, 22)
    }
    if procedure not in cost_map:
        return {"success": False, "message": "Geçersiz operasyon seçimi."}
    
    name, cost, looks_boost = cost_map[procedure]
    if char.money < cost:
        return {"success": False, "message": f"{name} için yeterli paran yok ({cost:,} TL gerekli)."}
    
    char.money -= cost
    if random.random() < 0.14:
        char.looks = max(5, char.looks - 22)
        char.happiness = max(0, char.happiness - 28)
        char.health = max(10, char.health - 12)
        msg = f"Korkunç hata! {name} operasyonun ters gitti! (Görünüş -22, Mutluluk -28)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="health", icon="😱"))
        return {"success": False, "message": msg}
    else:
        char.looks = min(100, char.looks + looks_boost)
        char.happiness = min(100, char.happiness + 15)
        msg = f"{name} operasyonun harika geçti! Görünüşün göz kamaştırıyor. (Görünüş +{looks_boost})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="health", icon="✨"))
        return {"success": True, "message": msg}

def do_gym_workout(char: Character) -> Dict[str, Any]:
    cost = 1500
    char.skills["athletics"] = min(100, char.skills.get("athletics", 15) + 6)
    if char.money < cost:
        char.health = min(100, char.health + 4)
        char.happiness = min(100, char.happiness + 3)
        return {"success": True, "message": "Belediye parkındaki aletlerde açık hava antrenmanı yaptın. (Sağlık +4, Atletizm +6)"}
    
    char.money -= cost
    char.health = min(100, char.health + 8)
    char.looks = min(100, char.looks + 4)
    char.happiness = min(100, char.happiness + 6)
    char.stress = max(0, char.stress - 12)
    return {"success": True, "message": "Spor salonunda sıkı bir antrenman yaptın! (Sağlık +8, Görünüş +4, Stres -12)"}

def do_meditation(char: Character) -> Dict[str, Any]:
    char.happiness = min(100, char.happiness + 8)
    char.karma = min(100, char.karma + 5)
    char.stress = max(0, char.stress - 15)
    return {"success": True, "message": "Derin nefes ve farkındalık meditasyonu yaptın. Zihnin berraklaştı! (Mutluluk +8, Stres -15)"}

# ----------------- EĞİTİM, KULÜPLER & BECERİLER -----------------

def do_study_hard(char: Character) -> Dict[str, Any]:
    char.smarts = min(100, char.smarts + 6)
    char.school_performance = min(100, char.school_performance + 15)
    return {"success": True, "message": "Kütüphanede saatlerce ders çalıştın ve kitap okudun. (Zeka +6, Okul Başarısı +15)"}

def join_school_club(char: Character, club_id: str) -> Dict[str, Any]:
    if char.age < 7 or (char.age > 24 and not char.current_school):
        return {"success": False, "message": "Okul kulüplerine sadece öğrencilik yıllarında katılabilirsin."}
    club = next((c for c in SCHOOL_CLUBS if c["id"] == club_id), None)
    if not club:
        return {"success": False, "message": "Kulüp bulunamadı."}
    
    char.school_club = club["name"]
    sk = club["skill"]
    char.skills[sk] = min(100, char.skills.get(sk, 10) + 15)
    char.smarts = min(100, char.smarts + club["smarts_boost"])
    char.happiness = min(100, char.happiness + 10)
    msg = f"{club['name']} üyesi oldun! Hem sosyal çevren genişledi hem de yeteneklerin gelişti."
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="school", icon="🏅"))
    return {"success": True, "message": msg}

def train_skill_course(char: Character, skill_key: str) -> Dict[str, Any]:
    courses = {
        "coding": ("Yazılım & Yapay Zeka Bootcamp", 8000, "💻"),
        "music": ("Enstrüman & Şan Eğitimi", 5000, "🎸"),
        "charisma": ("Hitabet, Diksiyon & Liderlik Kursu", 6000, "🗣️"),
        "martial_arts": ("Kickboks & Yakın Savunma Akademisi", 5500, "🥊")
    }
    if skill_key not in courses:
        return {"success": False, "message": "Geçersiz kurs."}
    title, cost, icon = courses[skill_key]
    if char.money < cost:
        return {"success": False, "message": f"{title} için {cost:,} TL gerekli."}
    
    char.money -= cost
    char.skills[skill_key] = min(100, char.skills.get(skill_key, 10) + 18)
    if skill_key == "coding":
        char.smarts = min(100, char.smarts + 6)
    elif skill_key == "martial_arts":
        char.health = min(100, char.health + 6)
    char.happiness = min(100, char.happiness + 8)
    return {"success": True, "message": f"{icon} {title} eğitimini tamamladın! Yetenek seviyen: %{char.skills[skill_key]}"}

def take_driving_license_manual(char: Character) -> Dict[str, Any]:
    if char.has_drivers_license:
        return {"success": False, "message": "Zaten B Sınıfı Sürücü Belgen var!"}
    if char.age < 18:
        return {"success": False, "message": "Ehliyet almak için en az 18 yaşında olmalısın."}
    cost = 15000
    if char.money < cost:
        return {"success": False, "message": f"Sürücü kursu ve harçlar için {cost:,} TL gerekli."}
    char.money -= cost
    char.has_drivers_license = True
    if "driver" not in char.achievements:
        char.achievements.append("driver")
    msg = "Sürücü kursu sınavlarını başarıyla geçtin ve B Sınıfı Ehliyetini aldın! 🚗"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🚗"))
    return {"success": True, "message": msg}

def apply_for_university(char: Character, faculty_id: str) -> Dict[str, Any]:
    if char.age < 18:
        return {"success": False, "message": "Üniversite için en az 18 yaşında olmalısın."}
    
    faculty = next((f for f in UNIVERSITIES if f["id"] == faculty_id), None)
    if not faculty:
        return {"success": False, "message": "Fakülte bulunamadı."}
    
    if char.smarts < faculty["smarts_required"]:
        return {"success": False, "message": f"Bu bölüm için en az %{faculty['smarts_required']} Zeka puanı gerekiyor (Senin Zekan: %{char.smarts})."}
    
    char.education_level = "Üniversite"
    char.current_school = faculty["name"]
    char.school_years_left = faculty["duration"]
    char.smarts = min(100, char.smarts + 10)
    char.happiness = min(100, char.happiness + 15)
    if "graduate" not in char.achievements:
        char.achievements.append("graduate")
    msg = f"Tebrikler! {faculty['name']} bölümüne kabul edildin!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="school", icon="🎓"))
    return {"success": True, "message": msg}

# ----------------- İŞ, KARİYER VE GİRİŞİMCİLİK -----------------

def apply_for_job(char: Character, job_id: str, chosen_opt: int) -> Dict[str, Any]:
    job_spec = next((j for j in JOBS_DATABASE if j["id"] == job_id), None)
    if not job_spec:
        return {"success": False, "message": "İş ilanı bulunamadı."}
    if char.is_in_prison:
        return {"success": False, "message": "Cezaevindeyken çalışamazsın!"}
    if char.age < 18:
        return {"success": False, "message": "Tam zamanlı çalışmak için en az 18 yaşında olmalısın. Öğrenciysen Yarı Zamanlı işlere bakabilirsin!"}
    
    edu_weights = {"Yok": 0, "İlkokul": 1, "Ortaokul": 2, "Lise": 3, "Üniversite": 4, "Yüksek Lisans": 5}
    if edu_weights.get(char.education_level, 0) < edu_weights.get(job_spec["required_education"], 0):
        return {"success": False, "message": f"Bu pozisyon en az '{job_spec['required_education']}' diploması istiyor (Senin: {char.education_level})."}
    
    if chosen_opt != job_spec["correct_opt"]:
        return {"success": False, "message": "Mülakatta verdiğin yanıt İK komitesi tarafından uygun bulunmadı!"}
    
    new_job = Job(
        id=job_spec["id"],
        title=job_spec["title"],
        category=job_spec["category"],
        salary=job_spec["salary"],
        required_education=job_spec["required_education"],
        required_smarts=job_spec["required_smarts"],
        performance=75,
        stress=35
    )
    char.current_job = new_job
    char.happiness = min(100, char.happiness + 18)
    msg = f"Mülakatı geçtin! '{job_spec['title']}' olarak işe başladın (Yıllık: {job_spec['salary']:,} TL)!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="💼"))
    return {"success": True, "message": msg}

def apply_part_time_job(char: Character, pt_id: str) -> Dict[str, Any]:
    if char.age < 14:
        return {"success": False, "message": "Yarı zamanlı işler için en az 14 yaşında olmalısın."}
    pt = next((p for p in PART_TIME_JOBS if p["id"] == pt_id), None)
    if not pt:
        return {"success": False, "message": "Yarı zamanlı iş bulunamadı."}
    
    char.part_time_job = Job(
        id=pt["id"],
        title=pt["title"],
        category="Yarı Zamanlı",
        salary=pt["salary"],
        performance=80,
        stress=20
    )
    msg = f"'{pt['title']}' olarak yarı zamanlı işe başladın (Yıllık Ek Gelir: {pt['salary']:,} TL)!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="⏱️"))
    return {"success": True, "message": msg}

def start_new_business(char: Character, biz_id: str) -> Dict[str, Any]:
    if char.age < 18:
        return {"success": False, "message": "Şirket kurmak için 18 yaşını doldurmuş olmalısın."}
    if char.business:
        return {"success": False, "message": f"Zaten '{char.business.name}' adlı bir girişimin var! Önce onu büyüt veya sat."}
    
    b_spec = next((b for b in BUSINESS_TYPES if b["id"] == biz_id), None)
    if not b_spec:
        return {"success": False, "message": "Girişim türü bulunamadı."}
    
    if char.money < b_spec["cost"]:
        return {"success": False, "message": f"'{b_spec['name']}' kurmak için {b_spec['cost']:,} TL sermaye gerekiyor."}
    
    char.money -= b_spec["cost"]
    char.business = Business(
        id=b_spec["id"],
        name=b_spec["name"],
        sector=b_spec["sector"],
        capital_invested=b_spec["cost"],
        valuation=b_spec["cost"],
        annual_profit=b_spec["base_profit"],
        employees=4,
        reputation=75
    )
    if "boss" not in char.achievements:
        char.achievements.append("boss")
    char.happiness = min(100, char.happiness + 25)
    msg = f"🏢 Kendi işinin patronu oldun! '{b_spec['name']}' resmen faaliyete başladı!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🏢"))
    return {"success": True, "message": msg}

def invest_in_business(char: Character) -> Dict[str, Any]:
    if not char.business:
        return {"success": False, "message": "Aktif bir şirketin yok."}
    invest_cost = int(char.business.valuation * 0.25)
    if char.money < invest_cost:
        return {"success": False, "message": f"Pazarlama ve büyüme yatırımı için {invest_cost:,} TL nakit gerekiyor."}
    
    char.money -= invest_cost
    char.business.capital_invested += invest_cost
    char.business.employees += random.randint(2, 6)
    boost = random.uniform(1.25, 1.45)
    char.business.annual_profit = int(char.business.annual_profit * boost)
    char.business.valuation = int(char.business.valuation * 1.35)
    char.business.reputation = min(100, char.business.reputation + 10)
    msg = f"🚀 Şirketine {invest_cost:,} TL yatırım yaptın! Yeni şube/ürün lansmanıyla yıllık kârın {char.business.annual_profit:,} TL'ye yükseldi!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🚀"))
    return {"success": True, "message": msg}

def sell_business(char: Character) -> Dict[str, Any]:
    if not char.business:
        return {"success": False, "message": "Satılacak bir şirketin yok."}
    sale_val = char.business.valuation
    b_name = char.business.name
    char.money += sale_val
    char.business = None
    char.happiness = min(100, char.happiness + 20)
    msg = f"🤝 '{b_name}' şirketini büyük bir yatırımcı gruba {sale_val:,} TL karşılığında sattın (Exit)!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="💰"))
    return {"success": True, "message": msg}

def work_harder(char: Character) -> Dict[str, Any]:
    if not char.current_job:
        return {"success": False, "message": "Şu anda bir işin yok."}
    char.current_job.performance = min(100, char.current_job.performance + 15)
    char.current_job.stress = min(100, char.current_job.stress + 8)
    char.stress = min(100, char.stress + 8)
    return {"success": True, "message": f"Fazla mesai yapıp projeleri yetiştirdin! (İş Performansı: %{char.current_job.performance})"}

def ask_for_raise_or_promotion(char: Character) -> Dict[str, Any]:
    if not char.current_job:
        return {"success": False, "message": "Çalıştığın bir iş yok."}
    if char.current_job.performance >= 78:
        increase = int(char.current_job.salary * 0.22)
        char.current_job.salary += increase
        char.current_job.level += 1
        char.current_job.performance = 65
        char.happiness = min(100, char.happiness + 15)
        msg = f"📈 Terfi ve %22 Maaş Zammı aldın! Yeni Maaşın: {char.current_job.salary:,} TL/yıl (Kademe {char.current_job.level})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="📈"))
        return {"success": True, "message": msg}
    else:
        return {"success": False, "message": f"Yöneticin: 'Terfi için performansın en az %78 olmalı (Şu an: %{char.current_job.performance})' diyerek reddetti."}

def quit_job(char: Character) -> Dict[str, Any]:
    if not char.current_job and not char.part_time_job:
        return {"success": False, "message": "Zaten bir işte çalışmıyorsun."}
    titles = []
    if char.current_job:
        titles.append(char.current_job.title)
        char.current_job = None
    if char.part_time_job:
        titles.append(char.part_time_job.title)
        char.part_time_job = None
    msg = f"{', '.join(titles)} görevinden istifa ettin."
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="👋"))
    return {"success": True, "message": msg}

# ================= DERİN FLÖRT, AŞK & İNSAN İLİŞKİLERİ SİSTEMİ =================

def _build_candidate(char: Character, filter_type: str = "standard", preferred_personalities: List[str] = None) -> DatingCandidate:
    partner_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
    p_names = FIRST_NAMES_FEMALE if partner_gender == "Kadın" else FIRST_NAMES_MALE
    p_name = f"{random.choice(p_names)} {random.choice(LAST_NAMES)}"
    p_age = max(16, char.age + random.randint(-3, 4))

    if preferred_personalities:
        eligible_p = [p for p in PERSONALITIES if p["id"] in preferred_personalities]
        p_spec = random.choice(eligible_p) if eligible_p else random.choice(PERSONALITIES)
    else:
        p_spec = random.choice(PERSONALITIES)

    looks = random.randint(45, 96)
    smarts = random.randint(45, 96)
    wealth = random.randint(30, 90)
    jobs_pool = ["Mimar", "Öğretmen", "Yazılım Mühendisi", "Diş Hekimi", "Avukat", "Grafik Tasarımcı", "Müzisyen", "Uzman Doktor", "Girişimci", "Pazarlama Uzmanı", "Pilot", "İç Mimar"]

    if filter_type == "vip_wealth":
        wealth = random.randint(85, 100)
        jobs_pool = ["Holding Veliahtı", "Başcerrah", "Yatırım Bankası Direktörü", "Teknoloji CEO'su", "Ünlü Müteahhit"]
    elif filter_type == "vip_looks":
        looks = random.randint(88, 100)
        jobs_pool = ["Moda İkonu / Manken", "Dizi & Sinema Oyuncusu", "Fitness Antrenörü", "Pilates Eğitmeni", "Hostes / Kabin Amiri"]
    elif filter_type == "vip_smarts":
        smarts = random.randint(88, 100)
        jobs_pool = ["Akademisyen / Profesör", "Yapay Zeka Araştırmacısı", "Beyin Cerrahı", "Uzay Mühendisi", "Yargıtay Hukukçusu"]

    if char.age < 21:
        job_title = "Üniversite Öğrencisi" if char.age >= 18 else "Lise Öğrencisi"
    else:
        job_title = random.choice(jobs_pool)

    interests = random.sample(INTERESTS_POOL, 3)
    bios = DATING_BIOS_BY_PERSONALITY.get(p_spec["id"], ["Hayatın tadını çıkarıyorum ✨"])
    bio = random.choice(bios)

    # Uyumluluk hesabı (karakterin statları ve karizmasına göre)
    base_comp = random.randint(58, 88)
    charisma_bonus = int(char.skills.get("charisma", 20) / 10)
    compatibility = min(99, base_comp + charisma_bonus)

    return DatingCandidate(
        id=f"cand_{uuid.uuid4().hex[:6]}",
        name=p_name,
        gender=partner_gender,
        age=p_age,
        job=job_title,
        city=char.city,
        zodiac=random.choice(ZODIAC_SIGNS),
        personality=p_spec["id"],
        looks=looks,
        smarts=smarts,
        craziness=max(10, min(95, p_spec["crazy_bias"] + random.randint(-12, 12))),
        loyalty=max(20, min(100, p_spec["loyalty_bias"] + random.randint(-10, 10))),
        wealth=wealth,
        money_generosity=random.randint(40, 95),
        interests=interests,
        bio=bio,
        love_language=random.choice(LOVE_LANGUAGES),
        compatibility=compatibility
    )

def generate_dating_candidates(char: Character, filter_type: str = "standard") -> Dict[str, Any]:
    """KısmetApp için 4 detaylı flört adayı üretir."""
    if char.age < 15:
        return {"success": False, "message": "KısmetApp kullanmak için en az 15 yaşında olmalısın."}

    cost_map = {
        "standard": 0,
        "vip_wealth": 5000,
        "vip_looks": 3000,
        "vip_smarts": 3000
    }
    cost = cost_map.get(filter_type, 0)
    if cost > 0 and char.money < cost:
        return {"success": False, "message": f"KısmetApp Gold VIP filtresi için {cost:,} TL gerekli."}
    if cost > 0:
        char.money -= cost

    char.dating_candidates = [_build_candidate(char, filter_type) for _ in range(4)]
    msg = "📱 KısmetApp profilleri yenilendi! Adayları inceleyip beğendiğin kişiyle eşleşebilirsin."
    return {"success": True, "message": msg, "candidates": [c.model_dump() for c in char.dating_candidates]}

def swipe_dating_candidate(char: Character, candidate_id: str, relation_mode: str = "Sevgili") -> Dict[str, Any]:
    """KısmetApp'te bir adayı beğenip eşleşme."""
    cand = next((c for c in char.dating_candidates if c.id == candidate_id), None)
    if not cand:
        return {"success": False, "message": "Aday profili bulunamadı."}

    # Mevcut eş/sevgili kontrolü
    existing_partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive), None)
    target_rel = "Flört" if existing_partner else relation_mode

    # Eşleşme şansı
    match_prob = (cand.compatibility / 100.0) * 0.75 + (char.looks / 400.0) + (char.skills.get("charisma", 20) / 400.0)
    if cand.personality == "Materyalist" and char.net_worth < 250000:
        match_prob -= 0.25

    char.dating_candidates = [c for c in char.dating_candidates if c.id != candidate_id]

    if random.random() < max(0.35, min(0.95, match_prob)):
        new_person = Person(
            id=f"person_lover_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=cand.name,
            relation=target_rel,
            gender=cand.gender,
            age=cand.age,
            relationship_level=82 if target_rel == "Sevgili" else 70,
            job=cand.job,
            money_generosity=cand.money_generosity,
            personality=cand.personality,
            zodiac=cand.zodiac,
            looks=cand.looks,
            smarts=cand.smarts,
            craziness=cand.craziness,
            loyalty=cand.loyalty,
            wealth=cand.wealth,
            interests=cand.interests,
            bio=cand.bio,
            love_language=cand.love_language,
            red_flags=random.sample(RED_FLAGS_POOL, 1) if random.random() < 0.65 else [],
            green_flags=random.sample(GREEN_FLAGS_POOL, 1) if random.random() < 0.75 else [],
            memories=[f"KısmetApp üzerinden %{cand.compatibility} uyumla eşleşip tanıştınız."],
            chat_history=[{"sender": "them", "text": f"Selam {char.first_name}! Eşleştiğimize çok sevindim 😊✨"}]
        )
        char.relationships.append(new_person)
        if target_rel == "Sevgili":
            char.dating_partner_id = new_person.id
        if "first_love" not in char.achievements:
            char.achievements.append("first_love")
        lovers_count = len([p for p in char.relationships if p.relation in ["Flört", "Sevgili", "Nişanlı", "Eş", "Eski Sevgili"]])
        if lovers_count >= 3 and "heartbreaker" not in char.achievements:
            char.achievements.append("heartbreaker")

        char.happiness = min(100, char.happiness + 18)
        msg = f"💘 EŞLEŞME! {cand.name} ({cand.age}, {cand.job} - {cand.personality}) seninle eşleşti ve ilk buluşmanız harika geçti! ({target_rel})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💘"))
        return {"success": True, "matched": True, "message": msg, "person_id": new_person.id}
    else:
        return {
            "success": False,
            "matched": False,
            "message": f"💔 {cand.name} profilini sağa kaydırmadı veya mesajına dönmedi. Başka kısmetlere bak!"
        }

def meet_someone_at_place(char: Character, place_id: str) -> Dict[str, Any]:
    """Sosyal mekanlarda veya Görücü Usulüyle tanışma."""
    if char.age < 16:
        return {"success": False, "message": "Sosyal tanışma mekanları için en az 16 yaşında olmalısın."}
    place = next((pl for pl in MEET_PLACES if pl["id"] == place_id), None)
    if not place:
        return {"success": False, "message": "Mekan bulunamadı."}
    if char.money < place["cost"]:
        return {"success": False, "message": f"{place['name']} için {place['cost']:,} TL gerekli."}

    char.money -= place["cost"]
    filter_mode = "vip_wealth" if place.get("wealth_boost") else "standard"
    cand = _build_candidate(char, filter_mode, place["preferred_personalities"])

    existing_partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive), None)
    rel_label = "Flört" if existing_partner else "Sevgili"

    new_person = Person(
        id=f"person_lover_{len(char.relationships)+1}_{random.randint(10,99)}",
        name=cand.name,
        relation=rel_label,
        gender=cand.gender,
        age=cand.age,
        relationship_level=84 if rel_label == "Sevgili" else 74,
        job=cand.job,
        money_generosity=cand.money_generosity,
        personality=cand.personality,
        zodiac=cand.zodiac,
        looks=cand.looks,
        smarts=cand.smarts,
        craziness=cand.craziness,
        loyalty=cand.loyalty,
        wealth=cand.wealth,
        interests=cand.interests,
        bio=cand.bio,
        love_language=cand.love_language,
        red_flags=random.sample(RED_FLAGS_POOL, 1) if random.random() < 0.65 else [],
        green_flags=random.sample(GREEN_FLAGS_POOL, 1) if random.random() < 0.75 else [],
        memories=[f"{place['name']} vasıtasıyla tanıştınız."],
        chat_history=[{"sender": "them", "text": f"Bugün {place['name']} ortamında tanışmamız harika bir tesadüftü 🌟"}]
    )
    char.relationships.append(new_person)
    if rel_label == "Sevgili":
        char.dating_partner_id = new_person.id
    if "first_love" not in char.achievements:
        char.achievements.append("first_love")
    char.happiness = min(100, char.happiness + 20)

    if place_id == "family_match":
        for p in char.relationships:
            if p.relation in ["Anne", "Baba"]:
                p.relationship_level = min(100, p.relationship_level + 12)
        msg = f"👵 Ailenin tanıştırdığı {cand.name} ({cand.job}, {cand.personality}) ile çay içip çok iyi anlaştınız! ({rel_label})"
    else:
        msg = f"✨ {place['name']} ortamında {cand.name} ({cand.age}, {cand.job} - {cand.personality}) ile göz göze gelip tanıştın! ({rel_label})"

    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🌹"))
    return {"success": True, "message": msg, "person_id": new_person.id}

def find_love_date(char: Character) -> Dict[str, Any]:
    """Hızlı flört bulma (KısmetApp adaylarını da hazırlar)."""
    return generate_dating_candidates(char, "standard")

def go_on_venue_date(char: Character, person_id: str, venue_id: str) -> Dict[str, Any]:
    """Partneri seçilen bir randevu mekanına götürme (kişilik uyumu etkili!)."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    venue = next((v for v in DATE_VENUES if v["id"] == venue_id), None)
    if not venue:
        return {"success": False, "message": "Randevu mekanı bulunamadı."}
    if char.money < venue["cost"]:
        return {"success": False, "message": f"{venue['name']} için {venue['cost']:,} TL gerekli."}

    char.money -= venue["cost"]
    boost = venue["rel_boost"]

    if person.personality in venue.get("disliked_by", []):
        person.relationship_level = max(10, person.relationship_level - 10)
        char.happiness = max(0, char.happiness - 8)
        msg = f"😒 {person.name} ({person.personality}), '{venue['name']}' seçimini fazla ucuz/sıradan buldu ve burun kıvırdı! (İlişki -10)"
        person.memories.append(f"{venue['name']} randevusunu pek beğenmedi.")
        return {"success": False, "message": msg}

    bonus_note = ""
    if person.personality in venue.get("best_for", []):
        boost = int(boost * 1.45)
        bonus_note = f" ({person.personality} ruhuna tam hitap etti! 🔥)"

    person.relationship_level = min(100, person.relationship_level + boost)
    char.happiness = min(100, char.happiness + 16)
    person.memories.append(f"Birlikte {venue['name']} randevusuna çıktınız.")

    # Eğer Flört ise ve ilişki >= 82 olduysa Sevgiliye dönüşsün!
    existing_main = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.id != person.id and p.is_alive), None)
    if person.relation == "Flört" and person.relationship_level >= 82 and not existing_main:
        person.relation = "Sevgili"
        char.dating_partner_id = person.id
        bonus_note += " ❤️ Artık resmen SEVGİLİ oldunuz!"

    msg = f"🌹 {person.name} ile '{venue['name']}' randevunuz büyüleyici geçti!{bonus_note} (İlişki +{boost})"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🌹"))
    return {"success": True, "message": msg}

def give_custom_gift(char: Character, person_id: str, gift_id: str) -> Dict[str, Any]:
    """Seçilen özel bir hediyeyi verme."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    gift = next((g for g in ROMANTIC_GIFTS if g["id"] == gift_id), None)
    if not gift:
        return {"success": False, "message": "Hediye bulunamadı."}
    if char.money < gift["cost"]:
        return {"success": False, "message": f"{gift['name']} almak için {gift['cost']:,} TL gerekli."}

    char.money -= gift["cost"]
    boost = gift["rel_boost"]
    if person.personality == "Materyalist" and gift["cost"] >= 45000:
        boost += 15

    person.relationship_level = min(100, person.relationship_level + boost)
    person.loyalty = min(100, person.loyalty + 6)
    char.happiness = min(100, char.happiness + 12)
    char.karma = min(100, char.karma + 5)
    person.memories.append(f"Ona {gift['name']} hediye ettin.")

    msg = f"🎁 {person.name} aldığın '{gift['name']}' hediyesine bayıldı ve boynuna sarıldı! (İlişki +{boost})"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🎁"))
    return {"success": True, "message": msg}

def propose_marriage(char: Character, ring_cost: int = 35000, person_id: str = None, ring_id: str = None) -> Dict[str, Any]:
    """Yüzük seçimiyle evlilik teklifi etme (Sevgili -> Nişanlı)."""
    if person_id:
        partner = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    else:
        partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Flört"] and p.is_alive), None)

    if not partner:
        return {"success": False, "message": "Evlenme teklif edecek bir sevgilin yok."}
    if char.age < 18:
        return {"success": False, "message": "Evlenmek için en az 18 yaşında olmalısın."}

    ring_name = "Tektaş Yüzük"
    bonus_chance = 0.20
    if ring_id:
        r_spec = next((r for r in ENGAGEMENT_RINGS if r["id"] == ring_id), None)
        if r_spec:
            ring_cost = r_spec["cost"]
            ring_name = r_spec["name"]
            bonus_chance = r_spec["bonus_chance"]

    if char.money < ring_cost:
        return {"success": False, "message": f"{ring_name} için {ring_cost:,} TL gerekli."}

    if partner.personality == "Materyalist" and ring_cost < 35000:
        partner.relationship_level = max(10, partner.relationship_level - 20)
        return {"success": False, "message": f"💔 {partner.name} (Materyalist) gümüş yüzüğe baktı: 'Bana pırlanta bile alamıyor musun?!' diyerek teklifi reddetti!"}

    char.money -= ring_cost
    accept_chance = 0.45 + (partner.relationship_level / 200.0) + bonus_chance
    if random.random() < accept_chance:
        partner.relation = "Nişanlı"
        partner.relationship_level = 100
        partner.memories.append(f"{ring_name} ile evlilik teklifini kabul etti ve nişanlandınız.")
        char.happiness = 100
        msg = f"💍 EVET DEDİ! {partner.name}, '{ring_name}' ile yaptığın teklifi gözyaşlarıyla kabul etti! Artık NİŞANLISINIZ! Şimdi düğün organize edebilirsin."
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💍"))
        return {"success": True, "message": msg}
    else:
        partner.relationship_level = max(15, partner.relationship_level - 20)
        char.happiness = max(0, char.happiness - 18)
        msg = f"💔 {partner.name} henüz evliliğe hazır hissetmediğini söyleyerek teklifini geri çevirdi."
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💔"))
        return {"success": False, "message": msg}

def plan_wedding_ceremony(
    char: Character,
    person_id: str,
    venue_id: str = "wedding_hall",
    sign_prenup: bool = False,
    guest_tier: str = "family_friends"
) -> Dict[str, Any]:
    """Nişanlı/Sevgili ile düğün töreni, Davetli Listesi ve Evlilik Sözleşmesi (Prenup)."""
    partner = next((p for p in char.relationships if (p.id == person_id or p.relation in ["Nişanlı", "Sevgili"]) and p.is_alive), None)
    if not partner:
        return {"success": False, "message": "Evlenecek bir nişanlın veya sevgilin yok."}
    if char.age < 18:
        return {"success": False, "message": "Evlenmek için en az 18 yaşında olmalısın."}

    venue = next((w for w in WEDDING_VENUES if w["id"] == venue_id), WEDDING_VENUES[1])
    if char.money < venue["cost"]:
        return {"success": False, "message": f"{venue['name']} organizasyonu için {venue['cost']:,} TL gerekli."}

    # Evlilik sözleşmesi (Prenup) tepkisi
    if sign_prenup and partner.personality in ["Kıskanç & Tutkulu", "Materyalist"] and partner.relationship_level < 85:
        partner.relationship_level = max(20, partner.relationship_level - 18)
        return {"success": False, "message": f"😤 {partner.name} evlilik sözleşmesini görünce öfkelendi: 'Bana güvenmiyorsan evlenmeyelim!' (Önce gönlünü alıp ilişkiyi %85 üstüne çıkar!)"}

    char.money -= venue["cost"]
    base_gifts = random.randint(venue["min_gifts"], venue["max_gifts"])
    guest_note = ""
    if guest_tier == "vip_press":
        wedding_gifts = int(base_gifts * 1.35)
        char.fame = min(100, char.fame + 15)
        guest_note = " (VIP Cemiyet & Magazin Basını katıldı, Şöhret +15!)"
    elif guest_tier == "core_family":
        wedding_gifts = int(base_gifts * 0.85)
        partner.family_approval = min(100, partner.family_approval + 18)
        guest_note = " (Samimi Çekirdek Aile töreni, Aile Onayı +18!)"
    else:
        wedding_gifts = base_gifts
        guest_note = " (Tüm Akrabalar & Dostlar katıldı!)"

    char.money += wedding_gifts

    partner.relation = "Eş"
    partner.cohabiting = True
    partner.has_prenup = bool(sign_prenup)
    partner.relationship_level = 100
    char.spouse_id = partner.id
    char.happiness = min(100, char.happiness + venue["hap_boost"])
    if "married" not in char.achievements:
        char.achievements.append("married")

    prenup_note = " (Mal ayrılığı sözleşmesi imzalandı)" if sign_prenup else ""
    partner.memories.append(f"{venue['name']} ile evlendiniz. Takıdan {wedding_gifts:,} TL toplandı.")
    msg = f"👰🤵 DÜĞÜN! {partner.name} ile '{venue['name']}' töreninde dünyaevine girdiniz!{prenup_note}{guest_note} Takı merasiminde {wedding_gifts:,} TL altın ve nakit toplandı!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="👰"))
    return {"success": True, "message": msg}

def try_for_baby(char: Character) -> Dict[str, Any]:
    partner = next((p for p in char.relationships if p.relation in ["Eş", "Nişanlı", "Sevgili"] and p.is_alive), None)
    if not partner:
        return {"success": False, "message": "Çocuk sahibi olmak için bir eşin veya sevgilin olmalı."}
    if char.age < 18 or partner.age > 52:
        return {"success": False, "message": "Şu anda biyolojik olarak çocuk sahibi olmak için uygun yaşta değilsiniz."}
    
    if random.random() < 0.75:
        b_gender = random.choice(["Erkek", "Kadın"])
        b_names = FIRST_NAMES_MALE if b_gender == "Erkek" else FIRST_NAMES_FEMALE
        baby_name = f"{random.choice(b_names)} {char.last_name}"
        p_spec = random.choice(PERSONALITIES)
        
        char.pregnancy_partner_id = partner.id
        char.pregnancy_baby_gender = b_gender

        baby = Person(
            id=f"person_child_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=baby_name,
            relation="Çocuk",
            gender=b_gender,
            age=0,
            relationship_level=100,
            personality=p_spec["id"],
            zodiac=random.choice(ZODIAC_SIGNS),
            looks=random.randint(55, 98),
            smarts=random.randint(55, 98),
            memories=[f"{char.age} yaşındayken dünyaya geldi."]
        )
        char.relationships.append(baby)
        partner.memories.append(f"{baby_name} adlı çocuğunuz dünyaya geldi.")
        char.happiness = min(100, char.happiness + 30)
        if "child" not in char.achievements:
            char.achievements.append("child")
        msg = f"👶 Müjde! Dünyalar tatlısı bir {'oğlunuz' if b_gender == 'Erkek' else 'kızınız'} doğdu! Adını {baby_name} koydunuz! (İstersen Baby Shower / Hoşgeldin Bebek partisi düzenleyebilirsin!)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🍼"))
        return {"success": True, "message": msg}
    else:
        return {"success": False, "message": "Bu yıl bebek denemeniz sonuç vermedi. Tekrar deneyebilirsiniz."}

def adopt_child_from_agency(char: Character) -> Dict[str, Any]:
    """Çocuk Esirgeme Kurumundan evlat edinme."""
    if char.age < 24:
        return {"success": False, "message": "Evlat edinmek için en az 24 yaşında olmalısın."}
    if char.is_in_prison or char.criminal_record:
        return {"success": False, "message": "Sabıka kaydın nedeniyle sosyal hizmetler evlat edinme başvurunu onaylamadı."}
    cost = 25000
    if char.money < cost:
        return {"success": False, "message": f"Evlat edinme dosya ve bakım hazırlıkları için {cost:,} TL gerekli."}

    char.money -= cost
    b_gender = random.choice(["Erkek", "Kadın"])
    b_names = FIRST_NAMES_MALE if b_gender == "Erkek" else FIRST_NAMES_FEMALE
    child_name = f"{random.choice(b_names)} {char.last_name}"
    child_age = random.randint(1, 5)
    p_spec = random.choice(PERSONALITIES)

    adopted = Person(
        id=f"person_child_{len(char.relationships)+1}_{random.randint(10,99)}",
        name=child_name,
        relation="Çocuk",
        gender=b_gender,
        age=child_age,
        relationship_level=100,
        personality=p_spec["id"],
        zodiac=random.choice(ZODIAC_SIGNS),
        memories=["Sevgi dolu yuvana evlat edinildi."]
    )
    char.relationships.append(adopted)
    char.karma = min(100, char.karma + 25)
    char.happiness = min(100, char.happiness + 30)
    if "child" not in char.achievements:
        char.achievements.append("child")

    msg = f"🍼 Sosyal Hizmetler başvurunu onayladı! {child_age} yaşındaki {child_name}'i evlat edinip sıcak bir yuva verdin! (Karma +25)"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="👶"))
    return {"success": True, "message": msg}

def make_new_friend(char: Character) -> Dict[str, Any]:
    f_gender = random.choice(["Erkek", "Kadın"])
    f_names = FIRST_NAMES_MALE if f_gender == "Erkek" else FIRST_NAMES_FEMALE
    f_name = f"{random.choice(f_names)} {random.choice(LAST_NAMES)}"
    p_spec = random.choice(PERSONALITIES)
    new_friend = Person(
        id=f"friend_{len(char.relationships)+1}_{random.randint(10,99)}",
        name=f_name,
        relation="Arkadaş",
        gender=f_gender,
        age=max(6, char.age + random.randint(-2, 2)),
        relationship_level=82,
        job=random.choice(["Mühendis", "Öğretmen", "Esnaf", "Avukat", "Müzisyen", "Sporcu"]),
        personality=p_spec["id"],
        zodiac=random.choice(ZODIAC_SIGNS),
        interests=random.sample(INTERESTS_POOL, 2),
        memories=[f"{char.age} yaşındayken arkadaş oldunuz."]
    )
    char.relationships.append(new_friend)
    char.happiness = min(100, char.happiness + 10)
    msg = f"🤝 {f_name} ({new_friend.personality}) ile sıkı bir dostluk kurdun!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🤝"))
    return {"success": True, "message": msg}

def adopt_pet_from_shelter(char: Character, breed_idx: int) -> Dict[str, Any]:
    if breed_idx < 0 or breed_idx >= len(PET_BREEDS):
        return {"success": False, "message": "Geçersiz evcil hayvan seçimi."}
    spec = PET_BREEDS[breed_idx]
    if char.money < spec["cost"]:
        return {"success": False, "message": f"{spec['breed']} sahiplenmek için {spec['cost']:,} TL gerekli."}
    
    char.money -= spec["cost"]
    pet_name = random.choice(PET_NAMES)
    new_pet = Pet(
        id=f"pet_{len(char.pets)+1}_{random.randint(10,99)}",
        name=pet_name,
        species=spec["species"],
        breed=spec["breed"],
        age=1,
        relationship_level=95
    )
    char.pets.append(new_pet)
    char.happiness = min(100, char.happiness + 18)
    char.karma = min(100, char.karma + 10)
    msg = f"🐾 '{pet_name}' ({spec['breed']}) adlı sevimli dostu sahiplendin!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🐾"))
    return {"success": True, "message": msg}

def interact_with_pet(char: Character, pet_id: str, action: str) -> Dict[str, Any]:
    pet = next((pt for pt in char.pets if pt.id == pet_id and pt.is_alive), None)
    if not pet:
        return {"success": False, "message": "Evcil hayvan bulunamadı."}
    if action == "play":
        pet.relationship_level = min(100, pet.relationship_level + 12)
        char.happiness = min(100, char.happiness + 8)
        return {"success": True, "message": f"🐾 {pet.name} ile parkta koşup oynadınız! Çok mutlu oldu."}
    elif action == "vet":
        if char.money < 1200:
            return {"success": False, "message": "Veteriner kontrolü için 1.200 TL gerekli."}
        char.money -= 1200
        pet.health = 100
        pet.relationship_level = min(100, pet.relationship_level + 8)
        return {"success": True, "message": f"🩺 {pet.name} veterinerde aşılarını oldu, sağlığı %100!"}
    return {"success": False, "message": "Geçersiz işlem."}

def interact_with_person(char: Character, person_id: str, action: str) -> Dict[str, Any]:
    """Kişilerle derin etkileşimler (Aile, Flört, Sevgili, Eş, Eski Sevgili, Çocuk, Arkadaş)."""
    person = next((p for p in char.relationships if p.id == person_id), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    if not person.is_alive:
        return {"success": False, "message": f"{person.name} maalesef hayatta değil."}
    
    if action == "chat":
        person.relationship_level = min(100, person.relationship_level + 10)
        char.happiness = min(100, char.happiness + 5)
        return {"success": True, "message": f"💬 {person.name} ile kahve eşliğinde samimi bir sohbet ettiniz. (İlişki +10)"}

    elif action == "compliment":
        person.relationship_level = min(100, person.relationship_level + 12)
        char.happiness = min(100, char.happiness + 6)
        char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + 3)
        return {"success": True, "message": f"✨ {person.name}'e içten bir iltifat ettin, yüzünde güller açtı! (İlişki +12)"}

    elif action == "deep_talk":
        person.relationship_level = min(100, person.relationship_level + 15)
        person.loyalty = min(100, person.loyalty + 5)
        person.memories.append("Gece boyu hayat ve gelecek hayalleriniz üzerine derin bir sohbet ettiniz.")
        return {"success": True, "message": f"🌙 {person.name} ile gelecek hayalleriniz ve sırlarınız üzerine derin bir konuşma yaptınız. Aranızdaki güven perçinlendi! (İlişki +15)"}

    elif action == "spend_time":
        person.relationship_level = min(100, person.relationship_level + 14)
        char.happiness = min(100, char.happiness + 10)
        return {"success": True, "message": f"🍿 {person.name} ile dışarı çıkıp çok eğlenceli bir gün geçirdiniz!"}

    elif action == "give_gift":
        gift_cost = 2500
        if char.money < gift_cost:
            return {"success": False, "message": f"Hediye için {gift_cost:,} TL gerekli."}
        char.money -= gift_cost
        person.relationship_level = min(100, person.relationship_level + 22)
        char.karma = min(100, char.karma + 5)
        person.memories.append("Ona sürpriz bir hediye aldın.")
        return {"success": True, "message": f"🎁 {person.name} aldığın hediyeye bayıldı! (İlişki +22)"}

    elif action == "ask_money":
        if person.relationship_level < 50:
            return {"success": False, "message": f"{person.name} seninle arası soğuk olduğu için para vermeyi reddetti."}
        amount = random.randint(2500, 18000)
        char.money += amount
        person.relationship_level = max(0, person.relationship_level - 8)
        person.memories.append(f"Sana {amount:,} TL maddi destek verdi.")
        return {"success": True, "message": f"💸 {person.name} sana {amount:,} TL maddi destek verdi!"}

    elif action == "family_dinner":
        cost = 2000
        if char.money < cost:
            return {"success": False, "message": "Aile yemeği organizasyonu için 2.000 TL gerekli."}
        char.money -= cost
        for p in char.relationships:
            if p.is_alive and p.relation in ["Anne", "Baba", "Ağabey", "Abla", "Kardeş", "Çocuk", "Eş"]:
                p.relationship_level = min(100, p.relationship_level + 18)
        char.happiness = min(100, char.happiness + 15)
        char.karma = min(100, char.karma + 8)
        return {"success": True, "message": "🍲 Tüm aileyi neşeli bir akşam yemeği sofrasında topladın! Bütün aile üyeleriyle ilişkin +18 arttı!"}

    elif action == "parent_blessing":
        person.relationship_level = min(100, person.relationship_level + 15)
        char.karma = min(100, char.karma + 12)
        char.happiness = min(100, char.happiness + 10)
        person.memories.append("Elini öpüp hayır duasını aldın.")
        return {"success": True, "message": f"🙏 {person.name}'in elini öpüp hayır duasını aldın: 'Allah işini gücünü rast getirsin evladım!' (Karma +12, Mutluluk +10)"}

    elif action == "educate_child":
        person.smarts = min(100, person.smarts + 12)
        person.relationship_level = min(100, person.relationship_level + 15)
        char.happiness = min(100, char.happiness + 10)
        person.memories.append("Derslerine yardım edip gelecek vizyonu kazandırdın.")
        return {"success": True, "message": f"📚 Çocuğun {person.name} ile ders çalışıp satranç oynadın! (Çocuğun Zekası: %{person.smarts}, İlişki +15)"}

    elif action == "ask_matchmake":
        if person.relationship_level < 60:
            return {"success": False, "message": f"{person.name} sana çöpçatanlık yapmak için önce aranızın daha iyi olmasını bekliyor."}
        return meet_someone_at_place(char, "library_cafe")

    elif action == "ask_relationship":
        # Flört -> Sevgili
        if person.relation != "Flört":
            return {"success": False, "message": "Sadece Flört aşamasındaki birine çıkma teklifi edebilirsin."}
        if person.relationship_level >= 65:
            # Eski sevgiliyi Eski Sevgili statüsüne çek
            for p in char.relationships:
                if p.relation == "Sevgili" and p.id != person.id:
                    p.relation = "Eski Sevgili"
            person.relation = "Sevgili"
            char.dating_partner_id = person.id
            person.relationship_level = min(100, person.relationship_level + 15)
            person.memories.append("Resmen sevgili oldunuz!")
            char.happiness = min(100, char.happiness + 20)
            msg = f"💘 {person.name} çıkma teklifini kabul etti! Artık resmen SEVGİLİSİNİZ!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💘"))
            return {"success": True, "message": msg}
        else:
            return {"success": False, "message": f"{person.name} henüz birbirinizi yeterince tanımadığınızı söyledi (Önce randevuya çıkıp ilişkiyi %65 üstüne çıkar)."}

    elif action == "move_in":
        if person.relation not in ["Sevgili", "Nişanlı", "Eş"]:
            return {"success": False, "message": "Sadece sevgilin veya nişanlınla aynı eve çıkabilirsin."}
        if person.cohabiting:
            return {"success": False, "message": f"{person.name} ile zaten aynı evde yaşıyorsunuz!"}
        if person.relationship_level < 75:
            return {"success": False, "message": f"{person.name} aynı eve çıkmak için ilişkinizin biraz daha güçlenmesini (%75+) istiyor."}
        person.cohabiting = True
        person.relationship_level = min(100, person.relationship_level + 15)
        person.memories.append("Anahtarları birleştirip aynı eve taşındınız.")
        char.happiness = min(100, char.happiness + 18)
        msg = f"🏠🔑 {person.name} ile aynı eve taşındınız! Artık hayatı ve ev masraflarını paylaşıyorsunuz!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🏠"))
        return {"success": True, "message": msg}

    elif action == "couples_therapy":
        cost = 4000
        if char.money < cost:
            return {"success": False, "message": f"Çift terapisi seansı için {cost:,} TL gerekli."}
        char.money -= cost
        person.relationship_level = min(100, person.relationship_level + 28)
        person.loyalty = min(100, person.loyalty + 12)
        person.craziness = max(10, person.craziness - 10)
        person.memories.append("Çift terapisine giderek aranızdaki sorunları çözdünüz.")
        return {"success": True, "message": f"🛋️ Uzman psikolog eşliğinde {person.name} ile çift terapisine gittiniz. İletişiminiz ve güveniniz yenilendi! (İlişki +28)"}

    elif action == "text_ex":
        if person.relation not in ["Eski Sevgili", "Eski Eş"]:
            return {"success": False, "message": "Bu kişi eski sevgilin değil."}
        if random.random() < (0.45 + person.relationship_level / 200.0):
            # Mevcut sevgili varsa
            for p in char.relationships:
                if p.relation == "Sevgili":
                    p.relation = "Eski Sevgili"
            person.relation = "Sevgili"
            person.relationship_level = max(75, person.relationship_level + 25)
            person.memories.append("Ayrılığa dayanamayıp yeniden barıştınız!")
            char.dating_partner_id = person.id
            char.happiness = min(100, char.happiness + 22)
            msg = f"❤️‍🔥 AŞK YENİDEN! Gece yarısı attığın 'Seni çok özledim' mesajına {person.name} anında cevap verdi ve buluşup barıştınız!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="❤️‍🔥"))
            return {"success": True, "message": msg}
        else:
            person.relationship_level = max(0, person.relationship_level - 10)
            return {"success": False, "message": f"💔 {person.name} mesajını 'Görüldü' bıraktı ve geri dönmek istemediğini söyledi."}

    elif action == "cheat":
        char.karma = max(0, char.karma - 25)
        if random.random() < 0.55:
            # Yakalandı!
            person.relationship_level = 5
            person.memories.append("Onu aldattığını öğrendi ve kalbi paramparça oldu!")
            char.happiness = max(0, char.happiness - 30)
            msg = f"😱 YAKALANDIN! {person.name} gizli kaçamağını öğrendi! Kıyamet koptu ve ilişkiniz uçurumun eşiğine geldi!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="😱"))
            return {"success": False, "message": msg}
        else:
            char.happiness = min(100, char.happiness + 10)
            return {"success": True, "message": f"🤫 Gizli bir kaçamak yaşadın. {person.name} hiçbir şey fark etmedi ama vicdanın sızlıyor. (Karma -25)"}

    elif action == "argue":
        person.relationship_level = max(0, person.relationship_level - 25)
        char.happiness = max(0, char.happiness - 12)
        person.memories.append("Şiddetli bir tartışma yaşadınız.")
        return {"success": True, "message": f"🤬 {person.name} ile şiddetli bir tartışma yaşadınız! (İlişki -25)"}

    elif action == "breakup":
        if person.relation in ["Flört", "Sevgili", "Nişanlı", "Eş"]:
            is_divorce = (person.relation == "Eş")
            person.cohabiting = False
            if is_divorce:
                person.relation = "Eski Eş"
                char.spouse_id = None
                if person.has_prenup:
                    loss = 0
                    prenup_msg = "Evlilik sözleşmen (Prenup) sayesinde tek kuruş nafaka/tazminat ödemedin!"
                else:
                    loss = max(0, int(char.money * 0.35))
                    char.money -= loss
                    prenup_msg = f"Mahkeme kararıyla mal paylaşımı olarak {loss:,} TL ödedin."
                char.happiness = max(0, char.happiness - 25)
                person.memories.append("Mahkemede resmen boşandınız.")
                msg = f"💔 {person.name} ile boşandınız! {prenup_msg}"
            else:
                person.relation = "Eski Sevgili"
                char.dating_partner_id = None
                char.happiness = max(0, char.happiness - 12)
                person.memories.append("Yollarınızı ayırdınız.")
                msg = f"💔 {person.name} ile ayrıldınız. Artık 'Eski Sevgili' statüsünde."
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💔"))
            return {"success": True, "message": msg}

    elif action == "introduce_family":
        if person.relation not in ["Flört", "Sevgili", "Nişanlı", "Eş"]:
            return {"success": False, "message": "Sadece romantik partnerini ailenle tanıştırabilirsin."}
        parents = [p for p in char.relationships if p.relation in ["Anne", "Baba"] and p.is_alive]
        if not parents:
            person.met_family = True
            person.family_approval = 85
            return {"success": True, "message": f"{person.name}'e aile yadigarı fotoğrafları gösterip geçmişini anlattın."}

        person.met_family = True
        approval_score = int((person.smarts * 0.4) + (person.loyalty * 0.4) + random.randint(10, 25))
        if person.personality in ["Sadık & Aileci", "Entelektüel", "Romantik", "Hırslı & Kariyerist"]:
            approval_score += 12
        elif person.personality in ["Çapkın & Özgür Ruhlu", "Materyalist"]:
            approval_score -= 10
        person.family_approval = max(15, min(100, approval_score))

        if person.family_approval >= 65:
            person.relationship_level = min(100, person.relationship_level + 16)
            for pr in parents:
                pr.relationship_level = min(100, pr.relationship_level + 12)
            person.memories.append(f"Ailenle tanıştı ve %{person.family_approval} aile onayı aldı!")
            char.happiness = min(100, char.happiness + 15)
            msg = f"👨‍👩‍👧‍👦 {person.name}'i ailenle tanıştırdın! Anne ve baban onun saygısına ve muhabbetine hayran kaldı! (Aile Onayı: %{person.family_approval}, İlişki +16)"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="👨‍👩‍👧"))
            return {"success": True, "message": msg}
        else:
            person.relationship_level = max(10, person.relationship_level - 6)
            person.memories.append("Ailenle tanışma yemeğinde biraz soğuk rüzgarlar esti.")
            msg = f"😬 {person.name} ile ailenin tanışma yemeğinde biraz gerginlik yaşandı. Ailen pek ısınamadı (Aile Onayı: %{person.family_approval})."
            return {"success": True, "message": msg}

    elif action == "check_loyalty":
        if person.loyalty < 45:
            person.has_prenup = True  # Kusurlu taraf olduğu için nafaka/mal paylaşımı hakkını kaybeder
            person.relationship_level = max(5, person.relationship_level - 35)
            person.memories.append("Gizli mesajlarını yakaladın!")
            msg = f"🕵️‍♂️ ŞOK GERÇEK! {person.name}'in telefonunda gizli flört mesajları yakaladın! Sadakati çok düşükmüş (%{person.loyalty}). Artık kusurlu sayıldığı için tazminatsız ayrılabilirsin!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🕵️‍♂️"))
            return {"success": True, "message": msg}
        else:
            if random.random() < 0.45:
                person.relationship_level = max(10, person.relationship_level - 14)
                person.memories.append("Telefonunu karıştırdığını fark edip kırıldı.")
                return {"success": False, "message": f"🕵️ {person.name} tertemiz ve sadık çıktı (%{person.loyalty}), ancak onu gizlice kontrol ettiğini fark edip sana kırıldı! (İlişki -14)"}
            return {"success": True, "message": f"🛡️ {person.name}'in sadakatini kontrol ettin: Sana tamamen bağlı ve sadık (%{person.loyalty})! İçini ferah tutabilirsin."}

    elif action == "celebrate_anniversary":
        cost = 3000
        if char.money < cost:
            return {"success": False, "message": f"Yıldönümü kutlaması için {cost:,} TL gerekli."}
        char.money -= cost
        boost = 22
        if person.love_language in ["Hediye & Sürprizler", "Kaliteli Zaman"]:
            boost += 8
        person.relationship_level = min(100, person.relationship_level + boost)
        person.loyalty = min(100, person.loyalty + 8)
        char.happiness = min(100, char.happiness + 16)
        person.memories.append("Romantik bir yıldönümü sürpriziyle aşkınızı tazelediniz.")
        msg = f"🥂✨ {person.name} için muhteşem bir yıldönümü sürprizi hazırladın! Gözleri mutluluktan parladı! (İlişki +{boost})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🥂"))
        return {"success": True, "message": msg}

    elif action == "apologize":
        boost = 20 if person.relationship_level < 60 else 10
        person.relationship_level = min(100, person.relationship_level + boost)
        char.karma = min(100, char.karma + 5)
        person.memories.append("İçten bir özür dileyip gönlünü aldın.")
        return {"success": True, "message": f"🕊️ {person.name}'den içtenlikle özür dileyip gönlünü aldın. Aranızdaki buzlar eridi! (İlişki +{boost})"}

    elif action == "visit_inlaws":
        # Kayınvalide / Görümce / Eşin Ailesini Ziyaret & Kriz Yönetimi
        if person.relation not in ["Flört", "Sevgili", "Nişanlı", "Eş"]:
            return {"success": False, "message": "Sadece romantik partnerinin ailesini ziyaret edebilirsin."}
        cost = 1500
        if char.money < cost:
            return {"success": False, "message": "Aile ziyaretine eli boş gitmemek (tatlı & çiçek) için 1.500 TL gerekli."}
        char.money -= cost
        person.met_family = True
        if random.random() < 0.72 + (char.skills.get("charisma", 20) / 400.0):
            person.family_approval = min(100, person.family_approval + 20)
            person.relationship_level = min(100, person.relationship_level + 16)
            char.happiness = min(100, char.happiness + 12)
            person.memories.append("Kayınvalide ve ailesini ziyaret edip gönüllerini fethettin.")
            msg = f"👵💐 {person.name}'in ailesini ziyarete gittin! Kayınvaliden götürdüğün baklavaya ve tatlı diline bayıldı! (Aile Onayı: %{person.family_approval}, İlişki +16)"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="👵"))
            return {"success": True, "message": msg}
        else:
            person.family_approval = max(10, person.family_approval - 8)
            person.relationship_level = min(100, person.relationship_level + 6)
            person.memories.append("Kayınvalide/görümce ziyaretinde ufak bir laf sokma krizi yaşandı ama eşinin yanında durdun.")
            msg = f"😅 {person.name}'in ailesini ziyarette kayınvalide/görümce biraz laf soktu ama ortamı kibarca idare ettin! ({person.name} sabrına hayran kaldı: İlişki +6)"
            return {"success": True, "message": msg}

    elif action == "baby_shower":
        # Baby Shower & Cinsiyet / Hoşgeldin Bebek Partisi
        cost = 5000
        if char.money < cost:
            return {"success": False, "message": f"Baby Shower & Cinsiyet Partisi organizasyonu için {cost:,} TL gerekli."}
        char.money -= cost
        gifts = random.randint(15000, 48000)
        char.money += gifts
        person.relationship_level = min(100, person.relationship_level + 22)
        for p in char.relationships:
            if p.is_alive and p.relation in ["Anne", "Baba", "Çocuk", "Arkadaş", "Kardeş", "Abla", "Ağabey"]:
                p.relationship_level = min(100, p.relationship_level + 12)
        char.happiness = min(100, char.happiness + 24)
        b_gen = char.pregnancy_baby_gender or random.choice(["Erkek", "Kadın"])
        confetti = "💙 MAVİ KONFETİ (Erkek Bebek!)" if b_gen == "Erkek" else "🩷 PEMBE KONFETİ (Kız Bebek!)"
        person.memories.append(f"Muhteşem bir Baby Shower & Cinsiyet Partisi düzenlediniz ({confetti}).")
        msg = f"🎈👶 BABY SHOWER & CİNSİYET PARTİSİ! Balon patlatıldı: {confetti}! Akraba ve dostlardan {gifts:,} TL altın ve bebek hediyesi toplandı!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🎈"))
        return {"success": True, "message": msg}

    elif action == "group_party":
        return do_group_party(char)

    elif action == "fake_stalk":
        # Sahte (Fake) Hesaptan Stalklama
        if person.relation in ["Eski Sevgili", "Eski Eş"]:
            person.memories.append("Onu fake hesaptan gizlice stalkladın.")
            if person.relationship_level >= 50:
                return {"success": True, "message": f"🕵️‍♀️ Fake hesaptan {person.name}'in profiline baktın: Hâlâ hüzünlü şarkılar paylaşıyor ve seni unutamamış! (Barışma şansı yüksek)"}
            else:
                return {"success": True, "message": f"🕵️‍♀️ Fake hesaptan {person.name}'i stalkladın: Yeni bir hayata başlamış görünüyor."}
        elif person.loyalty < 55:
            person.has_prenup = True
            person.relationship_level = max(10, person.relationship_level - 25)
            person.memories.append("Fake hesaptan gizli flörtlerini yakaladın!")
            msg = f"🕵️‍♀️🚨 FAKE HESAPTAN YAKALADIN! Açtığın sahte hesaptan {person.name}'in başkalarının fotoğraflarına '🔥' attığını ve DM'leştiğini belgeledin!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🕵️‍♀️"))
            return {"success": True, "message": msg}
        else:
            return {"success": True, "message": f"🕵️‍♀️ Fake hesaptan {person.name}'in takip ettiklerini ve beğenilerini inceledin: Şüpheli hiçbir durum yok, sana tamamen sadık (%{person.loyalty})!"}

    elif action == "ghost_block":
        # Ghostlama & Her Yerden Engelleme
        person.is_blocked = True
        person.cohabiting = False
        if person.relation in ["Flört", "Sevgili", "Nişanlı"]:
            person.relation = "Eski Sevgili"
            if char.dating_partner_id == person.id:
                char.dating_partner_id = None
        person.relationship_level = 0
        person.memories.append("Onu her yerden engelleyip (Ghosting) hayatından çıkardın.")
        msg = f"🚫👻 {person.name}'i WhatsApp ve tüm sosyal ağlardan engelleyip (Ghosting) hayatından çıkardın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🚫"))
        return {"success": True, "message": msg}

    elif action == "hire_detective":
        # Özel Dedektif Tutma (Paket 11)
        cost = 15000
        if char.money < cost:
            return {"success": False, "message": f"Özel dedektif ve gizli takip dosyası için {cost:,} TL gerekli."}
        char.money -= cost
        if person.loyalty < 60:
            person.has_prenup = True
            person.relationship_level = max(5, person.relationship_level - 35)
            person.memories.append("Özel dedektif tutarak gizli buluşmasını fotoğraflarla belgeledin!")
            msg = f"🕵️‍♂️📸 DEDEKTİF DOSYASI! Tuttuğun özel dedektif, {person.name}'in gizli bir buluşmasını fotoğraflarla belgeledi! Artık mahkemede %100 haklısın, tek kuruş nafaka ödemeden ayrılabilirsin!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🕵️‍♂️"))
            return {"success": True, "message": msg}
        else:
            person.memories.append("Özel dedektif takibinden tertemiz çıktı.")
            return {"success": True, "message": f"🕵️‍♂️✅ Özel dedektif 1 hafta boyunca {person.name}'i adım adım izledi: 'Rapor tertemiz! Eşiniz/partneriniz işten eve, evden işe gidiyor ve size %100 sadık!'"}

    elif action == "dna_test":
        # Gizli DNA / Babalık Testi (Paket 11)
        cost = 8000
        if char.money < cost:
            return {"success": False, "message": f"Özel genetik laboratuvarında DNA testi için {cost:,} TL gerekli."}
        char.money -= cost
        if random.random() < 0.88:
            person.relationship_level = min(100, person.relationship_level + 10)
            msg = f"🧬✅ DNA TEST SONUCU: %99.99 Biyolojik Uyum! {person.name} ile genetik bağınız resmi laboratuvar raporuyla doğrulandı. İçindeki tüm şüpheler silindi!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🧬"))
            return {"success": True, "message": msg}
        else:
            char.happiness = max(10, char.happiness - 25)
            msg = f"🧬😱 YASAK ELMA ŞOKU! Laboratuvardan gelen DNA raporunda hastanede bebeklerin karışmış olabileceği veya büyük bir aile sırrı olduğu ortaya çıktı! Tazminat davası açtın ve +250.000 TL kazandın!"
            char.money += 250000
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="😱"))
            return {"success": True, "message": msg}

    elif action == "kiz_isteme":
        # Geleneksel Kız İsteme & Tuzlu Kahve Merasimi (Paket 17)
        if person.relation not in ["Flört", "Sevgili", "Nişanlı"]:
            return {"success": False, "message": "Geleneksel isteme merasimi sadece sevgilin veya nişanlın için yapılabilir."}
        cost = 12000
        if char.money < cost:
            return {"success": False, "message": f"Gümüş gondol çikolata, çiçek buketi ve isteme hazırlığı için {cost:,} TL gerekli."}
        char.money -= cost

        # Gerçekçi Zorluk: Düzenli iş/gelir veya yüksek aile onayı & hitabet kontrolü
        has_income_source = bool(char.current_job or char.business or char.political_office or char.sports_career or char.money >= 250000)
        charisma = char.skills.get("charisma", 20)
        if not has_income_source and person.family_approval < 65 and charisma < 50:
            person.family_approval = max(15, person.family_approval - 8)
            return {
                "success": False,
                "message": f"☕😬 {person.name}'in babası kaşlarını çattı: 'Evladım henüz düzenli bir işin veya birikimin yok, önce hayatını kur sonra tekrar konuşalım!' diyerek yüzükleri takmayı reddetti!"
            }

        person.kiz_isteme_done = True
        person.met_family = True
        person.relation = "Nişanlı"
        person.family_approval = min(100, person.family_approval + 22)
        person.relationship_level = min(100, person.relationship_level + 18)
        char.happiness = min(100, char.happiness + 18)
        person.memories.append("Aile büyükleriyle istemeye gittiniz, bol tuzlu damat kahvesini son damlasına kadar içip söz yüzüklerini taktınız!")
        msg = f"☕💍 KIZ İSTEME & TUZLU KAHVE! Aile büyükleriyle {person.name}'i istemeye gittiniz! Bol tuzlu kahveyi yüzünü bile buruşturmadan içtin, 'Allah'ın emri peygamberin kavliyle' söz ve nişan yüzükleri takıldı! (Aile Onayı: %{person.family_approval})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="☕"))
        return {"success": True, "message": msg}

    elif action == "nisan_kina":
        # Karşılıklı Nişan Bohçası & Kına Gecesi / Bekarlığa Veda (Paket 17)
        if person.relation not in ["Sevgili", "Nişanlı", "Eş"]:
            return {"success": False, "message": "Nişan bohçası ve kına gecesi için bir partnerin olmalı."}
        cost = 35000
        if char.money < cost:
            return {"success": False, "message": f"Nişan bohçası alışverişi ve Kına / Bekarlığa Veda gecesi için {cost:,} TL gerekli."}
        char.money -= cost
        person.nisan_bohca_done = True
        kina_gold = random.randint(22000, 58000)
        char.money += kina_gold
        person.family_approval = min(100, person.family_approval + 18)
        person.relationship_level = min(100, person.relationship_level + 16)
        char.happiness = min(100, char.happiness + 20)
        person.memories.append("Özenli nişan bohçaları hazırlandı ve unutulmaz bir Kına Gecesi & Bekarlığa Veda kutlaması yapıldı.")
        msg = f"🎁💃 NİŞAN BOHÇASI & KINA GECESİ! Karşılıklı lüks nişan bohçaları verildi, kına gecesinde 'Yüksek Yüksek Tepelere' eşliğinde avuçlara altınlar konuldu (+{kina_gold:,} TL takı toplandı)!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💃"))
        return {"success": True, "message": msg}

    elif action == "private_school":
        # Çocuğu Özel Koleje / Kurs & Etüde Gönderme (Paket 17)
        cost = 45000
        if char.money < cost:
            return {"success": False, "message": f"Özel kolej, yabancı dil ve bilim/sanat akademisi kaydı için {cost:,} TL gerekli."}
        char.money -= cost
        person.smarts = min(100, person.smarts + 18)
        person.relationship_level = min(100, person.relationship_level + 15)
        char.happiness = min(100, char.happiness + 12)
        person.memories.append("Onu en iyi özel koleje ve yabancı dil/bilim kurslarına gönderdin.")
        msg = f"🎓🏫 {person.name}'i seçkin bir özel koleje ve yetenek kurslarına kaydettirdin! Zekası ve gelecek vizyonu parladı! (Çocuk Zekası: %{person.smarts})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🏫"))
        return {"success": True, "message": msg}

    elif action == "marry_off_child":
        # Çocuğunu Evlendirme & Torun Sahibi Olma (Paket 17)
        cost = 85000
        if char.money < cost:
            return {"success": False, "message": f"Çocuğunun düğün ve çeyiz/ev kurma desteği için {cost:,} TL gerekli."}
        char.money -= cost
        if person.age < 20:
            person.age = 22
        person.job = person.job or "Uzman Mühendis / Doktor"
        person.relationship_level = 100
        person.memories.append("Ona muhteşem bir düğün yaptın ve ilk torununu kucağına verdiler!")

        g_gender = random.choice(["Erkek", "Kadın"])
        pool = FIRST_NAMES_MALE if g_gender == "Erkek" else FIRST_NAMES_FEMALE
        g_name = f"{random.choice(pool)} {char.last_name}"
        grandchild = Person(
            id=f"grandchild_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=g_name,
            relation="Torun",
            gender=g_gender,
            age=0,
            relationship_level=100,
            zodiac=random.choice(ZODIAC_SIGNS),
            looks=random.randint(70, 98),
            smarts=random.randint(70, 98),
            memories=[f"{person.name}'in evliliğinden dünyaya gelen ilk torunun!"]
        )
        char.relationships.append(grandchild)
        char.happiness = 100
        if "grandparent" not in char.achievements:
            char.achievements.append("grandparent")

        msg = f"👰🤵👶 TORUN MÜJDESİ! Çocuğun {person.name}'i görkemli bir düğünle evlendirdin ve çok geçmeden nur topu gibi torunun '{g_name}' dünyaya geldi! Artık bir Büyükbaba/Büyükanne oldun!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="👶"))
        return {"success": True, "message": msg}

    return {"success": False, "message": "Geçersiz eylem."}

def send_dm_message(char: Character, person_id: str, topic_id: str) -> Dict[str, Any]:
    """Kişiye WhatsApp/DM üzerinden mesaj gönderir ve kişiliğine uygun canlı yanıt üretir."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    topic = next((t for t in DM_TOPICS if t["id"] == topic_id), None)
    if not topic:
        return {"success": False, "message": "Mesaj konusu bulunamadı."}

    my_msg = topic["my_text"]
    person.chat_history.append({"sender": "me", "text": my_msg})

    reply = "Teşekkür ederim canım 😊"
    rel_delta = 10

    if topic_id == "flirt_msg":
        rel_delta = 14
        if person.love_language == "Tatlı Sözler & İltifat":
            rel_delta += 8
        replies_by_p = {
            "Romantik": "Kalbim yerinden çıkacak gibi oldu... Ben de seni her saniye düşünüyorum aşkım 🌹❤️",
            "Kıskanç & Tutkulu": "Sadece beni düşün zaten! Akşam buluşalım, seni çok özledim ❤️‍🔥",
            "Materyalist": "Çok tatlısın hayatım! Akşam şık bir yerde kutlayalım mı? 💎🥂",
            "Entelektüel": "Ruhuma dokunan kelimelerin günümü aydınlattı, iyi ki varsın ✨📚",
            "Eğlenceli": "Ooo bugün romantizm tavan yapmış! Akşama hazır ol 😍🎉"
        }
        reply = replies_by_p.get(person.personality, "Senin bu tatlı mesajların beni benden alıyor, iyi ki hayatımdasın 💘")

    elif topic_id == "funny_meme":
        rel_delta = 12
        reply = "Ahahaha sesli güldüm! 😂 Seninle enerjimiz gerçekten bambaşka ya! 🔥"
        char.happiness = min(100, char.happiness + 8)

    elif topic_id == "future_dream":
        rel_delta = 15
        person.loyalty = min(100, person.loyalty + 6)
        reply = "Seninle kuracağımız güzel geleceği düşündükçe içim huzurla doluyor 🏡🤍"

    elif topic_id == "jealous_check":
        if person.craziness > 65 or person.personality == "Çapkın & Özgür Ruhlu":
            rel_delta = -12
            reply = "Bana sürekli hesap sormandan bunaldım artık! Biraz güvenmeyi öğren! 😤"
        else:
            rel_delta = 6
            reply = "Aşkım kıskandın mı sen beni? 😊 Merak etme, yanımdaki kuzenimdi, gözüm senden başkasını görmez ❤️"

    elif topic_id == "apology_msg":
        rel_delta = 18 if person.relationship_level < 65 else 9
        reply = "Böyle düşünmen ve yazman beni çok mutlu etti, kırgınlığım geçti bile 🕊️🤍"

    person.relationship_level = max(0, min(100, person.relationship_level + rel_delta))
    person.chat_history.append({"sender": "them", "text": reply})
    if len(person.chat_history) > 12:
        person.chat_history = person.chat_history[-12:]

    sign = f"+{rel_delta}" if rel_delta >= 0 else str(rel_delta)
    return {
        "success": rel_delta >= 0,
        "message": f"📱 {person.name}: \"{reply}\" (İlişki {sign})",
        "reply": reply
    }

def take_couple_vacation(char: Character, person_id: str, vacation_id: str) -> Dict[str, Any]:
    """Partnerle baş başa romantik tatil / balayı."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    vac = next((v for v in COUPLE_VACATIONS if v["id"] == vacation_id), None)
    if not vac:
        return {"success": False, "message": "Tatil rotası bulunamadı."}
    if char.money < vac["cost"]:
        return {"success": False, "message": f"{vac['name']} için {vac['cost']:,} TL gerekli."}

    char.money -= vac["cost"]
    boost = vac["rel_boost"]
    if person.love_language == "Kaliteli Zaman":
        boost += 10
    person.relationship_level = min(100, person.relationship_level + boost)
    person.loyalty = min(100, person.loyalty + 8)
    char.happiness = min(100, char.happiness + vac["hap_boost"])
    person.memories.append(f"Birlikte unutulmaz bir '{vac['name']}' tatiline çıktınız.")
    person.chat_history.append({"sender": "them", "text": f"{vac['name']} tatilimiz hayatımın en güzel günleriydi! 🥰✈️"})

    msg = f"✈️💑 {person.name} ile '{vac['name']}' kaçamağınız rüya gibi geçti! (İlişki +{boost}, Mutluluk +{vac['hap_boost']})"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="✈️"))
    return {"success": True, "message": msg}

def do_social_hangout(char: Character, person_id: str, hangout_id: str) -> Dict[str, Any]:
    """Arkadaş, kardeş veya aile üyesiyle sosyal aktivite."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    hg = next((h for h in SOCIAL_HANGOUTS if h["id"] == hangout_id), None)
    if not hg:
        return {"success": False, "message": "Aktivite bulunamadı."}
    if char.money < hg["cost"]:
        return {"success": False, "message": f"{hg['name']} için {hg['cost']:,} TL gerekli."}

    char.money -= hg["cost"]
    person.relationship_level = min(100, person.relationship_level + hg["rel_boost"])
    char.happiness = min(100, char.happiness + 14)
    person.memories.append(f"Birlikte '{hg['name']}' etkinliğinde harika vakit geçirdiniz.")
    person.chat_history.append({"sender": "them", "text": f"Bugünkü {hg['name']} çok iyi geldi, iyi ki varsın dostum! 🙌"})

    msg = f"🎉 {person.name} ile '{hg['name']}' yaptınız, dostluğunuz pekişti! (İlişki +{hg['rel_boost']})"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🎉"))
    return {"success": True, "message": msg}

def set_will_beneficiary(char: Character, target: str) -> Dict[str, Any]:
    char.will_beneficiary = target
    labels = {
        "all_children": "Tüm Çocuklara Eşit Pay",
        "spouse": "Yalnızca Eşe",
        "charity": "Hayır Kurumu & Eğitim Vakfına"
    }
    return {"success": True, "message": f"📜 Noter onaylı vasiyetnamen güncellendi: Mirasın '{labels.get(target, target)}' bırakılacak."}

# ----------------- VARLIKLAR & ALIM SATIM -----------------

def buy_real_estate(char: Character, index: int) -> Dict[str, Any]:
    if index < 0 or index >= len(REAL_ESTATE_MARKET):
        return {"success": False, "message": "Geçersiz mülk."}
    prop = REAL_ESTATE_MARKET[index]
    if char.money < prop["price"]:
        return {"success": False, "message": f"Bu mülkü almak için {prop['price']:,} TL gerekli."}
    
    char.money -= prop["price"]
    t_name = f"{random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}"
    new_asset = Asset(
        id=f"house_{len(char.assets)+1}_{random.randint(10,99)}",
        name=prop["name"],
        asset_type="Ev",
        purchase_price=prop["price"],
        current_value=prop["price"],
        annual_cost=prop["annual_cost"],
        annual_income=prop["annual_rent"],
        tenant_name=t_name
    )
    char.assets.append(new_asset)
    if "homeowner" not in char.achievements:
        char.achievements.append("homeowner")
    char.happiness = min(100, char.happiness + 20)
    msg = f"🏠 '{prop['name']}' tapusunu aldın! Yıllık {prop['annual_rent']:,} TL kira geliri sağlayacak."
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🏠"))
    return {"success": True, "message": msg}

def buy_vehicle(char: Character, index: int) -> Dict[str, Any]:
    if index < 0 or index >= len(VEHICLE_MARKET):
        return {"success": False, "message": "Geçersiz araç."}
    if not char.has_drivers_license:
        return {"success": False, "message": "Araç satın almak için önce ehliyet almalısın!"}
    car = VEHICLE_MARKET[index]
    if char.money < car["price"]:
        return {"success": False, "message": f"Bu aracı almak için {car['price']:,} TL gerekli."}
    
    char.money -= car["price"]
    new_asset = Asset(
        id=f"car_{len(char.assets)+1}_{random.randint(10,99)}",
        name=car["name"],
        asset_type="Araba",
        purchase_price=car["price"],
        current_value=car["price"],
        annual_cost=car["annual_cost"]
    )
    char.assets.append(new_asset)
    char.happiness = min(100, char.happiness + 18)
    msg = f"🏎️ '{car['name']}' satın aldın!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🏎️"))
    return {"success": True, "message": msg}

def sell_asset(char: Character, asset_id: str) -> Dict[str, Any]:
    asset = next((a for a in char.assets if a.id == asset_id), None)
    if not asset:
        return {"success": False, "message": "Varlık bulunamadı."}
    sale_price = int(asset.current_value * 0.96)
    char.money += sale_price
    char.assets = [a for a in char.assets if a.id != asset_id]
    msg = f"'{asset.name}' {sale_price:,} TL bedelle satıldı."
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="💰"))
    return {"success": True, "message": msg}

# ----------------- BORSA, İNTERAKTİF BLACKJACK & KAZI KAZAN -----------------

def buy_stock(char: Character, symbol: str, amount_tl: int) -> Dict[str, Any]:
    if amount_tl <= 0 or char.money < amount_tl:
        return {"success": False, "message": "Yeterli nakit paran yok."}
    if symbol not in char.stocks:
        return {"success": False, "message": "Hisse bulunamadı."}
    
    stock = char.stocks[symbol]
    shares_to_buy = int(amount_tl / stock.current_price)
    if shares_to_buy <= 0:
        return {"success": False, "message": f"En az 1 lot almak için {stock.current_price:.2f} TL gerekli."}
    
    total_cost = int(shares_to_buy * stock.current_price)
    prev_val = stock.shares * stock.avg_buy_price
    stock.shares += shares_to_buy
    stock.avg_buy_price = round((prev_val + total_cost) / stock.shares, 2)
    char.money -= total_cost
    return {"success": True, "message": f"🟢 {shares_to_buy} adet {symbol} aldın (Toplam: {total_cost:,} TL)."}

def sell_stock(char: Character, symbol: str, shares_count: int) -> Dict[str, Any]:
    if symbol not in char.stocks or char.stocks[symbol].shares <= 0:
        return {"success": False, "message": "Portföyünde bu hisseden yok."}
    stock = char.stocks[symbol]
    actual_sell = min(stock.shares, shares_count) if shares_count > 0 else stock.shares
    total_revenue = int(actual_sell * stock.current_price)
    stock.shares -= actual_sell
    if stock.shares == 0:
        stock.avg_buy_price = 0.0
    char.money += total_revenue
    return {"success": True, "message": f"🔴 {actual_sell} adet {symbol} sattın ve {total_revenue:,} TL tahsil ettin!"}

def _draw_card() -> tuple[str, int]:
    suits = ["♠️", "♥️", "♦️", "♣️"]
    ranks = [
        ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7),
        ("8", 8), ("9", 9), ("10", 10), ("J", 10), ("Q", 10), ("K", 10), ("A", 11)
    ]
    r, val = random.choice(ranks)
    s = random.choice(suits)
    return f"{r}{s}", val

def _calc_hand_total(cards: list[str]) -> int:
    total = 0
    aces = 0
    for c in cards:
        rank = c[:-2]
        if rank in ["J", "Q", "K", "10"]:
            total += 10
        elif rank == "A":
            total += 11
            aces += 1
        else:
            total += int(rank)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def blackjack_action(char: Character, sub_action: str, bet: int = 1000) -> Dict[str, Any]:
    bj = char.blackjack
    if sub_action == "start":
        if bet <= 0 or char.money < bet:
            return {"success": False, "message": "Bahis için yeterli nakit paran yok."}
        char.money -= bet
        c1, _ = _draw_card()
        c2, _ = _draw_card()
        d1, _ = _draw_card()
        d2, _ = _draw_card()
        bj.active = True
        bj.bet = bet
        bj.player_cards = [c1, c2]
        bj.dealer_cards = [d1, d2]
        bj.player_total = _calc_hand_total(bj.player_cards)
        bj.dealer_total = _calc_hand_total([d1])
        bj.status = "playing"

        if bj.player_total == 21:
            win = int(bet * 2.5)
            char.money += win
            bj.active = False
            bj.dealer_total = _calc_hand_total(bj.dealer_cards)
            bj.status = "won"
            return {"success": True, "won": True, "message": f"🎉 BLACKJACK! Doğrudan 21 yaptın ve +{win:,} TL kazandın!"}
        return {"success": True, "message": "Kartlar dağıtıldı! Kart Çek (Hit) veya Kal (Stand) seç."}

    elif sub_action == "hit":
        if not bj.active:
            return {"success": False, "message": "Aktif bir Blackjack eli yok."}
        nc, _ = _draw_card()
        bj.player_cards.append(nc)
        bj.player_total = _calc_hand_total(bj.player_cards)
        if bj.player_total > 21:
            bj.active = False
            bj.dealer_total = _calc_hand_total(bj.dealer_cards)
            bj.status = "lost"
            return {"success": False, "won": False, "message": f"💥 BUST! Elin {bj.player_total} oldu ve 21'i geçtin. {bj.bet:,} TL kaybettin."}
        return {"success": True, "message": f"Kart çektin: {nc}. Toplam elin: {bj.player_total}"}

    elif sub_action == "stand":
        if not bj.active:
            return {"success": False, "message": "Aktif bir Blackjack eli yok."}
        bj.active = False
        bj.dealer_total = _calc_hand_total(bj.dealer_cards)
        while bj.dealer_total < 17:
            nc, _ = _draw_card()
            bj.dealer_cards.append(nc)
            bj.dealer_total = _calc_hand_total(bj.dealer_cards)

        if bj.dealer_total > 21 or bj.player_total > bj.dealer_total:
            win = bj.bet * 2
            char.money += win
            bj.status = "won"
            char.happiness = min(100, char.happiness + 10)
            return {"success": True, "won": True, "message": f"🏆 KAZANDIN! Senin: {bj.player_total}, Krupiye: {bj.dealer_total}. +{win:,} TL kazandın!"}
        elif bj.player_total == bj.dealer_total:
            char.money += bj.bet
            bj.status = "push"
            return {"success": True, "won": False, "message": f"🤝 Berabere ({bj.player_total})! Bahsin ({bj.bet:,} TL) iade edildi."}
        else:
            bj.status = "lost"
            return {"success": False, "won": False, "message": f"❌ KAYBETTİN! Krupiye {bj.dealer_total} yaptı (Senin: {bj.player_total})."}

    return {"success": False, "message": "Geçersiz Blackjack hamlesi."}

def play_scratch_card(char: Character) -> Dict[str, Any]:
    cost = 1000
    if char.money < cost:
        return {"success": False, "message": "Kazı Kazan kartı için 1.000 TL gerekli."}
    char.money -= cost
    symbols = ["🍒", "🍋", "🔔", "💎", "🍀", "💰"]
    roll = random.random()
    if roll < 0.03:
        prize = 250000
        grid = ["💎", "💎", "💎"]
    elif roll < 0.18:
        prize = 15000
        grid = ["💰", "💰", "💰"]
    elif roll < 0.42:
        prize = 3000
        grid = ["🍀", "🍀", "🍀"]
    else:
        prize = 0
        grid = random.sample(symbols, 3)

    if prize > 0:
        char.money += prize
        char.happiness = min(100, char.happiness + 12)
        return {"success": True, "grid": grid, "prize": prize, "message": f"🎉 [{' - '.join(grid)}] Eşleşti! Kazı Kazan'dan +{prize:,} TL kazandın!"}
    else:
        return {"success": False, "grid": grid, "prize": 0, "message": f"[{' - '.join(grid)}] Maalesef bu karttan ikramiye çıkmadı."}

# ----------------- YERALTI, SUÇ VE HAPİSHANE -----------------

def commit_crime(char: Character, crime_type: str) -> Dict[str, Any]:
    if char.is_in_prison:
        return {"success": False, "message": "Zaten hapistesin!"}
    if "criminal" not in char.achievements:
        char.achievements.append("criminal")
    
    if crime_type == "pickpocket":
        if random.random() < (0.68 + char.smarts / 400):
            loot = random.randint(2500, 12000)
            char.money += loot
            char.karma = max(0, char.karma - 10)
            return {"success": True, "message": f"Kalabalıkta ustalıkla cüzdan çarptın! +{loot:,} TL kazandın."}
        else:
            char.is_in_prison = True
            char.prison_years_left = 1
            char.prison_sentence = 1
            char.criminal_record.append("Yankesicilik")
            char.happiness = max(0, char.happiness - 25)
            msg = "Yankesicilik yaparken sivil polise yakalandın! 1 Yıl hapis cezası aldın!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="🚔"))
            return {"success": False, "caught": True, "message": msg}
            
    elif crime_type == "grand_theft_auto":
        if random.random() < (0.48 + char.smarts / 300):
            loot = random.randint(80000, 300000)
            char.money += loot
            char.karma = max(0, char.karma - 20)
            return {"success": True, "message": f"Lüks bir aracı düz kontakla çalıp okuttun! +{loot:,} TL kazandın!"}
        else:
            char.is_in_prison = True
            char.prison_years_left = 3
            char.prison_sentence = 3
            char.criminal_record.append("Oto Hırsızlığı")
            char.happiness = max(0, char.happiness - 35)
            msg = "Aracı çalarken polis devriyesine yakalandın! 3 Yıl Hapis cezası!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="🚨"))
            return {"success": False, "caught": True, "message": msg}
            
    elif crime_type == "bank_robbery":
        if random.random() < (0.28 + char.smarts / 250):
            loot = random.randint(2000000, 9000000)
            char.money += loot
            char.karma = max(0, char.karma - 40)
            msg = f"🏦 KUSURSUZ VURGUN! Banka kasasını boşaltıp {loot:,} TL ile izini kaybettirdin!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="💰"))
            return {"success": True, "message": msg}
        else:
            char.is_in_prison = True
            char.prison_years_left = 8
            char.prison_sentence = 8
            char.criminal_record.append("Silahlı Banka Soygunu")
            char.happiness = max(0, char.happiness - 50)
            msg = "Özel harekat ekipleri bankayı kuşattı! Yakalandın ve 8 YIL AĞIR HAPİS cezası aldın!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="🚔"))
            return {"success": False, "caught": True, "message": msg}
            
    return {"success": False, "message": "Geçersiz suç türü."}

def prison_escape_attempt(char: Character, route: str = "tunnel") -> Dict[str, Any]:
    if not char.is_in_prison:
        return {"success": False, "message": "Hapiste değilsin."}
    
    chance = 0.25 + (char.smarts / 300) + (char.skills.get("athletics", 15) / 400)
    if route == "disguise":
        chance += 0.08
    if random.random() < chance:
        char.is_in_prison = False
        char.prison_years_left = 0
        char.happiness = min(100, char.happiness + 40)
        if "escaped" not in char.achievements:
            char.achievements.append("escaped")
        msg = "🏃💨 BÜYÜK FİRAR! Planın kusursuz işledi ve cezaevinden kaçmayı başardın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="🏃💨"))
        return {"success": True, "escaped": True, "message": msg}
    else:
        char.prison_years_left += 2
        char.health = max(10, char.health - 15)
        char.happiness = max(0, char.happiness - 25)
        msg = "Projektörler üzerine çevrildi ve sirenler çaldı! Firar girişimin başarısız oldu, cezana +2 Yıl eklendi!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="👮"))
        return {"success": False, "escaped": False, "message": msg}

def prison_activity(char: Character, activity: str) -> Dict[str, Any]:
    if not char.is_in_prison:
        return {"success": False, "message": "Hapiste değilsin."}
    
    if activity == "library":
        char.smarts = min(100, char.smarts + 6)
        return {"success": True, "message": "Cezaevi kütüphanesinde hukuk ve felsefe kitapları okudun. (Zeka +6)"}
    elif activity == "yard_workout":
        char.health = min(100, char.health + 8)
        char.skills["martial_arts"] = min(100, char.skills.get("martial_arts", 5) + 8)
        return {"success": True, "message": "Avluda ağırlık çalışıp güçlendin. (Sağlık +8, Dövüş +8)"}
    elif activity == "bribe_guard":
        cost = 30000
        if char.money < cost:
            return {"success": False, "message": f"Gardiyan için {cost:,} TL gerekli."}
        char.money -= cost
        char.prison_years_left = max(0, char.prison_years_left - 1)
        if char.prison_years_left == 0:
            char.is_in_prison = False
            return {"success": True, "message": "İyi hal dosyan onaylandı ve erken tahliye oldun!"}
        return {"success": True, "message": "Cezan 1 yıl indirildi!"}
    elif activity == "appeal_lawyer":
        cost = 60000
        if char.money < cost:
            return {"success": False, "message": f"Ünlü ceza avukatı tutmak için {cost:,} TL gerekli."}
        char.money -= cost
        if random.random() < 0.55:
            char.is_in_prison = False
            char.prison_years_left = 0
            msg = "⚖️ Tuttuğun usta avukat Yargıtay'da kararı bozdurdu ve beraat ederek tahliye oldun!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="⚖️"))
            return {"success": True, "message": msg}
        else:
            return {"success": False, "message": "Temyiz başvurusu mahkemece reddedildi."}
    return {"success": False, "message": "Bilinmeyen cezaevi aktivitesi."}

# ----------------- SOSYAL MEDYA & TATİL -----------------

def post_on_social_media(char: Character, platform: str) -> Dict[str, Any]:
    if platform not in char.social_media:
        char.social_media[platform] = SocialMediaAccount(platform=platform, followers=0)
    
    account = char.social_media[platform]
    account.posts_count += 1
    roll = random.random()
    charisma_bonus = char.skills.get("charisma", 20) * 80
    
    if roll < 0.25:
        gained = random.randint(15000, 95000) + charisma_bonus
        account.followers += gained
        char.fame = min(100, char.fame + 15)
        char.happiness = min(100, char.happiness + 18)
        if account.followers >= 100000 and "famous" not in char.achievements:
            char.achievements.append("famous")
        return {"success": True, "message": f"🔥 VİRAL OLDUN! Paylaşımın keşfete düştü ve +{gained:,} yeni takipçi kazandın!"}
    elif roll < 0.88:
        gained = random.randint(400, 4500) + int(charisma_bonus / 4)
        account.followers += gained
        if account.followers >= 100000 and "famous" not in char.achievements:
            char.achievements.append("famous")
        return {"success": True, "message": f"Harika bir içerik paylaştın. +{gained:,} takipçi geldi. (Toplam: {account.followers:,})"}
    else:
        lost = min(account.followers, random.randint(1000, 12000))
        account.followers -= lost
        char.happiness = max(0, char.happiness - 12)
        return {"success": False, "message": f"Paylaşımın tartışma yarattı ve -{lost:,} takipçi kaybettin."}

def take_vacation(char: Character, destination: str) -> Dict[str, Any]:
    dest_map = {
        "camping": ("Ege Kıyısında Çadır Kampı", 5000, 15, 10),
        "antalya": ("Antalya 5 Yıldızlı Her Şey Dahil Resort", 30000, 30, 15),
        "paris": ("Paris Romantik Kültür & Sanat Turu", 75000, 45, 12),
        "maldives": ("Maldivler Su Üstü Özel Villa", 200000, 65, 25)
    }
    if destination not in dest_map:
        return {"success": False, "message": "Geçersiz tatil rotası."}
    
    name, cost, hap_boost, health_boost = dest_map[destination]
    if char.money < cost:
        return {"success": False, "message": f"{name} için {cost:,} TL gerekli."}
    
    char.money -= cost
    char.happiness = min(100, char.happiness + hap_boost)
    char.health = min(100, char.health + health_boost)
    char.stress = 0
    # Eş veya sevgili varsa onunla ilişki de artar!
    for p in char.relationships:
        if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive:
            p.relationship_level = min(100, p.relationship_level + 18)
            p.memories.append(f"Birlikte unutulmaz bir {name} tatiline çıktınız.")
    msg = f"✈️ {name} tatiline çıktın! Tüm yorgunluğun ve stresin sıfırlandı. (Mutluluk +{hap_boost})"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="✈️"))
    return {"success": True, "message": msg}

# ----------------- PAKET 1: GRUP ARKADAŞ ORTAMI & EV PARTİSİ -----------------

def do_group_party(char: Character) -> Dict[str, Any]:
    """Tüm arkadaşlar, kardeşler ve partnerle toplu ev partisi / mangal gecesi."""
    cost = 3500
    if char.money < cost:
        return {"success": False, "message": f"Ev partisi & mangal organizasyonu için {cost:,} TL gerekli."}
    char.money -= cost
    attendees = 0
    for p in char.relationships:
        if p.is_alive and p.relation in ["Arkadaş", "Sevgili", "Nişanlı", "Eş", "Flört", "Ağabey", "Abla", "Kardeş"]:
            p.relationship_level = min(100, p.relationship_level + 18)
            attendees += 1
    char.happiness = min(100, char.happiness + 22)
    char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + 5)

    # Eğer bekarsa partide arkadaşının arkadaşıyla tanışma şansı!
    bonus_note = ""
    has_partner = any(p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive for p in char.relationships)
    if not has_partner and char.age >= 18 and random.random() < 0.45:
        meet_res = meet_someone_at_place(char, "night_club")
        if meet_res.get("success"):
            bonus_note = " Ayrıca partiye katılan sürpriz biriyle aranda kıvılcım çaktı!"

    msg = f"🍻🎶 EFSANE EV PARTİSİ! {max(1, attendees)} yakın dostun ve sevdiklerinle sabaha kadar müzik, mangal ve kahkaha dolu bir gece geçirdiniz! (Tüm Dostluklar +18, Karizma +5){bonus_note}"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🍻"))
    return {"success": True, "message": msg}

# ----------------- PAKET 2: ÜNLÜ OLMA, ŞÖHRET & MAGAZİN SİSTEMİ -----------------

def do_fame_activity(char: Character, sub_action: str) -> Dict[str, Any]:
    """Şöhret, Konser/Albüm/Film, TV Şovu, Sponsorluk, Magazin Skandalı ve VIP Ünlü Flörtü."""
    if char.age < 16:
        return {"success": False, "message": "Şöhret ve magazin dünyasına adım atmak için en az 16 yaşında olmalısın."}

    if sub_action == "audition_fame":
        cost = 2000
        if char.money < cost:
            return {"success": False, "message": f"Yetenek seçmeleri ve ajans kaydı için {cost:,} TL gerekli."}
        char.money -= cost
        score = char.looks + char.skills.get("charisma", 20) + char.skills.get("music", 10) + random.randint(10, 45)
        if score >= 110:
            fame_gain = random.randint(25, 42)
            char.fame = min(100, char.fame + fame_gain)
            char.happiness = min(100, char.happiness + 20)
            if "famous" not in char.achievements and char.fame >= 50:
                char.achievements.append("famous")
            msg = f"🌟 YILDIZ DOĞUYOR! Katıldığın Türkiye Yetenek & Ekran Seçmelerinde jüriyi büyüledin! (Şöhret +{fame_gain} -> %{char.fame})"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🌟"))
            return {"success": True, "message": msg}
        else:
            char.fame = min(100, char.fame + 8)
            return {"success": True, "message": f"🎭 Seçmelerde elinden geleni yaptın ve kamera önü tecrübesi kazandın. (Şöhret +8 -> %{char.fame})"}

    elif sub_action == "release_work":
        is_celeb_job = char.current_job and char.current_job.category in ["Sanat", "Spor"]
        if char.fame < 20 and not is_celeb_job:
            return {"success": False, "message": "Hit Albüm / Başrol Film / Şampiyonluk Maçı çıkarmak için en az %20 Şöhrete veya Sanat/Spor kariyerine sahip olmalısın!"}
        royalties = random.randint(250000, 1850000) + (char.fame * 12000)
        char.money += royalties
        char.fame = min(100, char.fame + 20)
        char.happiness = min(100, char.happiness + 24)
        if "famous" not in char.achievements:
            char.achievements.append("famous")
        msg = f"🏆🔥 ZİRVEDESİN! Yeni eserin / performansın tüm Türkiye'de 1 numaraya yerleşti! Telif ve primlerden +{royalties:,} TL kazandın! (Şöhret: %{char.fame})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🏆"))
        return {"success": True, "message": msg}

    elif sub_action == "tv_show":
        if char.fame < 15:
            return {"success": False, "message": "Prime-Time Talk Show'a davet edilmek için en az %15 Şöhret gerekli (Önce seçmelere katıl veya sosyal medyada büyü)."}
        char.fame = min(100, char.fame + 16)
        char.happiness = min(100, char.happiness + 15)
        if "Instagram" not in char.social_media:
            char.social_media["Instagram"] = SocialMediaAccount(platform="Instagram", followers=0)
        char.social_media["Instagram"].followers += 45000
        if "famous" not in char.achievements and char.fame >= 50:
            char.achievements.append("famous")
        msg = f"📺✨ Cuma gecesi en çok izlenen Talk Show programına konuk oldun! Esprilerin sosyal medyada gündem oldu! (Şöhret +16, +45.000 Takipçi)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="📺"))
        return {"success": True, "message": msg}

    elif sub_action == "brand_deal":
        if char.fame < 30:
            return {"success": False, "message": "Dev markaların reklam yüzü olmak için en az %30 Şöhret gerekli."}
        deal_pay = char.fame * 25000 + random.randint(100000, 500000)
        char.money += deal_pay
        char.fame = min(100, char.fame + 10)
        if "famous" not in char.achievements:
            char.achievements.append("famous")
        msg = f"💎📸 Lüks bir markanın reklam yüzü oldun! Billboardlarda fotoğrafların asıldı ve +{deal_pay:,} TL reklam ücreti aldın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="💎"))
        return {"success": True, "message": msg}

    elif sub_action == "paparazzi_stunt":
        char.fame = min(100, char.fame + 18)
        char.karma = max(0, char.karma - 8)
        bonus_cash = random.randint(35000, 140000)
        char.money += bonus_cash
        msg = f"📸💥 MAGAZİN BOMBA! Bebek sahilinde paparazzilere verdiğin sansasyonel demeç tüm magazin programlarında 1. sıraya oturdu! (Şöhret +18, Magazin Telifi +{bonus_cash:,} TL)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="📸"))
        return {"success": True, "message": msg}

    elif sub_action == "celebrity_date":
        if char.fame < 25 and char.money < 500000:
            return {"success": False, "message": "VIP Ünlüler Kulübünde bir yıldızla flört etmek için en az %25 Şöhret veya 500.000 TL servet gerekli!"}
        target_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
        pool = FIRST_NAMES_FEMALE if target_gender == "Kadın" else FIRST_NAMES_MALE
        celeb_name = f"{random.choice(pool)} {random.choice(LAST_NAMES)}"
        celeb_jobs = ["Ünlü Dizi Yıldızı", "Pop Müzik İkonu", "Milli Futbolcu / Sporcu", "Süpermodel", "Sosyal Medya Fenomeni"]
        p_spec = random.choice(PERSONALITIES)

        celeb_person = Person(
            id=f"celeb_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=celeb_name,
            relation="Sevgili",
            gender=target_gender,
            age=max(19, char.age + random.randint(-3, 3)),
            relationship_level=86,
            job=random.choice(celeb_jobs),
            personality=p_spec["id"],
            zodiac=random.choice(ZODIAC_SIGNS),
            looks=random.randint(88, 100),
            smarts=random.randint(70, 96),
            loyalty=random.randint(65, 95),
            wealth=random.randint(88, 100),
            interests=random.sample(INTERESTS_POOL, 3),
            love_language=random.choice(LOVE_LANGUAGES),
            memories=[f"VIP Ünlüler Galasında tanışıp yılın aşkına başladınız!"]
        )
        char.relationships.append(celeb_person)
        char.dating_partner_id = celeb_person.id
        char.fame = min(100, char.fame + 15)
        char.happiness = min(100, char.happiness + 25)
        if "first_love" not in char.achievements:
            char.achievements.append("first_love")
        msg = f"🌟💘 YILIN MAGAZİN AŞKI! {celeb_person.job} {celeb_name} (Görünüş: %{celeb_person.looks}, Servet: %{celeb_person.wealth}) ile VIP Galada tanışıp sevgili oldunuz!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🌟"))
        return {"success": True, "message": msg}

    return {"success": False, "message": "Geçersiz şöhret işlemi."}

# ----------------- PAKET 3: SİYASET & DEVLET YÖNETİMİ SİSTEMİ -----------------

def run_for_political_office(char: Character, office_id: str) -> Dict[str, Any]:
    """Muhtarlık, Belediye Başkanlığı, Milletvekilliği veya Cumhurbaşkanlığı seçimine katılma."""
    office = next((o for o in POLITICAL_OFFICES if o["id"] == office_id), None)
    if not office:
        return {"success": False, "message": "Seçim makamı bulunamadı."}
    if char.is_in_prison:
        return {"success": False, "message": "Cezaevindeyken aday olamazsın."}
    if char.age < office["min_age"]:
        return {"success": False, "message": f"{office['title']} adaylığı için en az {office['min_age']} yaşında olmalısın."}
    if office["req_edu"] == "Üniversite" and char.education_level != "Üniversite":
        return {"success": False, "message": f"{office['title']} için Üniversite mezunu olmalısın!"}
    if char.money < office["campaign_cost"]:
        return {"success": False, "message": f"Seçim kampanyası bütçesi için {office['campaign_cost']:,} TL gerekli."}

    char.money -= office["campaign_cost"]
    win_chance = 0.35 + (char.smarts / 300.0) + (char.skills.get("charisma", 20) / 250.0) + (char.fame / 300.0) + (char.karma / 400.0)
    if office_id == "muhtar":
        win_chance += 0.25

    if random.random() < win_chance:
        char.political_office = office["title"]
        char.political_salary = office["salary"]
        char.approval_rating = random.randint(58, 78)
        char.fame = min(100, char.fame + 20)
        char.happiness = min(100, char.happiness + 30)
        if "politician" not in char.achievements:
            char.achievements.append("politician")
        msg = f"🗳️🏛️ SEÇİM ZAFERİ! Sandıklar açıldı ve halkın büyük desteğiyle '{office['title']}' seçildin! (Yıllık Makam Maaşı: {office['salary']:,} TL, Halk Desteği: %{char.approval_rating})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🏛️"))
        return {"success": True, "won": True, "message": msg}
    else:
        char.fame = min(100, char.fame + 6)
        msg = f"🗳️ Seçim yarışı çok çekişmeli geçti ancak az farkla '{office['title']}' seçimini kaybettin. (Kampanya sayesinde bilinirliğin arttı!)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🗳️"))
        return {"success": False, "won": False, "message": msg}

def do_political_action(char: Character, sub_action: str) -> Dict[str, Any]:
    """Seçilmiş siyasetçi için miting, altyapı hizmeti, TV tartışması ve lobi faaliyetleri."""
    if not char.political_office:
        return {"success": False, "message": "Bu eylemi yapmak için önce bir siyasi makama (Muhtar, Belediye Başkanı, Vekil veya Cumhurbaşkanı) seçilmelisin!"}

    if sub_action == "hold_rally":
        cost = 25000
        if char.money < cost:
            return {"success": False, "message": f"Büyük meydan mitingi organizasyonu için {cost:,} TL gerekli."}
        char.money -= cost
        char.approval_rating = min(100, char.approval_rating + 15)
        char.fame = min(100, char.fame + 10)
        char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + 6)
        msg = f"📢🇹🇷 MEYDANLAR DOLDU TAŞTI! Coşkulu konuşmanla halkı selamladın! (Halk Desteği: %{char.approval_rating}, Karizma +6)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="📢"))
        return {"success": True, "message": msg}

    elif sub_action == "public_project":
        char.approval_rating = min(100, char.approval_rating + 18)
        char.karma = min(100, char.karma + 15)
        char.happiness = min(100, char.happiness + 14)
        msg = f"🏗️🌳 Yeni parklar, burslar ve altyapı projelerini hizmete açtın! Halk sana dua ediyor. (Halk Desteği: %{char.approval_rating}, Karma +15)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🏗️"))
        return {"success": True, "message": msg}

    elif sub_action == "tv_debate":
        if char.smarts + char.skills.get("charisma", 20) >= 95:
            char.approval_rating = min(100, char.approval_rating + 20)
            char.fame = min(100, char.fame + 12)
            return {"success": True, "message": f"📺⚖️ Canlı yayın açık oturumunda belgelerle ve hitabetinle rakiplerini mat ettin! (Halk Desteği: %{char.approval_rating})"}
        else:
            char.approval_rating = min(100, char.approval_rating + 8)
            return {"success": True, "message": f"📺 Canlı yayında projelerini anlattın ve seçmenin sorularını yanıtladın. (Halk Desteği: %{char.approval_rating})"}

    elif sub_action == "corrupt_lobby":
        char.karma = max(0, char.karma - 25)
        if random.random() < 0.68:
            kickback = random.randint(600000, 3500000)
            char.money += kickback
            char.approval_rating = max(10, char.approval_rating - 8)
            return {"success": True, "message": f"💼🤫 Gizli imar ve lobi anlaşmasından İsviçre hesabına +{kickback:,} TL komisyon aktarıldı!"}
        else:
            char.approval_rating = 10
            old_office = char.political_office
            char.political_office = None
            char.political_salary = 0
            msg = f"🚨📰 SKANDAL PATLADI! Gazeteciler gizli ihale belgelerini yayınladı! '{old_office}' görevinden istifa etmek zorunda kaldın!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="crime", icon="🚨"))
            return {"success": False, "message": msg}

    return {"success": False, "message": "Geçersiz siyasi eylem."}

# ----------------- PAKET 4: EV TADİLATI, KİRACI YÖNETİMİ, MODİFİYE & MÜZAYEDE -----------------

def manage_asset_extra(char: Character, asset_id: str, sub_action: str) -> Dict[str, Any]:
    """Ev dekorasyonu/tadilat, kiracı yönetimi ve araç modifiye sistemi."""
    asset = next((a for a in char.assets if a.id == asset_id), None)
    if not asset:
        return {"success": False, "message": "Mülk veya araç bulunamadı."}

    if sub_action == "renovate_house":
        if asset.asset_type != "Ev":
            return {"success": False, "message": "Sadece gayrimenkullere tadilat yapılabilir."}
        if asset.upgrade_level >= 3:
            return {"success": False, "message": f"'{asset.name}' zaten maksimum (Ultra Lüks VIP) dekorasyon seviyesinde!"}
        cost = int(asset.current_value * 0.15)
        if char.money < cost:
            return {"success": False, "message": f"Lüks iç mimari tadilat için {cost:,} TL gerekli."}
        char.money -= cost
        asset.upgrade_level += 1
        asset.current_value = int(asset.current_value * 1.28)
        asset.annual_income = int(asset.annual_income * 1.35)
        char.happiness = min(100, char.happiness + 15)
        msg = f"🛠️🏠 '{asset.name}' baştan aşağı lüks malzemelerle yenilendi! (Seviye {asset.upgrade_level}/3 — Yeni Değer: {asset.current_value:,} TL, Yıllık Kira: {asset.annual_income:,} TL)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🏠"))
        return {"success": True, "message": msg}

    elif sub_action == "find_tenant":
        if asset.asset_type != "Ev":
            return {"success": False, "message": "Sadece konutlara kiracı alınabilir."}
        t_name = f"{random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}"
        asset.tenant_name = t_name
        asset.is_rented_out = True
        asset.annual_income = int(max(asset.annual_income, asset.current_value * 0.09) * 1.15)
        return {"success": True, "message": f"🔑 '{asset.name}' için referanslı, düzenli ödeme yapan yeni kiracı ({t_name}) bulundu! (Yıllık Kira: {asset.annual_income:,} TL)"}

    elif sub_action == "raise_rent":
        if asset.asset_type != "Ev":
            return {"success": False, "message": "Sadece konutlarda kira zammı yapılabilir."}
        if not asset.tenant_name:
            asset.tenant_name = f"{random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}"
        if random.random() < 0.78:
            asset.annual_income = int(asset.annual_income * 1.25)
            return {"success": True, "message": f"📈 Kiracın {asset.tenant_name} %25 kira zammını kabul etti! Yeni yıllık kira geliri: {asset.annual_income:,} TL."}
        else:
            old_t = asset.tenant_name
            asset.tenant_name = f"{random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}"
            asset.annual_income = int(asset.annual_income * 1.15)
            return {"success": True, "message": f"📦 Eski kiracı ({old_t}) zammı yüksek bulup taşındı; yerine %15 zamlı fiyattan yeni kiracı ({asset.tenant_name}) girdi! (Kira: {asset.annual_income:,} TL)"}

    elif sub_action == "tune_car":
        if asset.asset_type != "Araba":
            return {"success": False, "message": "Sadece araçlar modifiye edilebilir."}
        if asset.upgrade_level >= 3:
            return {"success": False, "message": f"'{asset.name}' zaten Stage-3 Tam Performans modifiyeli!"}
        cost = int(asset.current_value * 0.15)
        if char.money < cost:
            return {"success": False, "message": f"Stage-3 Motor, Egzoz ve Bodykit modifiyesi için {cost:,} TL gerekli."}
        char.money -= cost
        asset.upgrade_level += 1
        asset.current_value = int(asset.current_value * 1.25)
        char.looks = min(100, char.looks + 5)
        char.happiness = min(100, char.happiness + 16)
        msg = f"🏎️🔥 '{asset.name}' aracına Stage-{asset.upgrade_level} performans paketi, seramik kaplama ve özel jant uygulandı! (Yeni Değer: {asset.current_value:,} TL)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🏎️"))
        return {"success": True, "message": msg}

    return {"success": False, "message": "Geçersiz mülk/araç işlemi."}

def buy_auction_item(char: Character, item_id: str) -> Dict[str, Any]:
    """Sanat, Antika ve Lüks Koleksiyon Müzayedesinden nadir eser satın alma."""
    item = next((a for a in AUCTION_ITEMS if a["id"] == item_id), None)
    if not item:
        return {"success": False, "message": "Müzayede eseri bulunamadı."}
    if char.money < item["price"]:
        return {"success": False, "message": f"'{item['name']}' için müzayedede {item['price']:,} TL nakit gerekli."}

    char.money -= item["price"]
    new_asset = Asset(
        id=f"art_{len(char.assets)+1}_{random.randint(10,99)}",
        name=item["name"],
        asset_type="Koleksiyon",
        purchase_price=item["price"],
        current_value=item["price"],
        annual_cost=0,
        annual_income=0
    )
    char.assets.append(new_asset)
    char.fame = min(100, char.fame + 10)
    char.happiness = min(100, char.happiness + 20)
    if "collector" not in char.achievements:
        char.achievements.append("collector")
    msg = f"🖼️🔨 SATILDI! Müzayedede en yüksek teklifi vererek '{item['name']}' eserini koleksiyonuna kattın! (Her yıl yüksek değer kazanır, Şöhret +10)"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🖼️"))
    return {"success": True, "message": msg}

# ----------------- PAKET 2 (YENİ): INSTASTORY, ALEV (🔥) & STALK SİSTEMİ -----------------

def do_insta_story(char: Character, story_type: str) -> Dict[str, Any]:
    """InstaStory paylaşımı: Alev (🔥) yanıtları, gizli hayranlar, eski sevgili dönüşü ve kıskançlık."""
    if char.age < 15:
        return {"success": False, "message": "Story paylaşmak için en az 15 yaşında olmalısın."}

    if "Instagram" not in char.social_media:
        char.social_media["Instagram"] = SocialMediaAccount(platform="Instagram", followers=250)
    char.social_media["Instagram"].followers += random.randint(120, 950)

    if story_type == "gym_mirror":
        char.looks = min(100, char.looks + 3)
        char.happiness = min(100, char.happiness + 10)
        # Yeni bir gizli hayran story'e 🔥 atar!
        meet_res = meet_someone_at_place(char, "fitness_club")
        new_admirer_name = "Gizli Hayran"
        if meet_res.get("success") and meet_res.get("person_id"):
            p_obj = next((p for p in char.relationships if p.id == meet_res["person_id"]), None)
            if p_obj:
                new_admirer_name = p_obj.name
                p_obj.chat_history.append({"sender": "them", "text": "🔥🔥 Story'n yıkılıyor! Kahve içelim mi?"})

        # Mevcut kıskanç partner tepkisi
        partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive and p.id != meet_res.get("person_id")), None)
        jealous_note = ""
        if partner and partner.personality in ["Kıskanç & Tutkulu"] and random.random() < 0.50:
            partner.relationship_level = max(15, partner.relationship_level - 8)
            partner.chat_history.append({"sender": "them", "text": "O attığın story ne öyle?! Kimler alev attı çabuk ekran görüntüsü at! 😤🔥"})
            jealous_note = f" (Ancak kıskanç partnerin {partner.name} story'ni görüp hesap sordu!)"

        msg = f"📸🔥 Spor & Ayna Story'n büyük ilgi gördü! {new_admirer_name} hikayene '🔥🔥' yanıtı gönderip DM kutuna düştü! (Görünüş +3){jealous_note}"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🔥"))
        return {"success": True, "message": msg}

    elif story_type == "night_out":
        char.happiness = min(100, char.happiness + 12)
        ex_partner = next((p for p in char.relationships if p.relation in ["Eski Sevgili", "Eski Eş"] and p.is_alive and not p.is_blocked), None)
        if ex_partner and random.random() < 0.70:
            ex_partner.relationship_level = min(100, ex_partner.relationship_level + 18)
            ex_partner.chat_history.append({"sender": "them", "text": "Story'de gördüm, bizim gittiğimiz mekandasın... Seni hâlâ unutamadım 😔❤️"})
            msg = f"🍸🌙 Gece gezmesi story'ni gören eski sevgilin {ex_partner.name} dayanamayıp DM attı: 'Seni hâlâ unutamadım...' (İstersen profilinden barışabilirsin!)"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🍸"))
            return {"success": True, "message": msg}
        else:
            meet_someone_at_place(char, "night_club")
            msg = "🍸✨ Gece kulübünden attığın story'ye yeni bir flört adayı '🔥' yanıtı bıraktı ve İlişkiler listene eklendi!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🍸"))
            return {"success": True, "message": msg}

    elif story_type == "couple_story":
        partner = next((p for p in char.relationships if p.relation in ["Flört", "Sevgili", "Nişanlı", "Eş"] and p.is_alive), None)
        if not partner:
            return {"success": False, "message": "Çift story'si paylaşmak için aktif bir flörtün, sevgilin veya eşin olmalı."}
        partner.relationship_level = min(100, partner.relationship_level + 18)
        partner.loyalty = min(100, partner.loyalty + 10)
        char.happiness = min(100, char.happiness + 14)
        partner.memories.append("Sosyal medyada baş başa romantik fotoğrafınızı paylaştın.")
        partner.chat_history.append({"sender": "them", "text": "Bizi paylaştığın story çok tatlı olmuş aşkım, herkese ilan ettik! 🥰❤️"})
        msg = f"💑💖 {partner.name} ile romantik bir çift story'si paylaştın! Nazardan korunmak için 🧿 koydunuz. (İlişki +18, Sadakat +10)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🧿"))
        return {"success": True, "message": msg}

    return {"success": False, "message": "Geçersiz story türü."}

# ----------------- PAKET 3 (YENİ): DETAYLI ASKERLİK, BEDELLİ & KIŞLA SİSTEMİ -----------------

def do_military_service(char: Character, service_type: str) -> Dict[str, Any]:
    """Bedelli Askerlik, 6 Ay Erbaş Kışla Görevi veya 12 Ay Yedek Subay (Asteğmen)."""
    if char.age < 18:
        return {"success": False, "message": "Askerlik şubesine başvurmak için en az 18 yaşında olmalısın."}
    if "Terhis" in char.military_status:
        return {"success": False, "message": f"Askerlik görevini zaten tamamladın ({char.military_status})!"}

    if service_type == "bedelli":
        cost = 180000
        if char.money < cost:
            return {"success": False, "message": f"Bedelli askerlik ücreti için {cost:,} TL gerekli."}
        char.money -= cost
        char.military_status = "Terhis (Bedelli)"
        char.happiness = min(100, char.happiness + 15)
        if "military_vet" not in char.achievements:
            char.achievements.append("military_vet")
        msg = f"🪖💳 Bedelli askerlik ücretini ({cost:,} TL) yatırıp 28 günlük temel kışla eğitimini tamamladın ve tezkereni aldın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🪖"))
        return {"success": True, "message": msg}

    elif service_type == "erbas":
        char.military_status = "Terhis (Çavuş)"
        char.health = min(100, char.health + 12)
        char.skills["athletics"] = min(100, char.skills.get("athletics", 15) + 15)
        char.skills["martial_arts"] = min(100, char.skills.get("martial_arts", 5) + 12)
        if "military_vet" not in char.achievements:
            char.achievements.append("military_vet")

        # Kışladan ömürlük asker arkadaşı (Tertip) kazan!
        tertip_name = f"{random.choice(FIRST_NAMES_MALE)} {random.choice(LAST_NAMES)}"
        tertip = Person(
            id=f"tertip_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=tertip_name,
            relation="Arkadaş",
            gender="Erkek",
            age=char.age,
            relationship_level=95,
            job="Asker Arkadaşı (Tertip)",
            personality="Sadık & Aileci",
            zodiac=random.choice(ZODIAC_SIGNS),
            loyalty=98,
            interests=random.sample(INTERESTS_POOL, 2),
            memories=["Askerde aynı koğuşta şafak sayıp nöbet tuttunuz."]
        )
        char.relationships.append(tertip)
        msg = f"🪖🇹🇷 ŞAFAK DOĞAN GÜNEŞ! 6 aylık kışla görevini Çavuş olarak tamamlayıp terhis oldun! Koğuş arkadaşı {tertip_name} ile ömürlük dost oldun! (Sağlık +12, Atletizm +15)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🪖"))
        return {"success": True, "message": msg}

    elif service_type == "yedek_subay":
        if char.education_level != "Üniversite":
            return {"success": False, "message": "Yedek Subay (Asteğmen) olmak için Üniversite mezunu olmalısın!"}
        pay = 380000
        char.money += pay
        char.military_status = "Terhis (Asteğmen)"
        char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + 15)
        char.karma = min(100, char.karma + 15)
        if "military_vet" not in char.achievements:
            char.achievements.append("military_vet")
        msg = f"⭐🪖 Yedek Subay (Asteğmen) olarak vatan görevini üstün başarıyla tamamladın! Görev süresince +{pay:,} TL subay maaşı aldın! (Hitabet +15)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="⭐"))
        return {"success": True, "message": msg}

    return {"success": False, "message": "Geçersiz askerlik seçeneği."}

# ----------------- PAKET 4 (YENİ): YKS / KPSS SINAVI & KYK YURDU / ÖĞRENCİ EVİ -----------------

def take_national_exam(char: Character, exam_type: str, ans1: int = 0, ans2: int = 1) -> Dict[str, Any]:
    """İnteraktif YKS (Burs & Üniversite) ve KPSS (Devlet Memurluğu / Kaymakamlık Ataması) Sınavı."""
    if char.age < 17:
        return {"success": False, "message": "Ulusal sınavlara (YKS / KPSS) girmek için en az 17 yaşında olmalısın."}

    questions = EXAM_QUESTIONS.get(exam_type, [])
    correct_count = 0
    if len(questions) >= 2:
        if int(ans1) == questions[0]["correct"]:
            correct_count += 1
        if int(ans2) == questions[1]["correct"]:
            correct_count += 1

    if exam_type == "yks":
        score = min(500, 260 + int(char.smarts * 1.4) + (correct_count * 55))
        char.yks_score = score
        char.smarts = min(100, char.smarts + 10)
        if score >= 410:
            char.scholarship_annual = 45000
            char.happiness = min(100, char.happiness + 25)
            msg = f"🎓🏆 YKS TÜRKİYE DERECESİ! Sınavdan {score} puan aldın ({correct_count}/2 Doğru)! Yıllık 45.000 TL Başarı & KYK Bursu kazandın! (Zeka +10)"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="school", icon="🎓"))
            return {"success": True, "score": score, "message": msg}
        else:
            msg = f"📝 YKS Sınavı tamamlandı! Puanın: {score} ({correct_count}/2 Doğru). Artık istediğin üniversite bölümüne başvurabilirsin!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="school", icon="📝"))
            return {"success": True, "score": score, "message": msg}

    elif exam_type == "kpss":
        score = min(100, 52 + int(char.smarts * 0.28) + (correct_count * 12))
        char.kpss_score = score
        if score >= 80:
            gov_title = "🏛️ Devlet Başmüfettişi / Kaymakam" if char.education_level == "Üniversite" else "📋 Kadrolu Devlet Memuru"
            gov_sal = 980000 if char.education_level == "Üniversite" else 640000
            char.current_job = Job(
                id="gov_appointed",
                title=gov_title,
                category="Kamu",
                salary=gov_sal,
                required_education=char.education_level,
                required_smarts=60,
                performance=90
            )
            char.happiness = min(100, char.happiness + 28)
            if "civil_servant" not in char.achievements:
                char.achievements.append("civil_servant")
            msg = f"🎉📋 KPSS ATAMA MÜJDESİ! KPSS'den {score} puan alarak '{gov_title}' kadrosuna (Maaş: {gov_sal:,} TL/yıl) resmen atandın!"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="📋"))
            return {"success": True, "score": score, "message": msg}
        else:
            return {"success": False, "score": score, "message": f"📝 KPSS Puanın: {score}. Kadrolu atama taban puanı (80) altında kaldın, sorulara dikkat edip tekrar deneyebilirsin!"}

    return {"success": False, "message": "Geçersiz sınav türü."}

def change_student_housing(char: Character, housing_mode: str) -> Dict[str, Any]:
    """KYK Yurdu veya Arkadaşlarla Öğrenci Evi yaşam seçimi."""
    if char.age < 17:
        return {"success": False, "message": "Yurt veya öğrenci evine çıkmak için en az 17 yaşında olmalısın."}

    if housing_mode == "kyk_dorm":
        char.housing_type = "🛏️ KYK Öğrenci Yurdu"
        char.happiness = min(100, char.happiness + 10)
        # Oda arkadaşı ekle
        rm_gender = char.gender
        pool = FIRST_NAMES_MALE if rm_gender == "Erkek" else FIRST_NAMES_FEMALE
        rm_name = f"{random.choice(pool)} {random.choice(LAST_NAMES)}"
        roommate = Person(
            id=f"roommate_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=rm_name,
            relation="Arkadaş",
            gender=rm_gender,
            age=char.age,
            relationship_level=85,
            job="Yurt Oda Arkadaşı",
            personality=random.choice([p["id"] for p in PERSONALITIES]),
            zodiac=random.choice(ZODIAC_SIGNS),
            interests=random.sample(INTERESTS_POOL, 2),
            memories=["KYK yurdunda ranzada sabaha kadar sınavlara çalıştınız."]
        )
        char.relationships.append(roommate)
        msg = f"🛏️ KYK Öğrenci Yurduna yerleştin! Yıllık yaşam masrafların düştü ve oda arkadaşın {rm_name} ile sıkı dost oldun!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="school", icon="🛏️"))
        return {"success": True, "message": msg}

    elif housing_mode == "student_house":
        cost = 15000
        if char.money < cost:
            return {"success": False, "message": f"Öğrenci evi depozito ve ikinci el eşya masrafı için {cost:,} TL gerekli."}
        char.money -= cost
        char.housing_type = "🍜 Öğrenci Evi"
        char.happiness = min(100, char.happiness + 20)
        char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + 8)
        rm_gender = random.choice(["Erkek", "Kadın"])
        pool = FIRST_NAMES_MALE if rm_gender == "Erkek" else FIRST_NAMES_FEMALE
        rm_name = f"{random.choice(pool)} {random.choice(LAST_NAMES)}"
        housemate = Person(
            id=f"housemate_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=rm_name,
            relation="Arkadaş",
            gender=rm_gender,
            age=char.age,
            relationship_level=88,
            job="Ev Arkadaşı",
            personality=random.choice([p["id"] for p in PERSONALITIES]),
            zodiac=random.choice(ZODIAC_SIGNS),
            interests=random.sample(INTERESTS_POOL, 2),
            memories=["Öğrenci evinde makarna yapıp vize/final haftalarını beraber atlattınız."]
        )
        char.relationships.append(housemate)
        msg = f"🍜🏠 Arkadaşın {rm_name} ile Öğrenci Evine çıktınız! Özgürlük, gitar geceleri ve dostluk! (Mutluluk +20, Karizma +8)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="school", icon="🍜"))
        return {"success": True, "message": msg}

    return {"success": False, "message": "Geçersiz barınma seçimi."}

# ----------------- PAKET 10 (YENİ): GARDIROP, TARZ & KOMBİN SİSTEMİ -----------------

def change_outfit_style(char: Character, style_id: str) -> Dict[str, Any]:
    """Karakterin giyim kuşam ve kombin tarzını değiştirir, görünüş ve karizmayı artırır."""
    style = next((s for s in OUTFIT_STYLES if s["id"] == style_id), None)
    if not style:
        return {"success": False, "message": "Kombin tarzı bulunamadı."}
    if char.money < style["cost"]:
        return {"success": False, "message": f"'{style['name']}' kombini için {style['cost']:,} TL gerekli."}

    char.money -= style["cost"]
    char.outfit_style = style["name"]
    char.looks = min(100, char.looks + style["looks_boost"])
    char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + style["charisma_boost"])
    char.happiness = min(100, char.happiness + 12)
    if style["cost"] >= 35000 and "fashion_icon" not in char.achievements:
        char.achievements.append("fashion_icon")

    msg = f"👔✨ Yeni Tarzın: '{style['name']}'! Aynadaki görüntüne hayran kaldın! (Görünüş +{style['looks_boost']}, Hitabet +{style['charisma_boost']})"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="👔"))
    return {"success": True, "message": msg}

# ----------------- PAKET 11 (YENİ): EVLİLİK TV ŞOVU, OFİS AŞKI & ENTRİKA -----------------

def do_drama_intrigue_action(char: Character, sub_action: str) -> Dict[str, Any]:
    """Kısmet Evi TV Evlilik Programı ve Plazalarda Ofis/Patron Aşkı."""
    if char.age < 18:
        return {"success": False, "message": "Bu etkinlik için en az 18 yaşında olmalısın."}

    if sub_action == "tv_dating_show":
        prize = random.randint(180000, 450000)
        char.money += prize
        char.fame = min(100, char.fame + 24)
        char.happiness = min(100, char.happiness + 25)
        if "tv_star_love" not in char.achievements:
            char.achievements.append("tv_star_love")

        target_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
        pool = FIRST_NAMES_FEMALE if target_gender == "Kadın" else FIRST_NAMES_MALE
        star_name = f"{random.choice(pool)} {random.choice(LAST_NAMES)}"
        p_spec = random.choice(PERSONALITIES)

        tv_partner = Person(
            id=f"tvlove_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=star_name,
            relation="Sevgili",
            gender=target_gender,
            age=max(19, char.age + random.randint(-2, 2)),
            relationship_level=92,
            job="TV Yıldızı & Model",
            personality=p_spec["id"],
            zodiac=random.choice(ZODIAC_SIGNS),
            looks=random.randint(85, 100),
            smarts=random.randint(65, 95),
            loyalty=random.randint(70, 95),
            wealth=random.randint(75, 98),
            interests=random.sample(INTERESTS_POOL, 3),
            love_language=random.choice(LOVE_LANGUAGES),
            memories=["'Kısmet Evi' TV yarışmasında halk oylamasıyla şampiyon olup aşkınızı ilan ettiniz!"]
        )
        char.relationships.append(tv_partner)
        char.dating_partner_id = tv_partner.id
        msg = f"📺💘 KISMET EVİ ŞAMPİYONU! Katıldığın izdivaç/flört TV programında hem {star_name} ile büyük aşkı buldun hem de halk oylamasıyla +{prize:,} TL büyük ödülü kazandın! (Şöhret +24)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="📺"))
        return {"success": True, "message": msg}

    elif sub_action == "office_romance":
        if not char.current_job:
            return {"success": False, "message": "Ofis aşkı yaşamak için önce tam zamanlı bir işte çalışıyor olmalısın!"}
        target_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
        pool = FIRST_NAMES_FEMALE if target_gender == "Kadın" else FIRST_NAMES_MALE
        boss_name = f"{random.choice(pool)} {random.choice(LAST_NAMES)}"

        if random.random() < 0.78:
            char.current_job.salary = int(char.current_job.salary * 1.28)
            char.current_job.level += 1
            office_lover = Person(
                id=f"office_{len(char.relationships)+1}_{random.randint(10,99)}",
                name=boss_name,
                relation="Sevgili",
                gender=target_gender,
                age=max(22, char.age + random.randint(-2, 5)),
                relationship_level=88,
                job=f"Üst Düzey Yönetici ({char.current_job.category})",
                personality="Hırslı & Kariyerist",
                zodiac=random.choice(ZODIAC_SIGNS),
                looks=random.randint(78, 98),
                smarts=random.randint(80, 98),
                wealth=random.randint(82, 98),
                interests=random.sample(INTERESTS_POOL, 2),
                love_language="Kaliteli Zaman",
                memories=["Şirket toplantısı sonrası kahve içerken başlayan tutkulu ofis aşkınız!"]
            )
            char.relationships.append(office_lover)
            char.dating_partner_id = office_lover.id
            msg = f"💼❤️‍🔥 PLAZA & OFİS AŞKI! Şirketteki üst düzey yönetici {boss_name} ile aranızda tutkulu bir aşk başladı! Sana özel %28 zam ve terfi onayladı! (Yeni Maaş: {char.current_job.salary:,} TL)"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💼"))
            return {"success": True, "message": msg}
        else:
            char.current_job.performance = max(20, char.current_job.performance - 15)
            return {"success": False, "message": "😬 İş yerinde flört girişimin İK (İnsan Kaynakları) dedikodularına takıldı! Performans puanın biraz düştü."}

    return {"success": False, "message": "Geçersiz entrika eylemi."}

# ----------------- PAKET 14 (YENİ): ROCK GRUBU / RAP KOLEKTİFİ & STADYUM TURNESİ -----------------

def create_music_band(char: Character, band_name: str, genre_id: str) -> Dict[str, Any]:
    """Kendi müzik grubunu veya rap kolektifini kurma."""
    if char.age < 15:
        return {"success": False, "message": "Müzik grubu kurmak için en az 15 yaşında olmalısın."}
    genre = next((g for g in BAND_GENRES if g["id"] == genre_id), BAND_GENRES[0])
    if char.money < genre["cost"]:
        return {"success": False, "message": f"Stüdyo ekipmanları ve grup kurulumu için {genre['cost']:,} TL gerekli."}

    char.money -= genre["cost"]
    clean_name = band_name.strip() if band_name and band_name.strip() else f"Grup {char.last_name} & Dostlar"
    char.band = MusicBand(
        name=clean_name,
        genre=genre["name"],
        albums_count=0,
        chemistry=85,
        fans=2500,
        annual_royalties=45000
    )
    char.skills["music"] = min(100, char.skills.get("music", 10) + 12)
    char.happiness = min(100, char.happiness + 20)
    msg = f"🎸🎤 '{clean_name}' ({genre['name']}) resmen kuruldu! Garajda ilk provalara başladınız!"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🎸"))
    return {"success": True, "message": msg}

def do_band_action(char: Character, sub_action: str) -> Dict[str, Any]:
    """Müzik grubuyla prova, albüm çıkarma, stadyum turnesi ve grup içi ego yönetimi."""
    if not char.band:
        return {"success": False, "message": "Önce bir müzik grubu veya rap kolektifi kurmalısın!"}

    b = char.band
    if sub_action == "rehearse":
        b.chemistry = min(100, b.chemistry + 15)
        char.skills["music"] = min(100, char.skills.get("music", 10) + 10)
        return {"success": True, "message": f"🎶 '{b.name}' ile 8 saatlik stüdyo provası yaptınız! (Grup Uyumu: %{b.chemistry}, Müzik: %{char.skills['music']})"}

    elif sub_action == "record_album":
        b.albums_count += 1
        earned = random.randint(250000, 950000) + (b.chemistry * 3000)
        new_fans = random.randint(25000, 90000)
        b.fans += new_fans
        b.annual_royalties += 180000
        char.money += earned
        char.fame = min(100, char.fame + 16)
        msg = f"💿🔥 '{b.name}' {b.albums_count}. stüdyo albümünü yayınladı! Spotify ve listelerde 1 numaraya yerleşti! (+{earned:,} TL Telif, +{new_fans:,} Hayran)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="💿"))
        return {"success": True, "message": msg}

    elif sub_action == "stadium_tour":
        tour_income = random.randint(650000, 2400000) + int(b.fans * 4)
        char.money += tour_income
        b.fans += 65000
        char.fame = min(100, char.fame + 20)
        char.happiness = min(100, char.happiness + 25)
        if "rockstar" not in char.achievements:
            char.achievements.append("rockstar")
        msg = f"🏟️🎸 DEV STADYUM TURNESİ! '{b.name}' ile 50.000 kişilik kapalı gişe stadyum konseri verdiniz! Bilet ve sponsorluktan +{tour_income:,} TL kazandın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🏟️"))
        return {"success": True, "message": msg}

    elif sub_action == "resolve_drama":
        b.chemistry = 100
        char.karma = min(100, char.karma + 8)
        return {"success": True, "message": f"🤝 Grup üyeleriyle akşam yemeğinde tüm ego tartışmalarını çözdün! '{b.name}' uyumu %100!"}

    return {"success": False, "message": "Geçersiz grup eylemi."}

# ----------------- PAKET 15 (YENİ): BANKA KREDİSİ (MORTGAGE) & İSVİÇRE OFFSHORE HESABI -----------------

def do_bank_offshore_action(char: Character, sub_action: str, amount: int = 250000) -> Dict[str, Any]:
    """Banka kredisi çekme, borç kapatma ve İsviçre gizli Offshore hesabına para aktarma/çekme."""
    if char.age < 18:
        return {"success": False, "message": "Bankacılık ve Offshore işlemleri için en az 18 yaşında olmalısın."}

    if sub_action == "take_loan":
        if char.debt >= 10000000:
            return {"success": False, "message": "Banka kredi limitin doldu! Önce mevcut kredi borcunun bir kısmını kapatmalısın."}
        char.money += amount
        repay_total = int(amount * 1.15)
        char.debt += repay_total
        msg = f"🏦💳 Bankadan +{amount:,} TL kredi çektin ve anında hesabına geçti! (Faiziyle toplam geri ödeme borcu: {char.debt:,} TL)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🏦"))
        return {"success": True, "message": msg}

    elif sub_action == "pay_debt":
        if char.debt <= 0:
            return {"success": False, "message": "Bankaya herhangi bir kredi borcun bulunmuyor!"}
        if char.money <= 0:
            return {"success": False, "message": "Borç ödemek için nakit paran yok."}
        pay = min(char.money, char.debt, amount if amount > 0 else char.debt)
        char.money -= pay
        char.debt -= pay
        return {"success": True, "message": f"🏦✅ Bankaya {pay:,} TL kredi borcu ödedin! Kalan borç: {char.debt:,} TL."}

    elif sub_action == "deposit_offshore":
        if char.money < amount or amount <= 0:
            return {"success": False, "message": f"Offshore hesabına aktarmak için en az {amount:,} TL nakit paran olmalı."}
        char.money -= amount
        char.offshore_balance += amount
        msg = f"🇨🇭🔒 İsviçre Gizli Offshore Hesabına {amount:,} TL aktardın! (Boşanma nafakasından ve hacizden %100 muaf, yıllık %8 döviz getirili • Toplam Offshore: {char.offshore_balance:,} TL)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🇨🇭"))
        return {"success": True, "message": msg}

    elif sub_action == "withdraw_offshore":
        if char.offshore_balance <= 0:
            return {"success": False, "message": "Offshore hesabında bakiye bulunmuyor."}
        w_amt = char.offshore_balance if amount <= 0 else min(char.offshore_balance, amount)
        char.offshore_balance -= w_amt
        char.money += w_amt
        return {"success": True, "message": f"🇨🇭💸 İsviçre Offshore hesabından {w_amt:,} TL'yi Türkiye'deki nakit hesabına geri çektin!"}

    return {"success": False, "message": "Geçersiz banka işlemi."}

# ----------------- PAKET 18 (YENİ): ÇİFTLER ARASI ORTAK GİRİŞİM & İNTERAKTİF BOŞANMA MAHKEMESİ -----------------

def do_couple_business(char: Character, person_id: str, biz_id: str) -> Dict[str, Any]:
    """Partnerle (Sevgili/Nişanlı/Eş) ortak kafe, moda atölyesi veya e-ticaret markası açma."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person or person.relation not in ["Sevgili", "Nişanlı", "Eş"]:
        return {"success": False, "message": "Ortak girişim kurmak için bir sevgilin, nişanlın veya eşin olmalı."}
    biz = next((b for b in COUPLE_BUSINESS_TYPES if b["id"] == biz_id), COUPLE_BUSINESS_TYPES[0])

    # Partnerin maddi durumuna göre sermayenin %30'unu o karşılar
    partner_share = int(biz["cost"] * 0.30) if person.wealth >= 45 else 0
    my_cost = biz["cost"] - partner_share
    if char.money < my_cost:
        return {"success": False, "message": f"'{biz['name']}' ortaklığı için senin payına düşen {my_cost:,} TL nakit gerekli."}

    char.money -= my_cost
    person.joint_venture_name = biz["name"]
    person.joint_venture_profit = biz["annual_profit"]
    person.relationship_level = min(100, person.relationship_level + 20)
    person.loyalty = min(100, person.loyalty + 10)
    char.happiness = min(100, char.happiness + 18)
    person.memories.append(f"Birlikte '{biz['name']}' ortak girişimini kurdunuz.")
    msg = f"🤝🏪 ÇİFT ORTAKLIĞI! {person.name} ile birlikte '{biz['name']}' açtınız! (Partnerin sermayeye {partner_share:,} TL kattı • Yıllık Ortak Gelir: +{biz['annual_profit']:,} TL/yıl)"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🏪"))
    return {"success": True, "message": msg}

def do_divorce_court(char: Character, person_id: str, lawyer_id: str = "baro") -> Dict[str, Any]:
    """İnteraktif Aile & Boşanma Mahkemesi: Avukat seçimi, deliller, tazminat ve nafaka kararı."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person or person.relation not in ["Eş", "Nişanlı", "Sevgili"]:
        return {"success": False, "message": "Boşanma / ayrılık mahkemesi için aktif bir eş veya partner seçmelisin."}

    lawyer = next((l for l in DIVORCE_LAWYERS if l["id"] == lawyer_id), DIVORCE_LAWYERS[0])
    if char.money < lawyer["cost"]:
        return {"success": False, "message": f"'{lawyer['name']}' vekalet ücreti için {lawyer['cost']:,} TL gerekli."}

    char.money -= lawyer["cost"]
    person.relation = "Eski Eş" if person.relation == "Eş" else "Eski Sevgili"
    person.cohabiting = False
    person.joint_venture_name = None
    person.joint_venture_profit = 0
    if char.spouse_id == person.id:
        char.spouse_id = None
    if char.dating_partner_id == person.id:
        char.dating_partner_id = None

    # Mahkeme kazanma puanı (Avukat + Evlilik Sözleşmesi/Dedektif Kanıtı + Hitabet/Zeka)
    court_score = lawyer["win_bonus"] + (char.smarts / 300.0) + (char.skills.get("charisma", 20) / 350.0)
    if person.has_prenup or person.loyalty < 55:
        court_score += 0.55

    if court_score >= 0.72:
        comp = random.randint(120000, 380000)
        char.money += comp
        char.alimony_annual = 0
        person.relationship_level = 10
        person.memories.append("Boşanma davasını kazandın ve ondan tazminat aldın.")
        msg = f"⚖️🏆 MAHKEME ZAFERİ! '{lawyer['name']}' savunması ve sunduğun delillerle hakimi ikna ettin! Tek kuruş nafaka ödemeden boşandın ve karşı taraftan +{comp:,} TL manevi tazminat kazandın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="⚖️"))
        return {"success": True, "message": msg}
    elif court_score >= 0.45:
        settlement = max(0, int(char.money * 0.15))
        char.money -= settlement
        char.alimony_annual = 0
        person.relationship_level = 25
        msg = f"⚖️🤝 ANLAŞMALI BOŞANMA: Mahkemede '{lawyer['name']}' aracılığıyla uzlaştınız. {settlement:,} TL protokol ödemesiyle nafakasız ayrıldınız."
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="⚖️"))
        return {"success": True, "message": msg}
    else:
        loss = max(0, int(char.money * 0.42))
        char.money -= loss
        char.alimony_annual = max(45000, int(loss * 0.15) + 45000)
        char.happiness = max(5, char.happiness - 25)
        person.relationship_level = 5
        msg = f"⚖️💸 AĞIR MAHKEME KARARI! Hakim seni kusurlu buldu! Nakit servetinin %42'sini ({loss:,} TL) tazminat ödedin ve eski eşine yıllık {char.alimony_annual:,} TL nafaka bağlandı! (Offshore hesabın korundu)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💸"))
        return {"success": True, "message": msg}

# ----------------- PAKET 19 (YENİ): PROFESYONEL FUTBOLCU / BASKETBOLCU KARİYERİ & KULÜP BAŞKANLIĞI -----------------

def do_pro_sports_action(char: Character, sub_action: str, club_id: str = "anadolu_fk") -> Dict[str, Any]:
    """Altyapı seçmeleri, Süper Lig/Avrupa transferi, Şampiyonluk maçı (Ballon d'Or) ve Kulüp Başkanlık Sistemi."""
    if char.age < 14:
        return {"success": False, "message": "Profesyonel spor kariyeri için en az 14 yaşında olmalısın."}

    ath = char.skills.get("athletics", 15)

    if sub_action == "join_academy":
        # Gerçekçi Zorluk: Kondisyon & Sağlık kontrolü
        char.skills["athletics"] = min(100, ath + 18)
        char.health = min(100, char.health + 8)
        if char.skills["athletics"] < 32 or char.health < 50:
            return {"success": False, "message": f"⚽😓 Altyapı seçmelerinde kondisyonun yetersiz kaldı (Atletizm: %{char.skills['athletics']}). Biraz daha spor yapıp tekrar dene!"}
        char.sports_career = ProSportsCareer(
            sport="Futbol",
            team_name=f"{char.city} Gençlik Akademisi",
            league_tier="Altyapı Akademisi",
            salary=240000
        )
        msg = f"⚽🏃 ALTYAPIYA SEÇİLDİN! '{char.city} Gençlik Akademisi' seçmelerinde yeteneğinle göz doldurdun ve profesyonel aday sözleşmesi imzaladın! (Yıllık: 240.000 TL, Atletizm: %{char.skills['athletics']})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="⚽"))
        return {"success": True, "message": msg}

    elif sub_action == "sign_club":
        club = next((c for c in SPORTS_CLUBS if c["id"] == club_id), SPORTS_CLUBS[0])
        if ath < club["req_ath"]:
            return {
                "success": False,
                "message": f"🏟️❌ '{club['name']}' scout ekibi transferi veto etti! Gereken Atletizm/Kondisyon: %{club['req_ath']} (Senin: %{ath}). Spor salonunda veya altyapıda kendini geliştirmelisin!"
            }
        signing_bonus = int(club["salary"] * 0.25)
        char.money += signing_bonus
        char.sports_career = ProSportsCareer(
            sport=club["sport"],
            team_name=club["name"],
            league_tier=club["tier"],
            salary=club["salary"],
            goals_or_points=char.sports_career.goals_or_points if char.sports_career else 0,
            trophies=char.sports_career.trophies if char.sports_career else 0,
            national_caps=char.sports_career.national_caps if char.sports_career else 0
        )
        char.fame = min(100, char.fame + 22)
        char.happiness = min(100, char.happiness + 25)
        msg = f"✍️🏟️ DEV TRANSFER! '{club['name']}' ({club['tier']}) ile yıllık {club['salary']:,} TL maaş + {signing_bonus:,} TL imza parasıyla sözleşme imzaladın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="⚽"))
        return {"success": True, "message": msg}

    elif sub_action == "play_season_match":
        if not char.sports_career:
            return {"success": False, "message": "Maça çıkmak için önce altyapıya veya bir spor kulübüne katılmalısın!"}
        sc = char.sports_career
        # Gerçekçi Sakatlık Riski (%15)
        if random.random() < 0.15 and char.health < 75:
            char.health = max(15, char.health - 18)
            return {"success": False, "message": f"🚑⚠️ Дерbi maçında sert bir müdahaleyle sakatlandın! Doktorlar dinlenmeni önerdi (Sağlık -18)."}

        scored = random.randint(12, 32)
        sc.goals_or_points += scored
        sc.trophies += 1
        sc.national_caps += 5
        bonus = random.randint(350000, 1800000)
        char.money += bonus
        char.fame = min(100, char.fame + 18)
        char.skills["athletics"] = min(100, ath + 8)
        if "ballon_dor" not in char.achievements:
            char.achievements.append("ballon_dor")
        msg = f"🏆⚽ ŞAMPİYONLUK & ALTIN TOP! '{sc.team_name}' formasıyla sezonda {scored} gol/sayı katkısı verdin, 90. dakikada kupayı getiren golü atıp +{bonus:,} TL şampiyonluk primi ve Milli Takım daveti kazandın!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🏆"))
        return {"success": True, "message": msg}

    elif sub_action == "buy_sports_club":
        cost = 20000000
        if char.money < cost:
            return {"success": False, "message": f"Bir Süper Lig kulübünün çoğunluk hisselerini satın alıp Kulüp Başkanı olmak için {cost:,} TL gerekli."}
        char.money -= cost
        club_name = f"{char.city} SK"
        char.sports_career = ProSportsCareer(
            sport="Futbol Kulüp Başkanlığı",
            team_name=club_name,
            league_tier="Kulüp Başkanı & Sahibi",
            salary=3200000,
            owns_club=True,
            club_valuation=cost
        )
        char.fame = min(100, char.fame + 30)
        char.happiness = 100
        msg = f"👑🏟️ KULÜP BAŞKANI OLDUN! 20.000.000 TL ödeyerek '{club_name}' kulübünü satın aldın! Artık protokol tribününde oturuyor ve yıldız transferleri yönetiyorsun (Yıllık Yayın/Gişe Geliri: +3.200.000 TL)!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="👑"))
        return {"success": True, "message": msg}

    return {"success": False, "message": "Geçersiz spor kariyeri eylemi."}

# ----------------- MEVCUT ALANLARI GELİŞTİRME & DERİNLEŞTİRME -----------------

def do_relationship_conflict(char: Character, person_id: str, conflict_id: str, choice_id: str) -> Dict[str, Any]:
    """Çiftler arası interaktif kriz yönetimi ve diyalog çözümü."""
    if not person_id:
        person = next((p for p in char.relationships if (p.relation in ["Sevgili", "Eş", "Nişanlı"] or p.id == char.dating_partner_id) and p.is_alive), None)
    else:
        person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Partner veya kişi bulunamadı."}
    conflict = next((c for c in RELATIONSHIP_CONFLICTS if c["id"] == conflict_id), RELATIONSHIP_CONFLICTS[0])
    chosen = next((opt for opt in conflict["options"] if opt["id"] == choice_id), conflict["options"][0])

    if chosen["id"] in ["compromise", "apologize_block", "tighten_belt", "warm_hug"]:
        person.relationship_level = min(100, person.relationship_level + 16)
        person.loyalty = min(100, person.loyalty + 6)
        char.happiness = min(100, char.happiness + 12)
        char.karma = min(100, char.karma + 6)
        person.memories.append(f"'{conflict['title']}' tartışmasını olgunluk ve sevgiyle tatlıya bağladınız.")
        msg = f"🕊️ KRİZ ÇÖZÜLDÜ! {person.name} uzlaşmacı ve sevgi dolu tavrına hayran kaldı, boynuna sarılıp barıştınız! (İlişki +16, Mutluluk +12)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🕊️"))
        return {"success": True, "message": msg}

    elif chosen["id"] in ["fight_back", "gaslight", "my_money", "defend_space"]:
        person.relationship_level = max(5, person.relationship_level - 22)
        char.stress = min(100, char.stress + 15)
        char.happiness = max(5, char.happiness - 16)
        person.memories.append(f"'{conflict['title']}' konusunda sertçe tartıştınız ve kırgınlık oluştu.")
        msg = f"💥 ŞİDDETLİ KAVGA! {person.name} kapıyı çarpıp odayı terk etti! Aranızda buz gibi rüzgarlar esiyor! (İlişki -22, Stres +15)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💥"))
        return {"success": True, "message": msg}

    else:
        # Hediye, kaçış veya jest
        cost = 10000 if chosen["id"] == "sweet_gift" else (8000 if chosen["id"] == "spa_treat" else 0)
        if char.money >= cost:
            char.money -= cost
        person.relationship_level = min(100, person.relationship_level + 10)
        char.happiness = min(100, char.happiness + 8)
        person.memories.append(f"'{conflict['title']}' krizinde gerginliği yumuşattın.")
        msg = f"🥂 TARTIŞMA YATIŞTI: {person.name} biraz sakinleşti ama konunun üstü şimdilik tatlıya bağlandı. (İlişki +10)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🥂"))
        return {"success": True, "message": msg}

def do_company_management_action(char: Character, action_id: str) -> Dict[str, Any]:
    """Şirket Patronu Karar Odası: Pazarlama, AR-GE, Çalışan Primi ve Yeni Şube."""
    if not char.business:
        return {"success": False, "message": "Aktif bir şirketin bulunmuyor!"}
    b = char.business
    act = next((a for a in COMPANY_EXPANSION_ACTIONS if a["id"] == action_id), None)
    if not act:
        return {"success": False, "message": "Geçersiz şirket kararı."}
    if char.money < act["cost"]:
        return {"success": False, "message": f"'{act['name']}' kararı için {act['cost']:,} TL şirket bütçesi gerekli."}

    char.money -= act["cost"]

    if action_id == "marketing":
        b.annual_profit = int(b.annual_profit * 1.35)
        b.reputation = min(100, b.reputation + 10)
        msg = f"📣🚀 VİRAL KAMPANYA PATLADI! '{b.name}' reklamları sosyal medyada viral oldu! Yıllık şirket kârın {b.annual_profit:,} TL'ye yükseldi!"
    elif action_id == "rd_patent":
        b.valuation = int(b.valuation * 1.40)
        char.smarts = min(100, char.smarts + 6)
        msg = f"💡🔬 AR-GE ZAFERİ! '{b.name}' yeni nesil tescilli ürününü duyurdu! Şirket değerlemesi {b.valuation:,} TL'ye fırladı!"
    elif action_id == "employee_bonus":
        b.reputation = 100
        char.happiness = min(100, char.happiness + 16)
        char.karma = min(100, char.karma + 10)
        msg = f"🎁🎉 ÇİFTE MAAŞ & MORAL PARTİSİ! Tüm çalışanlarına ikramiye dağıttın! Şirket itibarı ve çalışan sadakati tavan yaptı (%100)!"
    elif action_id == "open_branch":
        b.annual_profit += 220000
        b.employees += 8
        b.valuation += 450000
        msg = f"🏬✨ YENİ ŞUBE AÇILDI! '{b.name}' metropolde görkemli bir şube daha açtı! Yıllık kârına kalıcı +220.000 TL eklendi!"
    else:
        msg = "Karar uygulandı."

    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="career", icon="🏢"))
    return {"success": True, "message": msg}

def do_tenant_action(char: Character, asset_id: str, action_id: str) -> Dict[str, Any]:
    """Emlak & Kiracı Kriz Yönetimi: Noter ihtarnamesi, görüşme ve tahliye davası."""
    asset = next((a for a in char.assets if a.id == asset_id and a.asset_type == "Ev"), None)
    if not asset:
        return {"success": False, "message": "Ev bulunamadı."}

    act = next((a for a in TENANT_MANAGEMENT_ACTIONS if a["id"] == action_id), None)
    if not act:
        return {"success": False, "message": "Geçersiz kiracı işlemi."}
    if act["cost"] > 0 and char.money < act["cost"]:
        return {"success": False, "message": f"'{act['name']}' için {act['cost']:,} TL gerekli."}

    if act["cost"] > 0:
        char.money -= act["cost"]

    if action_id == "demand_letter":
        asset.tenant_issue = None
        asset.tenant_reliability = min(100, asset.tenant_reliability + 15)
        msg = f"📜⚖️ NOTER İHTARNAMESİ ÇEKİLDİ! Kiracın {asset.tenant_name} ihtarı görünce hemen gecikmiş kirasını ödedi ve kurallara uyacağını taahhüt etti!"
    elif action_id == "friendly_talk":
        asset.tenant_issue = None
        char.happiness = min(100, char.happiness + 6)
        char.karma = min(100, char.karma + 5)
        msg = f"🤝☕ TATLI DİLLE ÇÖZÜLDÜ: Kiracın {asset.tenant_name} ile çay içip dertleştin, aranızdaki pürüzler çözüldü."
    elif action_id == "eviction_lawsuit":
        old_t = asset.tenant_name or "Eski Kiracı"
        target_gender = random.choice(["Erkek", "Kadın"])
        pool = FIRST_NAMES_FEMALE if target_gender == "Kadın" else FIRST_NAMES_MALE
        new_t = f"{random.choice(pool)} {random.choice(LAST_NAMES)}"
        asset.tenant_name = new_t
        asset.tenant_reliability = 92
        asset.tenant_issue = None
        msg = f"⚖️📦 TAHLİYE BAŞARILI! Mahkeme kararıyla {old_t} tahliye edildi ve ev yüksek puanlı güvenilir yeni kiracı '{new_t}'ye kiralandı!"
    else:
        msg = "İşlem yapıldı."

    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🏠"))
    return {"success": True, "message": msg}

def do_car_care_action(char: Character, asset_id: str, action_id: str) -> Dict[str, Any]:
    """Araba Servisi, Full Kasko ve Otobanda Gece Gazlama."""
    asset = next((a for a in char.assets if a.id == asset_id and a.asset_type == "Araba"), None)
    if not asset:
        return {"success": False, "message": "Araba bulunamadı."}

    act = next((a for a in CAR_CARE_ACTIONS if a["id"] == action_id), None)
    if not act:
        return {"success": False, "message": "Geçersiz araç işlemi."}
    if char.money < act["cost"]:
        return {"success": False, "message": f"'{act['name']}' için {act['cost']:,} TL gerekli."}

    char.money -= act["cost"]

    if action_id == "maintenance":
        asset.condition = 100
        asset.annual_cost = max(10000, int(asset.annual_cost * 0.82))
        char.happiness = min(100, char.happiness + 8)
        msg = f"🔧✨ SANAYİ & YETKİLİ SERVİS BAKIMI YAPILDI! '{asset.name}' aracının yağı, filtreleri ve frenleri yenilendi! (Kondisyon: %100)"
    elif action_id == "insurance":
        asset.has_insurance = True
        char.happiness = min(100, char.happiness + 5)
        msg = f"🛡️📋 FULL KASKO POLİÇESİ YAPILDI! '{asset.name}' 1 yıl boyunca tüm kaza ve hasarlara karşı %100 sigorta altına alındı!"
    elif action_id == "highway_speed":
        char.stress = 0
        char.happiness = min(100, char.happiness + 25)
        roll = random.random()
        if roll < 0.20:
            radar_fine = 8500
            char.money -= radar_fine
            msg = f"🏎️💨 OTOBANDA GECE GAZLANDI! Hız kadranını zorladın, tüm stresin uçup gitti! Ancak EDS radarından 8.500 TL hız cezası yedin!"
        elif roll < 0.25:
            if asset.has_insurance:
                msg = f"🏎️💥 BARİYERE UFAK TEMAS: Virajda spin attın ancak kaskon olduğu için sigorta şirketi tüm masrafı karşıladı!"
            else:
                asset.condition = max(20, asset.condition - 25)
                repair_cost = 45000
                char.money -= repair_cost
                msg = f"🏎️💥 KAZA GEÇİRDİN! Kaskon olmadığı için sanayide 45.000 TL tamir parası ödedin! (Araba Kondisyonu: %{asset.condition})"
        else:
            msg = f"🏎️🌙 EFSANE GECE SÜRÜŞÜ! Gece otobanda gaza yüklendin, müzik son ses ve rüzgar yüzünde! Tüm dertlerini unuttun! (Stres: %0, Mutluluk +25)"
    else:
        msg = "İşlem yapıldı."

    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🏎️"))
    return {"success": True, "message": msg}

def do_wellness_action(char: Character, action_id: str) -> Dict[str, Any]:
    """Kişisel gelişim & Sağlık: Klinik Psikoloğu, Kütüphane Kitap Okuma ve Uzman Cerrahi."""
    act = next((a for a in WELLNESS_SERVICES if a["id"] == action_id), None)
    if not act:
        return {"success": False, "message": "Geçersiz hizmet."}
    if act["cost"] > 0 and char.money < act["cost"]:
        return {"success": False, "message": f"'{act['name']}' için {act['cost']:,} TL gerekli."}

    if act["cost"] > 0:
        char.money -= act["cost"]

    if action_id == "psychologist":
        char.stress = 0
        char.happiness = min(100, char.happiness + 24)
        char.health = min(100, char.health + 8)
        msg = "🧠🛋️ KLİNİK PSİKOLOG SEANSI: Terapistinle çocukluk travmalarını ve iş stresini konuştun. Kuş gibi hafifledin! (Stres: %0, Mutluluk +24)"
    elif action_id == "library":
        char.smarts = min(100, char.smarts + 6)
        char.happiness = min(100, char.happiness + 8)
        msg = "📚📖 KÜTÜPHANEDE BİLİM & KİTAP GÜNÜ: Gün boyu felsefe ve tarih kitapları okuyarak zihnini tazeledin! (Zeka +6, Mutluluk +8)"
    elif action_id == "surgery":
        char.health = min(100, char.health + 35)
        char.happiness = min(100, char.happiness + 25)
        if char.illnesses:
            cured = char.illnesses.pop(0)
            msg = f"🏥🩺 BAŞARILI AMELİYAT! Özel hastanede profesör cerrahlar tarafından ameliyat edildin ve '{cured}' rahatsızlığından tamamen kurtuldun! (Sağlık: %{char.health})"
        else:
            msg = f"🏥🩺 KAPSAMLI CHECK-UP & SAĞLIK DESTEĞİ: Özel klinikte tüm organların incelendi ve vitamin/ozon kürü uygulandı! (Sağlık: %{char.health})"
    else:
        msg = "İşlem yapıldı."

    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="health", icon="🩺"))
    return {"success": True, "message": msg}

# ----------------- DETAYLI İLİŞKİ SİSTEMLERİ: ÖP, DATE, KAVGA -----------------

def do_detailed_kiss(char: Character, person_id: str, kiss_id: str) -> Dict[str, Any]:
    """Detaylı öpüşme ve romantik yakınlaşma sistemi."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı veya hayatta değil."}
    
    kiss = next((k for k in KISS_STYLES if k["id"] == kiss_id), KISS_STYLES[1])
    is_partner = person.relation in ["Flört", "Sevgili", "Nişanlı", "Eş"]
    is_ex = person.relation in ["Eski Sevgili", "Eski Eş"]
    is_friend = person.relation == "Arkadaş"
    
    # Arkadaş durumunda öpücük
    if is_friend:
        if kiss_id in ["lips_gentle", "lips_passionate", "neck_whisper"]:
            if person.relationship_level >= 78 and random.random() < 0.70:
                person.relation = "Flört"
                person.relationship_level = min(100, person.relationship_level + 18)
                char.happiness = min(100, char.happiness + 20)
                msg = f"💘 BEKLENMEDİK AŞK KIVILCIMI! {person.name} dudaklarının dokunuşuyla donakaldı, gözleri parlayarak 'Ben de uzun zamandır bunu bekliyordum...' dedi! (Artık FLÖRT oldunuz!)"
                person.memories.append("Arkadaşlığınız tutkulu bir öpücükle aşka dönüştü!")
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💋"))
                return {"success": True, "message": msg}
            else:
                person.relationship_level = max(10, person.relationship_level - 18)
                char.happiness = max(5, char.happiness - 10)
                msg = f"😳 TERS TEPKİ: {person.name} geri çekilip kızardı: 'Biz sadece arkadaşız, ne yapıyorsun?!' Aranızdaki hava buz gibi oldu. (İlişki -18)"
                person.memories.append("Uygunsuz bir anda onu öpmeye kalkıştın.")
                return {"success": False, "message": msg}
        else:
            # Masum veya şefkatli öpücük (alın, yanak, el)
            person.relationship_level = min(100, person.relationship_level + 8)
            char.happiness = min(100, char.happiness + 6)
            msg = f"😊 {person.name} bu tatlı ve samimi jestine sıcacık bir tebessümle karşılık verdi. (İlişki +8)"
            return {"success": True, "message": msg}

    # Eski Sevgili durumunda öpücük
    if is_ex:
        if person.relationship_level >= 60 and random.random() < 0.65:
            person.relationship_level = min(100, person.relationship_level + 25)
            char.happiness = min(100, char.happiness + 18)
            msg = f"🔥 ESKİ AŞK YENİDEN ALEVLENDİ! {person.name} gözlerini kapatıp sana teslim oldu: 'Seni asla unutamamışım...' Kalpleriniz yeniden aynı ritimde atıyor! (İlişki +25)"
            person.memories.append("Ayrılığın ardından aranızda yeniden ateşli bir öpüşme yaşandı.")
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🔥"))
            return {"success": True, "message": msg}
        else:
            person.relationship_level = max(5, person.relationship_level - 15)
            char.happiness = max(5, char.happiness - 8)
            msg = f"💔 {person.name} seni hafifçe itti: 'Biz bittik, eski hataları tekrar yaşamayalım...' (İlişki -15)"
            return {"success": False, "message": msg}

    # Partner (Flört, Sevgili, Nişanlı, Eş)
    if is_partner:
        boost = kiss["rel_boost"]
        loyalty_boost = kiss["loyalty_boost"]
        stress_relief = kiss["stress_relief"]
        
        bonus_text = ""
        if person.personality in kiss.get("preferred_personalities", []):
            boost = int(boost * 1.35)
            loyalty_boost += 3
            bonus_text = f" ({person.personality} ruhunu adeta mest etti! ✨)"
            
        person.relationship_level = min(100, person.relationship_level + boost)
        person.loyalty = min(100, person.loyalty + loyalty_boost)
        char.stress = max(0, char.stress - stress_relief)
        char.happiness = min(100, char.happiness + 16)
        
        # Eğer Flört aşamasında ise ve dudaktan öpücükle ilişki >= 70 olduysa Sevgili'ye terfi!
        if person.relation == "Flört" and person.relationship_level >= 70 and kiss_id in ["lips_gentle", "lips_passionate", "neck_whisper"]:
            for p in char.relationships:
                if p.relation == "Sevgili" and p.id != person.id:
                    p.relation = "Eski Sevgili"
            person.relation = "Sevgili"
            char.dating_partner_id = person.id
            if "first_love" not in char.achievements:
                char.achievements.append("first_love")
            bonus_text += " ❤️ Bu büyülü öpücükle birlikte resmen SEVGİLİ oldunuz!"
            
        memory_desc = f"{kiss['name']} ile romantik ve unutulmaz bir an yaşadınız."
        person.memories.append(memory_desc)
        
        msg = f"{kiss['icon']} {person.name} ile romantik yakınlaşma: '{kiss['name']}'!{bonus_text} (İlişki +{boost}, Sadakat +{loyalty_boost}, Stres -{stress_relief})"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💋"))
        return {"success": True, "message": msg}
    
    # Aile veya diğerleri
    person.relationship_level = min(100, person.relationship_level + 8)
    return {"success": True, "message": f"🙏 {person.name} bu sevecen jestine gülümsedi. (İlişki +8)"}

def do_detailed_date(char: Character, person_id: str, venue_id: str, mid_choice: str = "", end_choice: str = "") -> Dict[str, Any]:
    """Çok aşamalı interaktif randevu simülasyonu."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Partner bulunamadı."}
    
    venue = next((v for v in DATE_VENUES if v["id"] == venue_id), DATE_VENUES[0])
    if char.money < venue["cost"]:
        return {"success": False, "message": f"'{venue['name']}' randevusu için {venue['cost']:,} TL gerekli."}
    
    char.money -= venue["cost"]
    
    # 1. Aşama: Mekan Uyumu
    base_boost = venue["rel_boost"]
    venue_comment = ""
    if person.personality in venue.get("disliked_by", []):
        base_boost = max(4, base_boost - 10)
        venue_comment = f"😒 {person.name} ({person.personality}) mekan seçimini pek beğenmedi ve hafifçe söylendi."
    elif person.personality in venue.get("best_for", []):
        base_boost = int(base_boost * 1.4)
        venue_comment = f"😍 {person.name} ({person.personality}) mekana bayıldı, gözleri parıldadı!"
    else:
        venue_comment = f"✨ {venue['name']} ortamında baş başa harika bir masa seçtiniz."
        
    # 2. Aşama: Randevu Ortası Olayı (mid_choice)
    mid_comment = ""
    mid_score = 0
    if mid_choice == "pay_all":
        mid_score += 8
        char.skills["charisma"] = min(100, char.skills.get("charisma", 20) + 3)
        mid_comment = "Hesabı cömertçe ve sessizce tek başına ödedin; partnerin karizmandan çok etkilendi."
    elif mid_choice == "split_bill":
        if person.personality == "Materyalist":
            mid_score -= 8
            mid_comment = "Hesabı kırışmayı teklif edince partnerin yüzünü astı ve burun kıvırdı."
        else:
            mid_score += 4
            mid_comment = "Hesabı adilce paylaştınız; eşitlikçi ve modern tavrını takdir etti."
    elif mid_choice == "let_them_pay":
        if person.wealth >= 60:
            mid_score += 5
            mid_comment = "Gülümseyerek hesabı ödemesine izin verdin; partnerin kendini güçlü ve önemsenmiş hissetti."
        else:
            mid_score -= 5
            mid_comment = "Hesabı ona ödetince biraz mahcup oldu ve cüzdanını zorladı."
    elif mid_choice == "dance_slow":
        mid_score += 12
        mid_comment = "Piste çıkıp romantik müzik eşliğinde birbirinize sarılarak dans ettiniz; etraftaki herkes size baktı!"
    elif mid_choice == "sing_toast":
        mid_score += 7
        mid_comment = "Göz göze kadeh kaldırıp şarkıya neşeyle eşlik ettiniz, kahkahalar havada uçuştu."
    elif mid_choice == "hold_hands":
        mid_score += 9
        mid_comment = "Masanın altından elini sımsıkı tuttun; parmakları parmaklarına kenetlendi ve sıcacık baktı."
    elif mid_choice == "vulnerable_truth":
        mid_score += 12
        person.loyalty = min(100, person.loyalty + 8)
        mid_comment = "Tüm samimiyetinle iç dünyanı açtın; partnerin sana olan güvenini ve hayranlığını dile getirdi."
    elif mid_choice == "witty_flirt":
        mid_score += 8
        mid_comment = "Zekice ve flörtöz bir espriyle tansiyonu yükselttin; yanakları al al oldu."
    elif mid_choice == "listen_them":
        mid_score += 10
        mid_comment = "Onun hayallerini ve geçmişini pürdikkat dinledin; 'Beni gerçekten anlayan tek insansın' dedi."
        
    # 3. Aşama: Gece Sonu Kapanışı (end_choice)
    end_comment = ""
    end_score = 0
    if end_choice == "kiss_goodbye":
        end_score += 10
        end_comment = "Ayrılırken kapısının önünde yanağına/dudağına büyüleyici bir veda busesi kondurdun; kalbi deli gibi çarptı!"
    elif end_choice == "invite_coffee":
        if person.relationship_level >= 65:
            end_score += 16
            char.stress = 0
            end_comment = "Davetini heyecanla kabul etti; gece boyu kahve içip sabahın ilk ışıklarına kadar baş başa kaldınız! 🔥"
        else:
            end_score += 2
            end_comment = "Gülümseyerek 'Biraz daha birbirimizi tanıyalım' dedi ama yanağından öpüp içeri girdi."
    elif end_choice == "warm_hug_walk":
        end_score += 8
        end_comment = "Birbirinize sımsıkı sarılıp 'Bu hayatımın en güzel gecesiydi' diyerek ayrıldınız."
        
    total_boost = base_boost + mid_score + end_score
    person.relationship_level = min(100, person.relationship_level + total_boost)
    char.happiness = min(100, char.happiness + 22)
    char.stress = max(0, char.stress - 15)
    
    # Flört Terfisi Kontrolü
    promo_note = ""
    if person.relation == "Flört" and person.relationship_level >= 75:
        existing_partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.id != person.id and p.is_alive), None)
        if not existing_partner:
            person.relation = "Sevgili"
            char.dating_partner_id = person.id
            promo_note = " ❤️ Randevu o kadar büyüleyici geçti ki artık resmen SEVGİLİSİNİZ!"
            
    memory_text = f"'{venue['name']}' randevusunda unutulmaz bir gece geçirdiniz."
    person.memories.append(memory_text)
    
    summary_msg = f"🌹 RANDEVU RAPORU: {venue_comment} {mid_comment} {end_comment}{promo_note} (İlişki +{total_boost}, Mutluluk +22, Stres -15)"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=summary_msg, category="love", icon="🌹"))
    return {
        "success": True,
        "message": summary_msg,
        "rel_boost": total_boost
    }

def do_detailed_fight(char: Character, person_id: str, topic_id: str, attitude_id: str) -> Dict[str, Any]:
    """Detaylı kavga, hesaplaşma ve ilişki krizi motoru."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
        
    topic = next((t for t in DETAILED_FIGHT_TOPICS if t["id"] == topic_id), DETAILED_FIGHT_TOPICS[0])
    attitude = next((a for a in DETAILED_FIGHT_ATTITUDES if a["id"] == attitude_id), DETAILED_FIGHT_ATTITUDES[0])
    
    craziness = getattr(person, "craziness", 50)
    loyalty = getattr(person, "loyalty", 70)
    rel_level = person.relationship_level
    
    char.stress = min(100, char.stress + 18)
    char.happiness = max(5, char.happiness - 16)
    
    if attitude_id == "emotional_tears":
        if loyalty >= 55:
            person.relationship_level = max(20, person.relationship_level - 6)
            person.loyalty = min(100, person.loyalty + 8)
            msg = f"🥺 KAVGA YATIŞTI: {person.name} gözyaşlarını görünce dayanamayıp sana sımsıkı sarıldı: 'Özür dilerim, seni bu kadar incittiğimi fark etmemiştim...' '{topic['name']}' konusundaki hatasını telafi etmeye söz verdi."
            person.memories.append(f"'{topic['name']}' krizinde döktüğün gözyaşları buzları eritti.")
        else:
            person.relationship_level = max(10, person.relationship_level - 16)
            msg = f"😒 SOĞUK TEPKİ: {person.name} ağlamana kayıtsız kaldı: 'Dram yapmayı bırak, her şeye ağlamak zorunda mısın?!' diyerek odayı terk etti."
            person.memories.append(f"'{topic['name']}' krizinde sana karşı son derece duyarsız davrandı.")
            
    elif attitude_id == "calm_ultimatum":
        if loyalty >= 70 and craziness < 65:
            person.relationship_level = max(25, person.relationship_level - 10)
            person.loyalty = min(100, person.loyalty + 12)
            msg = f"⚖️ RESTİNİ KABUL ETTİ: {person.name} masadaki ciddiyetini ve kararlılığını görünce sarsıldı: 'Haklısın, seni kaybetmek istemiyorum...' '{topic['name']}' konusunda kendini düzelteceğine yemin etti."
            person.memories.append(f"'{topic['name']}' konusunda ona açık bir ültimatom verdin ve geri adım attı.")
        else:
            if rel_level < 45 or craziness >= 70:
                if person.relation in ["Sevgili", "Flört"]:
                    person.relation = "Eski Sevgili"
                    char.dating_partner_id = None
                    msg = f"💔 RESTLEŞME VE AYRILIK! {person.name} 'Bana şart koşamazsın! Madem öyle bitti bu iş!' diyerek yüzüğü/eşyalarını fırlattı ve AYRILDINIZ!"
                    person.memories.append(f"'{topic['name']}' kavgası sonucu yollarınızı tamamen ayırdınız.")
                    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💔"))
                    return {"success": True, "message": msg, "breakup": True}
                else:
                    person.relationship_level = max(5, person.relationship_level - 35)
                    msg = f"💥 ŞİDDETLİ GERGİNLİK: {person.name} restine restle karşılık verdi: 'Ben buyum, işine gelirse!' Günlerce tek kelime konuşmadınız."
                    person.memories.append(f"'{topic['name']}' krizinde birbirinize rest çektiniz.")
            else:
                person.relationship_level = max(10, person.relationship_level - 20)
                msg = f"😤 TARTIŞMA SÜRÜYOR: {person.name} savunmaya geçip lafı çevirdi ama taviz vermedi. (İlişki -20)"
                person.memories.append(f"'{topic['name']}' konusunda sert bir tartışma yaşadınız.")
                
    elif attitude_id == "rage_explosion":
        person.relationship_level = max(5, person.relationship_level - 32)
        if craziness >= 55:
            msg = f"🔥🤬 KIYAMET KOPTU! Sesler yükseldi, {person.name} sehpadaki bardağı fırlatıp 'Yeter artık senden çektiğim!' diye haykırdı! Komşular kapıya dayandı! (İlişki -32, Stres +25)"
            person.memories.append(f"'{topic['name']}' krizinde karşılıklı bardaklar kırıldı ve şiddetli bir kavga yaşandı.")
        else:
            msg = f"🚪💥 KAPIYI ÇARPIP GİTTİ! {person.name} öfkene karşı dehşete düşüp çantasını aldı ve kapıyı çarpıp evi terk etti! (İlişki -32)"
            person.memories.append(f"'{topic['name']}' tartışmasında bağırıp çağırdığın için evi terk etti.")
            
    else:  # cold_sarcasm
        person.relationship_level = max(10, person.relationship_level - 22)
        msg = f"🧊 BUZ GİBİ SOĞUK SAVAŞ: İğneleyici laflarınla {person.name}'in canını yaktın. Hiçbir şey demeden telefonunu sessize aldı ve sana 'Silent Treatment' (sessiz ceza) uyguladı. (İlişki -22)"
        person.memories.append(f"'{topic['name']}' konusunda pasif-agresif iğnelemelerle birbirinizi kırdınız.")
        
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💥"))
    return {"success": True, "message": msg}

# ----------------- DERİNLEŞTİRİLMİŞ İNSAN İLİŞKİLERİ VE EYLEMLERİ -----------------

def do_parent_care_action(char: Character, person_id: str, care_id: str) -> Dict[str, Any]:
    """Yaşlanan anne/babanın bakım masası ve vefa eylemleri."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı veya hayatta değil."}
    if person.relation not in ["Anne", "Baba"]:
        return {"success": False, "message": "Yaşlı bakım masası sadece Anne veya Babanız için geçerlidir."}
    
    care = next((c for c in PARENT_CARE_OPTIONS if c["id"] == care_id), None)
    if not care:
        return {"success": False, "message": "Bakım seçeneği bulunamadı."}
    
    cost = care.get("cost", 0)
    if char.money < cost:
        return {"success": False, "message": f"{care['name']} için {cost:,} TL gerekli."}
    
    char.money -= cost
    person.care_status = care.get("status_label", care["name"])
    
    if care_id == "take_home":
        person.relationship_level = 100
        char.karma = min(100, char.karma + 25)
        char.happiness = min(100, char.happiness + 15)
        person.memories.append("Seni kendi evine yanına aldı ve baş tacı etti.")
        msg = f"🏡❤️ {person.name}'i kendi evine, yanına aldın! Baş tacı ettin, 'Allah senden razı olsun evladım' diyerek gözyaşlarıyla sarıldı! (İlişki: %100, Karma +25)"
    elif care_id == "hire_caregiver":
        person.relationship_level = min(100, person.relationship_level + 30)
        char.karma = min(100, char.karma + 20)
        char.stress = max(0, char.stress - 10)
        person.memories.append("Onun için en iyi yatılı özel bakıcı ve hemşireyi tuttun.")
        msg = f"👩‍⚕️💊 {person.name} için 7/24 profesyonel yatılı bakım hemşiresi tuttun! İlaçları ve sağlığı emin ellerde, huzur içinde yaşıyor. (İlişki +30, Karma +20)"
    elif care_id == "nursing_home":
        char.karma = min(100, char.karma + 8)
        if person.personality in ["Geleneksel & Muhafazakar", "Sadık & Aileci"]:
            person.relationship_level = max(25, person.relationship_level - 10)
            person.memories.append("Huzurevine yerleştirdin; biraz hüzünlense de nezih bir ortamda olduğunu biliyor.")
            msg = f"🏥🍂 {person.name}'i seçkin ve konforlu bir huzurevine yerleştirdin. Gözlerinde hafif bir burukluk olsa da doktor ve arkadaş ortamı iyi geldi. (İlişki -10, Bakım Sağlandı)"
        else:
            person.relationship_level = min(100, person.relationship_level + 15)
            person.memories.append("Seçkin bir huzurevine yerleştirdin, düzenli ziyaret ediyorsun.")
            msg = f"🏥✨ {person.name}'i 7/24 doktor gözetimli seçkin bir bakımevine yerleştirdin. Sosyal etkinlikler ve akranlarıyla çok mutlu. (İlişki +15)"
    else:  # hospital_vigil
        person.relationship_level = 100
        char.karma = min(100, char.karma + 20)
        char.happiness = min(100, char.happiness + 10)
        person.memories.append("Hastalığında günlerce başında refakatçi kalıp elini sımsıkı tuttun.")
        msg = f"🤲🩺 Hastanede günlerce {person.name}'in başucunda refakatçi kaldın, elini bir an bile bırakmadın! 'Sen benim hayırlı evladımsın' diyerek sana dua etti! (İlişki %100, Karma +20)"
    
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="family", icon="🤲"))
    return {"success": True, "message": msg}


def do_sibling_action(char: Character, person_id: str, action_id: str) -> Dict[str, Any]:
    """Kardeş dayanışması, borç, düğünde altın takma ve bayram barışması."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı veya hayatta değil."}
    if person.relation not in ["Kardeş", "Abla", "Ağabey"]:
        return {"success": False, "message": "Bu işlem yalnızca kardeşleriniz (Kardeş/Abla/Ağabey) için geçerlidir."}
    
    action_item = next((a for a in SIBLING_INTERACTIONS if a["id"] == action_id), None)
    if not action_item:
        return {"success": False, "message": "Eylem bulunamadı."}
    
    cost = action_item.get("cost", 0)
    if char.money < cost:
        return {"success": False, "message": f"{action_item['name']} için {cost:,} TL gerekli."}
    
    char.money -= cost
    
    if action_id == "ask_bail_loan":
        person.lent_amount += 50000
        person.is_estranged = False
        person.relationship_level = min(100, person.relationship_level + 35)
        char.karma = min(100, char.karma + 18)
        person.memories.append("En zor gününde 50.000 TL borç vererek iflastan kurtardın.")
        msg = f"💸🤝 Kardeşin {person.name}'e 50.000 TL el uzattın! Sana sarılıp ağladı: 'Sen olmasan batmıştım, bu vefanı ömrümce unutmayacağım!' (İlişki +35, Karma +18)"
    elif action_id == "wedding_gold_gift":
        person.relationship_level = 100
        char.happiness = min(100, char.happiness + 20)
        char.karma = min(100, char.karma + 12)
        person.memories.append("Düğününde kardeşine ağır tam altın ve beşi bir yerde taktın.")
        msg = f"🥇👰 Kardeşin {person.name}'in düğününde salonun alkışları arasında ağır tam altın taktın! Ailede başını dik tuttun! (İlişki: %100, Mutluluk +20)"
    elif action_id == "reconcile_peace":
        person.is_estranged = False
        bonus = 40 if person.relationship_level < 50 else 18
        person.relationship_level = min(100, person.relationship_level + bonus)
        char.happiness = min(100, char.happiness + 20)
        char.karma = min(100, char.karma + 15)
        person.memories.append("Bayramda aradaki soğukluğa son verip kucaklaştınız ve helalleştiniz.")
        msg = f"🕊️ Bayram sabahı {person.name}'in kapısını çaldın, gözyaşlarıyla sarıldınız! Yılların kırgınlığı ve küslüğü son buldu, kan bağınız galip geldi! (İlişki +{bonus}, Karma +15)"
    else:  # deep_heart_talk
        person.relationship_level = min(100, person.relationship_level + 20)
        char.happiness = min(100, char.happiness + 14)
        person.memories.append("Çocukluk günlerinizi ve eski bayramları yad edip dertleştiniz.")
        msg = f"☕ Kardeşin {person.name} ile baş başa kahve içip çocukluk günlerinizi, sokak oyunlarını ve anne-babanızın gençliğini yad ettiniz. Ruhunuz dinlendi! (İlişki +20)"
    
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="family", icon="🤝"))
    return {"success": True, "message": msg}


def do_parenting_action(char: Character, person_id: str, crisis_id: str, choice_id: str) -> Dict[str, Any]:
    """Çocuk yetiştirme, ergenlik isyanı ve kariyer seçiminde kritik ebeveynlik kararları."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Çocuk bulunamadı veya hayatta değil."}
    if person.relation != "Çocuk":
        return {"success": False, "message": "Bu eylem yalnızca çocuğunuz için geçerlidir."}
    
    crisis = next((c for c in PARENTING_CRISES if c["id"] == crisis_id), None)
    if not crisis:
        return {"success": False, "message": "Kriz konusu bulunamadı."}
    
    choice = next((opt for opt in crisis["options"] if opt["id"] == choice_id), None)
    if not choice:
        return {"success": False, "message": "Seçim bulunamadı."}
    
    if crisis_id == "teen_rebellion":
        if choice_id == "gentle_mentor":
            person.relationship_level = min(100, person.relationship_level + 25)
            person.smarts = min(100, person.smarts + 10)
            char.happiness = min(100, char.happiness + 12)
            person.memories.append("Ergenlik isyanında seni yargılamadan dinledi ve sevgiyle yol gösterdi.")
            msg = f"☕ Çocuğun {person.name}'i karşına alıp sıcacık bir çay eşliğinde yargılamadan dinledin. Gözyaşları içinde içini döktü ve tehlikeli arkadaş ortamından uzaklaşmaya söz verdi! (İlişki +25, Zeka +10)"
        elif choice_id == "strict_discipline":
            person.relationship_level = max(15, person.relationship_level - 18)
            person.smarts = min(100, person.smarts + 12)
            person.memories.append("Ergenlikte telefonuna ve harçlığına el koyup sert kurallar koydun.")
            msg = f"📵 Sert ebeveyn otoriteni koydun; telefonuna ve harçlığına 1 ay el koydun! Sana surat asıp odasına kapansa da zorunlu olarak derslerine odaklandı. (İlişki -18, Disiplin +12)"
        else:  # family_therapy
            cost = 6000
            if char.money < cost:
                return {"success": False, "message": f"Ergenlik psikoloğu ve aile terapisi için {cost:,} TL gerekli."}
            char.money -= cost
            person.relationship_level = min(100, person.relationship_level + 30)
            person.smarts = min(100, person.smarts + 15)
            char.happiness = min(100, char.happiness + 15)
            person.memories.append("Uzman aile terapisti ve ergen psikoloğuyla krizi sevgiyle aştınız.")
            msg = f"🛋️ Alanında uzman bir ergen psikoloğu ve aile terapisti desteği aldınız. Çocuğun kendini anlaşıldı hissetti ve ailesine olan saygısı katlandı! (İlişki +30, Zeka +15)"
            
    else:  # career_choice
        if choice_id == "support_dream":
            cost = 40000
            if char.money < cost:
                return {"success": False, "message": f"Başlangıç sermayesi ve hayal desteği için {cost:,} TL gerekli."}
            char.money -= cost
            person.relationship_level = 100
            person.smarts = min(100, person.smarts + 20)
            char.happiness = min(100, char.happiness + 20)
            char.karma = min(100, char.karma + 15)
            person.memories.append("Hayallerinin arkasında durup 40.000 TL başlangıç sermayesi verdin.")
            msg = f"🌟 'Hayalinin arkasındayım evladım!' diyerek 40.000 TL başlangıç sermayesi verdin! Gözlerindeki mutluluk paha biçilemezdi, kendi işini kurmak için canla başla çalışıyor! (İlişki: %100, Zeka +20)"
        elif choice_id == "push_traditional":
            person.relationship_level = max(20, person.relationship_level - 18)
            person.smarts = min(100, person.smarts + 15)
            person.memories.append("Geleneksel garantici meslekler (Tıp/Hukuk/Mühendislik) için baskı kurdun.")
            msg = f"🏛️ 'Önce altın bileziğin olsun!' dedin ve geleneksel garantili bir bölüme yazdırdın. Sana biraz sitem etse de kariyer garantisini kabul etti. (İlişki -18, Meslek Garantisi)"
        else:  # compromise_school
            person.relationship_level = min(100, person.relationship_level + 18)
            person.smarts = min(100, person.smarts + 14)
            char.happiness = min(100, char.happiness + 12)
            person.memories.append("Hem örgün üniversite diploması alıp hem de hayalindeki projeyi büyütmesi için anlaştınız.")
            msg = f"🤝 Muazzam bir orta yol buldunuz: 'Diplomanı alırken aynı zamanda hayalindeki projeyi büyüt!' Çocuğun bu dengeli tavrına minnettar kaldı! (İlişki +18, Zeka +14)"
            
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="family", icon="🎓"))
    return {"success": True, "message": msg}


def do_friend_action(char: Character, person_id: str, action_id: str) -> Dict[str, Any]:
    """Gerçekçi dostluk sınavları: borç verme, sır paylaşma, gece imdadına koşma ve road trip."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı veya hayatta değil."}
    if person.relation != "Arkadaş":
        return {"success": False, "message": "Bu eylem yalnızca arkadaşlarınız için geçerlidir."}
    
    act = next((a for a in FRIEND_INTERACTIONS if a["id"] == action_id), None)
    if not act:
        return {"success": False, "message": "Dostluk eylemi bulunamadı."}
    
    cost = act.get("cost", 0)
    if char.money < cost:
        return {"success": False, "message": f"{act['name']} için {cost:,} TL gerekli."}
    
    char.money -= cost
    
    if action_id == "lend_money":
        person.lent_amount += 15000
        if person.loyalty >= 60:
            person.relationship_level = min(100, person.relationship_level + 30)
            char.karma = min(100, char.karma + 12)
            person.memories.append("Zor gününde 15.000 TL kira borcu verdin, sana sonsuz vefalı.")
            msg = f"🤝 Zor durumdaki {person.name}'e 15.000 TL borç verdin. Gözleri doldu: 'Hızır gibi yetiştin, ilk maaşımda kuruşu kuruşuna geri ödeyeceğim dostum!' (İlişki +30, Karma +12)"
        else:
            person.relationship_level = max(10, person.relationship_level - 15)
            person.memories.append("15.000 TL borç verdin ama parayı aldıktan sonra telefonlarına geç dönmeye başladı.")
            msg = f"😬 {person.name}'e 15.000 TL borç verdin. Fakat parayı aldıktan sonra aramalarına geç dönmeye, bahaneler üretmeye başladı! Sadakati düşükmüş (%{person.loyalty}), borcu almak zor olacak!"
    elif action_id == "share_secret":
        if person.loyalty >= 75:
            person.relationship_level = min(100, person.relationship_level + 25)
            person.memories.append("En karanlık sırrını paylaştın ve aranızdaki güven mezara kadar mühürlendi.")
            msg = f"🤫 Hayatında hiç kimseye anlatmadığın en derin sırrını {person.name}'e açtın. 'Bu sır benimle mezara gider dostum' diyerek elini omzuna koydu. Güveniniz çelikleşti! (İlişki +25)"
        else:
            person.relationship_level = max(15, person.relationship_level - 10)
            char.stress = min(100, char.stress + 15)
            person.memories.append("Bir sırrını anlattın ama ortak arkadaş grubunda dedikodusu döndü!")
            msg = f"🤐 Sırrını {person.name}'e emanet ettin fakat birkaç gün sonra ortak arkadaşların imalı laflar soktuğunu duydun! Sırrını tutamamış! (Stres +15, Güven Zedelendi)"
    elif action_id == "stand_by_night":
        person.relationship_level = min(100, person.relationship_level + 35)
        person.loyalty = min(100, person.loyalty + 15)
        char.karma = min(100, char.karma + 15)
        person.memories.append("Gece saat 03:00'te zor gününde hiç düşünmeden yanına koştun.")
        msg = f"🚨 Gece 03:00'te gelen panik telefonuna hiç düşünmeden yataktan fırlayıp yanına koştun! 'Dost kara günde belli olur' sözünü kanıtladın, sana bir ömür sadık bir dost kazandın! (İlişki +35, Sadakat +15)"
    else:  # fun_road_trip
        person.relationship_level = min(100, person.relationship_level + 25)
        char.happiness = min(100, char.happiness + 20)
        char.stress = max(0, char.stress - 20)
        person.memories.append("Ege sahillerinde unutulmaz bir kamp ve road trip yaptınız.")
        msg = f"🚗🏕️ Arabaya atlayıp sahil rotasında müzik, çadır ve kamp ateşi eşliğinde unutulmaz bir hafta sonu geçirdiniz! Tüm stresiniz uçup gitti, dostluğunuz pekişti! (İlişki +25, Stres -20)"
    
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="🤝"))
    return {"success": True, "message": msg}


def do_consolidated_chat(char: Character, person_id: str) -> Dict[str, Any]:
    """Tüm roller için tek, akıllı ve zengin samimi sohbet & dertleşme eylemi."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı veya hayatta değil."}
    
    rel = person.relation
    if rel in ["Anne", "Baba"]:
        person.relationship_level = min(100, person.relationship_level + 15)
        char.happiness = min(100, char.happiness + 10)
        char.karma = min(100, char.karma + 6)
        dialogues = [
            f"☕ {person.name} ile çay demleyip eski aile hatıralarını, dedelerinin hikayelerini dinledin. 'Bizi unutma evladım' diyerek sırtını sıvazladı. (İlişki +15, Mutluluk +10)",
            f"📞 {person.name} ile uzun bir telefon konuşması yaptınız, sağlığını ve tansiyonunu sordun. Sesini duymak ona ilaç gibi geldi. (İlişki +15, Karma +6)"
        ]
        msg = random.choice(dialogues)
    elif rel in ["Kardeş", "Abla", "Ağabey"]:
        person.relationship_level = min(100, person.relationship_level + 16)
        char.happiness = min(100, char.happiness + 12)
        msg = f"☕ Kardeşin {person.name} ile kahve içerken ailedeki son dedikoduları kaynattınız ve eski bayram harçlıklarınızı yarıştırdınız! Aranızdaki bağ tazelendi. (İlişki +16, Mutluluk +12)"
    elif rel == "Çocuk":
        person.relationship_level = min(100, person.relationship_level + 18)
        person.smarts = min(100, person.smarts + 6)
        char.happiness = min(100, char.happiness + 12)
        msg = f"📚 Çocuğun {person.name} ile yan yana oturup okuldaki gününü, arkadaşlarını ve gelecekte ne olmak istediğini konuştunuz. Sana güvenle sarıldı! (İlişki +18, Zeka +6)"
    elif rel in ["Sevgili", "Eş", "Nişanlı", "Flört"]:
        person.relationship_level = min(100, person.relationship_level + 16)
        person.loyalty = min(100, person.loyalty + 4)
        char.happiness = min(100, char.happiness + 14)
        msg = f"🌹 {person.name} ile mum ışığında baş başa verip duygularınızı, gelecek hayallerinizi ve birbirinize olan sevginizi konuştunuz. Gözlerinin içi parladı! (İlişki +16, Mutluluk +14)"
    elif rel in ["Eski Sevgili", "Eski Eş"]:
        person.relationship_level = min(100, person.relationship_level + 10)
        char.happiness = min(100, char.happiness + 6)
        msg = f"💬 {person.name} ile medeni bir şekilde hal hatır sordunuz. Geçmişin burukluğu yerini sakin bir olgunluğa bıraktı. (İlişki +10)"
    else:  # Arkadaş ve diğerleri
        person.relationship_level = min(100, person.relationship_level + 15)
        char.happiness = min(100, char.happiness + 12)
        msg = f"☕ Dostun {person.name} ile salaş bir kafede buluşup hayatın koşuşturmacasını, işleri ve anıları konuştunuz. Çok iyi geldi! (İlişki +15, Mutluluk +12)"
    
    person.memories.append(f"Samimi ve derin bir sohbet gerçekleştirdiniz.")
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="💬"))
    return {"success": True, "message": msg}

# ----------------- TEK GECELİK İLİŞKİ, FLÖRT & AŞK SİSTEMLERİ -----------------

def do_hookup(char: Character, venue_id: str, use_protection: bool = True) -> Dict[str, Any]:
    """Gece hayatı, mekan kaçamağı ve tek gecelik ilişki (Hookup)."""
    if char.age < 18:
        return {"success": False, "message": "Gece hayatı ve kaçamak aktiviteleri için en az 18 yaşında olmalısın."}
    
    venue = next((v for v in HOOKUP_VENUES if v["id"] == venue_id), None)
    if not venue:
        return {"success": False, "message": "Mekan bulunamadı."}
    
    cost = venue.get("cost", 0)
    if char.money < cost:
        return {"success": False, "message": f"{venue['name']} için {cost:,} TL gerekli."}
    
    char.money -= cost
    char.hookup_count += 1
    
    partner_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
    pool_names = FIRST_NAMES_FEMALE if partner_gender == "Kadın" else FIRST_NAMES_MALE
    p_name = f"{random.choice(pool_names)} {random.choice(LAST_NAMES)}"
    p_age = max(18, min(58, char.age + random.randint(-3, 6)))
    p_job = random.choice(["DJ", "Model", "Barmen / Barmeyd", "Mimar", "Finansçı", "Dövme Sanatçısı", "Yazılımcı", "Dansçı", "Turist"])
    p_looks = random.randint(70, 99)
    p_personality = random.choice(PERSONALITIES)["id"]
    
    # Mevcut partner varsa aldatma cezası
    existing_partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive), None)
    cheating_warning = ""
    if existing_partner:
        char.karma = max(0, char.karma - 25)
        if random.random() < 0.38:
            existing_partner.relationship_level = max(5, existing_partner.relationship_level - 40)
            existing_partner.memories.append(f"{venue['name']} kaçamağını öğrendi ve büyük bir skandal çıktı!")
            cheating_warning = f"\n\n😱 ALDATMA SKANDALI! {existing_partner.name} kaçamağını ortak bir tanıdıktan öğrendi! İlişkiniz yerle bir oldu (-40 İlişki)!"

    # 1. Korumasız İlişki Riskleri (CYBH / İstenmeyen Gebelik)
    if not use_protection:
        # CYBH İhtimali (%28)
        if random.random() < 0.28:
            std = random.choice(["Klamidya Enfeksiyonu", "Genital Herpes", "Bel Soğukluğu (Gonore)"])
            if std not in char.illnesses:
                char.illnesses.append(std)
            char.health = max(10, char.health - 24)
            char.stress = min(100, char.stress + 30)
            msg = f"⚡🦠 KORUMASIZ İLİŞKİ VE HASTALIK! {venue['name']} ortamında {p_name} ({p_age}, {p_job}) ile korumasız bir gece geçirdin. Birkaç gün sonra şiddetli semptomlarla doktora gittin ve '{std}' teşhisi konuldu! Hemen tedavi olmalısın! (Sağlık -24, Stres +30){cheating_warning}"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"Korumasız kaçamak sonucu '{std}' rahatsızlığına yakalandın!", category="health", icon="🦠"))
            if "casanova_hookup" not in char.achievements:
                char.achievements.append("casanova_hookup")
            return {"success": True, "message": msg, "std": std}
        
        # İstenmeyen Gebelik (%20)
        elif random.random() < 0.20:
            char.stress = min(100, char.stress + 25)
            if char.gender == "Kadın":
                msg = f"⚡🤰 SÜRPRİZ GEBELİK! {venue['name']} ortamında {p_name} ({p_job}) ile yaşadığın korumasız kaçamağın ardından hamile kaldığını öğrendin! (Stres +25){cheating_warning}"
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"Tek gecelik kaçamak sonrası hamile kaldın (Baba: {p_name})!", category="love", icon="🤰"))
            else:
                comp_cost = min(char.money, 35000)
                char.money -= comp_cost
                msg = f"⚡🍼 BABA OLUYORSUN ŞOKU! Kaçamak yaşadığın {p_name} ({p_job}) 1 ay sonra seni aradı: 'Hamileyim ve çocuk senden!' Doğum ve hastane masrafları için {comp_cost:,} TL ödemek zorunda kaldın!{cheating_warning}"
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"Tek gecelik kaçamak yaşadığın {p_name} hamile kaldı!", category="love", icon="🍼"))
            if "casanova_hookup" not in char.achievements:
                char.achievements.append("casanova_hookup")
            return {"success": True, "message": msg, "pregnancy": True}

    # 2. Genel Sabah Olayları (Twists)
    roll = random.random()
    if roll < 0.12:
        # Cüzdan / Saat Hırsızlığı
        theft_amount = min(char.money, random.randint(4000, 18000))
        char.money -= theft_amount
        char.happiness = max(0, char.happiness - 20)
        char.stress = min(100, char.stress + 25)
        msg = f"💸😱 YANKESİCİLİK ŞOKU! Sabah uyandığında {p_name}'in erkenden gittiğini, komodindeki saatini, telefonunu ve {theft_amount:,} TL nakit paranı çaldığını fark ettin! Polise gidip ifade verdin! (Stres +25){cheating_warning}"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"Kaçamak sonrası cüzdanın ve {theft_amount:,} TL nakit paran çalındı!", category="general", icon="💸"))
    elif roll < 0.22:
        # Evli Çıktı & Kapı Tekmelendi
        char.stress = min(100, char.stress + 30)
        char.happiness = max(0, char.happiness - 15)
        msg = f"🚪💥 MEĞER EVLİYMİŞ! Sabah 07:00'de evin kapısı tekmelendi, içeri öfkeli eşi daldı! Pantolonunu bile zor toplayıp yangın merdiveninden kaçtın! Günlerce korkudan arkana baktın! (Stres +30){cheating_warning}"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"{venue['name']} kaçamağında partnerin evli olduğu ortaya çıktı, kıl payı kaçtın!", category="general", icon="🚪"))
    elif roll < 0.40:
        # Kaçamak Aşka Dönüştü (Flörte Eklendi)
        char.happiness = min(100, char.happiness + 26)
        char.stress = max(0, char.stress - 20)
        new_flirt = Person(
            id=f"flirt_hookup_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=p_name,
            relation="Flört",
            gender=partner_gender,
            age=p_age,
            relationship_level=85,
            job=p_job,
            looks=p_looks,
            smarts=random.randint(65, 95),
            craziness=random.randint(20, 60),
            loyalty=random.randint(60, 95),
            wealth=random.randint(40, 85),
            personality=p_personality,
            red_flags=random.sample(RED_FLAGS_POOL, 1) if random.random() < 0.5 else [],
            green_flags=random.sample(GREEN_FLAGS_POOL, 1) if random.random() < 0.75 else [],
            memories=[f"{venue['name']} kaçamağıyla tanıştınız; sabah mükemmel bir serpme kahvaltı yapıp flört etmeye başladınız."]
        )
        char.relationships.append(new_flirt)
        msg = f"💘✨ KAÇAMAK AŞKA DÖNÜŞTÜ! {venue['name']} ortamında {p_name} ({p_job}) ile harika bir uyum yakaladınız. Sabah kahve içip uzun uzun sohbet ettiniz, telefon numaralarınızı aldınız ve resmen FLÖRT etmeye başladınız! (Flört Eklendi, Mutluluk +26){cheating_warning}"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"{venue['name']} kaçamağı flörte dönüştü: {p_name} ile tanıştın!", category="love", icon="💘"))
    else:
        # Sorunsuz Güzel Bir Kaçamak
        char.happiness = min(100, char.happiness + 20)
        char.stress = max(0, char.stress - 15)
        msg = f"🔥 {venue['name']} ortamında {p_name} ({p_age}, {p_job}) ile unutulmaz, tutku dolu bir gece geçirdiniz! Sabah birbirinize sarılıp teşekkür ederek medenice ayrıldınız. (Mutluluk +20, Stres -15){cheating_warning}"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"{venue['name']} ortamında {p_name} ile tek gecelik kaçamak yaşadın.", category="love", icon="🔥"))

    if "casanova_hookup" not in char.achievements:
        char.achievements.append("casanova_hookup")
        
    return {"success": True, "message": msg}


def do_flirt_opening(char: Character, candidate_id: str, line_id: str) -> Dict[str, Any]:
    """KısmetApp veya sosyal tanışmada ilk mesaj / açılış cümlesi testi."""
    cand = next((c for c in char.dating_candidates if c.id == candidate_id), None)
    if not cand:
        return {"success": False, "message": "Flört adayı bulunamadı."}
    line = next((l for l in DATING_OPENING_LINES if l["id"] == line_id), None)
    if not line:
        return {"success": False, "message": "Açılış cümlesi bulunamadı."}
    
    cand_p = cand.personality
    if cand_p in line.get("best_for", []):
        cand.compatibility = min(99, cand.compatibility + 22)
        reply = f"Ahaha harikasın! Uzun zamandır duyduğum en zeki ve tatlı açılıştı 😊 Kesinlikle tanışmalıyız!"
        success = True
    elif cand_p in line.get("penalty_for", []):
        cand.compatibility = max(10, cand.compatibility - 25)
        reply = f"Böyle bayat ve laubali laflardan hiç hoşlanmam. Şansını başkasında dene..."
        success = False
    else:
        cand.compatibility = min(99, cand.compatibility + 8)
        reply = f"Selam! Fena bir giriş değildi, kahve teklifine hayır demem sanırım :)"
        success = True
        
    return {
        "success": success,
        "message": f"💬 {cand.name}: \"{reply}\" (Uyum: %{cand.compatibility})",
        "reply": reply,
        "candidate": cand.model_dump()
    }


def do_situationship_talk(char: Character, person_id: str) -> Dict[str, Any]:
    """Flört aşamasında 'Biz Şimdi Neyiz?' resti ve adını koyma."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    if person.relation != "Flört":
        return {"success": False, "message": "Bu konuşma sadece Flört aşamasındaki kişiler için geçerlidir."}
    
    if person.relationship_level >= 65:
        # Sevgili yap
        for p in char.relationships:
            if p.relation == "Sevgili" and p.id != person.id:
                p.relation = "Eski Sevgili"
        person.relation = "Sevgili"
        char.dating_partner_id = person.id
        person.relationship_level = min(100, person.relationship_level + 20)
        char.happiness = min(100, char.happiness + 20)
        person.memories.append("Kahve içerken 'Biz şimdi neyiz?' dedin; ellerini tutup 'Artık resmen sevgilimsin' dedi!")
        msg = f"💑 'BİZ SEVGİLİYİZ!' {person.name} ellerini tutup gözlerinin içine baktı: 'Ben de günlerdir bunu bekliyordum! Artık resmen hayatımın aşkısın!' (İlişki: Sevgili, Mutluluk +20)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💑"))
        return {"success": True, "message": msg, "relation": "Sevgili"}
    elif person.relationship_level < 45 or person.craziness > 65 or person.personality == "Çapkın & Özgür Ruhlu":
        person.relation = "Eski Sevgili"
        char.happiness = max(0, char.happiness - 15)
        person.memories.append("'Biz neyiz?' diye sordun; bağlanamayacağını söyleyip ilişkiyi bitirdi.")
        msg = f"💔 'BEN BAĞLANAMAM...' {person.name} geri adım attı: 'Ben şu sıralar ciddi bir ilişkiye hazır değilim, hayatımı özgür yaşamak istiyorum...' Yollarınızı ayırdınız!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💔"))
        return {"success": True, "message": msg, "relation": "Eski Sevgili"}
    else:
        person.relationship_level = min(100, person.relationship_level + 6)
        msg = f"⏳ 'BİRAZ ZAMAN VER...' {person.name} acele etmek istemediğini, birbirinizi biraz daha tanımanız gerektiğini söyledi. Flörtünüz devam ediyor."
        return {"success": True, "message": msg, "relation": "Flört"}


def do_confess_love(char: Character, person_id: str) -> Dict[str, Any]:
    """İlk 'Seni Seviyorum' İtirafı (Aşk Dönüm Noktası)."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    if person.relation not in ["Flört", "Sevgili", "Nişanlı", "Eş"]:
        return {"success": False, "message": "Sadece romantik partnerine aşkını ilan edebilirsin."}
    if person.love_confessed:
        return {"success": False, "message": f"{person.name}'e zaten daha önce aşkını ilan ettin!"}
    
    person.love_confessed = True
    if person.relationship_level >= 68:
        person.relationship_level = min(100, person.relationship_level + 25)
        char.happiness = min(100, char.happiness + 25)
        char.stress = max(0, char.stress - 15)
        person.memories.append("İlk kez gözlerinin içine bakıp 'Seni seviyorum' dedin; ağlayarak sarıldı.")
        msg = f"❤️ 'BEN DE SENİ ÇOK SEVİYORUM!' {person.name}'in gözleri doldu, boynuna sarılıp seni sımsıkı öptü: 'Bunu duymayı o kadar uzun zamandır bekliyordum ki!' (İlişki +25, Mutluluk +25)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="❤️"))
        return {"success": True, "message": msg}
    else:
        person.relationship_level = max(20, person.relationship_level - 12)
        char.happiness = max(10, char.happiness - 18)
        char.stress = min(100, char.stress + 20)
        person.memories.append("Erken bir 'Seni seviyorum' dedin; ortam buz kesti.")
        msg = f"😬 'TEŞEKKÜR EDERİM...' Masada ölümcül bir sessizlik oldu. {person.name} gözlerini kaçırıp: 'Sen gerçekten harika bir insansın ama ben henüz o noktada değilim...' dedi. Yerin dibine geçtin! (Stres +20, Mutluluk -18)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"{person.name}'e erken aşk ilanı yaptın ve soğuk bir karşılık aldın.", category="love", icon="😬"))
        return {"success": False, "message": msg}


def do_hard_launch(char: Character, person_id: str) -> Dict[str, Any]:
    """Sosyal medyada 'Hard Launch' (İlişkiyi Fotoğrafla Resmen İlan Etme)."""
    person = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    if person.relation not in ["Sevgili", "Nişanlı", "Eş"]:
        return {"success": False, "message": "Hard Launch sadece sevgilin, nişanlın veya eşinle yapılabilir."}
    if person.hard_launched:
        return {"success": False, "message": "İlişkinizi zaten daha önce sosyal medyada ilan ettiniz!"}
    
    if person.loyalty >= 55 and person.personality != "Çapkın & Özgür Ruhlu":
        person.hard_launched = True
        person.relationship_level = min(100, person.relationship_level + 20)
        char.fame = min(100, char.fame + 5)
        char.happiness = min(100, char.happiness + 16)
        person.memories.append("Instagram'da ilişkinizi 'Hard Launch' ile resmen duyurdunuz.")
        msg = f"📸❤️ HARD LAUNCH! Instagram'da sevgilin {person.name} ile el ele romantik fotoğrafınızı '🤍' emojisiyle paylaştın! Beğeni ve tebrik yağdı, {person.name} fotoğrafı kendi profiline sabitledi! (İlişki +20, Şöhret +5)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="📸"))
        return {"success": True, "message": msg}
    else:
        person.relationship_level = max(15, person.relationship_level - 18)
        char.stress = min(100, char.stress + 18)
        person.memories.append("Fotoğrafını paylaştığın için kıyamet kopardı, sildirdi.")
        msg = f"🤨 'HEMEN KALDIR O FOTOĞRAFI!' {person.name} öfkeyle aradı: 'Benden habersiz neden paylaşıyorsun? Nazar değer, özel hayatımız bu!' diyerek sildirdi. İçine büyük bir sadakat şüphesi düştü! (Stres +18, İlişki -18)"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"{person.name} sosyal medyadaki çift fotoğrafınızı öfkeyle sildirdi!", category="love", icon="🤨"))
        return {"success": False, "message": msg}


def do_handle_ex_midnight_text(char: Character, person_id: str, choice_id: str) -> Dict[str, Any]:
    """Gece saat 02:30'da eski sevgiliden gelen 'Uyudun mu?' mesajı krizi."""
    ex = next((p for p in char.relationships if p.id == person_id and p.is_alive), None)
    if not ex:
        return {"success": False, "message": "Kişi bulunamadı."}
    
    current_partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Nişanlı", "Eş"] and p.is_alive), None)
    
    if choice_id == "show_partner":
        if current_partner:
            current_partner.relationship_level = min(100, current_partner.relationship_level + 20)
            current_partner.loyalty = min(100, current_partner.loyalty + 12)
            char.karma = min(100, char.karma + 10)
            msg = f"📱🤝 DÜRÜST DAVRANDIN! Gece {ex.name}'den gelen mesajı sabah sevgilin {current_partner.name}'e gösterdin. Sana olan güveni tavan yaptı: 'İyi ki varsın aşkım' diyerek sımsıkı sarıldı! (İlişki +20, Sadakat +12)"
        else:
            msg = f"📱 {ex.name}'in mesajını yakın arkadaşlarına gösterip güldünüz ve 'Geçmiş geçmişte kaldı' dediniz."
        ex.memories.append("Gece mesaj attı ama yüz bulamadı.")
    elif choice_id == "reply_secretly":
        char.karma = max(0, char.karma - 20)
        ex.relationship_level = min(100, ex.relationship_level + 18)
        if current_partner and random.random() < 0.45:
            current_partner.relationship_level = max(5, current_partner.relationship_level - 35)
            msg = f"😱 YAKALANDIN! Gece gizlice {ex.name}'e 'Uyumadım, sen nasılsın?' yazdın. Sabah sevgilin {current_partner.name} ekran bildirimini gördü ve kıyamet koptu! (İlişki -35, Güven Sarsıldı)"
        else:
            msg = f"🤫 Gece yarısı {ex.name} ile gizlice eski günleri yad ettiniz. Şimdilik kimse fark etmedi ama vicdanın sızlıyor. (Karma -20)"
        ex.memories.append("Gece gizlice mesajlaştınız.")
    else:  # block_ex
        ex.is_blocked = True
        ex.relationship_level = 0
        char.karma = min(100, char.karma + 8)
        msg = f"🚫 HİÇ ACIMADAN ENGELLEDİN! {ex.name}'in 'Uyudun mu?' mesajına tek kelime cevap vermeden her yerden engeli bastın. Huzurun tadını çıkarıyorsun!"
        ex.memories.append("Gece mesaj attı ve anında engellendi.")
        
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="📱"))
    return {"success": True, "message": msg}







