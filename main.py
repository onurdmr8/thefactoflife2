# -*- coding: utf-8 -*-
"""
BitLife Türkiye - Hayat Simülatörü
FastAPI Web Sunucusu ve API Katmanı
"""

import os
import sys
import webbrowser
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from game.engine import GameEngine
from game.models import Character
from game.events import resolve_event_choice
from game.data import (
    CITIES, JOBS_DATABASE, PART_TIME_JOBS, BUSINESS_TYPES,
    SCHOOL_CLUBS, REAL_ESTATE_MARKET, VEHICLE_MARKET,
    UNIVERSITIES, PET_BREEDS, ACHIEVEMENT_DEFINITIONS,
    PERSONALITIES, MEET_PLACES, DATE_VENUES, ROMANTIC_GIFTS,
    ENGAGEMENT_RINGS, WEDDING_VENUES
)
from game.activities import (
    do_doctor_checkup, do_plastic_surgery, do_gym_workout, do_meditation,
    do_study_hard, join_school_club, train_skill_course, take_driving_license_manual,
    apply_for_university, apply_for_job, apply_part_time_job,
    start_new_business, invest_in_business, sell_business,
    work_harder, ask_for_raise_or_promotion, quit_job,
    find_love_date, make_new_friend, adopt_pet_from_shelter, interact_with_pet,
    propose_marriage, try_for_baby, interact_with_person, set_will_beneficiary,
    generate_dating_candidates, swipe_dating_candidate, meet_someone_at_place,
    go_on_venue_date, give_custom_gift, plan_wedding_ceremony, adopt_child_from_agency,
    buy_real_estate, buy_vehicle, sell_asset,
    buy_stock, sell_stock, blackjack_action, play_scratch_card,
    commit_crime, prison_escape_attempt, prison_activity,
    post_on_social_media, take_vacation
)

app = FastAPI(title="BitLife Türkiye", description="Türkçe Hayat Simülatörü")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

engine = GameEngine()
current_character: Optional[Character] = engine.saved_character

class NewGameRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None

class EventChoiceRequest(BaseModel):
    event_id: str
    choice_id: str

class ActivityRequest(BaseModel):
    action: str
    params: Dict[str, Any] = {}

def _sync_net_worth(char: Character):
    assets_val = sum(a.current_value for a in char.assets)
    stocks_val = sum(int(s.shares * s.current_price) for s in char.stocks.values())
    biz_val = char.business.valuation if char.business else 0
    char.net_worth = char.money + assets_val + stocks_val + biz_val

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/new_game")
def start_new_game(req: NewGameRequest):
    global current_character
    current_character = engine.create_character(
        first_name=req.first_name,
        last_name=req.last_name,
        gender=req.gender,
        city=req.city
    )
    return {
        "success": True,
        "character": current_character.model_dump()
    }

@app.get("/api/state")
def get_game_state():
    global current_character
    if not current_character:
        current_character = engine.create_character()
    return {
        "success": True,
        "character": current_character.model_dump()
    }

@app.post("/api/age_up")
def age_up():
    global current_character
    if not current_character:
        return JSONResponse(status_code=400, content={"success": False, "message": "Aktif bir hayat yok."})
    
    result = engine.age_up(current_character)
    result["character"] = current_character.model_dump()
    return result

@app.post("/api/event_choice")
def choose_event_option(req: EventChoiceRequest):
    global current_character
    if not current_character:
        return JSONResponse(status_code=400, content={"success": False, "message": "Karakter yok."})
    
    outcome_text = resolve_event_choice(current_character, req.event_id, req.choice_id)
    _sync_net_worth(current_character)
    engine.save_to_disk(current_character)
    return {
        "success": True,
        "message": outcome_text,
        "character": current_character.model_dump()
    }

