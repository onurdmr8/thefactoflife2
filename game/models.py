# -*- coding: utf-8 -*-
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Person(BaseModel):
    id: str
    name: str
    relation: str  # Anne, Baba, Ağabey, Abla, Kardeş, Flört, Sevgili, Nişanlı, Eş, Eski Sevgili, Eski Eş, Çocuk, Arkadaş
    gender: str  # Erkek, Kadın
    age: int
    relationship_level: int = 80  # 0 - 100
    is_alive: bool = True
    job: Optional[str] = None
    money_generosity: int = 50  # 0 - 100
    
    # Detaylı İlişki ve Karakter Özellikleri
    personality: str = "Uyumlu"  # Romantik, Kıskanç, Eğlenceli, Hırslı, Sadık, Materyalist, Entelektüel, Maceracı
    zodiac: str = "Koç ♈"
    looks: int = 70      # 0 - 100
    smarts: int = 65     # 0 - 100
    craziness: int = 25  # 0 - 100 (Çılgınlık / Kıskançlık)
    loyalty: int = 80    # 0 - 100 (Sadakat)
    wealth: int = 50     # 0 - 100 (Maddi Durum)
    interests: List[str] = Field(default_factory=list)
    bio: str = ""
    love_language: str = "Kaliteli Zaman"  # Hediye Alma, Kaliteli Zaman, Tatlı Sözler, Sürprizler & Jestler, Güven & Sadakat
    family_approval: int = 65  # 0 - 100 (Ailenin bu partnere onayı)
    met_family: bool = False
    cohabiting: bool = False
    has_prenup: bool = False
    years_together: int = 0
    is_blocked: bool = False
    kiz_isteme_done: bool = False
    nisan_bohca_done: bool = False
    joint_venture_name: Optional[str] = None
    joint_venture_profit: int = 0
    care_status: Optional[str] = None  # Yaşlı Anne/Baba Bakım Durumu
    is_estranged: bool = False         # Küs / İletişim kesik mi?
    lent_amount: int = 0               # Borç verilen miktar
    love_confessed: bool = False       # İlk "Seni Seviyorum" itirafı yapıldı mı?
    hard_launched: bool = False        # Sosyal medyada resmi çift olarak ilan edildi mi?
    situationship_turns: int = 0       # Flörtte arafta geçen tur
    red_flags: List[str] = Field(default_factory=list)
    green_flags: List[str] = Field(default_factory=list)
    memories: List[str] = Field(default_factory=list)
    chat_history: List[Dict[str, str]] = Field(default_factory=list)
    intimacy_count: int = 0             # Karakterle bu kişi arasındaki toplam birliktelik sayısı
    intimacy_chemistry: int = 50        # Ten uyumu ve tecrübe seviyesi (50-100)

class DatingCandidate(BaseModel):
    id: str
    name: str
    gender: str
    age: int
    job: str
    city: str
    zodiac: str
    personality: str
    looks: int
    smarts: int
    craziness: int
    loyalty: int
    wealth: int
    money_generosity: int
    interests: List[str]
    bio: str
    love_language: str = "Kaliteli Zaman"
    compatibility: int = 75

class Pet(BaseModel):
    id: str
    name: str
    species: str  # Kedi, Köpek, Kuş
    breed: str = "Melez"
    age: int = 0
    relationship_level: int = 90
    health: int = 95
    is_alive: bool = True

class Job(BaseModel):
    id: str
    title: str
    category: str
    salary: int
    required_education: str = "Yok"
    required_smarts: int = 0
    performance: int = 70
    stress: int = 30
    experience_years: int = 0
    level: int = 1

class Business(BaseModel):
    id: str
    name: str
    sector: str
    capital_invested: int
    valuation: int
    annual_profit: int
    employees: int = 3
    reputation: int = 70
    years_active: int = 0

class MusicBand(BaseModel):
    name: str
    genre: str
    albums_count: int = 0
    chemistry: int = 80
    fans: int = 1000
    annual_royalties: int = 0

class ProSportsCareer(BaseModel):
    sport: str = "Futbol"
    team_name: str
    league_tier: str = "Altyapı Akademisi"
    salary: int = 0
    goals_or_points: int = 0
    trophies: int = 0
    national_caps: int = 0
    owns_club: bool = False
    club_valuation: int = 0

class Asset(BaseModel):
    id: str
    name: str
    asset_type: str  # Ev, Araba, Koleksiyon
    purchase_price: int
    current_value: int
    condition: int = 100
    annual_cost: int = 0
    annual_income: int = 0
    is_rented_out: bool = True
    tenant_name: Optional[str] = None
    tenant_reliability: int = 85  # 0 - 100
    tenant_issue: Optional[str] = None  # Gecikmiş Kira, Gürültü Şikayeti, vb.
    has_insurance: bool = False  # Kasko / Sigorta
    upgrade_level: int = 0

