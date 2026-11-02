// BitLife Türkiye - Gelişmiş Frontend Controller
let gameState = null;
let marketData = null;
let activePersonId = null;
let currentLogFilter = "all";

// ----------------- MODERN WEB GUIDANCE: TOP-LAYER & DIALOG FALLBACKS -----------------

let supportsDisplayTransition;
function canTransitionDisplay() {
    if (supportsDisplayTransition !== undefined) return supportsDisplayTransition;
    if (!window.CSS?.supports?.("transition-behavior", "allow-discrete") || !document.body) {
        return false;
    }
    const probe = document.createElement("div");
    probe.style.cssText = "transition: display 1s allow-discrete !important; display: block;";
    document.body.appendChild(probe);
    getComputedStyle(probe).display;
    probe.style.display = "none";
    supportsDisplayTransition = getComputedStyle(probe).display === "block";
    probe.remove();
    return supportsDisplayTransition;
}

function supportsTopLayerExit() {
    return window.CSS?.supports?.("overlay", "auto") && canTransitionDisplay();
}

async function closeTopLayer(dialog) {
    if (!dialog || !dialog.open) return;
    if (!supportsTopLayerExit()) {
        dialog.setAttribute("data-closing", "");
        const animations = dialog.getAnimations({ subtree: true });
        if (animations.length > 0) {
            await Promise.race([
                Promise.allSettled(animations.map((a) => a.finished)),
                new Promise((r) => setTimeout(r, 2000)),
            ]);
        }
        if (!dialog.hasAttribute("data-closing")) return;
        dialog.removeAttribute("data-closing");
    }
    dialog.close();
}

function openDialogModal(dialogId) {
    const dialog = document.getElementById(dialogId);
    if (!dialog) return;
    dialog.removeAttribute("data-closing");
    if (!dialog.open) {
        dialog.showModal();
    }
}

function closeModal(dialogId) {
    sound.playClick();
    const dialog = document.getElementById(dialogId);
    if (dialog && dialog.open) {
        closeTopLayer(dialog);
    }
}

function setupDialogBehaviors() {
    // Route Esc cancel events through animated closeTopLayer for dismissible dialogs,
    // and guard mandatory dialogs (closedby="none")
    for (const dialog of document.querySelectorAll("dialog.app-dialog")) {
        dialog.addEventListener("cancel", (event) => {
            event.preventDefault();
            if (dialog.getAttribute("closedby") === "none") {
                return;
            }
            closeTopLayer(dialog);
        });
    }

    // Fallback for browsers without native <dialog closedby="any"> support
    if (!("closedBy" in HTMLDialogElement.prototype)) {
        const outside = (e, dialog) => {
            const r = dialog.getBoundingClientRect();
            return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
        };
        for (const dialog of document.querySelectorAll('dialog[closedby="any"]')) {
            let pressedOutside = false;
            dialog.addEventListener("pointerdown", (e) => {
                pressedOutside = outside(e, dialog);
            });
            dialog.addEventListener("pointerup", (e) => {
                if (pressedOutside && outside(e, dialog)) {
                    closeTopLayer(dialog);
                }
            });
        }
    }
}

// ----------------- BAŞLATMA -----------------

document.addEventListener("DOMContentLoaded", async () => {
    setupDialogBehaviors();
    await fetchMarketData();
    await fetchGameState();
    setupEventListeners();
});

async function fetchMarketData() {
    try {
        const res = await fetch("/api/market_data");
        const data = await res.json();
        if (data.success) {
            marketData = data;
        }
    } catch (e) {
        console.error("Market verisi alınamadı:", e);
    }
}

async function fetchGameState() {
    try {
        const res = await fetch("/api/state");
        const data = await res.json();
        if (data.success && data.character) {
            gameState = data.character;
            renderAll();
        }
    } catch (e) {
        console.error("Oyun durumu alınamadı:", e);
    }
}

function toggleSound() {
    sound.muted = !sound.muted;
    const btn = document.getElementById("btnSoundToggle");
    if (btn) {
        btn.textContent = sound.muted ? "🔇" : "🔊";
    }
    if (!sound.muted) sound.playClick();
}

// ----------------- ANA RENDER -----------------

function renderAll() {
    if (!gameState) return;

    renderHeader();
    renderStats();
    renderLifeFeed();
    renderRelationships();
    renderCareerTab();
    renderAssetsTab();

    if (gameState.active_event && gameState.is_alive) {
        openEventModal(gameState.active_event);
    } else {
        const evDialog = document.getElementById("eventModal");
        if (evDialog && evDialog.open) closeTopLayer(evDialog);
    }

    if (!gameState.is_alive) {
        openDeathModal();
    }
}

function getCharacterAvatarEmoji(char) {
    if (!char.is_alive) return "🪦";
    if (char.is_in_prison) return "⛓️";
    const isMale = char.gender === "Erkek";
    if (char.age < 4) return "👶";
    if (char.age < 13) return isMale ? "👦" : "👧";
    if (char.age < 25) return isMale ? "🧑" : "👩";
    if (char.age < 60) return isMale ? "🧔" : "👩‍💼";
    return isMale ? "👴" : "👵";
}

function renderHeader() {
    const avatarEl = document.getElementById("charAvatar");
    const nameEl = document.getElementById("charName");
    const ageEl = document.getElementById("charAge");
    const subEl = document.getElementById("charSubtitle");
    const moneyEl = document.getElementById("charMoney");
    const netEl = document.getElementById("charNetworth");
    const achBadge = document.getElementById("achCountBadge");
    const chipsRow = document.getElementById("statusChipsRow");

    if (avatarEl) avatarEl.textContent = getCharacterAvatarEmoji(gameState);
    nameEl.textContent = `${gameState.first_name} ${gameState.last_name}`;
    ageEl.textContent = `${gameState.age} Yaş`;

    let jobOrSchool = "İşsiz";
    if (gameState.is_in_prison) {
        jobOrSchool = `Mahkum (${gameState.prison_years_left} Yıl)`;
    } else if (gameState.business) {
        jobOrSchool = `Patron (${gameState.business.name})`;
    } else if (gameState.current_job) {
        jobOrSchool = gameState.current_job.title;
    } else if (gameState.age < 6) {
        jobOrSchool = "Okul Öncesi Çocuk";
    } else if (gameState.current_school) {
        jobOrSchool = `Öğrenci (${gameState.current_school})`;
    }

    subEl.textContent = `${jobOrSchool} • ${gameState.city} • ${gameState.zodiac}`;
    moneyEl.textContent = `₺ ${gameState.money.toLocaleString("tr-TR")}`;
    moneyEl.style.color = gameState.money < 0 ? "var(--accent-red)" : "var(--accent-green)";
    netEl.textContent = `Net Servet: ₺ ${gameState.net_worth.toLocaleString("tr-TR")}`;

    const totalAch = marketData && marketData.achievements ? marketData.achievements.length : 15;
    const myAch = gameState.achievements ? gameState.achievements.length : 1;
    if (achBadge) achBadge.textContent = `${myAch}/${totalAch}`;

    // Status Chips
    if (chipsRow) {
        let html = `<span class="status-chip">👑 ${gameState.generation || 1}. Kuşak</span>`;
        html += `<span class="status-chip">☯️ Karma: %${gameState.karma}</span>`;
        if (gameState.fame > 0) {
            html += `<span class="status-chip chip-gold">🌟 Şöhret: %${gameState.fame}</span>`;
        }
        if (gameState.is_in_prison) {
            html += `<span class="status-chip chip-danger">🚨 Cezaevinde (${gameState.prison_years_left} Yıl)</span>`;
        }
        if (gameState.illnesses && gameState.illnesses.length > 0) {
            gameState.illnesses.forEach(ill => {
                html += `<span class="status-chip chip-danger" onclick="performActivity('doctor_checkup')" style="cursor:pointer" title="Tedavi için tıkla">🤒 ${ill}</span>`;
            });
        }
        chipsRow.innerHTML = html;
    }
}