@app.post("/api/activity")
def handle_activity(req: ActivityRequest):
    global current_character
    if not current_character:
        return JSONResponse(status_code=400, content={"success": False, "message": "Aktif hayat yok."})
    
    if not current_character.is_alive:
        return JSONResponse(status_code=400, content={"success": False, "message": "Karakter vefat etmiş."})
        
    act = req.action
    p = req.params
    res = {"success": False, "message": "Geçersiz işlem."}

    # Sağlık
    if act == "doctor_checkup":
        res = do_doctor_checkup(current_character)
    elif act == "plastic_surgery":
        res = do_plastic_surgery(current_character, p.get("procedure", "rhinoplasty"))
    elif act == "gym_workout":
        res = do_gym_workout(current_character)
    elif act == "meditation":
        res = do_meditation(current_character)

    # Eğitim, Kulüp & Beceriler
    elif act == "study_hard":
        res = do_study_hard(current_character)
    elif act == "join_club":
        res = join_school_club(current_character, p.get("club_id", "robotics"))
    elif act == "train_skill":
        res = train_skill_course(current_character, p.get("skill_key", "coding"))
    elif act == "take_driving_license":
        res = take_driving_license_manual(current_character)
    elif act == "apply_university":
        res = apply_for_university(current_character, p.get("faculty_id", "eng"))

    # İş, Kariyer & Girişimcilik
    elif act == "apply_job":
        res = apply_for_job(current_character, p.get("job_id", ""), int(p.get("chosen_opt", 0)))
    elif act == "apply_part_time":
        res = apply_part_time_job(current_character, p.get("pt_id", "pt_barista"))
    elif act == "start_business":
        res = start_new_business(current_character, p.get("biz_id", "cigkofte"))
    elif act == "invest_business":
        res = invest_in_business(current_character)
    elif act == "sell_business":
        res = sell_business(current_character)
    elif act == "work_harder":
        res = work_harder(current_character)
    elif act == "ask_raise":
        res = ask_for_raise_or_promotion(current_character)
    elif act == "quit_job":
        res = quit_job(current_character)

    # Aşk, Flört, KısmetApp, Evlilik, Arkadaşlık, Evcil Hayvan & Vasiyetname
    elif act == "find_love":
        res = find_love_date(current_character)
    elif act == "kismet_generate":
        res = generate_dating_candidates(current_character, p.get("filter_type", "standard"))
    elif act == "kismet_swipe":
        res = swipe_dating_candidate(current_character, p.get("candidate_id", ""), p.get("relation_mode", "Flört"))
    elif act == "meet_place":
        res = meet_someone_at_place(current_character, p.get("place_id", "cafe"))
    elif act == "venue_date":
        res = go_on_venue_date(current_character, p.get("person_id", ""), p.get("venue_id", "tea_simit"))
    elif act == "custom_gift":
        res = give_custom_gift(current_character, p.get("person_id", ""), p.get("gift_id", "roses"))
    elif act == "make_friend":
        res = make_new_friend(current_character)
    elif act == "adopt_pet":
        res = adopt_pet_from_shelter(current_character, int(p.get("breed_idx", 0)))
    elif act == "interact_pet":
        res = interact_with_pet(current_character, p.get("pet_id", ""), p.get("pet_action", "play"))
    elif act == "propose_marriage":
        res = propose_marriage(
            current_character,
            int(p.get("ring_cost", 20000)),
            person_id=p.get("person_id"),
            ring_id=p.get("ring_id")
        )
    elif act == "plan_wedding":
        res = plan_wedding_ceremony(
            current_character,
            p.get("person_id", ""),
            p.get("venue_id", "salon"),
            bool(p.get("sign_prenup", False))
        )
    elif act == "try_baby":
        res = try_for_baby(current_character)
    elif act == "adopt_child":
        res = adopt_child_from_agency(current_character)
    elif act == "interact_person":
        res = interact_with_person(current_character, p.get("person_id", ""), p.get("person_action", "chat"))
    elif act == "set_will":
        res = set_will_beneficiary(current_character, p.get("target", "all_children"))

    # Varlıklar
    elif act == "buy_house":
        res = buy_real_estate(current_character, int(p.get("index", 0)))
    elif act == "buy_car":
        res = buy_vehicle(current_character, int(p.get("index", 0)))
    elif act == "sell_asset":
        res = sell_asset(current_character, p.get("asset_id", ""))

    # Borsa, İnteraktif Blackjack & Kazı Kazan
    elif act == "buy_stock":
        res = buy_stock(current_character, p.get("symbol", ""), int(p.get("amount", 10000)))
    elif act == "sell_stock":
        res = sell_stock(current_character, p.get("symbol", ""), int(p.get("shares", 0)))
    elif act == "blackjack":
        res = blackjack_action(current_character, p.get("sub_action", "start"), int(p.get("bet", 1000)))
    elif act == "scratch_card":
        res = play_scratch_card(current_character)

    # Suç & Cezaevi
    elif act == "crime":
        res = commit_crime(current_character, p.get("crime_type", "pickpocket"))
    elif act == "prison_escape":
        res = prison_escape_attempt(current_character, p.get("route", "tunnel"))
    elif act == "prison_act":
        res = prison_activity(current_character, p.get("activity", "library"))

    # Sosyal Medya & Tatil
    elif act == "social_post":
        res = post_on_social_media(current_character, p.get("platform", "Instagram"))
    elif act == "vacation":
        res = take_vacation(current_character, p.get("destination", "antalya"))

    _sync_net_worth(current_character)
    engine.save_to_disk(current_character)
    res["character"] = current_character.model_dump()
    return res

@app.get("/api/market_data")
def get_market_data():
    return {
        "success": True,
        "jobs": JOBS_DATABASE,
        "part_time_jobs": PART_TIME_JOBS,
        "businesses": BUSINESS_TYPES,
        "school_clubs": SCHOOL_CLUBS,
        "real_estate": REAL_ESTATE_MARKET,
        "vehicles": VEHICLE_MARKET,
        "universities": UNIVERSITIES,
        "pet_breeds": PET_BREEDS,
        "cities": CITIES,
        "achievements": ACHIEVEMENT_DEFINITIONS,
        "personalities": PERSONALITIES,
        "meet_places": MEET_PLACES,
        "date_venues": DATE_VENUES,
        "romantic_gifts": ROMANTIC_GIFTS,
        "engagement_rings": ENGAGEMENT_RINGS,
        "wedding_venues": WEDDING_VENUES
    }

@app.get("/api/graveyard")
def get_graveyard():
    return {
        "success": True,
        "graveyard": engine.graveyard
    }

@app.post("/api/reincarnate")
def reincarnate():
    global current_character
    if not current_character:
        return JSONResponse(status_code=400, content={"success": False, "message": "Karakter yok."})
        
    child_char = engine.reincarnate_as_child(current_character)
    if child_char:
        current_character = child_char
        return {
            "success": True,
            "message": "Çocuğun olarak aile mirasını devraldın!",
            "character": current_character.model_dump()
        }
    else:
        current_character = engine.create_character()
        return {
            "success": True,
            "message": "Hayatta kalan bir çocuğun olmadığı için sıfırdan yeni bir hayata başladın.",
            "character": current_character.model_dump()
        }

if __name__ == "__main__":
    port = 8000
    url = f"http://localhost:{port}"
    print("\n=======================================================")
    print("BitLife Turkiye Baslatiliyor...")
    print(f"Tarayici Aciliyor: {url}")
    print("=======================================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)
