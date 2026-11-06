# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Ana Oyun Motoru (Game Engine)
Karakter yaratımı, yaşlandırma döngüsü, otomatik okul geçişleri, şirket/finans hesaplamaları ve JSON kayıt sistemi.
"""

import os
import json
import random
import uuid
from typing import Optional, Dict, Any, List
from .models import Character, Person, Pet, Asset, Stock, SocialMediaAccount, LifeLog
from .data import (
    FIRST_NAMES_MALE, FIRST_NAMES_FEMALE, LAST_NAMES, CITIES,
    ZODIAC_SIGNS, PARENT_JOBS, ILLNESSES, INITIAL_STOCKS,
    PERSONALITIES, INTERESTS_POOL, LOVE_LANGUAGES, PRISON_ROLES, CHRONIC_CONDITIONS
)
from .events import check_for_annual_event
from .activities import populate_classmates_if_needed, populate_coworkers_if_needed

SAVE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "save_data.json")

class GameEngine:
    def __init__(self):
        self.graveyard: List[Dict[str, Any]] = []
        self.saved_character: Optional[Character] = None
        self.load_from_disk()

    def save_to_disk(self, char: Optional[Character] = None):
        """Mevcut karakteri ve mezarlığı diske (save_data.json) kaydeder."""
        if char is not None:
            self.saved_character = char
        try:
            payload = {
                "character": self.saved_character.model_dump() if self.saved_character else None,
                "graveyard": self.graveyard
            }
            with open(SAVE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_from_disk(self) -> Optional[Character]:
        """Diskte kayıtlı oyun varsa yükler."""
        if not os.path.exists(SAVE_FILE_PATH):
            return None
        try:
            with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.graveyard = data.get("graveyard", [])
            char_data = data.get("character")
            if char_data:
                self.saved_character = Character(**char_data)
                return self.saved_character
        except Exception:
            pass
        return None

    def create_character(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        gender: Optional[str] = None,
        city: Optional[str] = None
    ) -> Character:
        """Yeni bir hayat ve karakter oluşturur."""
        char_gender = gender if gender in ["Erkek", "Kadın"] else random.choice(["Erkek", "Kadın"])
        
        if not first_name:
            pool = FIRST_NAMES_MALE if char_gender == "Erkek" else FIRST_NAMES_FEMALE
            char_first_name = random.choice(pool)
        else:
            char_first_name = first_name.strip()
            
        char_last_name = last_name.strip() if last_name else random.choice(LAST_NAMES)
        city_info = next((c for c in CITIES if c["city"] == city), None) or random.choice(CITIES)
        
        birth_year = random.randint(1996, 2008)
        
        happiness = random.randint(75, 98)
        health = random.randint(85, 100)
        smarts = random.randint(45, 95)
        looks = random.randint(40, 95)
        
        char = Character(
            id=str(uuid.uuid4())[:8],
            first_name=char_first_name,
            last_name=char_last_name,
            gender=char_gender,
            birth_year=birth_year,
            current_year=birth_year,
            age=0,
            city=city_info["city"],
            country=city_info["country"],
            zodiac=random.choice(ZODIAC_SIGNS),
            happiness=happiness,
            health=health,
            smarts=smarts,
            looks=looks,
            money=0,
            karma=55,
            achievements=["born"]
        )
        
        # Aile Üyelerini Oluştur (Anne ve Baba)
        mother_age = random.randint(23, 36)
        father_age = mother_age + random.randint(-1, 5)
        mother_name = f"{random.choice(FIRST_NAMES_FEMALE)} {char_last_name}"
        father_name = f"{random.choice(FIRST_NAMES_MALE)} {char_last_name}"
        
        char.relationships.append(Person(
            id="person_mother",
            name=mother_name,
            relation="Anne",
            gender="Kadın",
            age=mother_age,
            relationship_level=random.randint(82, 100),
            job=random.choice(PARENT_JOBS),
            money_generosity=random.randint(55, 95),
            personality=random.choice([p["id"] for p in PERSONALITIES]),
            zodiac=random.choice(ZODIAC_SIGNS),
            looks=random.randint(50, 92),
            smarts=random.randint(50, 95),
            loyalty=random.randint(85, 100),
            craziness=random.randint(15, 60),
            wealth=random.randint(40, 88),
            interests=random.sample(INTERESTS_POOL, 3),
            love_language=random.choice(LOVE_LANGUAGES),
            memories=[f"{birth_year}: Seni dünyaya getirdi."]
        ))
        
        char.relationships.append(Person(
            id="person_father",
            name=father_name,
            relation="Baba",
            gender="Erkek",
            age=father_age,
            relationship_level=random.randint(78, 100),
            job=random.choice(PARENT_JOBS),
            money_generosity=random.randint(50, 90),
            personality=random.choice([p["id"] for p in PERSONALITIES]),
            zodiac=random.choice(ZODIAC_SIGNS),
            looks=random.randint(50, 92),
            smarts=random.randint(50, 95),
            loyalty=random.randint(80, 100),
            craziness=random.randint(15, 65),
            wealth=random.randint(45, 90),
            interests=random.sample(INTERESTS_POOL, 3),
            love_language=random.choice(LOVE_LANGUAGES),
            memories=[f"{birth_year}: Doğumunda hastane koridorunda heyecanla bekledi."]
        ))
        
        if random.random() < 0.50:
            sib_gender = random.choice(["Erkek", "Kadın"])
            sib_names = FIRST_NAMES_MALE if sib_gender == "Erkek" else FIRST_NAMES_FEMALE
            sib_age = max(1, random.randint(1, 6))
            char.relationships.append(Person(
                id="person_sibling_1",
                name=f"{random.choice(sib_names)} {char_last_name}",
                relation="Ağabey" if sib_gender == "Erkek" else "Abla",
                gender=sib_gender,
                age=sib_age,
                relationship_level=random.randint(72, 95),
                personality=random.choice([p["id"] for p in PERSONALITIES]),
                zodiac=random.choice(ZODIAC_SIGNS),
                looks=random.randint(45, 92),
                smarts=random.randint(45, 92),
                interests=random.sample(INTERESTS_POOL, 2),
                memories=[f"{birth_year}: Kardeşin olarak seninle büyümeye başladı."]
            ))
            
        for s in INITIAL_STOCKS:
            char.stocks[s["symbol"]] = Stock(
                symbol=s["symbol"],
                name=s["name"],
                shares=0,
                current_price=s["initial_price"],
                history=[s["initial_price"]]
            )
            
        birth_log = (
            f"👶 {city_info['city']}, {city_info['country']} sınırları içinde dünyaya gözlerini açtın. "
            f"Annen: {mother_name} ({char.relationships[0].job}), Baban: {father_name} ({char.relationships[1].job})."
        )
        char.logs.append(LifeLog(
            age=0,
            year=birth_year,
            text=birth_log,
            category="milestone",
            icon="🍼"
        ))
        
        self.save_to_disk(char)
        return char

    def age_up(self, char: Character) -> Dict[str, Any]:
        """Karakteri 1 yıl yaşlandırır ve tüm yıllık döngüyü işler."""
        if not char.is_alive:
            return {"success": False, "message": "Karakter zaten hayatta değil."}
            
        char.age += 1
        char.current_year += 1
        annual_summary_lines = []
        annual_income = 0
        annual_expense = 0
        income_items = []
        expense_items = []

        # 0. Otomatik Eğitim Kademesi Geçişleri
        if char.age == 6:
            char.education_level = "İlkokul"
            char.current_school = f"{char.city} İlkokulu"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"🎒 {char.current_school}'na başladın.", category="school", icon="🎒"))
            populate_classmates_if_needed(char)
        elif char.age == 10:
            for p in char.relationships:
                if p.relation == "Sınıf Arkadaşı":
                    if p.relationship_level >= 65:
                        p.relation = "Arkadaş"
                        p.memories.append("İlkokuldan sonra da bağınızı koparmadınız; artık yakın dostsunuz.")
                    else:
                        p.relation = "Eski Sınıf Arkadaşı"
                elif p.relation == "Öğretmen":
                    p.relation = "Eski Öğretmen"
            char.education_level = "Ortaokul"
            char.current_school = f"{char.city} Ortaokulu"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"📘 İlkokulu bitirip {char.current_school}'na geçtin.", category="school", icon="📘"))
            populate_classmates_if_needed(char)
        elif char.age == 14:
            for p in char.relationships:
                if p.relation == "Sınıf Arkadaşı":
                    if p.relationship_level >= 65:
                        p.relation = "Arkadaş"
                        p.memories.append("Ortaokuldan sonra da bağınızı koparmadınız; artık yakın dostsunuz.")
                    else:
                        p.relation = "Eski Sınıf Arkadaşı"
                elif p.relation == "Öğretmen":
                    p.relation = "Eski Öğretmen"
            char.education_level = "Lise"
            if not char.high_school_type:
                score = min(500, int(260 + char.smarts * 2.2))
                char.lgs_score = score
                if score >= 450:
                    char.high_school_type = "Fen Lisesi (TÜBİTAK Odaklı)"
                    char.current_school = f"{char.city} Fen Lisesi"
                elif score >= 410 and char.money >= 180000:
                    char.high_school_type = "Köklü Yabancı Özel Kolej"
                    char.current_school = f"{char.city} Özel Robert & Fransız Koleji"
                elif score >= 340:
                    char.high_school_type = "Nitelikli Anadolu Lisesi"
                    char.current_school = f"{char.city} Anadolu Lisesi"
                elif score >= 240:
                    char.high_school_type = "Anadolu İmam Hatip Lisesi"
                    char.current_school = f"{char.city} Anadolu İmam Hatip Lisesi"
                else:
                    char.high_school_type = "Mesleki ve Teknik Anadolu Lisesi"
                    char.current_school = f"{char.city} Mesleki ve Teknik Anadolu Lisesi"
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"🏫 LGS'de {score} puan alarak '{char.current_school}'ne kayıt oldun!", category="school", icon="🏫"))
            else:
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"🏫 LGS puanınla '{char.current_school}' bünyesinde lise hayatına başladın!", category="school", icon="🏫"))
            populate_classmates_if_needed(char)
        elif char.age == 18 and char.education_level == "Lise":
            char.current_school = None
            char.school_club = None
            for p in char.relationships:
                if p.relation == "Sınıf Arkadaşı":
                    if p.relationship_level >= 65:
                        p.relation = "Arkadaş"
                        p.memories.append("Liseden mezun olduktan sonra da dostluğunuz devam etti.")
                    else:
                        p.relation = "Eski Sınıf Arkadaşı"
                elif p.relation == "Öğretmen":
                    p.relation = "Eski Öğretmen"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text="🎓 Liseden başarıyla mezun oldun!", category="school", icon="🎓"))

        # Erasmus ve Değişim Programı Tamamlanması
        if char.is_erasmus_active:
            char.smarts = min(100, char.smarts + 14)
            char.looks = min(100, char.looks + 8)
            char.happiness = min(100, char.happiness + 20)
            char.is_erasmus_active = False
            char.logs.append(LifeLog(
                age=char.age,
                year=char.current_year,
                text=f"🇪🇺✈️ ERASMUS YILI TAMAMLANDI! {char.erasmus_country} ülkesindeki 1 yıllık öğrenci değişimi hayatının en güzel yılı oldu! Akıcı yabancı dil ve global vizyon kazandın! (Zeka +14, Görünüş +8)",
                category="school",
                icon="🇪🇺"
            ))

        # Üniversite Mezuniyet Takibi
        if char.school_years_left > 0:
            char.school_years_left -= 1
            if char.school_years_left == 0 and char.current_school:
                grad_school = char.current_school
                char.current_school = None
                char.school_club = None
                char.smarts = min(100, char.smarts + 8)
                if "graduate" not in char.achievements:
                    char.achievements.append("graduate")
                if char.double_major:
                    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"🎓📜 ÇİFT DİPLOMAYLA MEZUN OLDUN! Hem {grad_school} hem de '{char.double_major}' ÇAP programını başarıyla tamamladın!", category="milestone", icon="🎓"))
                for p in char.relationships:
                    if p.relation == "Sınıf Arkadaşı":
                        if p.relationship_level >= 65:
                            p.relation = "Arkadaş"
                            p.memories.append(f"{grad_school} mezuniyetinden sonra da dostluğunuz devam etti.")
                        else:
                            p.relation = "Eski Sınıf Arkadaşı"
                    elif p.relation == "Öğretmen":
                        p.relation = "Eski Öğretmen"
                char.logs.append(LifeLog(
                    age=char.age,
                    year=char.current_year,
                    text=f"🎓 Kep attın! '{grad_school}' eğitimini başarıyla tamamlayıp diplomanı aldın!",
                    category="school",
                    icon="🎓"
                ))

        # 1. Hapishane Kontrolü
        if char.is_in_prison:
            char.prison_years_left -= 1
            char.happiness = max(5, char.happiness - 10)
            char.health = max(10, char.health - 5)
            
            # Koğuş Hiyerarşisi & Tütün Dağıtımı
            if char.prison_role == "👑 Koğuş Ağası":
                char.prison_contraband_cigarettes += 30
                char.stress = max(0, char.stress - 15)
                annual_summary_lines.append("👑 Koğuş Ağası olarak koğuştan yıllık tütün ve çay haracını eksiksiz topladın.")
            else:
                char.prison_reputation = min(100, char.prison_reputation + random.randint(3, 8))
                for r in reversed(PRISON_ROLES):
                    if char.prison_reputation >= r["min_rep"]:
                        char.prison_role = r["role"]
                        break

            if char.prison_years_left <= 0:
                char.is_in_prison = False
                annual_summary_lines.append("🕊️ Tahliye oldun! Cezaevinden çıkıp özgürlüğüne kavuştun!")
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text="Cezanı tamamlayıp tahliye oldun.", category="crime", icon="🕊️"))
            else:
                annual_summary_lines.append(f"🔒 Cezaevinde bir yıl daha geçti. Rolün: {char.prison_role} (Kalan ceza: {char.prison_years_left} yıl).")

        # 2. İş, Yarı Zamanlı İş ve Girişim Gelirleri
        if not char.is_in_prison:
            if char.current_job:
                salary = char.current_job.salary
                char.current_job.experience_years += 1
                # Otomatik yıllık enflasyon/kıdem artışı (%6)
                char.current_job.salary = int(char.current_job.salary * 1.06)
                annual_income += salary
                income_items.append({"label": f"💼 {char.current_job.title} Maaşı", "amount": salary})
                annual_summary_lines.append(f"💼 {char.current_job.title} maaşı: +{salary:,} TL.")
                if char.current_job.category in ["Sanat", "Spor"]:
                    char.fame = min(100, char.fame + 8)
                    if char.fame >= 50 and "famous" not in char.achievements:
                        char.achievements.append("famous")
                
                # Yıllık izin yenileme ve Headhunter şansı
                char.annual_leave_days = 14
                if char.current_job.performance >= 85 and char.current_job.experience_years >= 2:
                    if random.random() < 0.35:
                        char.has_headhunter_offer = True

            # Moonlighting / Gizli Ek İş Geliri
            if char.moonlighting_income > 0:
                annual_income += char.moonlighting_income
                income_items.append({"label": f"🌙 Ek İş / Danışmanlık ({char.moonlighting_job})", "amount": char.moonlighting_income})
                annual_summary_lines.append(f"🌙 Ek iş geliri: +{char.moonlighting_income:,} TL.")
                if random.random() < 0.05 and char.current_job:
                    char.stress = min(100, char.stress + 18)
                    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"⚠️🤫 Şirket yönetimi mesai sonrası gizlice danışmanlık yaptığını duydu! Patronun seni odasına çağırıp uyardı: 'İşine odaklan!'", category="career", icon="⚠️"))

            if char.political_office:
                pol_sal = char.political_salary
                annual_income += pol_sal
                income_items.append({"label": f"🏛️ {char.political_office} Ödeneği", "amount": pol_sal})
                char.approval_rating = max(5, min(100, char.approval_rating + random.randint(-6, 5)))
                if char.approval_rating < 22:
                    lost_off = char.political_office
                    char.political_office = None
                    char.political_salary = 0
                    annual_summary_lines.append(f"🗳️ Halk desteğin çok düştüğü için '{lost_off}' makamını kaybettin.")
                else:
                    annual_summary_lines.append(f"🏛️ {char.political_office} makam ödeneği: +{pol_sal:,} TL (Halk Desteği: %{char.approval_rating}).")
                
            if char.part_time_job:
                pt_sal = char.part_time_job.salary
                annual_income += pt_sal
                income_items.append({"label": f"⏱️ {char.part_time_job.title} Ek Geliri", "amount": pt_sal})
                annual_summary_lines.append(f"⏱️ {char.part_time_job.title} ek geliri: +{pt_sal:,} TL.")

            if char.business:
                char.business.years_active += 1
                if char.business.is_traditional_shop:
                    b = char.business
                    fluct = random.uniform(0.88, 1.25)
                    calc_profit = int((b.annual_profit + (b.apprentice_skill * 1200) + (b.courier_fleet * 95000)) * fluct)
                    if b.secret_recipe:
                        calc_profit = int(calc_profit * 1.25)
                    b.valuation = max(50000, int(b.valuation * random.uniform(1.02, 1.15)))
                    annual_income += calc_profit
                    income_items.append({"label": f"🥙 '{b.name}' Esnaf Hasılatı", "amount": calc_profit})
                    annual_summary_lines.append(f"🥙 '{b.name}' yıllık esnaf hasılatı: +{calc_profit:,} TL.")
                else:
                    # Gerçek Hayat Zorluğu: Ekonomik dalgalanma veya durgunluk riski
                    fluct = random.uniform(-0.15, 1.15)
                    profit = int(char.business.annual_profit * fluct)
                    char.business.valuation = max(50000, int(char.business.valuation * random.uniform(0.95, 1.16)))
                    if profit >= 0:
                        annual_income += profit
                        income_items.append({"label": f"🏢 '{char.business.name}' Şirket Kârı", "amount": profit})
                        annual_summary_lines.append(f"🏢 '{char.business.name}' yıllık şirket kârı: +{profit:,} TL.")
                    else:
                        loss_amt = abs(profit)
                        annual_expense += loss_amt
                        expense_items.append({"label": f"📉 '{char.business.name}' Şirket Zararı", "amount": loss_amt})
                        annual_summary_lines.append(f"📉 '{char.business.name}' ekonomik durgunluk nedeniyle {loss_amt:,} TL zarar etti!")

            if char.band and char.band.annual_royalties > 0:
                roy = char.band.annual_royalties
                annual_income += roy
                income_items.append({"label": f"🎸 '{char.band.name}' Telif & Konser", "amount": roy})
                annual_summary_lines.append(f"🎸 '{char.band.name}' telif ve konser geliri: +{roy:,} TL.")

            if char.sports_career and char.sports_career.salary > 0:
                sp_sal = char.sports_career.salary
                annual_income += sp_sal
                income_items.append({"label": f"⚽ '{char.sports_career.team_name}' Spor Maaşı", "amount": sp_sal})
                annual_summary_lines.append(f"⚽ '{char.sports_career.team_name}' spor kariyeri geliri: +{sp_sal:,} TL.")

            for p in char.relationships:
                if p.is_alive and p.joint_venture_profit > 0 and p.relation in ["Sevgili", "Nişanlı", "Eş"]:
                    annual_income += p.joint_venture_profit
                    income_items.append({"label": f"🏪 Ortak Girişim ({p.joint_venture_name})", "amount": p.joint_venture_profit})
                    annual_summary_lines.append(f"🏪 {p.name} ile ortak girişim ('{p.joint_venture_name}') geliri: +{p.joint_venture_profit:,} TL.")

        # 3. Mülk Kira Gelirleri ve Bakım Masrafları
        total_asset_income = sum(a.annual_income for a in char.assets)
        total_asset_cost = sum(a.annual_cost for a in char.assets)
        if total_asset_income > 0:
            annual_income += total_asset_income
            income_items.append({"label": "🏠 Mülk Kira Gelirleri", "amount": total_asset_income})
            annual_summary_lines.append(f"🏠 Kira gelirleri: +{total_asset_income:,} TL.")
        if total_asset_cost > 0:
            annual_expense += total_asset_cost
            expense_items.append({"label": "🛠️ Gayrimenkul & Araç Bakım Masrafları", "amount": total_asset_cost})

        # 4. Sosyal Medya Reklam Gelirleri
        for sm in char.social_media.values():
            if sm.followers >= 25000:
                ad_money = int((sm.followers / 1000) * 1400)
                sm.earnings_annual = ad_money
                annual_income += ad_money
                income_items.append({"label": f"📱 {sm.platform} Sponsorluk", "amount": ad_money})
                annual_summary_lines.append(f"📱 {sm.platform} sponsorluk geliri: +{ad_money:,} TL.")

        # 5. Burs Gelirleri, Gerçekçi Vergi Dilimi, Kira, Çocuk Masrafı, Nafaka ve Yaşam Gideri
        if char.scholarship_annual > 0 and (char.current_school or char.age <= 24):
            annual_income += char.scholarship_annual
            income_items.append({"label": "🎓 YKS / KYK Başarı Bursu", "amount": char.scholarship_annual})
            annual_summary_lines.append(f"🎓 YKS Başarı / KYK Bursu: +{char.scholarship_annual:,} TL.")

        if char.age >= 18 and not char.is_in_prison and not char.current_school:
            cohab_partner = next((p for p in char.relationships if (p.cohabiting or p.relation == "Eş") and p.is_alive), None)
            owns_home = any(a.asset_type == "Ev" for a in char.assets)
            if "KYK" in char.housing_type:
                living_cost = 42000
            elif owns_home:
                living_cost = 95000
            elif cohab_partner:
                living_cost = 135000
            else:
                living_cost = 185000  # Büyükşehir ev kirası + faturalar + mutfak enflasyonu
            annual_expense += living_cost
            expense_items.append({"label": "🛒 Yıllık Yaşam, Fatura & Mutfak Gideri", "amount": living_cost})
            annual_summary_lines.append(f"🛒 Yıllık yaşam, fatura ve mutfak giderleri: -{living_cost:,} TL.")

            # Çocuk Büyütme & Okul Masrafları (Gerçek Hayat Zorluğu)
            young_children = [p for p in char.relationships if p.is_alive and p.relation == "Çocuk" and p.age < 22]
            if young_children:
                child_cost = len(young_children) * 55000
                annual_expense += child_cost
                expense_items.append({"label": f"👶 {len(young_children)} Çocuk Okul & Bakım", "amount": child_cost})
                annual_summary_lines.append(f"👶 {len(young_children)} çocuğun okul ve bakım masrafı: -{child_cost:,} TL.")

            if cohab_partner and cohab_partner.wealth >= 40:
                partner_contrib = int(cohab_partner.wealth * 1100)
                annual_income += partner_contrib
                income_items.append({"label": f"💑 {cohab_partner.name} Ev Katkısı", "amount": partner_contrib})
                annual_summary_lines.append(f"💑 {cohab_partner.name} ortak ev bütçesine +{partner_contrib:,} TL katkıda bulundu.")

        # 5a. Boşanma Nafakası Gideri
        if char.alimony_annual > 0 and not char.is_in_prison:
            annual_expense += char.alimony_annual
            expense_items.append({"label": "⚖️ Eski Eşe Mahkeme Nafakası", "amount": char.alimony_annual})
            annual_summary_lines.append(f"⚖️ Eski eşe ödenen yıllık mahkeme nafakası: -{char.alimony_annual:,} TL.")

        # Huzurevi ve Yaşlı Bakıcı Giderleri
        if char.nursing_home:
            nh_cost = 48000 if "Devlet" in char.nursing_home else 320000
            annual_expense += nh_cost
            expense_items.append({"label": f"🏡 {char.nursing_home} Aidatı", "amount": nh_cost})
            char.happiness = min(100, char.happiness + 20)
            char.stress = max(0, char.stress - 25)

        if char.elderly_caregiver:
            cg_cost = 45000
            annual_expense += cg_cost
            expense_items.append({"label": "👵 Yatılı Hasta Bakıcı Maaşı", "amount": cg_cost})
            char.health = max(55, char.health)

        # 5b. Artan Oranlı Gelir Vergisi, SGK & Servet Vergisi (Gerçek Hayat Zorluğu)
        tax_paid = 0
        if annual_income > 180000:
            if annual_income <= 650000:
                tax_paid = int((annual_income - 180000) * 0.18)
            elif annual_income <= 2500000:
                tax_paid = int(84600 + (annual_income - 650000) * 0.27)
            else:
                tax_paid = int(584100 + (annual_income - 2500000) * 0.35)
        assets_total_for_tax = sum(a.current_value for a in char.assets)
        if assets_total_for_tax > 5000000:
            tax_paid += int((assets_total_for_tax - 5000000) * 0.015)
        char.last_tax_paid = tax_paid
        if tax_paid > 0:
            annual_expense += tax_paid
            expense_items.append({"label": "🏛️ Gelir Vergisi, SGK & Emlak/MTV", "amount": tax_paid})
            annual_summary_lines.append(f"🏛️ Gelir Vergisi, SGK & Emlak/MTV kesintisi: -{tax_paid:,} TL.")

        # 5c. Banka Kredisi Taksidi & Offshore Faiz Getirisi
        if char.offshore_balance > 0:
            off_gain = int(char.offshore_balance * 0.08)
            char.offshore_balance += off_gain
            income_items.append({"label": "🇨🇭 İsviçre Offshore Döviz Getirisi", "amount": off_gain})
            annual_summary_lines.append(f"🇨🇭 Offshore döviz getirisi: +{off_gain:,} TL.")

        if char.debt > 0:
            installment = min(char.debt, max(35000, int(char.debt * 0.18)))
            if char.money >= installment:
                char.money -= installment
                char.debt -= installment
                annual_expense += installment
                expense_items.append({"label": "🏦 Banka Kredi Taksidi", "amount": installment})
                annual_summary_lines.append(f"🏦 Banka kredi taksidi ödendi: -{installment:,} TL (Kalan Borç: {char.debt:,} TL).")
            else:
                char.debt = int(char.debt * 1.18)
                char.happiness = max(5, char.happiness - 12)
                annual_summary_lines.append("⚠️ Banka kredi taksidini ödeyemedin, %18 gecikme faizi işledi!")

        char.annual_income_last = annual_income
        char.annual_expense_last = annual_expense
        char.money += (annual_income - annual_expense)

        char.last_annual_summary = {
            "year": char.current_year,
            "age": char.age,
            "total_income": annual_income,
            "total_expense": annual_expense,
            "net": annual_income - annual_expense,
            "incomes": income_items,
            "expenses": expense_items
        }

        if char.money < 0:
            char.happiness = max(5, char.happiness - 12)
            annual_summary_lines.append("⚠️ Giderlerin gelirini aştı, bakiyen eksiye düştü!")

        # 6. Mülk Değerleme, Koleksiyon, Kiracı Olayları & Araç Amortismanı
        for a in char.assets:
            if a.asset_type == "Ev":
                appreciation = random.uniform(0.04, 0.12)
                a.current_value = int(a.current_value * (1 + appreciation))
                # Kiracı krizi kontrolü
                if a.is_rented_out and not a.tenant_issue and random.random() < 0.22:
                    a.tenant_issue = random.choice([
                        "Gecikmiş Kira (2 Aydır Ödenmedi)",
                        "Komşulardan Gece Gürültüsü Şikayeti",
                        "Banyo & Tesisat Acil Onarım Talebi"
                    ])
                    a.tenant_reliability = max(30, a.tenant_reliability - 18)
                    annual_summary_lines.append(f"🏠 '{a.name}' kiracın {a.tenant_name}: {a.tenant_issue}!")
            elif a.asset_type == "Koleksiyon":
                appreciation = random.uniform(0.08, 0.18)
                a.current_value = int(a.current_value * (1 + appreciation))
            elif a.asset_type == "Araba":
                depreciation = random.uniform(0.07, 0.13)
                a.current_value = max(15000, int(a.current_value * (1 - depreciation)))
                if random.random() < 0.15:
                    if a.has_insurance:
                        annual_summary_lines.append(f"🛡️ '{a.name}' aracında ufak bir hasar oluştu ancak Kasko şirketi tüm masrafı karşıladı!")
                    else:
                        rep = random.randint(12000, 35000)
                        a.condition = max(30, a.condition - 15)
                        char.money -= rep
                        annual_summary_lines.append(f"🔧 '{a.name}' aracın arızalandı, kaskon olmadığı için {rep:,} TL masraf çıktı!")

        # 7. Borsa, Kripto Fiyat Dalgalanmaları & Temettü Gelirleri
        total_dividends = 0
        for s in char.stocks.values():
            s_spec = next((item for item in INITIAL_STOCKS if item["symbol"] == s.symbol), None)
            vol = s_spec["volatility"] if s_spec else 0.15
            div_rate = s_spec.get("dividend", 0.0) if s_spec else 0.0
            
            change = random.uniform(-vol * 1.02, vol * 1.04)
            s.current_price = max(1.0, round(s.current_price * (1 + change), 2))
            s.history.append(s.current_price)
            if len(s.history) > 15:
                s.history.pop(0)
            
            if div_rate > 0 and s.shares > 0:
                div_payout = int(s.shares * s.current_price * div_rate)
                total_dividends += div_payout

        if total_dividends > 0:
            char.money += total_dividends
            char.logs.append(LifeLog(
                age=char.age,
                year=char.current_year,
                text=f"📈💰 TEMETTÜ DAĞITIMI: Borsa hisse portföyünden hesabına +{total_dividends:,} TL nakit kâr payı yattı!",
                category="finance",
                icon="💰"
            ))

        # Kripto Staking Faiz Getirisi
        if hasattr(char, "crypto_staked") and char.crypto_staked:
            total_staked_yield = 0
            for c_sym, s_val in list(char.crypto_staked.items()):
                if s_val > 0:
                    y_gain = int(s_val * 0.12)
                    total_staked_yield += y_gain
                    char.crypto_staked[c_sym] += y_gain
            if total_staked_yield > 0:
                char.money += total_staked_yield
                char.logs.append(LifeLog(
                    age=char.age,
                    year=char.current_year,
                    text=f"🪙 STAKING GELİRİ: Kilitli kripto cüzdanından +{total_staked_yield:,} TL DeFi faizi hesabına aktarıldı!",
                    category="finance",
                    icon="🪙"
                ))

        # Yeraltı Dünyası & Mekan Koruma Haracı Geliri
        if hasattr(char, "syndicate_racket_annual") and char.syndicate_racket_annual > 0:
            char.money += char.syndicate_racket_annual
            char.logs.append(LifeLog(
                age=char.age,
                year=char.current_year,
                text=f"💼🔫 YERALTI HARACI: Kontrolündeki mekanlardan yıllık +{char.syndicate_racket_annual:,} TL koruma haracı kasaya girdi!",
                category="crime",
                icon="💼"
            ))

        # Net Servet Hesaplama & Zaman Serisi Kaydı
        assets_val = sum(a.current_value for a in char.assets)
        stocks_val = sum(int(s.shares * s.current_price) for s in char.stocks.values())
        biz_val = char.business.valuation if char.business else 0
        club_val = char.sports_career.club_valuation if (char.sports_career and char.sports_career.owns_club) else 0
        char.net_worth = char.money + char.offshore_balance - char.debt + assets_val + stocks_val + biz_val + club_val
        char.wealth_history.append(char.net_worth)
        char.happiness_history.append(char.happiness)
        if len(char.wealth_history) > 40:
            char.wealth_history = char.wealth_history[-40:]
        if len(char.happiness_history) > 40:
            char.happiness_history = char.happiness_history[-40:]

        # Başarım Kontrolleri
        if char.net_worth >= 1000000 and "millionaire" not in char.achievements:
            char.achievements.append("millionaire")
            annual_summary_lines.append("🏆 BAŞARIM: Milyoner Kulübü! Net servetin 1 Milyon TL'yi aştı!")
        if char.net_worth >= 20000000 and "multimillionaire" not in char.achievements:
            char.achievements.append("multimillionaire")
            annual_summary_lines.append("🏆 BAŞARIM: Zenginler Listesi! Net servetin 20 Milyon TL'yi aştı!")
        if char.net_worth >= 100000000 and "billionaire" not in char.achievements:
            char.achievements.append("billionaire")
            annual_summary_lines.append("🏆 BAŞARIM: İmparator! Net servetin 100 Milyon TL'yi aştı!")
        if char.age >= 100 and "centenarian" not in char.achievements:
            char.achievements.append("centenarian")
            annual_summary_lines.append("🏆 BAŞARIM: Asırlık Çınar! 100 Yaşına ulaştın!")

        # 8. İlişkiler Yaşlandırma, İlişki Soğuması (Gerçek Hayat Zorluğu) ve Vefat Kontrolü
        for person in char.relationships:
            if person.is_alive:
                person.age += 1
                if person.relation in ["Flört", "Sevgili", "Nişanlı", "Eş"]:
                    person.years_together += 1
                    # İlişkiler emek ister: Yıllık doğal ilişki soğuması
                    person.relationship_level = max(5, person.relationship_level - 5)
                    if char.money < 0 and person.personality == "Materyalist":
                        person.relationship_level = max(5, person.relationship_level - 12)
                        annual_summary_lines.append(f"💔 {person.name} maddi sıkıntılardan şikayet ederek soğuk davranmaya başladı! (İlişki -12)")
                    if person.years_together in [5, 10, 25, 50]:
                        person.memories.append(f"{char.current_year}: Birlikte {person.years_together}. yılınızı kutladınız!")
                        char.happiness = min(100, char.happiness + 8)
                        annual_summary_lines.append(f"💖 {person.name} ile birlikteliğinizin {person.years_together}. yıl dönümü!")
                else:
                    person.relationship_level = max(10, person.relationship_level - 2)
                if person.relation == "Çocuk" and person.age == 6 and not person.interests:
                    person.interests = random.sample(INTERESTS_POOL, 2)
                if person.age > 72:
                    death_chance = (person.age - 70) * 0.035
                    if random.random() < death_chance:
                        person.is_alive = False
                        char.happiness = max(0, char.happiness - 30)
                        if person.relation in ["Anne", "Baba", "Eş"]:
                            inheritance = random.randint(150000, 950000)
                            char.money += inheritance
                            msg = f"🕊️ Başın sağ olsun: {person.relation} {person.name} ({person.age} yaşında) vefat etti ve sana {inheritance:,} TL miras bıraktı."
                        else:
                            msg = f"🕊️ {person.relation} {person.name} ({person.age} yaşında) hayata veda etti."
                        annual_summary_lines.append(msg)
                        char.logs.append(LifeLog(age=char.age, year=char.current_year, text=msg, category="milestone", icon="🕊️"))

        # 8b. İş Stresi & Tükenmişlik Sendromu (Gerçek Hayat Zorluğu)
        # Yaşa Bağlı Kronik Rahatsızlıklar
        if char.age >= 45 and not char.is_in_prison and random.random() < 0.16:
            if len(char.chronic_conditions) < 3:
                av = [c for c in CHRONIC_CONDITIONS if c["name"] not in char.chronic_conditions]
                if av:
                    picked_c = random.choice(av)
                    char.chronic_conditions.append(picked_c["name"])
                    char.health = max(10, char.health - picked_c["health_penalty"])
                    char.stress = min(100, char.stress + picked_c["stress_impact"])
                    char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"🩺😣 Yaşa Bağlı Rahatsızlık: '{picked_c['name']}' teşhisi konuldu! {picked_c['desc']}", category="health", icon="🩺"))

        if char.current_job and not char.is_in_prison:
            char.stress = min(100, char.stress + 6)
            char.current_job.performance = max(20, char.current_job.performance - 4)
            if char.stress >= 88:
                char.health = max(5, char.health - 10)
                char.happiness = max(5, char.happiness - 14)
                annual_summary_lines.append("🥵 Yoğun iş stresinden 'Tükenmişlik Sendromu' yaşıyorsun! Tatil veya terapi şart! (Sağlık -10, Mutluluk -14)")

        # 9. Evcil Hayvan Yaşlanması
        for pet in char.pets:
            if pet.is_alive:
                pet.age += 1
                if pet.age > 14 and random.random() < 0.25:
                    pet.is_alive = False
                    char.happiness = max(0, char.happiness - 18)
                    annual_summary_lines.append(f"🐾 Sadık dostun {pet.name} yaşlılık nedeniyle hayata gözlerini yumdu.")

        # 10. Sağlık Değişimi & Hastalıklar
        if char.age > 55:
            decay = int((char.age - 52) * 0.35)
            char.health = max(5, char.health - decay)
            
        for ill_name in char.illnesses:
            ill_spec = next((i for i in ILLNESSES if i["name"] == ill_name), None)
            if ill_spec:
                char.health = max(5, char.health - ill_spec["health_drain"])
                char.happiness = max(0, char.happiness - ill_spec["happiness_drain"])

        if random.random() < 0.16 and len(char.illnesses) < 2:
            new_ill = random.choice(ILLNESSES)
            if new_ill["name"] not in char.illnesses:
                char.illnesses.append(new_ill["name"])
                annual_summary_lines.append(f"🤒 Sana '{new_ill['name']}' teşhisi kondu! Doktora görünmelisin.")
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"'{new_ill['name']}' rahatsızlığı başladı.", category="health", icon="🤒"))

        # 11. Ölüm Kontrolü
        is_dead, death_reason = self._check_death(char)
        if is_dead:
            char.is_alive = False
            char.death_reason = death_reason
            self._handle_character_death(char)
            self.save_to_disk(char)
            return {
                "success": True,
                "character_died": True,
                "death_reason": death_reason,
                "summary": annual_summary_lines
            }

        # 12. Olay Günlüğüne Ekleme
        summary_log = f"{char.age} Yaşına bastın."
        if annual_summary_lines:
            summary_log += " " + " | ".join(annual_summary_lines[:3])
            
        char.logs.append(LifeLog(
            age=char.age,
            year=char.current_year,
            text=summary_log,
            category="general",
            icon="🎂"
        ))

        # 13. Yeni Dönüm Noktası veya Olay Seçimi
        event = check_for_annual_event(char)
        char.active_event = event
        self.save_to_disk(char)

        return {
            "success": True,
            "character_died": False,
            "has_event": event is not None,
            "event": event.model_dump() if event else None,
            "summary": annual_summary_lines
        }

    def _check_death(self, char: Character) -> tuple[bool, Optional[str]]:
        if char.health <= 0:
            return True, "Tedavi edilmeyen ağır sağlık sorunları nedeniyle vefat etti."
            
        if char.age > 76:
            base_risk = (char.age - 75) * 0.038
            health_factor = (100 - char.health) / 100
            total_prob = base_risk + (health_factor * 0.14)
            if random.random() < total_prob:
                reasons = [
                    "Uykusunda huzur içinde kalp durması nedeniyle vefat etti.",
                    "İlerlemiş yaşa bağlı doğal nedenlerle sevdiklerinin yanında hayata veda etti.",
                    "Ani bir kalp krizi sonucunda tüm müdahalelere rağmen kurtarılamadı."
                ]
                return True, random.choice(reasons)
                
        return False, None

    def _handle_character_death(self, char: Character):
        if char.net_worth >= 50000000:
            title = "Efsanevi Milyarder & İş İmparatoru"
        elif char.business:
            title = "Vizyoner Girişimci & Şirket Kurucusu"
        elif "bank_robbery" in char.criminal_record or char.is_in_prison:
            title = "Yeraltı Dünyasının Korku Salan İsmi"
        elif char.current_job and char.current_job.category == "Tıp":
            title = "Hayat Kurtaran Şifalı Hekim"
        elif char.current_job and char.current_job.category == "Teknoloji":
            title = "Teknoloji Dehası & Yazılım Mimarı"
        elif char.age >= 90:
            title = "Asırlık Bilge & Aile Çınarı"
        elif char.happiness >= 85:
            title = "Daima Güler Yüzlü & Sevgi Dolu İnsan"
        else:
            title = "Onurlu ve Saygın Bir Vatandaş"
            
        char.tombstone_title = title
        
        tombstone_entry = {
            "id": char.id,
            "name": f"{char.first_name} {char.last_name}",
            "gender": char.gender,
            "generation": char.generation,
            "birth_year": char.birth_year,
            "death_year": char.current_year,
            "age": char.age,
            "city": char.city,
            "country": char.country,
            "net_worth": char.net_worth,
            "death_reason": char.death_reason,
            "title": title,
            "achievements_count": len(char.achievements),
            "children_count": len([p for p in char.relationships if p.relation == "Çocuk"])
        }
        self.graveyard.insert(0, tombstone_entry)

    def reincarnate_as_child(self, parent_char: Character, child_id: Optional[str] = None) -> Optional[Character]:
        children = [p for p in parent_char.relationships if p.relation == "Çocuk" and p.is_alive and not getattr(p, "is_disowned", False)]
        if not children:
            return None
            
        chosen_child = children[0]
        if child_id:
            match = next((c for c in children if c.id == child_id), None)
            if match:
                chosen_child = match
        elif parent_char.will_beneficiary and parent_char.will_beneficiary.startswith("child_"):
            target_id = parent_char.will_beneficiary.replace("child_", "")
            match = next((c for c in children if c.id == target_id), None)
            if match:
                chosen_child = match

        # Vasiyetnameye göre miras aktarımı
        inherited_money = max(0, parent_char.net_worth)
        if parent_char.will_beneficiary == "charity":
            inherited_money = 0
        elif parent_char.will_beneficiary == "spouse":
            inherited_money = int(inherited_money * 0.25)
        elif parent_char.will_beneficiary == "all_children" and len(children) > 1:
            inherited_money = int(inherited_money / len(children))
        elif parent_char.will_beneficiary and parent_char.will_beneficiary.startswith("child_"):
            target_id = parent_char.will_beneficiary.replace("child_", "")
            if chosen_child.id != target_id:
                inherited_money = int(inherited_money * 0.10)

        child_char = Character(
            id=str(uuid.uuid4())[:8],
            first_name=chosen_child.name.split()[0],
            last_name=parent_char.last_name,
            gender=chosen_child.gender,
            birth_year=parent_char.current_year - chosen_child.age,
            current_year=parent_char.current_year,
            age=chosen_child.age,
            city=parent_char.city,
            country=parent_char.country,
            zodiac=random.choice(ZODIAC_SIGNS),
            generation=parent_char.generation + 1,
            happiness=80,
            health=95,
            smarts=getattr(chosen_child, "smarts", random.randint(55, 95)),
            looks=getattr(chosen_child, "looks", random.randint(50, 95)),
            money=inherited_money,
            net_worth=inherited_money,
            education_level="Üniversite" if chosen_child.age >= 22 else ("Lise" if chosen_child.age >= 18 else "İlkokul"),
            achievements=["born"]
        )

        if parent_char.business and inherited_money > 0:
            child_char.business = parent_char.business
            child_char.logs.append(LifeLog(
                age=child_char.age,
                year=child_char.current_year,
                text=f"🏢 Aile şirketi '{parent_char.business.name}' ({parent_char.business.sector}) yönetimini devraldın!",
                category="career",
                icon="🏢"
            ))

        for a in parent_char.assets:
            if a.asset_type in ["Ev", "Yat"]:
                child_char.assets.append(a)
        
        for s in INITIAL_STOCKS:
            child_char.stocks[s["symbol"]] = Stock(
                symbol=s["symbol"],
                name=s["name"],
                shares=0,
                current_price=s["initial_price"],
                history=[s["initial_price"]]
            )

        child_char.logs.append(LifeLog(
            age=child_char.age,
            year=child_char.current_year,
            text=f"👑 {parent_char.generation}. Kuşak {parent_char.first_name} {parent_char.last_name}'ın vefatının ardından {child_char.generation}. Kuşak olarak aile mirasını ({inherited_money:,} TL) devraldın!",
            category="milestone",
            icon="👑"
        ))
        
        self.save_to_disk(child_char)
        return child_char
