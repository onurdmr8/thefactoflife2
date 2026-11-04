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
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
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
    ENGAGEMENT_RINGS, WEDDING_VENUES,
    LOVE_LANGUAGES, COUPLE_VACATIONS, SOCIAL_HANGOUTS, DM_TOPICS,
    POLITICAL_OFFICES, AUCTION_ITEMS, OUTFIT_STYLES, EXAM_QUESTIONS,
    BAND_GENRES, COUPLE_BUSINESS_TYPES, DIVORCE_LAWYERS, SPORTS_CLUBS,
    RELATIONSHIP_CONFLICTS, COMPANY_EXPANSION_ACTIONS, CAR_CARE_ACTIONS,
    TENANT_MANAGEMENT_ACTIONS, WELLNESS_SERVICES,
    KISS_STYLES, DETAILED_DATE_SCENARIOS, DETAILED_FIGHT_TOPICS, DETAILED_FIGHT_ATTITUDES,
    PARENT_CARE_OPTIONS, SIBLING_INTERACTIONS, PARENTING_CRISES, FRIEND_INTERACTIONS,
    HOOKUP_VENUES, HOOKUP_PROTECTION_CHOICES, DATING_OPENING_LINES, RED_FLAGS_POOL, GREEN_FLAGS_POOL,
    DATE_OUTFITS, DATE_GREETINGS, DATE_CONVERSATION_TOPICS, DATE_TACTILE_ACTIONS, DATE_MID_EVENTS, DATE_FINALES,
    INTIMACY_VENUES, INTIMACY_MOODS, INTIMACY_PROTECTIONS, INTIMACY_AFTERGLOWS,
    INTIMACY_OUTFITS, INTIMACY_FOREPLAY_ACTIONS, INTIMACY_STYLES, INTIMACY_TWISTS, INTIMACY_MORNING_ACTIONS,
    INTIMACY_MUSICS,
    COWORKER_PROJECT_OPTIONS, COWORKER_GOSSIP_STORIES, COWORKER_GOSSIP_REACTIONS,
    COWORKER_HANGOUT_OPTIONS, BOSS_MENTORSHIP_TOPICS, BOSS_NEGOTIATION_TACTICS
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
    send_dm_message, take_couple_vacation, do_social_hangout, do_group_party,
    do_fame_activity, run_for_political_office, do_political_action,
    manage_asset_extra, buy_auction_item,
    do_insta_story, do_military_service, take_national_exam,
    change_student_housing, change_outfit_style,
    do_drama_intrigue_action, create_music_band, do_band_action, do_bank_offshore_action,
    do_couple_business, do_divorce_court, do_pro_sports_action,
    do_relationship_conflict, do_company_management_action,
    do_tenant_action, do_car_care_action, do_wellness_action,
    do_detailed_kiss, do_detailed_date, do_detailed_fight, run_date_simulation, do_intimacy,
    do_parent_care_action, do_sibling_action, do_parenting_action, do_friend_action, do_consolidated_chat,
    do_hookup, do_flirt_opening, do_situationship_talk, do_confess_love, do_hard_launch, do_handle_ex_midnight_text,
    do_friend_to_lover, do_classmate_action, do_coworker_action, do_boss_action,
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
    club_val = char.sports_career.club_valuation if (char.sports_career and char.sports_career.owns_club) else 0
    char.net_worth = char.money + char.offshore_balance - char.debt + assets_val + stocks_val + biz_val + club_val

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse(os.path.join(static_dir, "manifest.json"), media_type="application/manifest+json")

