# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Gelişmiş Aktiviteler, Girişimcilik, İnteraktif Blackjack ve Eylemler Motoru
"""

import random
from typing import Dict, Any
from .models import (
    Character, Person, Pet, Asset, Job, Business, LifeLog,
    SocialMediaAccount, BlackjackHand
)
from .data import (
    JOBS_DATABASE, PART_TIME_JOBS, BUSINESS_TYPES, SCHOOL_CLUBS,
    REAL_ESTATE_MARKET, VEHICLE_MARKET, UNIVERSITIES,
    FIRST_NAMES_MALE, FIRST_NAMES_FEMALE, LAST_NAMES,
    PET_BREEDS, PET_NAMES
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

# ----------------- AŞK, ARKADAŞLIK & EVCİL HAYVANLAR -----------------

def find_love_date(char: Character) -> Dict[str, Any]:
    if char.age < 15:
        return {"success": False, "message": "Flört ve aşk için henüz yaşın küçük."}
    existing_partner = next((p for p in char.relationships if p.relation in ["Sevgili", "Eş"] and p.is_alive), None)
    if existing_partner:
        return {"success": False, "message": f"Zaten {existing_partner.name} ile birliktesin!"}
    
    partner_gender = "Kadın" if char.gender == "Erkek" else "Erkek"
    p_names = FIRST_NAMES_FEMALE if partner_gender == "Kadın" else FIRST_NAMES_MALE
    p_name = f"{random.choice(p_names)} {random.choice(LAST_NAMES)}"
    p_age = max(16, char.age + random.randint(-2, 3))
    jobs_list = ["Mimar", "Öğretmen", "Yazılımcı", "Diş Hekimi", "Avukat", "Tasarımcı", "Müzisyen", "Doktor"]
    
    new_lover = Person(
        id=f"person_lover_{len(char.relationships)+1}_{random.randint(10,99)}",
        name=p_name,
        relation="Sevgili",
        gender=partner_gender,
        age=p_age,
        relationship_level=85,
        job=random.choice(jobs_list),
        money_generosity=random.randint(45, 90)
    )
    char.relationships.append(new_lover)
    char.dating_partner_id = new_lover.id
    char.happiness = min(100, char.happiness + 22)
    if "first_love" not in char.achievements:
        char.achievements.append("first_love")
    
    msg = f"{p_name} ({p_age} yaşında, {new_lover.job}) ile tanıştın ve sevgili oldunuz! ❤️"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💘"))
    return {"success": True, "message": msg}

def make_new_friend(char: Character) -> Dict[str, Any]:
    f_gender = random.choice(["Erkek", "Kadın"])
    f_names = FIRST_NAMES_MALE if f_gender == "Erkek" else FIRST_NAMES_FEMALE
    f_name = f"{random.choice(f_names)} {random.choice(LAST_NAMES)}"
    new_friend = Person(
        id=f"friend_{len(char.relationships)+1}_{random.randint(10,99)}",
        name=f_name,
        relation="Arkadaş",
        gender=f_gender,
        age=max(6, char.age + random.randint(-2, 2)),
        relationship_level=80,
        job="Sosyal Çevre"
    )
    char.relationships.append(new_friend)
    char.happiness = min(100, char.happiness + 10)
    msg = f"{f_name} ile sıkı bir dostluk kurdun!"
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

def propose_marriage(char: Character, ring_cost: int) -> Dict[str, Any]:
    partner = next((p for p in char.relationships if p.relation == "Sevgili" and p.is_alive), None)
    if not partner:
        return {"success": False, "message": "Evlenme teklif edecek bir sevgilin yok."}
    if char.age < 18:
        return {"success": False, "message": "Evlenmek için en az 18 yaşında olmalısın."}
    if char.money < ring_cost:
        return {"success": False, "message": "Yüzük için yeterli paran yok."}
    
    char.money -= ring_cost
    accept_chance = 0.55 + (partner.relationship_level / 200) + (ring_cost / 100000)
    if random.random() < accept_chance:
        partner.relation = "Eş"
        char.spouse_id = partner.id
        char.happiness = 100
        if "married" not in char.achievements:
            char.achievements.append("married")
        # Düğün takı geliri!
        wedding_gifts = random.randint(45000, 180000)
        char.money += wedding_gifts
        msg = f"💍 {partner.name} teklifini kabul etti! Görkemli düğünde akrabalar {wedding_gifts:,} TL değerinde altın ve para taktı!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="👰"))
        return {"success": True, "message": msg}
    else:
        partner.relationship_level = max(10, partner.relationship_level - 25)
        char.happiness = max(0, char.happiness - 20)
        msg = f"{partner.name} henüz evliliğe hazır olmadığını söyledi."
        return {"success": False, "message": msg}

def try_for_baby(char: Character) -> Dict[str, Any]:
    partner = next((p for p in char.relationships if p.relation in ["Eş", "Sevgili"] and p.is_alive), None)
    if not partner:
        return {"success": False, "message": "Çocuk sahibi olmak için bir eşin veya sevgilin olmalı."}
    if char.age < 18 or partner.age > 52:
        return {"success": False, "message": "Şu anda çocuk sahibi olmak için uygun yaşta değilsiniz."}
    
    if random.random() < 0.72:
        b_gender = random.choice(["Erkek", "Kadın"])
        b_names = FIRST_NAMES_MALE if b_gender == "Erkek" else FIRST_NAMES_FEMALE
        baby_name = f"{random.choice(b_names)} {char.last_name}"
        
        baby = Person(
            id=f"person_child_{len(char.relationships)+1}_{random.randint(10,99)}",
            name=baby_name,
            relation="Çocuk",
            gender=b_gender,
            age=0,
            relationship_level=100
        )
        char.relationships.append(baby)
        char.happiness = min(100, char.happiness + 30)
        if "child" not in char.achievements:
            char.achievements.append("child")
        msg = f"👶 Dünyalar tatlısı bir {'oğlunuz' if b_gender == 'Erkek' else 'kızınız'} doğdu! Adını {baby_name} koydunuz!"
        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="🍼"))
        return {"success": True, "message": msg}
    else:
        return {"success": False, "message": "Bu yıl bebek denemeniz sonuç vermedi. Tekrar deneyebilirsiniz."}

def interact_with_person(char: Character, person_id: str, action: str) -> Dict[str, Any]:
    person = next((p for p in char.relationships if p.id == person_id), None)
    if not person:
        return {"success": False, "message": "Kişi bulunamadı."}
    if not person.is_alive:
        return {"success": False, "message": f"{person.name} hayatta değil."}
    
    if action == "chat":
        person.relationship_level = min(100, person.relationship_level + 10)
        char.happiness = min(100, char.happiness + 5)
        return {"success": True, "message": f"{person.name} ile çay içip samimi bir sohbet ettiniz. (İlişki +10)"}
    elif action == "spend_time":
        person.relationship_level = min(100, person.relationship_level + 15)
        char.happiness = min(100, char.happiness + 10)
        return {"success": True, "message": f"{person.name} ile harika vakit geçirdiniz!"}
    elif action == "give_gift":
        gift_cost = 2500
        if char.money < gift_cost:
            return {"success": False, "message": f"Hediye için {gift_cost:,} TL gerekli."}
        char.money -= gift_cost
        person.relationship_level = min(100, person.relationship_level + 25)
        char.karma = min(100, char.karma + 5)
        return {"success": True, "message": f"{person.name} aldığın hediyeye bayıldı! (İlişki +25)"}
    elif action == "ask_money":
        if person.relationship_level < 50:
            return {"success": False, "message": f"{person.name} seninle arası soğuk olduğu için para vermeyi reddetti."}
        amount = random.randint(2000, 15000)
        char.money += amount
        person.relationship_level = max(0, person.relationship_level - 8)
        return {"success": True, "message": f"{person.name} sana {amount:,} TL destek verdi!"}
    elif action == "argue":
        person.relationship_level = max(0, person.relationship_level - 25)
        char.happiness = max(0, char.happiness - 12)
        return {"success": True, "message": f"{person.name} ile şiddetli bir tartışma yaşadınız!"}
    elif action == "breakup":
        if person.relation in ["Sevgili", "Eş"]:
            is_divorce = (person.relation == "Eş")
            char.relationships = [p for p in char.relationships if p.id != person_id]
            if is_divorce:
                loss = max(0, int(char.money * 0.35))
                char.money -= loss
                char.happiness = max(0, char.happiness - 30)
                msg = f"{person.name} ile boşandınız! Mal paylaşımı olarak {loss:,} TL ödedin."
            else:
                char.happiness = max(0, char.happiness - 12)
                msg = f"{person.name} ile ayrıldınız."
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="love", icon="💔"))
            return {"success": True, "message": msg}
    return {"success": False, "message": "Geçersiz eylem."}

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
    new_asset = Asset(
        id=f"house_{len(char.assets)+1}_{random.randint(10,99)}",
        name=prop["name"],
        asset_type="Ev",
        purchase_price=prop["price"],
        current_value=prop["price"],
        annual_cost=prop["annual_cost"],
        annual_income=prop["annual_rent"]
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
    """Tam interaktif Blackjack (start, hit, stand)."""
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
    
    # Rotaya ve zekaya göre kaçış şansı
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
    msg = f"✈️ {name} tatiline çıktın! Tüm yorgunluğun ve stresin sıfırlandı. (Mutluluk +{hap_boost})"
    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="general", icon="✈️"))
    return {"success": True, "message": msg}