class Stock(BaseModel):
    symbol: str
    name: str
    shares: int = 0
    avg_buy_price: float = 0.0
    current_price: float
    history: List[float] = Field(default_factory=list)

class SocialMediaAccount(BaseModel):
    platform: str  # Instagram, YouTube, TikTok
    followers: int = 0
    verified: bool = False
    posts_count: int = 0
    earnings_annual: int = 0

class LifeLog(BaseModel):
    age: int
    year: int
    text: str
    category: str = "general"  # general, milestone, health, love, crime, career, school
    icon: str = "📌"

class EventChoice(BaseModel):
    id: str
    text: str

class ActiveEvent(BaseModel):
    id: str
    title: str
    description: str
    image_emoji: str = "❓"
    choices: List[EventChoice]
    category: str = "general"

class BlackjackHand(BaseModel):
    active: bool = False
    bet: int = 0
    player_cards: List[str] = Field(default_factory=list)
    dealer_cards: List[str] = Field(default_factory=list)
    player_total: int = 0
    dealer_total: int = 0
    status: str = "playing"

class Character(BaseModel):
    id: str
    first_name: str
    last_name: str
    gender: str
    birth_year: int = 2000
    current_year: int = 2000
    age: int = 0
    city: str = "İstanbul"
    country: str = "Türkiye"
    zodiac: str = "Koç ♈"
    generation: int = 1
    
    # Primary Stats (0 - 100)
    happiness: int = 80
    health: int = 95
    smarts: int = 65
    looks: int = 70
    
    # Secondary Stats & Skills
    fame: int = 0
    karma: int = 50
    stress: int = 10
    skills: Dict[str, int] = Field(default_factory=lambda: {
        "coding": 10,
        "music": 10,
        "athletics": 15,
        "charisma": 20,
        "martial_arts": 5
    })
    
    # Finances
    money: int = 0
    debt: int = 0
    net_worth: int = 0
    annual_income_last: int = 0
    annual_expense_last: int = 0
    will_beneficiary: str = "all_children"
    
    # Crime & Military
    criminal_record: List[str] = Field(default_factory=list)
    is_in_prison: bool = False
    prison_years_left: int = 0
    prison_sentence: int = 0
    military_status: str = "Muaf/Yaş Gelmedi"
    
    # Education & Occupation
    education_level: str = "Yok"
    current_school: Optional[str] = None
    school_years_left: int = 0
    school_performance: int = 75
    school_club: Optional[str] = None
    has_drivers_license: bool = False
    
    current_job: Optional[Job] = None
    part_time_job: Optional[Job] = None
    business: Optional[Business] = None
    job_history: List[str] = Field(default_factory=list)
    
    # Life status
    is_alive: bool = True
    death_reason: Optional[str] = None
    tombstone_title: Optional[str] = None
    
    # Collections
    relationships: List[Person] = Field(default_factory=list)
    dating_candidates: List[DatingCandidate] = Field(default_factory=list)
    pets: List[Pet] = Field(default_factory=list)
    assets: List[Asset] = Field(default_factory=list)
    stocks: Dict[str, Stock] = Field(default_factory=dict)
    social_media: Dict[str, SocialMediaAccount] = Field(default_factory=dict)
    illnesses: List[str] = Field(default_factory=list)
    logs: List[LifeLog] = Field(default_factory=list)
    active_event: Optional[ActiveEvent] = None
    blackjack: BlackjackHand = Field(default_factory=BlackjackHand)
    
    # Marriage, Dating & Pregnancy
    spouse_id: Optional[str] = None
    dating_partner_id: Optional[str] = None
    pregnancy_partner_id: Optional[str] = None
    pregnancy_baby_gender: Optional[str] = None
    
    # Politics & State Governance
    political_office: Optional[str] = None
    political_salary: int = 0
    approval_rating: int = 55

    # Style, Exams & Housing (Packs 2, 3, 4, 10)
    outfit_style: str = "👕 Günlük & Rahat"
    housing_type: str = "Aile Evi"
    scholarship_annual: int = 0
    yks_score: int = 0
    kpss_score: int = 0

    # Music Band, Offshore Banking & Life Analytics (Packs 11, 14, 15, 16)
    band: Optional[MusicBand] = None
    offshore_balance: int = 0
    wealth_history: List[int] = Field(default_factory=lambda: [0])
    happiness_history: List[int] = Field(default_factory=lambda: [80])

    # Packs 17, 18, 19 & Real-Life Realism Overhaul
    sports_career: Optional[ProSportsCareer] = None
    alimony_annual: int = 0
    last_tax_paid: int = 0
    hookup_count: int = 0
    intimacy_count: int = 0  # Toplam yatak odası birliktelik sayısı
    difficulty_mode: str = "Gerçek Hayat (Zor)"
    last_annual_summary: Dict[str, Any] = Field(default_factory=dict)
    
    # Achievements
    achievements: List[str] = Field(default_factory=list)