function renderStats() {
    setStatBar("happinessBar", "happinessVal", gameState.happiness);
    setStatBar("healthBar", "healthVal", gameState.health);
    setStatBar("smartsBar", "smartsVal", gameState.smarts);
    setStatBar("looksBar", "looksVal", gameState.looks);
}

function setStatBar(barId, valId, value) {
    const bar = document.getElementById(barId);
    const val = document.getElementById(valId);
    if (!bar || !val) return;

    const clamped = Math.max(0, Math.min(100, value));
    bar.style.width = `${clamped}%`;
    val.textContent = `%${clamped}`;

    if (clamped < 30) {
        bar.style.backgroundColor = "var(--accent-red)";
    } else if (clamped < 60) {
        bar.style.backgroundColor = "var(--accent-yellow)";
    } else {
        if (barId === "happinessBar") bar.style.backgroundColor = "var(--accent-yellow)";
        else if (barId === "healthBar") bar.style.backgroundColor = "var(--accent-green)";
        else if (barId === "smartsBar") bar.style.backgroundColor = "var(--accent-blue)";
        else if (barId === "looksBar") bar.style.backgroundColor = "var(--accent-purple)";
    }
}

// ----------------- HAYAT GÜNLÜĞÜ & FİLTRELEME -----------------

function setLogFilter(filterKey, btnEl) {
    sound.playClick();
    currentLogFilter = filterKey;
    document.querySelectorAll(".filter-pill").forEach(b => b.classList.remove("active"));
    if (btnEl) btnEl.classList.add("active");
    renderLifeFeed();
}

function renderLifeFeed() {
    const feed = document.getElementById("lifeFeed");
    if (!feed) return;
    feed.innerHTML = "";

    const filteredLogs = gameState.logs.filter(log => {
        if (currentLogFilter === "all") return true;
        return log.category === currentLogFilter;
    });

    if (filteredLogs.length === 0) {
        feed.innerHTML = `<div class="panel-card"><p class="card-desc">Bu kategoride henüz bir olay kaydı bulunmuyor.</p></div>`;
        return;
    }

    const logsByAge = {};
    filteredLogs.forEach(log => {
        if (!logsByAge[log.age]) logsByAge[log.age] = [];
        logsByAge[log.age].push(log);
    });

    const ages = Object.keys(logsByAge).map(Number).sort((a, b) => b - a);

    ages.forEach(age => {
        const group = document.createElement("div");
        group.className = "log-year-group";
        const year = gameState.birth_year + age;
        const groupLogs = logsByAge[age];

        let entriesHtml = "";
        groupLogs.forEach(entry => {
            entriesHtml += `
                <div class="log-entry">
                    <span class="log-icon">${entry.icon || "📌"}</span>
                    <div>${entry.text}</div>
                </div>
            `;
        });

        group.innerHTML = `
            <div class="log-header">
                <span>${age} Yaşında (${year})</span>
            </div>
            ${entriesHtml}
        `;
        feed.appendChild(group);
    });
}

// ----------------- İLİŞKİLER VE EVCİL HAYVANLAR -----------------

function renderRelationships() {
    const listEl = document.getElementById("relationshipsList");
    if (!listEl) return;
    listEl.innerHTML = "";

    if (!gameState.relationships || gameState.relationships.length === 0) {
        listEl.innerHTML = `<div class="panel-card"><p class="card-desc">Henüz kayıtlı bir ilişkin yok.</p></div>`;
    } else {
        gameState.relationships.forEach(person => {
            const card = document.createElement("div");
            card.className = "panel-card clickable-card";
            card.onclick = () => openPersonModal(person.id);

            const statusBadge = person.is_alive
                ? `<span class="card-badge badge-green">İlişki: %${person.relationship_level}</span>`
                : `<span class="card-badge badge-red">Vefat Etti</span>`;

            card.innerHTML = `
                <div class="card-title-row">
                    <span class="card-title">
                        ${getRelationEmoji(person.relation)} ${person.name}
                    </span>
                    ${statusBadge}
                </div>
                <div class="card-desc">
                    ${person.relation} • ${person.age} Yaşında ${person.job ? `• ${person.job}` : ""}
                </div>
            `;
            listEl.appendChild(card);
        });
    }

    // Evcil hayvanlar
    if (gameState.pets && gameState.pets.length > 0) {
        const petsTitle = document.createElement("h4");
        petsTitle.style.cssText = "font-size: 13px; color: var(--text-secondary); margin: 14px 0 8px;";
        petsTitle.textContent = "🐾 Evcil Hayvanların";
        listEl.appendChild(petsTitle);

        gameState.pets.forEach(pet => {
            const petCard = document.createElement("div");
            petCard.className = "panel-card";
            petCard.innerHTML = `
                <div class="card-title-row">
                    <span class="card-title">🐾 ${pet.name} (${pet.breed || pet.species})</span>
                    <span class="card-badge ${pet.is_alive ? 'badge-green' : 'badge-red'}">
                        ${pet.is_alive ? `Sevgi: %${pet.relationship_level}` : 'Vefat Etti'}
                    </span>
                </div>
                <div class="card-desc">${pet.age} Yaşında • Sağlık: %${pet.health}</div>
                ${pet.is_alive ? `
                    <div style="display:flex; gap:8px; margin-top:8px;">
                        <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('interact_pet', {pet_id: '${pet.id}', pet_action: 'play'})">🎾 Oyna</button>
                        <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('interact_pet', {pet_id: '${pet.id}', pet_action: 'vet'})">🩺 Veteriner (1.200 TL)</button>
                    </div>
                ` : ""}
            `;
            listEl.appendChild(petCard);
        });
    }
}

