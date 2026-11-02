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
    PERSONALITIES, INTERESTS_POOL
)
from .events import check_for_annual_event

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

        # 0. Otomatik Eğitim Kademesi Geçişleri
        if char.age == 6:
            char.education_level = "İlkokul"
            char.current_school = f"{char.city} İlkokulu"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"🎒 {char.current_school}'na başladın.", category="school", icon="🎒"))
        elif char.age == 10:
            char.education_level = "Ortaokul"
            char.current_school = f"{char.city} Ortaokulu"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"📘 İlkokulu bitirip {char.current_school}'na geçtin.", category="school", icon="📘"))
        elif char.age == 14:
            char.education_level = "Lise"
            char.current_school = f"{char.city} Anadolu Lisesi"
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text=f"🏫 {char.current_school}'ne kayıt oldun!", category="school", icon="🏫"))
        elif char.age == 18 and char.education_level == "Lise":
            char.current_school = None
            char.school_club = None
            char.logs.append(LifeLog(age=char.age, year=char.current_year, text="🎓 Liseden başarıyla mezun oldun!", category="school", icon="🎓"))

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
            if char.prison_years_left <= 0:
                char.is_in_prison = False
                annual_summary_lines.append("🕊️ Tahliye oldun! Cezaevinden çıkıp özgürlüğüne kavuştun!")
                char.logs.append(LifeLog(age=char.age, year=char.current_year, text="Cezanı tamamlayıp tahliye oldun.", category="crime", icon="🕊️"))
            else:
                annual_summary_lines.append(f"🔒 Cezaevinde bir yıl daha geçti. Kalan ceza: {char.prison_years_left} yıl.")

        # 2. İş, Yarı Zamanlı İş ve Girişim Gelirleri
        if not char.is_in_prison:
            if char.current_job:
                salary = char.current_job.salary
                char.current_job.experience_years += 1
                # Otomatik yıllık enflasyon/kıdem artışı (%6)
                char.current_job.salary = int(char.current_job.salary * 1.06)
                annual_income += salary
                annual_summary_lines.append(f"💼 {char.current_job.title} maaşı: +{salary:,} TL.")
                
            if char.part_time_job:
                pt_sal = char.part_time_job.salary
                annual_income += pt_sal
                annual_summary_lines.append(f"⏱️ {char.part_time_job.title} ek geliri: +{pt_sal:,} TL.")

            if char.business:
                char.business.years_active += 1
                fluct = random.uniform(0.90, 1.22)
                profit = int(char.business.annual_profit * fluct)
                char.business.valuation = int(char.business.valuation * random.uniform(1.05, 1.18))
                annual_income += profit
                annual_summary_lines.append(f"🏢 '{char.business.name}' yıllık şirket kârı: +{profit:,} TL.")

        # 3. Mülk Kira Gelirleri ve Bakım Masrafları
        total_asset_income = sum(a.annual_income for a in char.assets)
        total_asset_cost = sum(a.annual_cost for a in char.assets)
        if total_asset_income > 0:
            annual_income += total_asset_income
            annual_summary_lines.append(f"🏠 Kira gelirleri: +{total_asset_income:,} TL.")
        if total_asset_cost > 0:
            annual_expense += total_asset_cost

        # 4. Sosyal Medya Reklam Gelirleri
        for sm in char.social_media.values():
            if sm.followers >= 25000:
                ad_money = int((sm.followers / 1000) * 1400)
                sm.earnings_annual = ad_money
                annual_income += ad_money
                annual_summary_lines.append(f"📱 {sm.platform} sponsorluk geliri: +{ad_money:,} TL.")

        # 5. Temel Yaşam Gideri (18+ Yaş)
        if char.age >= 18 and not char.is_in_prison and not char.current_school:
            is_cohabiting = any(p.cohabiting and p.is_alive for p in char.relationships)
            living_cost = 65000 if is_cohabiting else 120000
            annual_expense += living_cost

        char.annual_income_last = annual_income
        char.annual_expense_last = annual_expense
        char.money += (annual_income - annual_expense)

        if char.money < 0:
            char.happiness = max(5, char.happiness - 10)
            annual_summary_lines.append("⚠️ Giderlerin gelirini aştı, bakiyen eksiye düştü!")

        # 6. Mülk Değerleme & Araç Amortismanı
        for a in char.assets:
            if a.asset_type == "Ev":
                appreciation = random.uniform(0.05, 0.14)
                a.current_value = int(a.current_value * (1 + appreciation))
            elif a.asset_type == "Araba":
                depreciation = random.uniform(0.05, 0.10)
                a.current_value = max(15000, int(a.current_value * (1 - depreciation)))

        # 7. Borsa & Kripto Fiyat Dalgalanmaları
        for s in char.stocks.values():
            vol = next((item["volatility"] for item in INITIAL_STOCKS if item["symbol"] == s.symbol), 0.15)
            change = random.uniform(-vol * 0.85, vol * 1.15)
            s.current_price = max(1.0, round(s.current_price * (1 + change), 2))
            s.history.append(s.current_price)
            if len(s.history) > 15:
                s.history.pop(0)

        # Net Servet Hesaplama
        assets_val = sum(a.current_value for a in char.assets)
        stocks_val = sum(int(s.shares * s.current_price) for s in char.stocks.values())
        biz_val = char.business.valuation if char.business else 0
        char.net_worth = char.money + assets_val + stocks_val + biz_val

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

        # 8. İlişkiler Yaşlandırma ve Vefat Kontrolü
        for person in char.relationships:
            if person.is_alive:
                person.age += 1
                if person.relation in ["Flört", "Sevgili", "Nişanlı", "Eş"]:
                    person.years_together += 1
                    if person.years_together in [5, 10, 25, 50]:
                        person.memories.append(f"{char.current_year}: Birlikte {person.years_together}. yılınızı kutladınız!")
                        char.happiness = min(100, char.happiness + 8)
                        annual_summary_lines.append(f"💖 {person.name} ile birlikteliğinizin {person.years_together}. yıl dönümü!")
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

    def reincarnate_as_child(self, parent_char: Character) -> Optional[Character]:
        children = [p for p in parent_char.relationships if p.relation == "Çocuk" and p.is_alive]
        if not children:
            return None
            
        chosen_child = children[0]
        # Vasiyetnameye göre miras aktarımı
        inherited_money = max(0, parent_char.net_worth)
        if parent_char.will_beneficiary == "charity":
            inherited_money = 0
        elif parent_char.will_beneficiary == "all_children" and len(children) > 1:
            inherited_money = int(inherited_money / len(children))

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
            smarts=random.randint(55, 95),
            looks=random.randint(50, 95),
            money=inherited_money,
            net_worth=inherited_money,
            education_level="Üniversite" if chosen_child.age >= 22 else ("Lise" if chosen_child.age >= 18 else "İlkokul"),
            achievements=["born"]
        )
        
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