@app.get("/sw.js")
async def get_service_worker():
    return FileResponse(os.path.join(static_dir, "sw.js"), media_type="application/javascript")

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
            bool(p.get("sign_prenup", False)),
            p.get("guest_tier", "family_friends")
        )
    elif act == "try_baby":
        res = try_for_baby(current_character)
    elif act == "adopt_child":
        res = adopt_child_from_agency(current_character)
    elif act == "send_dm":
        res = send_dm_message(current_character, p.get("person_id", ""), p.get("topic_id", "flirt_msg"))
    elif act == "couple_vacation":
        res = take_couple_vacation(current_character, p.get("person_id", ""), p.get("vacation_id", "sapanca_bungalow"))
    elif act == "social_hangout":
        res = do_social_hangout(current_character, p.get("person_id", ""), p.get("hangout_id", "coffee_gossip"))
    elif act == "group_party":
        res = do_group_party(current_character)
    elif act == "fame_action":
        res = do_fame_activity(current_character, p.get("sub_action", "audition_fame"))
    elif act == "politics_run":
        res = run_for_political_office(current_character, p.get("office_id", "muhtar"))
    elif act == "politics_action":
        res = do_political_action(current_character, p.get("sub_action", "hold_rally"))
    elif act == "asset_manage":
        res = manage_asset_extra(current_character, p.get("asset_id", ""), p.get("sub_action", "renovate_house"))
    elif act == "buy_auction":
        res = buy_auction_item(current_character, p.get("item_id", "patek_watch"))
    elif act == "insta_story":
        res = do_insta_story(current_character, p.get("story_type", "gym_mirror"))
    elif act == "military_service":
        res = do_military_service(current_character, p.get("service_type", "bedelli"))
    elif act == "national_exam":
        res = take_national_exam(
            current_character,
            p.get("exam_type", "yks"),
            int(p.get("ans1", 0)),
            int(p.get("ans2", 1))
        )
    elif act == "student_housing":
        res = change_student_housing(current_character, p.get("housing_mode", "kyk_dorm"))
    elif act == "outfit_style":
        res = change_outfit_style(current_character, p.get("style_id", "casual"))
    elif act == "drama_intrigue":
        res = do_drama_intrigue_action(current_character, p.get("sub_action", "tv_dating_show"))
    elif act == "create_band":
        res = create_music_band(current_character, p.get("band_name", ""), p.get("genre_id", "anadolu_rock"))
    elif act == "band_action":
        res = do_band_action(current_character, p.get("sub_action", "rehearse"))
    elif act == "bank_action":
        res = do_bank_offshore_action(current_character, p.get("sub_action", "take_loan"), int(p.get("amount", 250000)))
    elif act == "couple_business":
        res = do_couple_business(current_character, p.get("person_id", ""), p.get("biz_id", "boutique_cafe"))
    elif act == "divorce_court":
        res = do_divorce_court(current_character, p.get("person_id", ""), p.get("lawyer_id", "baro"))
    elif act == "pro_sports":
        res = do_pro_sports_action(current_character, p.get("sub_action", "join_academy"), p.get("club_id", "anadolu_fk"))
    elif act == "rel_conflict":
        res = do_relationship_conflict(current_character, p.get("person_id", ""), p.get("conflict_id", ""), p.get("choice_id", ""))
    elif act == "company_manage":
        res = do_company_management_action(current_character, p.get("action_id", "marketing"))
    elif act == "tenant_manage":
        res = do_tenant_action(current_character, p.get("asset_id", ""), p.get("action_id", "demand_letter"))
    elif act == "car_care":
        res = do_car_care_action(current_character, p.get("asset_id", ""), p.get("action_id", "maintenance"))
    elif act == "wellness_action":
        res = do_wellness_action(current_character, p.get("action_id") or p.get("service_id", "psychologist"))
    elif act == "detailed_kiss":
        res = do_detailed_kiss(current_character, p.get("person_id", ""), p.get("kiss_id", "lips_gentle"))
    elif act == "detailed_date":
        res = do_detailed_date(current_character, p.get("person_id", ""), p.get("venue_id", "tea_simit"), p.get("mid_choice", ""), p.get("end_choice", ""))
    elif act in ["run_date_simulation", "date_sim"]:
        res = run_date_simulation(
            current_character,
            person_id=p.get("person_id", ""),
            venue_id=p.get("venue_id", "tea_simit"),
            outfit_id=p.get("outfit_id", "smart_casual"),
            greeting_id=p.get("greeting_id", "passionate_hug"),
            dialogue_id=p.get("dialogue_id", "topic_destiny"),
            dialogue_choice_id=p.get("dialogue_choice_id", "destiny_romantic"),
            tactile_id=p.get("tactile_id", "hand_caress_table"),
            mid_event_id=p.get("mid_event_id", "live_music_slow"),
            mid_choice_id=p.get("mid_choice_id", "dance_floor"),
            finale_id=p.get("finale_id", "passionate_kiss")
        )
    elif act in ["intimacy", "make_love", "do_intimacy"]:
        res = do_intimacy(
            current_character,
            person_id=p.get("person_id", ""),
            venue_id=p.get("venue_id", "bedroom_candlelight"),
            music_id=p.get("music_id", "acoustic_jazz"),
            outfit_id=p.get("outfit_id", "natural_cozy"),
            foreplay_id=p.get("foreplay_id", "massage_oil"),
            style_id=p.get("style_id", "tender_sensual"),
            twist_id=p.get("twist_id"),
            twist_choice_id=p.get("twist_choice_id"),
            protection_id=p.get("protection_id", "condom_safe"),
            morning_id=p.get("morning_id", "breakfast_in_bed"),
            mood_id=p.get("mood_id")
        )
    elif act == "detailed_fight":
        res = do_detailed_fight(current_character, p.get("person_id", ""), p.get("topic_id", "jealousy_dm"), p.get("attitude_id", "calm_ultimatum"))
    elif act == "parent_care":
        res = do_parent_care_action(current_character, p.get("person_id", ""), p.get("care_id", "take_home"))
    elif act == "sibling_action":
        res = do_sibling_action(current_character, p.get("person_id", ""), p.get("action_id", "deep_heart_talk"))
    elif act == "parenting_crisis":
        res = do_parenting_action(current_character, p.get("person_id", ""), p.get("crisis_id", "teen_rebellion"), p.get("choice_id", "gentle_mentor"))
    elif act == "friend_action":
        res = do_friend_action(current_character, p.get("person_id", ""), p.get("action_id", "fun_road_trip"))
    elif act == "consolidated_chat":
        res = do_consolidated_chat(current_character, p.get("person_id", ""))
    elif act == "hookup":
        res = do_hookup(current_character, p.get("venue_id", "nightclub"), bool(p.get("use_protection", True)))
    elif act == "flirt_opening":
        res = do_flirt_opening(current_character, p.get("candidate_id", ""), p.get("line_id", "witty_smart"))
    elif act == "situationship_talk":
        res = do_situationship_talk(current_character, p.get("person_id", ""))
    elif act == "confess_love":
        res = do_confess_love(current_character, p.get("person_id", ""))
    elif act == "hard_launch":
        res = do_hard_launch(current_character, p.get("person_id", ""))
    elif act == "handle_ex_midnight_text":
        res = do_handle_ex_midnight_text(current_character, p.get("person_id", ""), p.get("choice_id", "show_partner"))
    elif act == "friend_to_lover":
        res = do_friend_to_lover(current_character, p.get("person_id", ""), p.get("action_id", "friend_hookup"))
    elif act == "classmate_action":
        res = do_classmate_action(current_character, p.get("person_id", ""), p.get("action_id", "hangout_canteen"))
    elif act == "coworker_action":
        res = do_coworker_action(current_character, p.get("person_id", ""), p.get("action_id", "happy_hour"), p.get("sub_id", ""), p.get("story_id", ""))
    elif act == "boss_action":
        res = do_boss_action(current_character, p.get("person_id", ""), p.get("action_id", "suck_up_boss"), p.get("sub_id", ""))
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
        "wedding_venues": WEDDING_VENUES,
        "love_languages": LOVE_LANGUAGES,
        "couple_vacations": COUPLE_VACATIONS,
        "social_hangouts": SOCIAL_HANGOUTS,
        "dm_topics": DM_TOPICS,
        "political_offices": POLITICAL_OFFICES,
        "auction_items": AUCTION_ITEMS,
        "outfit_styles": OUTFIT_STYLES,
        "exam_questions": EXAM_QUESTIONS,
        "band_genres": BAND_GENRES,
        "couple_businesses": COUPLE_BUSINESS_TYPES,
        "divorce_lawyers": DIVORCE_LAWYERS,
        "sports_clubs": SPORTS_CLUBS,
        "relationship_conflicts": RELATIONSHIP_CONFLICTS,
        "company_expansion_actions": COMPANY_EXPANSION_ACTIONS,
        "car_care_actions": CAR_CARE_ACTIONS,
        "tenant_management_actions": TENANT_MANAGEMENT_ACTIONS,
        "wellness_services": WELLNESS_SERVICES,
        "kiss_styles": KISS_STYLES,
        "detailed_date_scenarios": DETAILED_DATE_SCENARIOS,
        "detailed_fight_topics": DETAILED_FIGHT_TOPICS,
        "detailed_fight_attitudes": DETAILED_FIGHT_ATTITUDES,
        "parent_care_options": PARENT_CARE_OPTIONS,
        "sibling_interactions": SIBLING_INTERACTIONS,
        "parenting_crises": PARENTING_CRISES,
        "friend_interactions": FRIEND_INTERACTIONS,
        "hookup_venues": HOOKUP_VENUES,
        "hookup_protection_choices": HOOKUP_PROTECTION_CHOICES,
        "dating_opening_lines": DATING_OPENING_LINES,
        "red_flags_pool": RED_FLAGS_POOL,
        "green_flags_pool": GREEN_FLAGS_POOL,
        "date_outfits": DATE_OUTFITS,
        "date_greetings": DATE_GREETINGS,
        "date_conversations": DATE_CONVERSATION_TOPICS,
        "date_tactiles": DATE_TACTILE_ACTIONS,
        "date_mid_events": DATE_MID_EVENTS,
        "date_finales": DATE_FINALES,
        "intimacy_venues": INTIMACY_VENUES,
        "intimacy_musics": INTIMACY_MUSICS,
        "intimacy_outfits": INTIMACY_OUTFITS,
        "intimacy_foreplays": INTIMACY_FOREPLAY_ACTIONS,
        "intimacy_styles": INTIMACY_STYLES,
        "intimacy_twists": INTIMACY_TWISTS,
        "intimacy_mornings": INTIMACY_MORNING_ACTIONS,
        "intimacy_moods": INTIMACY_MOODS,
        "intimacy_protections": INTIMACY_PROTECTIONS,
        "intimacy_afterglows": INTIMACY_AFTERGLOWS,
        "coworker_projects": COWORKER_PROJECT_OPTIONS,
        "coworker_gossips": COWORKER_GOSSIP_STORIES,
        "coworker_gossip_reactions": COWORKER_GOSSIP_REACTIONS,
        "coworker_hangouts": COWORKER_HANGOUT_OPTIONS,
        "boss_mentorships": BOSS_MENTORSHIP_TOPICS,
        "boss_negotiations": BOSS_NEGOTIATION_TACTICS
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
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