function getRelationEmoji(rel) {
    switch (rel) {
        case "Anne": return "👩";
        case "Baba": return "👨";
        case "Ağabey": case "Kardeş": return "👦";
        case "Abla": return "👧";
        case "Sevgili": return "💘";
        case "Eş": return "💍";
        case "Çocuk": return "👶";
        case "Arkadaş": return "🤝";
        default: return "👤";
    }
}

// ----------------- KARİYER, EĞİTİM, BECERİLER & ŞİRKET -----------------

function renderCareerTab() {
    const careerEl = document.getElementById("careerContent");
    if (!careerEl) return;
    careerEl.innerHTML = "";

    // 1. Eğitim ve Okul Kulüpleri
    const eduCard = document.createElement("div");
    eduCard.className = "panel-card";
    eduCard.innerHTML = `
        <div class="card-title-row">
            <span class="card-title">🎓 Eğitim & Akademi</span>
            <span class="card-badge badge-blue">${gameState.education_level}</span>
        </div>
        <p class="card-desc">
            ${gameState.current_school ? `Okul: <b>${gameState.current_school}</b>` : "Aktif öğrenci değilsin."}
            ${gameState.school_club ? ` • Kulüp: <b>${gameState.school_club}</b>` : ""}
            <br>
            ${gameState.has_drivers_license ? "🚗 B Sınıfı Ehliyet: Var" : "🚗 Ehliyet: Yok"}
            ${gameState.gender === "Erkek" ? ` • 🪖 Askerlik: ${gameState.military_status}` : ""}
        </p>
        <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">
            <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('study_hard')">📚 Ders Çalış</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openClubsModal()">🏅 Okul Kulüpleri</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openUniversityModal()">🏛️ Üniversite</button>
        </div>
    `;
    careerEl.appendChild(eduCard);

    // 2. Kendi Şirketin / Girişimcilik
    const bizCard = document.createElement("div");
    bizCard.className = "panel-card";
    if (gameState.business) {
        const b = gameState.business;
        bizCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">🏢 ${b.name}</span>
                <span class="card-badge badge-yellow">Değer: ₺ ${b.valuation.toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc">
                Sektör: ${b.sector} • Yıllık Kâr: <b>+₺ ${b.annual_profit.toLocaleString("tr-TR")}</b> • Çalışan: ${b.employees} Kişi • İtibar: %${b.reputation}
            </p>
            <div style="margin-top: 10px; display: flex; gap: 8px;">
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('invest_business')">🚀 Büyüt & Yatırım Yap</button>
                <button type="button" class="btn-action-outline" style="flex:1; border-color: var(--accent-green); color: var(--accent-green);" onclick="performActivity('sell_business')">💰 Şirketi Sat (Exit)</button>
            </div>
        `;
    } else {
        bizCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">🏢 Girişimcilik & Kendi İşin</span>
                <span class="card-badge badge-purple">Fırsat</span>
            </div>
            <p class="card-desc">Kendi dükkanını, kafenizi veya teknoloji şirketinizi kurup patron olabilirsiniz.</p>
            <button type="button" class="btn-action-outline" style="width:100%; margin-top:8px;" onclick="openBusinessModal()">🏢 Yeni Şirket / Bayi Kur</button>
        `;
    }
    careerEl.appendChild(bizCard);

    // 3. Tam Zamanlı ve Yarı Zamanlı İş
    const jobCard = document.createElement("div");
    jobCard.className = "panel-card";
    if (gameState.is_in_prison) {
        jobCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">🚨 Cezaevi Hükümlüsü</span>
                <span class="card-badge badge-red">${gameState.prison_years_left} Yıl Kaldı</span>
            </div>
            <p class="card-desc">Hapishanedeyken dışarıda çalışamazsın.</p>
        `;
    } else if (gameState.current_job) {
        const j = gameState.current_job;
        jobCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">💼 ${j.title} (Kademe ${j.level || 1})</span>
                <span class="card-badge badge-green">₺ ${j.salary.toLocaleString("tr-TR")}/yıl</span>
            </div>
            <div class="card-desc">
                Sektör: ${j.category} • Performans: %${j.performance} • Kıdem: ${j.experience_years} Yıl
                ${gameState.part_time_job ? `<br>⏱️ Ek İş: ${gameState.part_time_job.title} (+₺ ${gameState.part_time_job.salary.toLocaleString("tr-TR")}/yıl)` : ""}
            </div>
            <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('work_harder')">💪 Mesai Yap</button>
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('ask_raise')">📈 Zam/Terfi İste</button>
                <button type="button" class="btn-action-outline" style="flex:1; border-color: var(--accent-red); color: var(--accent-red);" onclick="performActivity('quit_job')">🚪 İstifa</button>
            </div>
        `;
    } else {
        jobCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">💼 Kariyer & İş İlanları</span>
                <span class="card-badge badge-red">${gameState.part_time_job ? gameState.part_time_job.title : 'İşsiz'}</span>
            </div>
            <p class="card-desc">Mülakat sorularını geçerek tam zamanlı işe girebilir veya öğrenciysen yarı zamanlı çalışabilirsin.</p>
            <div style="margin-top: 10px; display: flex; gap: 8px;">
                <button type="button" class="btn-primary" style="flex:2" onclick="openJobsModal()">💼 Tam Zamanlı İşler</button>
                <button type="button" class="btn-action-outline" style="flex:1" onclick="openPartTimeModal()">⏱️ Part-Time</button>
            </div>
        `;
    }
    careerEl.appendChild(jobCard);

    // 4. Yetenekler / Beceriler Kartı
    const sk = gameState.skills || {};
    const skillsCard = document.createElement("div");
    skillsCard.className = "panel-card";
    skillsCard.innerHTML = `
        <div class="card-title-row">
            <span class="card-title">🎯 Kişisel Beceriler</span>
            <button type="button" class="btn-action-outline" style="padding:4px 10px; font-size:11px;" onclick="openSkillsModal()">+ Kursa Git</button>
        </div>
        <div class="card-desc" style="display:grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 6px;">
            <div>💻 Yazılım: <b>%${sk.coding || 10}</b></div>
            <div>🗣️ Hitabet: <b>%${sk.charisma || 20}</b></div>
            <div>🎸 Müzik: <b>%${sk.music || 10}</b></div>
            <div>⚽ Atletizm: <b>%${sk.athletics || 15}</b></div>
            <div>🥊 Savunma: <b>%${sk.martial_arts || 5}</b></div>
        </div>
    `;
    careerEl.appendChild(skillsCard);
}

// ----------------- VARLIKLAR VE PORTFÖY -----------------

function renderAssetsTab() {
    const assetsEl = document.getElementById("assetsContent");
    if (!assetsEl) return;
    assetsEl.innerHTML = "";

    const summaryCard = document.createElement("div");
    summaryCard.className = "panel-card";
    summaryCard.innerHTML = `
        <div class="card-title-row">
            <span class="card-title">💰 Finansal Bilanço</span>
            <span class="card-badge badge-green">Nakit: ₺ ${gameState.money.toLocaleString("tr-TR")}</span>
        </div>
        <div class="card-desc">
            Toplam Net Servet: <b>₺ ${gameState.net_worth.toLocaleString("tr-TR")}</b><br>
            Son Yıl Gelir: +₺ ${(gameState.annual_income_last || 0).toLocaleString("tr-TR")} • Son Yıl Gider: -₺ ${(gameState.annual_expense_last || 0).toLocaleString("tr-TR")}
        </div>
        <div style="display: flex; gap: 6px; margin-top: 10px;">
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openRealEstateModal()">🏠 Emlak Al</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openVehiclesModal()">🚗 Araç Al</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openStocksModal()">📈 Borsa</button>
        </div>
    `;
    assetsEl.appendChild(summaryCard);

    if (!gameState.assets || gameState.assets.length === 0) {
        const noAsset = document.createElement("div");
        noAsset.className = "panel-card";
        noAsset.innerHTML = `<p class="card-desc">Henüz tapulu bir gayrimenkulün veya aracın bulunmuyor.</p>`;
        assetsEl.appendChild(noAsset);
    } else {
        gameState.assets.forEach(asset => {
            const card = document.createElement("div");
            card.className = "panel-card";
            const icon = asset.asset_type === "Ev" ? "🏠" : "🏎️";
            const diff = asset.current_value - asset.purchase_price;
            const diffStr = diff >= 0 ? `+₺ ${diff.toLocaleString("tr-TR")}` : `-₺ ${Math.abs(diff).toLocaleString("tr-TR")}`;
            card.innerHTML = `
                <div class="card-title-row">
                    <span class="card-title">${icon} ${asset.name}</span>
                    <span class="card-badge badge-blue">₺ ${asset.current_value.toLocaleString("tr-TR")}</span>
                </div>
                <div class="card-desc">
                    Değer Değişimi: <b>${diffStr}</b> • Yıllık Masraf: ₺ ${asset.annual_cost.toLocaleString("tr-TR")}
                    ${asset.annual_income > 0 ? ` • Kira Geliri: +₺ ${asset.annual_income.toLocaleString("tr-TR")}/yıl` : ""}
                </div>
                <div style="margin-top: 8px;">
                    <button type="button" class="btn-action-outline" style="border-color: var(--accent-yellow); color: var(--accent-yellow); width:100%;" onclick="sellAsset('${asset.id}')">🏷️ Sat ve Nakte Çevir</button>
                </div>
            `;
            assetsEl.appendChild(card);
        });
    }
}

// ----------------- EVENT LISTENERS & CORE ACTIONS -----------------

function setupEventListeners() {
    const btnAgeUp = document.getElementById("btnAgeUp");
    if (btnAgeUp) {
        btnAgeUp.addEventListener("click", handleAgeUp);
    }

    document.querySelectorAll(".nav-item").forEach(item => {
        item.addEventListener("click", () => {
            sound.playClick();
            document.querySelectorAll(".nav-item").forEach(i => i.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

            item.classList.add("active");
            const target = item.getAttribute("data-tab");
            const targetEl = document.getElementById(target);
            if (targetEl) targetEl.classList.add("active");
        });
    });
}

async function handleAgeUp() {
    if (!gameState || !gameState.is_alive) return;
    sound.playAgeUp();

    try {
        const res = await fetch("/api/age_up", { method: "POST" });
        const data = await res.json();
        if (data.success) {
            gameState = data.character;
            renderAll();

            if (data.character_died) {
                sound.playDeath();
                openDeathModal();
            } else if (data.has_event) {
                openEventModal(data.event);
            }
        }
    } catch (e) {
        console.error("Yaşlanma hatası:", e);
    }
}

function openEventModal(ev) {
    const titleEl = document.getElementById("eventTitle");
    const descEl = document.getElementById("eventDesc");
    const choicesEl = document.getElementById("eventChoices");

    titleEl.innerHTML = `${ev.image_emoji || "⚡"} ${ev.title}`;
    descEl.textContent = ev.description;
    choicesEl.innerHTML = "";

    ev.choices.forEach((ch, idx) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "btn-choice";
        if (idx === 0) btn.setAttribute("autofocus", "");
        btn.textContent = ch.text;
        btn.onclick = () => submitEventChoice(ev.id, ch.id);
        choicesEl.appendChild(btn);
    });

    openDialogModal("eventModal");
}

async function submitEventChoice(eventId, choiceId) {
    sound.playClick();
    try {
        const res = await fetch("/api/event_choice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ event_id: eventId, choice_id: choiceId })
        });
        const data = await res.json();
        if (data.success) {
            gameState = data.character;
            await closeTopLayer(document.getElementById("eventModal"));
            showToast(data.message, "info");
            renderAll();
        }
    } catch (e) {
        console.error("Seçim iletilemedi:", e);
    }
}

async function performActivity(action, params = {}) {
    sound.playClick();
    try {
        const res = await fetch("/api/activity", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action, params })
        });
        const data = await res.json();
        if (data.character) {
            gameState = data.character;
            renderAll();
        }

        if (data.success) {
            sound.playSuccess();
            showToast(data.message, "success");
        } else {
            sound.playFail();
            showToast(data.message, "error");
        }
        return data;
    } catch (e) {
        console.error("Aktivite hatası:", e);
    }
}

// ----------------- KİŞİ ETKİLEŞİM MODALI -----------------

function openPersonModal(personId) {
    sound.playClick();
    activePersonId = personId;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("personModalName").textContent = `${getRelationEmoji(person.relation)} ${person.name}`;
    document.getElementById("personModalDetails").textContent = `${person.relation} • ${person.age} Yaşında ${person.job ? `• Meslek: ${person.job}` : ""}`;
    document.getElementById("personModalLevel").textContent = `%${person.relationship_level}`;
    document.getElementById("personModalBar").style.width = `${person.relationship_level}%`;

    const actionsContainer = document.getElementById("personModalActions");
    actionsContainer.innerHTML = "";

    if (!person.is_alive) {
        actionsContainer.innerHTML = `<p class="card-desc">Bu kişi vefat etti. Huzur içinde yatsın.</p>`;
    } else {
        const actions = [
            { id: "chat", text: "💬 Sohbet Et & Dertleş" },
            { id: "spend_time", text: "🍿 Birlikte Vakit Geçir" },
            { id: "give_gift", text: "🎁 Hediye Al (2.500 TL)" },
            { id: "ask_money", text: "💸 Harçlık / Destek İste" },
            { id: "argue", text: "🤬 Tartış ve Hesap Sor" }
        ];

        if (person.relation === "Sevgili") {
            actions.push({ id: "propose", text: "💍 Pırlanta Yüzükle Evlenme Teklifi Et (20.000 TL)" });
            actions.push({ id: "breakup", text: "💔 Ayrıl" });
        } else if (person.relation === "Eş") {
            actions.push({ id: "try_baby", text: "🍼 Çocuk Yapmayı Dene" });
            actions.push({ id: "breakup", text: "💔 Boşanma Davası Aç" });
        }

        actions.forEach(act => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "btn-choice";
            btn.textContent = act.text;
            btn.onclick = () => handlePersonAction(act.id);
            actionsContainer.appendChild(btn);
        });
    }

    openDialogModal("personModal");
}

async function handlePersonAction(actId) {
    if (!activePersonId) return;
    if (actId === "propose") {
        await performActivity("propose_marriage", { ring_cost: 20000 });
        closeModal("personModal");
        return;
    }
    if (actId === "try_baby") {
        await performActivity("try_baby");
        closeModal("personModal");
        return;
    }
    await performActivity("interact_person", {
        person_id: activePersonId,
        person_action: actId
    });
    closeModal("personModal");
}

// ----------------- İNTERAKTİF BLACKJACK (21) MASASI -----------------

function openBlackjackModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🃏 Kumarhane: İnteraktif 21 (Blackjack)";
    renderBlackjackTable();
    openDialogModal("genericModal");
}

function renderCardPill(cardStr) {
    const isRed = cardStr.includes("♥️") || cardStr.includes("♦️");
    return `<span class="playing-card ${isRed ? 'red-suit' : ''}">${cardStr}</span>`;
}

function renderBlackjackTable(lastMessage = "") {
    const body = document.getElementById("genericModalBody");
    const bj = gameState.blackjack || { active: false };

    let tableHtml = "";
    if (bj.active || (bj.player_cards && bj.player_cards.length > 0)) {
        const dealerCardsHtml = bj.active
            ? `${renderCardPill(bj.dealer_cards[0])} <span class="playing-card">🂠</span>`
            : bj.dealer_cards.map(renderCardPill).join("");

        const playerCardsHtml = bj.player_cards.map(renderCardPill).join("");

        tableHtml = `
            <div class="bj-table">
                <div style="font-size:12px; color:#a7f3d0; font-weight:700;">KRUPİYE (${bj.active ? bj.dealer_total + '+' : bj.dealer_total})</div>
                <div class="bj-cards-row">${dealerCardsHtml}</div>
                <div style="font-size:12px; color:#a7f3d0; font-weight:700;">SENİN ELİN (${bj.player_total}) • Bahis: ₺ ${(bj.bet || 0).toLocaleString("tr-TR")}</div>
                <div class="bj-cards-row">${playerCardsHtml}</div>
                ${lastMessage ? `<div style="font-size:13px; font-weight:700; color:#fff; margin-top:6px;">${lastMessage}</div>` : ""}
            </div>
        `;
    }

    let controlsHtml = "";
    if (bj.active) {
        controlsHtml = `
            <div style="display:flex; gap:10px;">
                <button type="button" class="btn-primary" style="background:var(--accent-green);" onclick="bjMove('hit')">🃏 Kart Çek (Hit)</button>
                <button type="button" class="btn-primary" style="background:var(--accent-yellow); color:#000;" onclick="bjMove('stand')">✋ Kal (Stand)</button>
            </div>
        `;
    } else {
        controlsHtml = `
            <p class="card-desc" style="text-align:center; margin-bottom:10px;">Yeni el başlatmak için bahis miktarını seç:</p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <button type="button" class="btn-choice" style="text-align:center" onclick="bjMove('start', 2000)">₺ 2.000 Bahis</button>
                <button type="button" class="btn-choice" style="text-align:center" onclick="bjMove('start', 10000)">₺ 10.000 Bahis</button>
                <button type="button" class="btn-choice" style="text-align:center" onclick="bjMove('start', 50000)">₺ 50.000 Bahis</button>
                <button type="button" class="btn-choice" style="text-align:center" onclick="bjMove('start', 200000)">₺ 200.000 Bahis</button>
            </div>
        `;
    }

    body.innerHTML = `${tableHtml}${controlsHtml}`;
}

async function bjMove(subAction, bet = 2000) {
    const res = await performActivity("blackjack", { sub_action: subAction, bet });
    renderBlackjackTable(res ? res.message : "");
}

// ----------------- BORSA VE SVG SPARKLINE GRAFİĞİ -----------------

function createSparklineSvg(history) {
    if (!history || history.length < 2) return "";
    const w = 110, h = 32;
    const min = Math.min(...history);
    const max = Math.max(...history);
    const range = max - min || 1;
    const pts = history.map((val, idx) => {
        const x = (idx / (history.length - 1)) * (w - 6) + 3;
        const y = h - 4 - ((val - min) / range) * (h - 8);
        return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(" ");
    const isUp = history[history.length - 1] >= history[0];
    const stroke = isUp ? "#10b981" : "#ef4444";
    return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><polyline fill="none" stroke="${stroke}" stroke-width="2.2" points="${pts}"/></svg>`;
}

function openStocksModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "📈 Borsa İstanbul & Kripto Piyasası";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    if (!gameState.stocks) return;

    Object.values(gameState.stocks).forEach(stock => {
        const card = document.createElement("div");
        card.className = "panel-card";
        const valTotal = Math.round(stock.shares * stock.current_price);
        let pnlHtml = "";
        if (stock.shares > 0 && stock.avg_buy_price > 0) {
            const pct = (((stock.current_price - stock.avg_buy_price) / stock.avg_buy_price) * 100).toFixed(1);
            const color = pct >= 0 ? "var(--accent-green)" : "var(--accent-red)";
            pnlHtml = ` • Maliyet: ₺ ${stock.avg_buy_price.toFixed(2)} (<span style="color:${color}; font-weight:700;">${pct >= 0 ? '+' : ''}%${pct}</span>)`;
        }

        card.innerHTML = `
            <div class="card-title-row">
                <div>
                    <div class="card-title">${stock.symbol}</div>
                    <div style="font-size:11px; color:var(--text-secondary);">${stock.name}</div>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                    ${createSparklineSvg(stock.history)}
                    <span class="card-badge badge-green">₺ ${stock.current_price.toFixed(2)}</span>
                </div>
            </div>
            <p class="card-desc">Elindeki Lot: <b>${stock.shares}</b> (₺ ${valTotal.toLocaleString("tr-TR")})${pnlHtml}</p>
            <div style="display: flex; gap: 6px; margin-top: 8px;">
                <button type="button" class="btn-action-outline" style="flex:1" onclick="tradeStock('${stock.symbol}', 'buy', 15000)">🟢 Al (15B TL)</button>
                <button type="button" class="btn-action-outline" style="flex:1" onclick="tradeStock('${stock.symbol}', 'buy', 100000)">🟢 Al (100B TL)</button>
                <button type="button" class="btn-action-outline" style="flex:1; border-color:var(--accent-red); color:#fca5a5;" onclick="tradeStock('${stock.symbol}', 'sell', 0)">🔴 Tümünü Sat</button>
            </div>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

async function tradeStock(symbol, type, amountOrShares) {
    if (type === "buy") {
        await performActivity("buy_stock", { symbol, amount: amountOrShares });
    } else {
        await performActivity("sell_stock", { symbol, shares: amountOrShares });
    }
    openStocksModal();
}

// ----------------- EMLAK, ARAÇ, İŞ, ŞİRKET, KULÜP & DİĞER MODALLAR -----------------

function openRealEstateModal() {
    sound.playClick();
    if (!marketData || !marketData.real_estate) return;
    document.getElementById("genericModalTitle").textContent = "🏠 Emlakçı & Gayrimenkul";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    marketData.real_estate.forEach((prop, idx) => {
        const card = document.createElement("div");
        card.className = "panel-card";
        card.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${prop.name}</span>
                <span class="card-badge badge-green">₺ ${prop.price.toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc">Yıllık Kira Geliri: <b>+₺ ${prop.annual_rent.toLocaleString("tr-TR")}</b> • Aidat/Vergi: ₺ ${prop.annual_cost.toLocaleString("tr-TR")}</p>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="buyHouse(${idx})">Satın Al</button>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

async function buyHouse(index) {
    await performActivity("buy_house", { index });
    closeModal("genericModal");
}

function openVehiclesModal() {
    sound.playClick();
    if (!marketData || !marketData.vehicles) return;
    document.getElementById("genericModalTitle").textContent = "🚗 Oto Galeri & Lüks Araçlar";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    marketData.vehicles.forEach((car, idx) => {
        const card = document.createElement("div");
        card.className = "panel-card";
        card.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${car.name}</span>
                <span class="card-badge badge-blue">₺ ${car.price.toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc">Sınıf: ${car.speed} • Yıllık Kasko/Bakım: ₺ ${car.annual_cost.toLocaleString("tr-TR")}</p>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="buyCar(${idx})">Satın Al</button>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

async function buyCar(index) {
    await performActivity("buy_car", { index });
    closeModal("genericModal");
}

async function sellAsset(assetId) {
    await performActivity("sell_asset", { asset_id: assetId });
}

function openBusinessModal() {
    sound.playClick();
    if (!marketData || !marketData.businesses) return;
    document.getElementById("genericModalTitle").textContent = "🏢 Girişimcilik & Şirket Kur";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    marketData.businesses.forEach(b => {
        const card = document.createElement("div");
        card.className = "panel-card";
        card.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${b.name}</span>
                <span class="card-badge badge-yellow">Sermaye: ₺ ${b.cost.toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc">Sektör: ${b.sector} • Beklenen Yıllık Kâr: <b>+₺ ${b.base_profit.toLocaleString("tr-TR")}/yıl</b></p>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="createBusiness('${b.id}')">Şirketi Kur</button>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

async function createBusiness(bizId) {
    await performActivity("start_business", { biz_id: bizId });
    closeModal("genericModal");
}

function openJobsModal() {
    sound.playClick();
    if (!marketData || !marketData.jobs) return;
    document.getElementById("genericModalTitle").textContent = "💼 Tam Zamanlı İş İlanları";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    marketData.jobs.forEach(j => {
        const card = document.createElement("div");
        card.className = "panel-card";
        card.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${j.title}</span>
                <span class="card-badge badge-green">₺ ${j.salary.toLocaleString("tr-TR")}/yıl</span>
            </div>
            <p class="card-desc">Sektör: ${j.category} • Eğitim Şartı: ${j.required_education}</p>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="startInterview('${j.id}')">Başvur & Mülakata Gir</button>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

function startInterview(jobId) {
    sound.playClick();
    const job = marketData.jobs.find(j => j.id === jobId);
    if (!job) return;

    document.getElementById("genericModalTitle").textContent = `🎤 İş Mülakatı: ${job.title}`;
    const body = document.getElementById("genericModalBody");

    let optsHtml = "";
    job.options.forEach((optText, optIdx) => {
        optsHtml += `
            <button type="button" class="btn-choice" style="margin-bottom: 8px;" onclick="submitJobInterview('${job.id}', ${optIdx})">
                ${optText}
            </button>
        `;
    });

    body.innerHTML = `
        <div style="padding: 4px;">
            <p style="font-size: 14.5px; font-weight: 700; margin-bottom: 12px; color: #fff;">
                İK Yöneticisi: "${job.interview_q}"
            </p>
            ${optsHtml}
        </div>
    `;
}

async function submitJobInterview(jobId, chosenOpt) {
    await performActivity("apply_job", { job_id: jobId, chosen_opt: chosenOpt });
    closeModal("genericModal");
}

function openPartTimeModal() {
    sound.playClick();
    if (!marketData || !marketData.part_time_jobs) return;
    document.getElementById("genericModalTitle").textContent = "⏱️ Yarı Zamanlı (Part-Time) İşler";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    marketData.part_time_jobs.forEach(pt => {
        const card = document.createElement("div");
        card.className = "panel-card";
        card.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${pt.title}</span>
                <span class="card-badge badge-green">+₺ ${pt.salary.toLocaleString("tr-TR")}/yıl</span>
            </div>
            <p class="card-desc">Minimum Yaş: ${pt.min_age}</p>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="selectPartTime('${pt.id}')">İşe Başla</button>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

async function selectPartTime(ptId) {
    await performActivity("apply_part_time", { pt_id: ptId });
    closeModal("genericModal");
}

function openUniversityModal() {
    sound.playClick();
    if (!marketData || !marketData.universities) return;
    document.getElementById("genericModalTitle").textContent = "🏛️ Üniversite Fakülteleri";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    marketData.universities.forEach(u => {
        const card = document.createElement("div");
        card.className = "panel-card";
        card.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${u.name}</span>
                <span class="card-badge badge-blue">Taban Zeka: %${u.smarts_required}</span>
            </div>
            <p class="card-desc">Eğitim Süresi: ${u.duration} Yıl • Alan: ${u.unlocked_category}</p>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="enrollUniversity('${u.id}')">Kayıt Ol</button>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

async function enrollUniversity(facultyId) {
    await performActivity("apply_university", { faculty_id: facultyId });
    closeModal("genericModal");
}

function openClubsModal() {
    sound.playClick();
    if (!marketData || !marketData.school_clubs) return;
    document.getElementById("genericModalTitle").textContent = "🏅 Öğrenci Kulüpleri & Takımlar";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    marketData.school_clubs.forEach(c => {
        const card = document.createElement("div");
        card.className = "panel-card";
        card.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${c.name}</span>
                <span class="card-badge badge-purple">+Zeka & Beceri</span>
            </div>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="joinClub('${c.id}')">Kulübe Katıl</button>
        `;
        body.appendChild(card);
    });
    openDialogModal("genericModal");
}

async function joinClub(clubId) {
    await performActivity("join_club", { club_id: clubId });
    closeModal("genericModal");
}

function openSkillsModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🎯 Kişisel Gelişim & Akademi Kursları";
    const body = document.getElementById("genericModalBody");
    const courses = [
        { key: "coding", name: "💻 Yazılım & Yapay Zeka Bootcamp", cost: "8.000 TL" },
        { key: "charisma", name: "🗣️ Hitabet, Diksiyon & Liderlik", cost: "6.000 TL" },
        { key: "music", name: "🎸 Enstrüman & Şan Eğitimi", cost: "5.000 TL" },
        { key: "martial_arts", name: "🥊 Kickboks & Yakın Savunma", cost: "5.500 TL" }
    ];
    body.innerHTML = courses.map(c => `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">${c.name}</span>
                <span class="card-badge badge-green">${c.cost}</span>
            </div>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="takeSkillCourse('${c.key}')">Kursa Katıl</button>
        </div>
    `).join("");
    openDialogModal("genericModal");
}

async function takeSkillCourse(skillKey) {
    await performActivity("train_skill", { skill_key: skillKey });
    closeModal("genericModal");
}

function openPetsModal() {
    sound.playClick();
    if (!marketData || !marketData.pet_breeds) return;
    document.getElementById("genericModalTitle").textContent = "🐾 Hayvan Barınağı & Sahiplenme";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = marketData.pet_breeds.map((p, idx) => `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">${p.breed} (${p.species})</span>
                <span class="card-badge badge-green">${p.cost === 0 ? 'Ücretsiz Barınak' : '₺ ' + p.cost.toLocaleString('tr-TR')}</span>
            </div>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="adoptPet(${idx})">Yuva Ol & Sahiplen</button>
        </div>
    `).join("");
    openDialogModal("genericModal");
}

async function adoptPet(idx) {
    await performActivity("adopt_pet", { breed_idx: idx });
    closeModal("genericModal");
}

function openPlasticSurgeryModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "💉 Estetik & Plastik Cerrahi";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = `
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">👃 Burun Estetiği (Rinoplasti)</span><span class="card-badge badge-green">₺ 45.000</span></div>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="performPlasticSurgery('rhinoplasty')">Operasyon Ol</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">✨ Botoks ve Yüz Dolgusu</span><span class="card-badge badge-green">₺ 15.000</span></div>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="performPlasticSurgery('botox')">Uygulat</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">💇 Mikro FUE Saç Ekimi</span><span class="card-badge badge-green">₺ 35.000</span></div>
            <button type="button" class="btn-primary" style="margin-top: 8px;" onclick="performPlasticSurgery('hair_transplant')">Saç Ektir</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function performPlasticSurgery(procedure) {
    await performActivity("plastic_surgery", { procedure });
    closeModal("genericModal");
}

function openCrimeModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🦹 Yeraltı & Cezaevi";
    const body = document.getElementById("genericModalBody");

    if (gameState.is_in_prison) {
        body.innerHTML = `
            <div class="panel-card" style="border-color: var(--accent-red);">
                <h4>🚨 Cezaevindesin (Kalan: ${gameState.prison_years_left} Yıl)</h4>
                <p class="card-desc" style="margin: 8px 0;">Özgürlüğüne kavuşmak için bir hamle seç:</p>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <button type="button" class="btn-choice" onclick="doPrisonAction('escape_tunnel')">🏃💨 Havalandırma Tünelinden Firar Dene</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('escape_disguise')">🎭 Gardiyan Üniformasıyla Firar Dene</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('appeal_lawyer')">⚖️ Ünlü Ceza Avukatı Tut & Temyiz (60.000 TL)</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('bribe_guard')">👮 Gardiyana Rüşvet Ver (30.000 TL -> -1 Yıl)</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('library')">📖 Kütüphanede Hukuk Kitapları Oku</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('yard_workout')">🏋️ Avluda Ağırlık Çalış</button>
                </div>
            </div>
        `;
    } else {
        body.innerHTML = `
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">👛 Yankesicilik</span><span class="card-badge badge-blue">Düşük Risk</span></div>
                <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="doCrime('pickpocket')">Kalabalıkta Cüzdan Çarp</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">🏎️ Lüks Oto Hırsızlığı</span><span class="card-badge badge-yellow">Orta Risk</span></div>
                <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="doCrime('grand_theft_auto')">Düz Kontakla Araba Çal</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">🏦 Merkez Bankası Soygunu</span><span class="card-badge badge-red">Yüksek Risk / Milyonluk Vurgun</span></div>
                <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="doCrime('bank_robbery')">Soygun Planını Başlat!</button>
            </div>
        `;
    }
    openDialogModal("genericModal");
}

async function doCrime(type) {
    await performActivity("crime", { crime_type: type });
    closeModal("genericModal");
}

async function doPrisonAction(act) {
    if (act === "escape_tunnel") {
        await performActivity("prison_escape", { route: "tunnel" });
    } else if (act === "escape_disguise") {
        await performActivity("prison_escape", { route: "disguise" });
    } else {
        await performActivity("prison_act", { activity: act });
    }
    closeModal("genericModal");
}

function openSocialMediaModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "📱 Sosyal Medya & İçerik Üretimi";
    const body = document.getElementById("genericModalBody");

    const ig = gameState.social_media?.Instagram?.followers || 0;
    const yt = gameState.social_media?.YouTube?.followers || 0;
    const tt = gameState.social_media?.TikTok?.followers || 0;

    body.innerHTML = `
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">📸 Instagram</span><span class="card-badge badge-blue">${ig.toLocaleString("tr-TR")} Takipçi</span></div>
            <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="postSocial('Instagram')">Reels & Hikaye Paylaş</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">▶️ YouTube</span><span class="card-badge badge-red">${yt.toLocaleString("tr-TR")} Abone</span></div>
            <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="postSocial('YouTube')">Vlog / İçerik Videosu Yükle</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">🎵 TikTok</span><span class="card-badge badge-purple">${tt.toLocaleString("tr-TR")} Takipçi</span></div>
            <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="postSocial('TikTok')">Viral Akım Videosu Çek</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function postSocial(platform) {
    await performActivity("social_post", { platform });
    openSocialMediaModal();
}

function openVacationModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "✈️ Tatil & Seyahat Rotaları";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = `
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">🏕️ Ege Kıyısında Çadır Kampı</span><span class="card-badge badge-green">₺ 5.000</span></div>
            <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="goVacation('camping')">Kampa Git</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">🏖️ Antalya 5* Ultra Her Şey Dahil</span><span class="card-badge badge-blue">₺ 30.000</span></div>
            <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="goVacation('antalya')">Tatile Çık</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">🗼 Paris Kültür & Sanat Turu</span><span class="card-badge badge-yellow">₺ 75.000</span></div>
            <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="goVacation('paris')">Uçak Biletini Al</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">🏝️ Maldivler Su Üstü Özel Villa</span><span class="card-badge badge-purple">₺ 200.000</span></div>
            <button type="button" class="btn-choice" style="margin-top: 8px;" onclick="goVacation('maldives')">Lüks Tatile Çık</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function goVacation(destination) {
    await performActivity("vacation", { destination });
    closeModal("genericModal");
}

function openWillModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "📜 Noter & Vasiyetname";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Vefat ettiğinde tüm mal varlığının ve nakit servetinin kime devredileceğini belirle:</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <button type="button" class="btn-choice" onclick="saveWill('all_children')">👶 Tüm Çocuklarıma Eşit Olarak Paylaştır</button>
            <button type="button" class="btn-choice" onclick="saveWill('spouse')">💍 Yalnızca Eşime Bırak</button>
            <button type="button" class="btn-choice" onclick="saveWill('charity')">🏛️ Hayır Kurumu ve Eğitim Vakfına Bağışla</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function saveWill(target) {
    await performActivity("set_will", { target });
    closeModal("genericModal");
}

// ----------------- BAŞARIMLAR & MEZARLIK (GEÇMİŞ HAYATLAR) -----------------

function openAchievementsModal() {
    sound.playClick();
    if (!marketData || !marketData.achievements) return;
    document.getElementById("genericModalTitle").textContent = "🏆 Hayat Başarımları";
    const body = document.getElementById("genericModalBody");
    const unlocked = new Set(gameState.achievements || []);

    body.innerHTML = marketData.achievements.map(a => {
        const has = unlocked.has(a.id);
        return `
            <div class="panel-card" style="opacity: ${has ? '1' : '0.48'}; border-color: ${has ? 'var(--accent-yellow)' : 'var(--border-color)'};">
                <div class="card-title-row">
                    <span class="card-title">${a.icon || "🏅"} ${a.title}</span>
                    <span class="card-badge ${has ? 'badge-green' : ''}">${has ? 'Açıldı ✓' : 'Kilitli 🔒'}</span>
                </div>
                <p class="card-desc">${a.desc}</p>
            </div>
        `;
    }).join("");
    openDialogModal("genericModal");
}

async function openGraveyardModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "⚰️ Aile Mezarlığı & Geçmiş Hayatlar";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = `<p class="card-desc">Yükleniyor...</p>`;
    openDialogModal("genericModal");

    try {
        const res = await fetch("/api/graveyard");
        const data = await res.json();
        if (!data.graveyard || data.graveyard.length === 0) {
            body.innerHTML = `<div class="panel-card"><p class="card-desc">Henüz vefat eden bir geçmiş karakter kaydı bulunmuyor.</p></div>`;
            return;
        }
        body.innerHTML = data.graveyard.map(g => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">🪦 ${g.name} (${g.age} Yaş)</span>
                    <span class="card-badge badge-yellow">₺ ${g.net_worth.toLocaleString("tr-TR")}</span>
                </div>
                <div class="card-desc">
                    <b>${g.title}</b> (${g.birth_year} - ${g.death_year})<br>
                    ${g.death_reason}
                </div>
            </div>
        `).join("");
    } catch (e) {
        body.innerHTML = `<p class="card-desc">Mezarlık bilgisi alınamadı.</p>`;
    }
}

// ----------------- ÖLÜM VE YENİ HAYAT MODALLARI -----------------

function openDeathModal() {
    document.getElementById("tombName").textContent = `${gameState.first_name} ${gameState.last_name}`;
    document.getElementById("tombDates").textContent = `${gameState.birth_year} - ${gameState.current_year} (${gameState.age} Yaşında)`;
    document.getElementById("tombTitle").textContent = gameState.tombstone_title || "Onurlu Bir Vatandaş";
    document.getElementById("tombReason").textContent = gameState.death_reason || "Doğal nedenlerle vefat etti.";
    document.getElementById("tombNetWorth").textContent = `Bıraktığı Miras: ₺ ${gameState.net_worth.toLocaleString("tr-TR")}`;

    openDialogModal("deathModal");
}

async function continueAsChild() {
    sound.playClick();
    try {
        const res = await fetch("/api/reincarnate", { method: "POST" });
        const data = await res.json();
        if (data.success) {
            gameState = data.character;
            await closeTopLayer(document.getElementById("deathModal"));
            showToast(data.message, "success");
            renderAll();
        }
    } catch (e) {
        console.error("Miras hatası:", e);
    }
}

function openNewCustomLifeModal() {
    sound.playClick();
    const citySelect = document.getElementById("inputCity");
    citySelect.innerHTML = "";

    if (marketData && marketData.cities) {
        marketData.cities.forEach(c => {
            const opt = document.createElement("option");
            opt.value = c.city;
            opt.textContent = `${c.city}, ${c.country}`;
            citySelect.appendChild(opt);
        });
    }
    openDialogModal("customLifeModal");
}

async function submitCustomLife() {
    const fn = document.getElementById("inputFirstName").value;
    const ln = document.getElementById("inputLastName").value;
    const gender = document.getElementById("inputGender").value;
    const city = document.getElementById("inputCity").value;

    try {
        const res = await fetch("/api/new_game", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                first_name: fn || null,
                last_name: ln || null,
                gender: gender || null,
                city: city || null
            })
        });
        const data = await res.json();
        if (data.success) {
            gameState = data.character;
            await closeTopLayer(document.getElementById("customLifeModal"));
            await closeTopLayer(document.getElementById("deathModal"));
            showToast("Yeni hayatına başarıyla başladın!", "success");
            renderAll();
        }
    } catch (e) {
        console.error("Yeni karakter oluşturulamadı:", e);
    }
}

function showToast(text, type = "info") {
    const container = document.getElementById("toastContainer");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>🔔</span><div>${text}</div>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}
