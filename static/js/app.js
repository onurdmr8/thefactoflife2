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

const THEMES = ["midnight", "emerald", "royal", "rose"];
let currentThemeIndex = 0;

function cycleTheme() {
    sound.playClick();
    currentThemeIndex = (currentThemeIndex + 1) % THEMES.length;
    const theme = THEMES[currentThemeIndex];
    if (theme === "midnight") {
        document.body.removeAttribute("data-theme");
    } else {
        document.body.setAttribute("data-theme", theme);
    }
    try {
        localStorage.setItem("bitlife_tr_theme", theme);
    } catch (e) {}
}

function openSettingsMenuModal() {
    sound.playClick();
    openDialogModal("settingsMenuModal");
}

function toggleSound() {
    sound.muted = !sound.muted;
    const btn = document.getElementById("btnSoundToggle");
    if (btn) {
        btn.textContent = sound.muted ? "🔇 Ses: Kapalı" : "🔊 Ses: Açık";
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
        let html = `<span class="status-chip" style="cursor:pointer;" onclick="openFamilyTreeModal()">🌳 ${gameState.generation || 1}. Kuşak</span>`;
        html += `<span class="status-chip">☯️ Karma: %${gameState.karma}</span>`;
        if (gameState.outfit_style) {
            html += `<span class="status-chip" style="cursor:pointer;" onclick="openWardrobeModal()" title="Tarzını Değiştir">${gameState.outfit_style}</span>`;
        }

        const mainPartner = (gameState.relationships || []).find(p => p.is_alive && ["Eş", "Nişanlı", "Sevgili", "Flört"].includes(p.relation));
        if (mainPartner) {
            html += `<span class="status-chip" style="background:rgba(236,72,153,0.18); color:#fbcfe8; cursor:pointer;" onclick="openPersonModal('${mainPartner.id}')">${getRelationEmoji(mainPartner.relation)} ${mainPartner.relation}: ${mainPartner.name.split(" ")[0]}</span>`;
        } else if (gameState.age >= 16) {
            html += `<span class="status-chip">💔 Bekar</span>`;
        }

        if (gameState.fame > 0) {
            html += `<span class="status-chip chip-gold" style="cursor:pointer;" onclick="openFameModal()">🌟 Şöhret: %${gameState.fame}</span>`;
        }
        if (gameState.political_office) {
            html += `<span class="status-chip" style="background:rgba(59,130,246,0.22); color:#93c5fd; cursor:pointer;" onclick="openPoliticsModal()">${gameState.political_office} (%${gameState.approval_rating})</span>`;
        }
        if (gameState.is_in_prison) {
            html += `<span class="status-chip chip-danger" style="cursor:pointer;" onclick="openPrisonModal()" title="Koğuş Hiyerarşisi">🚨 Cezaevinde: ${gameState.prison_role || 'Mahkum'} (${gameState.prison_years_left} Yıl)</span>`;
        }
        if (gameState.chronic_conditions && gameState.chronic_conditions.length > 0) {
            gameState.chronic_conditions.forEach(cond => {
                html += `<span class="status-chip" style="background:rgba(239,68,68,0.18); color:#fca5a5; cursor:pointer;" onclick="openAlternativeMedicineModal()" title="Alternatif Tıp Tedavisi">⚠️ ${cond}</span>`;
            });
        }
        if (gameState.nursing_home) {
            html += `<span class="status-chip" style="background:rgba(99,102,241,0.2); color:#c7d2fe; cursor:pointer;" onclick="openElderlyCareModal()" title="Huzurevi">🏡 ${gameState.nursing_home}</span>`;
        }
        if (gameState.elderly_caregiver) {
            html += `<span class="status-chip" style="background:rgba(16,185,129,0.2); color:#a7f3d0; cursor:pointer;" onclick="openElderlyCareModal()" title="Hasta Bakıcı">👩‍⚕️ Yatılı Hasta Bakıcı</span>`;
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

// ----------------- İLİŞKİLER, FLÖRT, KISMETAPP VE EVCİL HAYVANLAR -----------------

function getPersonalityLabel(personalityId) {
    if (!marketData || !marketData.personalities) return personalityId || "Uyumlu";
    const found = marketData.personalities.find(p => p.id === personalityId);
    return found ? `${found.emoji} ${found.name}` : (personalityId || "Uyumlu");
}

function getMoodBadge(person) {
    if (!person.is_alive) return `<span class="person-mood-pill badge-red">🕊️ Vefat Etti</span>`;
    const lvl = person.relationship_level;
    const isRom = ["Flört", "Sevgili", "Nişanlı", "Eş"].includes(person.relation);
    if (lvl >= 85) return `<span class="person-mood-pill badge-green">${isRom ? "❤️‍🔥 Sırılsıklam Aşık" : "🥰 Çok Yakın"} (%${lvl})</span>`;
    if (lvl >= 60) return `<span class="person-mood-pill badge-blue">${isRom ? "💕 Mutlu & Uyumlu" : "😊 Samimi"} (%${lvl})</span>`;
    if (lvl >= 35) return `<span class="person-mood-pill badge-yellow">😐 Mesafeli (%${lvl})</span>`;
    return `<span class="person-mood-pill badge-red">😡 Kırgın / Soğuk (%${lvl})</span>`;
}

function renderPersonCard(person) {
    const card = document.createElement("article");
    card.className = "panel-card person-card";

    const extraBadges = [];
    if (person.cohabiting && person.is_alive) extraBadges.push(`<span class="person-chip" style="background:rgba(16,185,129,0.18); color:#6ee7b7;">🏠 Aynı Evde</span>`);
    if (person.has_prenup && person.relation === "Eş") extraBadges.push(`<span class="person-chip" style="background:rgba(245,158,11,0.18); color:#fcd34d;">📜 Sözleşmeli</span>`);
    if (person.personality) extraBadges.push(`<span class="person-chip">${getPersonalityLabel(person.personality)}</span>`);
    if (person.love_language) extraBadges.push(`<span class="person-chip">💝 ${person.love_language}</span>`);
    if (person.met_family && ["Flört", "Sevgili", "Nişanlı", "Eş"].includes(person.relation)) {
        extraBadges.push(`<span class="person-chip">👨‍👩‍👧 Aile Onayı: %${person.family_approval ?? 65}</span>`);
    }
    if (person.years_together && person.years_together > 0 && ["Flört", "Sevgili", "Nişanlı", "Eş"].includes(person.relation)) {
        extraBadges.push(`<span class="person-chip">⏳ ${person.years_together} Yıl</span>`);
    }

    const relBarColor = person.relationship_level >= 65 ? "var(--accent-green)" : (person.relationship_level >= 35 ? "var(--accent-yellow)" : "var(--accent-red)");
    const isPartner = ["Flört", "Sevgili", "Nişanlı", "Eş"].includes(person.relation);
    const lastChat = (person.chat_history && person.chat_history.length > 0)
        ? person.chat_history[person.chat_history.length - 1].text
        : null;

    let quickActionsHtml = "";
    if (person.is_alive) {
        if (isPartner) {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="openDetailedKissModal('${person.id}')">💋 Öp</button>
                    <button type="button" class="btn-quick-rel" onclick="openDetailedDateModal('${person.id}')">🌹 Randevu</button>
                    <button type="button" class="btn-quick-rel" onclick="openDetailedFightModal('${person.id}')">💥 Kavga</button>
                    <button type="button" class="btn-quick-rel" onclick="openCustomGiftModal('${person.id}')">🎁 Hediye</button>
                </footer>
            `;
        } else if (["Anne", "Baba"].includes(person.relation)) {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'parent_blessing'})">🙏 El Öp</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'chat'})">💬 Sohbet</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'ask_money'})">💸 Harçlık</button>
                </footer>
            `;
        } else if (person.relation === "Çocuk") {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'educate_child'})">📚 Eğit (+Zeka)</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'spend_time'})">🍿 Vakit Geçir</button>
                </footer>
            `;
        } else if (["Eski Sevgili", "Eski Eş"].includes(person.relation)) {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="openDetailedKissModal('${person.id}')">💋 Öp</button>
                    <button type="button" class="btn-quick-rel" onclick="openDetailedFightModal('${person.id}')">🤬 Kavga Et</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'text_ex'})">📱 Barışma Mesajı</button>
                </footer>
            `;
        } else if (person.relation === "Sınıf Arkadaşı") {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="performActivity('classmate_action', {person_id: '${person.id}', action_id: 'hangout_canteen'})">🥪 Tost Ismarla</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('classmate_action', {person_id: '${person.id}', action_id: 'cheat_homework'})">📝 Kopya İste</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('classmate_action', {person_id: '${person.id}', action_id: 'school_crush'})">💌 Aşk Mektubu</button>
                </footer>
            `;
        } else if (person.relation === "Öğretmen") {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="performActivity('classmate_action', {person_id: '${person.id}', action_id: 'suck_up_teacher'})">🍎 Yağ Çek</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('classmate_action', {person_id: '${person.id}', action_id: 'prank_teacher'})">🤪 Şaka Yap</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('consolidated_chat', {person_id: '${person.id}'})">💬 Akıl Danış</button>
                </footer>
            `;
        } else if (person.relation === "İş Arkadaşı") {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="openCoworkerProjectModal('${person.id}')">💼 Proje</button>
                    <button type="button" class="btn-quick-rel" onclick="openCoworkerGossipModal('${person.id}')">☕ Dedikodu</button>
                    <button type="button" class="btn-quick-rel" onclick="openCoworkerHangoutModal('${person.id}')">🍻 Çıkış</button>
                </footer>
            `;
        } else if (person.relation === "Patron") {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="openBossMentorshipModal('${person.id}')">👑 Mentorluk</button>
                    <button type="button" class="btn-quick-rel" onclick="openBossNegotiationModal('${person.id}')">📈 Zam & Terfi</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('boss_action', {person_id: '${person.id}', action_id: 'annual_bonus'})">💰 Prim İste</button>
                </footer>
            `;
        } else if (person.relation === "Arkadaş") {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="openFriendActionModal('${person.id}')">🤝 Dostluk</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('friend_to_lover', {person_id: '${person.id}', action_id: 'friend_hookup'})">🔥 Kaçamak</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('friend_to_lover', {person_id: '${person.id}', action_id: 'confess_friend'})">💘 Aşk İtirafı</button>
                </footer>
            `;
        } else {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="openDetailedKissModal('${person.id}')">💋 Öp</button>
                    <button type="button" class="btn-quick-rel" onclick="openSocialHangoutModal('${person.id}')">🎉 Dışarı Çıkar</button>
                    <button type="button" class="btn-quick-rel" onclick="openDetailedFightModal('${person.id}')">🤬 Tartış</button>
                </footer>
            `;
        }
    }

    card.innerHTML = `
        <header class="card-title-row">
            <h4 class="card-title">
                <button type="button" class="card-primary-btn" onclick="openPersonModal('${person.id}')">
                    <span class="person-avatar-badge">${getRelationEmoji(person.relation)}</span>
                    <span>
                        <div>${person.name}</div>
                        <div style="font-size:11.5px; font-weight:500; color:var(--text-secondary);">
                            <b>${person.relation}</b> • ${person.age} Yaş ${person.job ? `• ${person.job}` : ""}
                        </div>
                    </span>
                </button>
            </h4>
            ${getMoodBadge(person)}
        </header>
        <div>
            ${extraBadges.length > 0 ? `<div class="person-chip-row" style="margin:6px 0 4px;">${extraBadges.join("")}</div>` : ""}
            ${lastChat && person.is_alive ? `<div style="font-size:11.5px; color:#cbd5e1; font-style:italic; margin:4px 0;">💬 "${lastChat}"</div>` : ""}
            ${person.is_alive ? `
                <div class="stat-progress-bg" style="height:5px; margin-top:6px;">
                    <div class="stat-progress-bar" style="width:${person.relationship_level}%; background:${relBarColor};"></div>
                </div>
            ` : ""}
        </div>
        ${quickActionsHtml}
    `;
    return card;
}

async function quickSendDmFromCard(personId, topicId) {
    await performActivity("send_dm", { person_id: personId, topic_id: topicId });
}

function renderRelationships() {
    const listEl = document.getElementById("relationshipsList");
    const summaryEl = document.getElementById("relationshipsSummary");
    if (!listEl) return;
    listEl.innerHTML = "";

    const rels = (gameState.relationships || []).filter(p => !p.is_blocked);
    const aliveRels = rels.filter(p => p.is_alive);

    if (summaryEl) {
        const partner = aliveRels.find(p => ["Eş", "Nişanlı", "Sevgili", "Flört"].includes(p.relation));
        const partnerText = partner ? `${getRelationEmoji(partner.relation)} ${partner.name.split(" ")[0]}` : "💔 Bekar";
        const avgRel = aliveRels.length > 0
            ? Math.round(aliveRels.reduce((acc, p) => acc + p.relationship_level, 0) / aliveRels.length)
            : 0;
        summaryEl.innerHTML = `
            <div class="rel-summary-stat">
                <div class="rel-summary-label">Aşk Durumu</div>
                <div class="rel-summary-val">${partnerText}</div>
            </div>
            <div class="rel-summary-stat">
                <div class="rel-summary-label">Sosyal Çevre</div>
                <div class="rel-summary-val">👥 ${aliveRels.length} Kişi</div>
            </div>
            <div class="rel-summary-stat">
                <div class="rel-summary-label">Sosyal Uyum</div>
                <div class="rel-summary-val" style="color:var(--accent-green);">%${avgRel}</div>
            </div>
        `;
    }
    if (rels.length === 0) {
        listEl.innerHTML = `<div class="panel-card"><p class="card-desc">Henüz kayıtlı bir ilişkin yok.</p></div>`;
    } else {
        const romanticRels = rels.filter(p => ["Eş", "Nişanlı", "Sevgili", "Flört"].includes(p.relation));
        const familyRels = rels.filter(p => ["Anne", "Baba", "Ağabey", "Abla", "Kardeş", "Çocuk", "Torun"].includes(p.relation));
        const workSchoolRels = rels.filter(p => ["Sınıf Arkadaşı", "Öğretmen", "İş Arkadaşı", "Patron"].includes(p.relation));
        const socialRels = rels.filter(p => !["Eş", "Nişanlı", "Sevgili", "Flört", "Anne", "Baba", "Ağabey", "Abla", "Kardeş", "Çocuk", "Torun", "Sınıf Arkadaşı", "Öğretmen", "İş Arkadaşı", "Patron"].includes(p.relation));

        if (romanticRels.length > 0) {
            const h = document.createElement("div");
            h.className = "rel-section-header";
            h.innerHTML = `<span>💘 Aşk, Flört & Evlilik (${romanticRels.length})</span>`;
            listEl.appendChild(h);
            romanticRels.forEach(p => listEl.appendChild(renderPersonCard(p)));
        }

        if (familyRels.length > 0) {
            const h = document.createElement("div");
            h.className = "rel-section-header";
            h.innerHTML = `<span>👨‍👩‍👧‍👦 Aile & Çocuklar (${familyRels.length})</span>`;
            listEl.appendChild(h);
            familyRels.forEach(p => listEl.appendChild(renderPersonCard(p)));
        }

        if (workSchoolRels.length > 0) {
            const h = document.createElement("div");
            h.className = "rel-section-header";
            h.innerHTML = `<span>🎒💼 Okul & İş Çevresi (${workSchoolRels.length})</span>`;
            listEl.appendChild(h);
            workSchoolRels.forEach(p => listEl.appendChild(renderPersonCard(p)));
        }

        if (socialRels.length > 0) {
            const h = document.createElement("div");
            h.className = "rel-section-header";
            h.innerHTML = `<span>🤝 Dostlar & Eski İlişkiler (${socialRels.length})</span>`;
            listEl.appendChild(h);
            socialRels.forEach(p => listEl.appendChild(renderPersonCard(p)));
        }
    }

    // Evcil hayvanlar
    if (gameState.pets && gameState.pets.length > 0) {
        const petsTitle = document.createElement("div");
        petsTitle.className = "rel-section-header";
        petsTitle.innerHTML = `<span>🐾 Evcil Hayvanların (${gameState.pets.length})</span>`;
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
        case "Flört": return "🔥";
        case "Sevgili": return "💘";
        case "Nişanlı": return "💎";
        case "Eş": return "💍";
        case "Eski Sevgili": case "Eski Eş": return "💔";
        case "Çocuk": return "👶";
        case "Arkadaş": return "🤝";
        case "Sınıf Arkadaşı": case "Eski Sınıf Arkadaşı": return "🎒";
        case "Öğretmen": case "Eski Öğretmen": return "🧑‍🏫";
        case "İş Arkadaşı": case "Eski İş Arkadaşı": return "💼";
        case "Patron": case "Eski Patron": return "👔";
        default: return "👤";
    }
}

async function triggerFamilyDinnerQuick() {
    const aliveParentOrFam = (gameState.relationships || []).find(p => p.is_alive && ["Anne", "Baba", "Ağabey", "Abla", "Kardeş", "Çocuk"].includes(p.relation));
    if (!aliveParentOrFam) {
        showToast("Aile yemeği düzenleyebileceğin hayatta bir aile üyen yok.", "error");
        return;
    }
    await performActivity("interact_person", { person_id: aliveParentOrFam.id, person_action: "family_dinner" });
}

// ----------------- KARİYER, EĞİTİM, BECERİLER & ŞİRKET -----------------

function renderCareerTab() {
    const careerEl = document.getElementById("careerContent");
    if (!careerEl) return;
    careerEl.innerHTML = "";

    // 1. Eğitim, LGS/YKS/KPSS Sınavları, Kampüs ve Askerlik
    const eduCard = document.createElement("div");
    eduCard.className = "panel-card";
    eduCard.innerHTML = `
        <div class="card-title-row">
            <span class="card-title">🎓 Eğitim & Kampüs</span>
            <span class="card-badge badge-blue">${gameState.education_level}</span>
        </div>
        <p class="card-desc">
            ${gameState.current_school ? `Okul: <b>${gameState.current_school}</b>` : "Aktif öğrenci değilsin."}
            ${gameState.school_president ? ` • 👑 <b>Okul Başkanı</b>` : ""}
            ${gameState.is_erasmus_active ? ` • 🇪🇺 <b>Erasmus (${gameState.erasmus_country})</b>` : ""}
            ${gameState.double_major ? ` • 📜 <b>ÇAP: ${gameState.double_major}</b>` : ""}
            ${gameState.school_club ? ` • 🏅 <b>${gameState.school_club}</b>` : ""}
            ${gameState.scholarship_annual > 0 ? ` • 🎓 Burs: <b>+₺ ${gameState.scholarship_annual.toLocaleString("tr-TR")}/yıl</b>` : ""}
            <br>
            🏠 Barınma: <b>${gameState.housing_type || "Aile Evi"}</b>
            • ${gameState.has_drivers_license ? "🚗 Ehliyet: Var" : "🚗 Ehliyet: Yok"}
            • 🪖 Askerlik: <b>${gameState.military_status}</b>
        </p>
        <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
            <button type="button" class="btn-action-outline" onclick="performActivity('study_hard')">📚 Ders Çalış</button>
            <button type="button" class="btn-action-outline" onclick="openExamsModal()">📝 Sınavlar (LGS, YKS, KPSS)</button>
            <button type="button" class="btn-action-outline" onclick="openUniversityModal()">🏛️ Üniversite</button>
            <button type="button" class="btn-action-outline" style="border-color:#60a5fa; color:#93c5fd;" onclick="openSchoolActionsModal()">🎒 Okul & Kampüs Eylemleri</button>
            <button type="button" class="btn-action-outline" onclick="openStudentHousingModal()">🍜 Yurt & Öğrenci Evi</button>
            <button type="button" class="btn-action-outline" onclick="openClubsModal()">🏅 Okul Kulüpleri</button>
            <button type="button" class="btn-action-outline" onclick="openMilitaryModal()">🪖 Askerlik Şubesi</button>
        </div>
    `;
    careerEl.appendChild(eduCard);

    // 2. Kendi Şirketin / Girişimcilik
    const bizCard = document.createElement("div");
    bizCard.className = "panel-card";
    if (gameState.business) {
        const b = gameState.business;
        if (b.is_traditional_shop) {
            bizCard.innerHTML = `
                <div class="card-title-row">
                    <span class="card-title">🥙 ${b.name} (${b.sector})</span>
                    <span class="card-badge badge-green">Değer: ₺ ${b.valuation.toLocaleString("tr-TR")}</span>
                </div>
                <div class="person-chip-row" style="margin:6px 0 8px;">
                    <span class="person-chip" style="color:#6ee7b7;">📈 Yıllık Kâr: +₺ ${b.annual_profit.toLocaleString("tr-TR")}/yıl</span>
                    <span class="person-chip" style="color:#60a5fa;">👦 Çırak Ustalığı: %${b.apprentice_skill || 15}</span>
                    <span class="person-chip" style="color:#f59e0b;">🛵 Kurye Motoru: ${b.courier_fleet || 0} Adet</span>
                    <span class="person-chip">🧼 Zabıta Hijyen: %${b.hygiene_score || 85}</span>
                    <span class="person-chip" style="color:#ec4899;">🌶️ ${b.secret_recipe ? 'Gizli Reçete Var ✨' : 'Standart Tarif'}</span>
                </div>
                <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
                    <button type="button" class="btn-action-outline" onclick="performShopAction('train_apprentice')">👦 Çırak Eğit (Eti Senin...)</button>
                    <button type="button" class="btn-action-outline" onclick="performShopAction('develop_secret_recipe')">🌶️ Gizli Sos/Tarif Geliştir</button>
                    <button type="button" class="btn-action-outline" onclick="performShopAction('inspect_hygiene_zabita')">👮 Zabıta Hijyen Teftişi</button>
                    <button type="button" class="btn-action-outline" onclick="performShopAction('expand_courier_fleet')">🛵 Kurye Motoru Ekle (65B ₺)</button>
                    <button type="button" class="btn-action-outline" onclick="performShopAction('negotiate_wholesaler')">📦 Hal / Toptancı Pazarlığı</button>
                    <button type="button" class="btn-action-outline" style="border-color: var(--accent-red); color: var(--accent-red);" onclick="performActivity('sell_business')">💰 Dükkanı Devret (Exit)</button>
                </div>
            `;
        } else {
            bizCard.innerHTML = `
                <div class="card-title-row">
                    <span class="card-title">🏢 ${b.name} (${b.sector})</span>
                    <span class="card-badge ${b.is_ipo ? 'badge-green' : 'badge-yellow'}">${b.is_ipo ? '🔔 BIST: Halka Açık' : 'Değer: ₺ ' + b.valuation.toLocaleString("tr-TR")}</span>
                </div>
                <div class="person-chip-row" style="margin:6px 0 8px;">
                    <span class="person-chip" style="color:#60a5fa;">📍 Aşama: ${b.stage || 'Tohum (Startup)'}</span>
                    <span class="person-chip" style="color:#6ee7b7;">📈 Kâr: +₺ ${b.annual_profit.toLocaleString("tr-TR")}/yıl</span>
                    <span class="person-chip">📊 Hisse: %${b.shares_owned || 100}</span>
                    <span class="person-chip">🏬 Şube: ${b.branches || 1}</span>
                    <span class="person-chip">👥 Ekip: ${b.employees} Kişi</span>
                    <span class="person-chip">⭐ İtibar: %${b.reputation}</span>
                    ${b.has_manager ? `<span class="person-chip" style="color:#a78bfa;">👔 Profesyonel CEO</span>` : ""}
                </div>
                <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 8px;">
                    <button type="button" class="btn-primary" style="flex:2;" onclick="openCompanyDecisionsModal()">🏬 Patron Karar Odası (Büyüme & BIST)</button>
                    <button type="button" class="btn-action-outline" style="flex:1;" onclick="openCompanyCrisisModal()">🚨 Kriz Masası</button>
                    <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('invest_business')">🚀 Hızlı Yatırım</button>
                    <button type="button" class="btn-action-outline" style="flex:1; border-color: var(--accent-green); color: var(--accent-green);" onclick="performActivity('sell_business')">💰 Şirketi Sat (Exit)</button>
                </div>
            `;
        }
    } else {
        bizCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">🏢 Girişimcilik & Kendi İşin</span>
                <span class="card-badge badge-purple">Fırsat</span>
            </div>
            <p class="card-desc">Kendi esnaf dükkanını, sanayi servisini veya teknoloji şirketini kurup patron olabilirsiniz.</p>
            <div style="display:flex; gap:6px; margin-top:8px;">
                <button type="button" class="btn-action-outline" style="flex:1;" onclick="openBusinessModal()">🏢 Yeni Şirket Kur</button>
                <button type="button" class="btn-action-outline" style="flex:1; border-color:#10b981; color:#6ee7b7;" onclick="openTraditionalShopModal()">🥙 Esnaf & Sanayi Aç</button>
            </div>
        `;
    }
    careerEl.appendChild(bizCard);

    // 3. Tam Zamanlı ve Yarı Zamanlı İş
    const jobCard = document.createElement("div");
    jobCard.className = "panel-card";
    if (gameState.is_in_prison) {
        jobCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">🚨 Cezaevi: ${gameState.prison_role || 'Mahkum'}</span>
                <span class="card-badge badge-red">${gameState.prison_years_left} Yıl Kaldı</span>
            </div>
            <p class="card-desc">Hapishanedeyken dışarıda çalışamazsın. Koğuş hiyerarşisinde hayatta kalıp infazını bekle.</p>
            <div style="margin-top: 8px;">
                <button type="button" class="btn-primary" style="width:100%;" onclick="openPrisonModal()">⛓️ Koğuş Hayatı & Cezaevi Masası</button>
            </div>
        `;`
    } else if (gameState.current_job) {
        const j = gameState.current_job;
        const jobTitle = j.rank_title || j.title;
        jobCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">💼 ${jobTitle} (Kademe ${j.level || 1})</span>
                <span class="card-badge badge-green">₺ ${j.salary.toLocaleString("tr-TR")}/yıl</span>
            </div>
            <div class="card-desc">
                Sektör: ${j.category} • Performans: %${j.performance} • Kıdem: ${j.experience_years} Yıl
                • 🏖️ Yıllık İzin: <b>${gameState.annual_leave_days != null ? gameState.annual_leave_days : 14} Gün</b>
                ${gameState.moonlighting_job ? `<br>🌙 Ek İş: <b>${gameState.moonlighting_job} (+₺ ${gameState.moonlighting_income.toLocaleString("tr-TR")}/yıl)</b>` : ""}
                ${gameState.part_time_job ? `<br>⏱️ Part-Time: <b>${gameState.part_time_job.title} (+₺ ${gameState.part_time_job.salary.toLocaleString("tr-TR")}/yıl)</b>` : ""}
                ${gameState.has_headhunter_offer ? `<br><span style="color:#fbbf24; font-weight:700;">💼 LinkedIn'den yeni bir Headhunter transfer teklifin var!</span>` : ""}
            </div>
            <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 6px;">
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('work_harder')">💪 Mesai Yap</button>
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performWorkplaceAction('kpi_review')">📊 KPI & Terfi</button>
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performWorkplaceAction('take_annual_leave')">🏖️ İzin Kullan</button>
                <button type="button" class="btn-action-outline" style="flex:1.5; border-color:#38bdf8; color:#7dd3fc;" onclick="openWorkplaceActionsModal()">💼 Plaza Eylemleri</button>
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

    // 5. Siyaset & Devlet Yönetimi Kartı
    const polCard = document.createElement("div");
    polCard.className = "panel-card";
    if (gameState.political_office) {
        polCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">${gameState.political_office}</span>
                <span class="card-badge badge-blue">Halk Desteği: %${gameState.approval_rating}</span>
            </div>
            <p class="card-desc">Yıllık Makam Ödeneği: <b>+₺ ${(gameState.political_salary || 0).toLocaleString("tr-TR")}/yıl</b></p>
            <div style="margin-top:8px; display:flex; gap:6px; flex-wrap:wrap;">
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('politics_action', {sub_action: 'hold_rally'})">📢 Miting Yap</button>
                <button type="button" class="btn-action-outline" style="flex:1" onclick="performActivity('politics_action', {sub_action: 'public_project'})">🏗️ Hizmet Aç</button>
                <button type="button" class="btn-primary" style="flex:1" onclick="openPoliticsModal()">🏛️ Meclis & Seçim</button>
            </div>
        `;
    } else {
        polCard.innerHTML = `
            <div class="card-title-row">
                <span class="card-title">🏛️ Siyaset & Devlet Yönetimi</span>
                <span class="card-badge badge-blue">Seçimler</span>
            </div>
            <p class="card-desc">Mahalle Muhtarlığından Belediye Başkanlığına, Milletvekilliğinden Cumhurbaşkanlığına kadar aday ol!</p>
            <button type="button" class="btn-action-outline" style="width:100%; margin-top:8px;" onclick="openPoliticsModal()">🗳️ Seçim & Siyaset Merkezini Aç</button>
        `;
    }
    careerEl.appendChild(polCard);

    // 6. Şöhret, Sanat & Magazin Merkezi Kartı
    const fameCard = document.createElement("div");
    fameCard.className = "panel-card";
    fameCard.innerHTML = `
        <div class="card-title-row">
            <span class="card-title">🌟 Şöhret, Sahne & Magazin</span>
            <span class="card-badge badge-yellow">Şöhret: %${gameState.fame || 0}</span>
        </div>
        <p class="card-desc">Yetenek seçmelerine katıl, Hit Albüm/Film çıkar, Talk Show'a konuk ol, reklam anlaşması imzala veya VIP ünlülerle flört et!</p>
        <div style="display:flex; gap:6px; margin-top:8px;">
            <button type="button" class="btn-action-outline" style="flex:1;" onclick="openFameModal()">🌟 Şöhret Merkezi</button>
            <button type="button" class="btn-action-outline" style="flex:1;" onclick="openBandModal()">🎸 Müzik Grubu (${gameState.band ? gameState.band.name : 'Kur'})</button>
            <button type="button" class="btn-action-outline" style="flex:1;" onclick="openProSportsModal()">⚽ Spor Kariyeri</button>
        </div>
    `;
    careerEl.appendChild(fameCard);
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
            🇨🇭 İsviçre Offshore: <b>₺ ${(gameState.offshore_balance || 0).toLocaleString("tr-TR")}</b> • 🏦 Kredi Borcu: <b style="color:var(--accent-red);">₺ ${(gameState.debt || 0).toLocaleString("tr-TR")}</b><br>
            Son Yıl Gelir: +₺ ${(gameState.annual_income_last || 0).toLocaleString("tr-TR")} • Son Yıl Gider: -₺ ${(gameState.annual_expense_last || 0).toLocaleString("tr-TR")}
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px;">
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openRealEstateModal()">🏠 Emlak</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openVehiclesModal()">🚗 Araç</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openAuctionModal()">🖼️ Müzayede</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openBankOffshoreModal()">🏦 Banka & Offshore</button>
            <button type="button" class="btn-action-outline" style="flex:1" onclick="openStocksModal()">📈 Borsa</button>
        </div>
    `;
    assetsEl.appendChild(summaryCard);

    if (!gameState.assets || gameState.assets.length === 0) {
        const noAsset = document.createElement("div");
        noAsset.className = "panel-card";
        noAsset.innerHTML = `<p class="card-desc">Henüz tapulu bir gayrimenkulün, aracın veya koleksiyon eserin bulunmuyor.</p>`;
        assetsEl.appendChild(noAsset);
    } else {
        gameState.assets.forEach(asset => {
            const card = document.createElement("div");
            card.className = "panel-card";
            const icon = asset.asset_type === "Ev" ? "🏠" : (asset.asset_type === "Koleksiyon" ? "🖼️" : "🏎️");
            const diff = asset.current_value - asset.purchase_price;
            const diffStr = diff >= 0 ? `+₺ ${diff.toLocaleString("tr-TR")}` : `-₺ ${Math.abs(diff).toLocaleString("tr-TR")}`;

            let extraControlsHtml = "";
            if (asset.asset_type === "Ev") {
                const renCost = Math.round(asset.current_value * 0.15);
                const issueBanner = asset.tenant_issue
                    ? `<div class="person-chip" style="background:rgba(239,68,68,0.22); color:#fca5a5; width:100%; margin:4px 0;">⚠️ Kiracı Sorunu: ${asset.tenant_issue}</div>`
                    : "";
                extraControlsHtml = `
                    <div class="person-chip-row" style="margin:6px 0; flex-wrap:wrap;">
                        <span class="person-chip">🔑 Kiracı: ${asset.tenant_name || "Atanmadı"} (%${asset.tenant_reliability || 85} Güven)</span>
                        <span class="person-chip">🛠️ Dekorasyon: Lvl ${asset.upgrade_level || 0}/3</span>
                        ${issueBanner}
                    </div>
                    <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:8px;">
                        <button type="button" class="btn-quick-rel" onclick="manageAssetExtra('${asset.id}', 'renovate_house')">🛠️ Tadilat (₺${renCost.toLocaleString("tr-TR")})</button>
                        <button type="button" class="btn-quick-rel" onclick="manageAssetExtra('${asset.id}', 'raise_rent')">📈 Kira Zammı (%25)</button>
                        <button type="button" class="btn-quick-rel" onclick="openTenantManageModal('${asset.id}')">🔑 Kiracı Kriz Masası</button>
                    </div>
                `;
            } else if (asset.asset_type === "Araba") {
                const tuneCost = Math.round(asset.current_value * 0.15);
                extraControlsHtml = `
                    <div class="person-chip-row" style="margin:6px 0; flex-wrap:wrap;">
                        <span class="person-chip">🔧 Modifiye: Stage-${asset.upgrade_level || 0}/3</span>
                        <span class="person-chip" style="background:${asset.has_insurance ? 'rgba(16,185,129,0.18)' : 'rgba(239,68,68,0.18)'}; color:${asset.has_insurance ? '#6ee7b7' : '#fca5a5'};">🛡️ Kasko: ${asset.has_insurance ? 'Aktif ✅' : 'Yok ❌'}</span>
                        <span class="person-chip">⚙️ Kondisyon: %${asset.condition || 100}</span>
                    </div>
                    <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:8px;">
                        <button type="button" class="btn-quick-rel" onclick="manageAssetExtra('${asset.id}', 'tune_car')">🔧 Stage Modifiye (₺${tuneCost.toLocaleString("tr-TR")})</button>
                        <button type="button" class="btn-quick-rel" onclick="performActivity('car_care', {asset_id: '${asset.id}', action_id: 'maintenance'})">🔧 Sanayi Bakımı</button>
                        <button type="button" class="btn-quick-rel" onclick="performActivity('car_care', {asset_id: '${asset.id}', action_id: 'insurance'})">🛡️ Kasko Yaptır</button>
                        <button type="button" class="btn-quick-rel" onclick="performActivity('car_care', {asset_id: '${asset.id}', action_id: 'highway_speed'})">🏎️ Gece Gazla</button>
                    </div>
                `;
            } else if (asset.asset_type === "Koleksiyon") {
                extraControlsHtml = `
                    <div class="person-chip-row" style="margin:6px 0;">
                        <span class="person-chip" style="color:#fde68a;">💎 Nadir Müzayede Koleksiyonu (Her yıl değerlenir)</span>
                    </div>
                `;
            }

            card.innerHTML = `
                <div class="card-title-row">
                    <span class="card-title">${icon} ${asset.name}</span>
                    <span class="card-badge badge-blue">₺ ${asset.current_value.toLocaleString("tr-TR")}</span>
                </div>
                <div class="card-desc">
                    Değer Değişimi: <b>${diffStr}</b> • Yıllık Masraf: ₺ ${asset.annual_cost.toLocaleString("tr-TR")}
                    ${asset.annual_income > 0 ? ` • Kira Geliri: <b>+₺ ${asset.annual_income.toLocaleString("tr-TR")}/yıl</b>` : ""}
                </div>
                ${extraControlsHtml}
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

// ----------------- KİŞİ ETKİLEŞİM MODALI & DERİN İLİŞKİ MENÜLERİ -----------------

function openPersonModal(personId) {
    sound.playClick();
    activePersonId = personId;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("personModalName").textContent = `${getRelationEmoji(person.relation)} ${person.name}`;
    document.getElementById("personModalDetails").textContent = `${person.relation} • ${person.age} Yaşında ${person.job ? `• Meslek: ${person.job}` : ""}`;
    document.getElementById("personModalLevel").textContent = `%${person.relationship_level}`;
    document.getElementById("personModalBar").style.width = `${person.relationship_level}%`;

    const isPartner = ["Flört", "Sevgili", "Nişanlı", "Eş"].includes(person.relation);
    const isEx = ["Eski Sevgili", "Eski Eş"].includes(person.relation);
    const isParent = ["Anne", "Baba"].includes(person.relation);
    const isSibling = ["Kardeş", "Abla", "Ağabey"].includes(person.relation);
    const isChild = person.relation === "Çocuk";
    const isFriend = person.relation === "Arkadaş";
    const isClassmate = person.relation === "Sınıf Arkadaşı";
    const isTeacher = person.relation === "Öğretmen";
    const isCoworker = person.relation === "İş Arkadaşı";
    const isBoss = person.relation === "Patron";

    const extraContainer = document.getElementById("personModalProfileExtra");
    if (extraContainer) {
        const interestsHtml = (person.interests && person.interests.length > 0)
            ? `<div class="person-chip-row">${person.interests.map(i => `<span class="person-chip">${i}</span>`).join("")}</div>`
            : "";

        const memoriesHtml = (person.memories && person.memories.length > 0)
            ? `
                <div class="person-action-group-title">📖 Ortak Anılarınız (${person.memories.length})</div>
                <div class="memories-timeline">
                    ${person.memories.slice().reverse().slice(0, 5).map(m => `<div class="memory-item">• ${m}</div>`).join("")}
                </div>
            `
            : "";

        extraContainer.innerHTML = `
            <div class="person-chip-row">
                <span class="person-chip">${getPersonalityLabel(person.personality)}</span>
                <span class="person-chip">✨ Burç: ${person.zodiac || "Aslan"}</span>
                ${person.love_language ? `<span class="person-chip">💝 Sevgi Dili: ${person.love_language}</span>` : ""}
                ${person.care_status ? `<span class="person-chip" style="color:#6ee7b7;">🤲 Bakım: ${person.care_status}</span>` : ""}
                ${person.is_estranged ? `<span class="person-chip" style="color:#f87171;">⚠️ Küs / İletişim Soğuk</span>` : ""}
                ${(person.lent_amount && person.lent_amount > 0) ? `<span class="person-chip" style="color:#fcd34d;">💸 Borç: ₺ ${person.lent_amount.toLocaleString('tr-TR')}</span>` : ""}
                ${person.love_confessed ? `<span class="person-chip" style="color:#f43f5e;">❤️ Aşk İlan Edildi</span>` : ""}
                ${person.hard_launched ? `<span class="person-chip" style="color:#60a5fa;">📸 Hard Launch Yapıldı</span>` : ""}
                ${person.met_family && isPartner ? `<span class="person-chip" style="color:#93c5fd;">👨‍👩‍👧 Aile Onayı: %${person.family_approval ?? 65}</span>` : ""}
                ${person.cohabiting ? `<span class="person-chip" style="color:#6ee7b7;">🏠 Aynı Evdesiniz</span>` : ""}
                ${person.has_prenup ? `<span class="person-chip" style="color:#fcd34d;">📜 Evlilik Sözleşmeli</span>` : ""}
                ${person.years_together > 0 ? `<span class="person-chip">⏳ ${person.years_together} Yıllık Birliktelik</span>` : ""}
                ${isChild ? `
                    <span class="person-chip" style="color:#60a5fa;">📝 Okul Notu: %${person.child_grades ?? 80}</span>
                    ${person.child_talent ? `<span class="person-chip" style="color:#f59e0b;">🌟 Yetenek: ${person.child_talent}</span>` : ""}
                    <span class="person-chip" style="color:#f87171;">⚡ Ergenlik İsyanı: %${person.child_rebellion ?? 15}</span>
                    ${person.is_disowned ? `<span class="person-chip" style="color:#ef4444; font-weight:700;">📜 Reddedilmiş Evlat</span>` : ""}
                ` : ""}
            </div>
            ${(person.red_flags && person.red_flags.length > 0) ? `<div class="person-chip-row" style="margin:4px 0;">${person.red_flags.map(rf => `<span class="person-chip" style="color:#f87171; border:1px solid rgba(239,68,68,0.3);">🚩 ${rf}</span>`).join("")}</div>` : ""}
            ${(person.green_flags && person.green_flags.length > 0) ? `<div class="person-chip-row" style="margin:4px 0;">${person.green_flags.map(gf => `<span class="person-chip" style="color:#4ade80; border:1px solid rgba(74,222,128,0.3);">🌿 ${gf}</span>`).join("")}</div>` : ""}
            ${person.bio ? `<div class="kismet-bio-box" style="margin:6px 0 8px;">"${person.bio}"</div>` : ""}
            <div class="person-stats-grid">
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>✨ Görünüş</span><span>%${person.looks ?? 65}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-looks" style="width:${person.looks ?? 65}%"></div></div>
                </div>
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>🧠 Zeka</span><span>%${person.smarts ?? 65}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-smarts" style="width:${person.smarts ?? 65}%"></div></div>
                </div>
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>🤝 Sadakat</span><span>%${person.loyalty ?? 75}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-health" style="width:${person.loyalty ?? 75}%"></div></div>
                </div>
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>💰 Varlık</span><span>%${person.wealth ?? 50}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-happiness" style="width:${person.wealth ?? 50}%"></div></div>
                </div>
            </div>
            ${interestsHtml}
            ${memoriesHtml}
        `;
    }

    const actionsContainer = document.getElementById("personModalActions");
    actionsContainer.innerHTML = "";

    if (!person.is_alive) {
        actionsContainer.innerHTML = `<p class="card-desc">Bu kişi vefat etti. Huzur içinde yatsın.</p>`;
    } else {
        const actions = [];

        if (isPartner) {
            actions.push({ id: "modal_intimacy", text: "🔥 Birlikte Ol & Seviş (Yatak Odası & İntimite)", primary: true });
            actions.push({ id: "modal_detailed_kiss", text: "💋 Romantik Öp & Yakınlaş (Öpüşme Stili Seç)", primary: true });
            actions.push({ id: "modal_detailed_date", text: "🌹 Çok Aşamalı Özel Randevuya Çık (Mekan & Diyalog)", primary: true });
            actions.push({ id: "modal_detailed_fight", text: "💥 Şiddetli Kavga Et & Hesap Sor (Rest Çek)" });
            actions.push({ id: "modal_couple_vacation", text: "✈️ Baş Başa Romantik Tatile / Balayına Çık" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Özel Romantik Hediye Al (Çiçek, Mücevher, Araba...)" });

            if (person.relation === "Flört") {
                actions.push({ id: "ask_relationship", text: "💑 'İlişkimizin Adını Koyalım' (Sevgili Ol)", primary: true });
                actions.push({ id: "situationship_talk", text: "🗣️ 'Biz Şimdi Neyiz?' Resti Çek (Adını Koy ya da Bitir)" });
            }
            if (person.relation === "Sevgili") {
                actions.push({ id: "modal_propose_ring", text: "💍 Evlenme Teklifi Et (Yüzük Seç)", primary: true });
            }
            if (person.relation === "Nişanlı") {
                actions.push({ id: "modal_plan_wedding", text: "👰 Düğün Organize Et (Mekan & Sözleşme Seç)", primary: true });
            }
            if (["Sevgili", "Nişanlı", "Eş"].includes(person.relation)) {
                if (!person.love_confessed) {
                    actions.push({ id: "confess_love", text: "❤️ İlk 'Seni Seviyorum' İtirafı Yap" });
                }
                if (!person.hard_launched) {
                    actions.push({ id: "hard_launch", text: "📸 Sosyal Medyada 'Hard Launch' (İlişkiyi İlan Et)" });
                }
            }
            if (!person.met_family) {
                actions.push({ id: "introduce_family", text: "👨‍👩‍👧 Ailemle Tanıştır (El Öpmeye Götür)" });
            }
            if (["Sevgili", "Nişanlı"].includes(person.relation) && !person.kiz_isteme_done) {
                actions.push({ id: "kiz_isteme", text: "☕💍 Geleneksel Kız İsteme & Tuzlu Kahve Merasimi (12.000 TL)", primary: true });
            }
            if (["Sevgili", "Nişanlı", "Eş"].includes(person.relation) && !person.nisan_bohca_done) {
                actions.push({ id: "nisan_kina", text: "🎁💃 Nişan Bohçası & Kına Gecesi / Bekarlığa Veda (35.000 TL)" });
            }
            if (["Sevgili", "Nişanlı"].includes(person.relation) && !person.cohabiting) {
                actions.push({ id: "move_in", text: "🏠 Aynı Eve Çıkma Teklifi Et (Ortak Ev Bütçesi)" });
            }
            if (["Sevgili", "Nişanlı", "Eş"].includes(person.relation)) {
                actions.push({ id: "modal_couple_business", text: `🤝🏪 Çiftler Arası Ortak Girişim Aç (${person.joint_venture_name || 'Kafe/Moda/Marka'})` });
                actions.push({ id: "celebrate_anniversary", text: "🥂 Yıldönümü Sürprizi Hazırla (3.000 TL)" });
                actions.push({ id: "visit_inlaws", text: "👵 Kayınvalide & Eşin Ailesini Ziyaret Et (1.500 TL)" });
                actions.push({ id: "try_baby", text: "🍼 Çocuk Yapmayı Dene" });
                actions.push({ id: "baby_shower", text: "🎈 Baby Shower & Cinsiyet Partisi Düzenle (5.000 TL)" });
                actions.push({ id: "couples_therapy", text: "🛋️ Çift Terapisine Git (4.000 TL)" });
            }
            actions.push({ id: "consolidated_chat", text: "💬 Romantik Dertleş & Hal Hatır Sor" });
            actions.push({ id: "modal_rel_conflict", text: "🗣️ Çift Tartışması & Kriz Masası (Diyalog Seç)" });
            actions.push({ id: "apologize", text: "🕊️ Özür Dile & Gönlünü Al" });
            actions.push({ id: "check_loyalty", text: "🕵️‍♂️ Sadakatini & Telefonunu Gizlice Kontrol Et" });
            actions.push({ id: "hire_detective", text: "🕵️‍♂️📸 Özel Dedektif Tut & Adım Adım İzlet (15.000 TL)" });
            actions.push({ id: "dna_test", text: "🧬 Gizli DNA & Soybağı Testi Yaptır (8.000 TL)" });
            actions.push({ id: "fake_stalk", text: "🕵️‍♀️ Fake Hesaptan Gizlice Stalkla (Takip & Beğeni Kontrolü)" });
            actions.push({ id: "cheat", text: "🔥 Gizli Kaçamak Yap (Aldat - Riskli!)" });
            actions.push({ id: "ghost_block", text: "🚫 Her Yerden Engelle & Ghostla" });
            actions.push({ id: "modal_divorce_court", text: "⚖️ İnteraktif Boşanma & Nafaka Mahkemesi (Avukat Tut)" });
            const breakupLabel = person.relation === "Eş" ? "💔 Hızlı Boşanma" : (person.relation === "Nişanlı" ? "💔 Nişanı At" : "💔 Ayrıl");
            actions.push({ id: "breakup", text: breakupLabel });
        } else if (isEx) {
            actions.push({ id: "modal_intimacy", text: "🔥 Eski Sevgiliyle Yatak Odası Yakınlaşması (Aşkı Alevlendir)" });
            actions.push({ id: "text_ex", text: "📱 Gece Yarısı 'Seni Özledim' Mesajı At & Barışmayı Dene", primary: true });
            actions.push({ id: "modal_handle_ex_text", text: "📱 Gece 02:30 'Uyudun mu?' Krizini Yönet" });
            actions.push({ id: "modal_detailed_kiss", text: "💋 Dudaktan Ateşli Öp & Aşkı Alevlendir" });
            actions.push({ id: "modal_detailed_fight", text: "🤬 Eski Defterleri Aç & Hesaplaş (Kavga Et)" });
            actions.push({ id: "fake_stalk", text: "🕵️‍♀️ Fake Hesaptan Profilini Gizlice Stalkla" });
            actions.push({ id: "apologize", text: "🕊️ Geçmiş İçin Özür Dile & Buzları Erit" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Gönlünü Almak İçin Hediye Gönder" });
            actions.push({ id: "consolidated_chat", text: "💬 Halini Hatırını Sor & Dertleş" });
            actions.push({ id: "ghost_block", text: "🚫 Her Yerden Engelle (Hayatından Çıkar)" });
        } else if (isParent) {
            actions.push({ id: "modal_parent_care", text: "🤲 Yaşlı Bakım Masası (Huzurevi / Bakıcı / Eve Alma / Refakat)", primary: true });
            actions.push({ id: "parent_blessing", text: "🙏 Elini Öp & Hayır Duası Al", primary: true });
            actions.push({ id: "family_dinner", text: "🍲 Büyük Aile Yemeği Düzenle (2.000 TL)" });
            actions.push({ id: "ask_money", text: "💸 Harçlık / Maddi Destek İste" });
            actions.push({ id: "consolidated_chat", text: "💬 Samimi Sohbet & Hal Hatır Sor" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Özel Hediye Al" });
        } else if (isSibling) {
            actions.push({ id: "modal_sibling_action", text: "🤝 Kardeş Masası & Dayanışma (Borç / Altın / Barışma)", primary: true });
            actions.push({ id: "family_dinner", text: "🍲 Büyük Aile Yemeği Düzenle (2.000 TL)" });
            actions.push({ id: "consolidated_chat", text: "💬 Dertleş & Çocukluk Hatıralarını Konuş" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Hediye Al" });
            actions.push({ id: "modal_detailed_fight", text: "🤬 Tartış ve Hesap Sor" });
        } else if (isChild) {
            actions.push({ id: "modal_parenting_crisis", text: "🎓 Ebeveynlik & Kriz Masası (Ergenlik / Gelecek Seçimi)", primary: true });
            actions.push({ id: "parent_tutor", text: "📚 Özel Ders Aldır & Birlikte Sınavlara Hazırlan (4.500 TL)", primary: true });
            actions.push({ id: "parent_talent", text: "⚽🎹 Spor & Piyano / Sanat Akademisine Yazdır (15.000 TL)", primary: true });
            actions.push({ id: "parent_theme_park", text: "🎡 Lunapark & Süper Lig Derbisine Götür (2.500 TL)" });
            actions.push({ id: "parent_discipline", text: "🗣️ Ergenlik & Disiplin Nasihati Ver (İsyanı Düşür)" });
            actions.push({ id: "private_school", text: "🎓🏫 Özel Koleje & Yetenek Akademisine Gönder (45.000 TL)" });
            actions.push({ id: "marry_off_child", text: "👰🤵👶 Çocuğuna Düğün Yap, Evlendir & Torun Sahibi Ol (85.000 TL)" });
            if (person.age >= 18) {
                actions.push({ id: "parent_gift_car", text: "🏎️ 18 Yaşında İlk Arabasını Hediye Et (380.000 TL)" });
                actions.push({ id: "parent_gift_flat", text: "🏠 Evlilik Çeyizine Lüks Daire Satın Al (2.200.000 TL)" });
            }
            actions.push({ id: "disown_child", text: "📜 Evlatlıktan Reddet & Mirastan Men Et" });
            actions.push({ id: "consolidated_chat", text: "💬 Vakit Geçir & Sohbet Et" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Hediye Al" });
            actions.push({ id: "dna_test", text: "🧬 Gizli DNA & Babalık Testi Yaptır (8.000 TL)" });
        } else if (isFriend) {
            actions.push({ id: "modal_friend_action", text: "🤝 Dostluk Sınavı & Sadakat (Borç / Sır / Gece İmdadı / Yolculuk)", primary: true });
            actions.push({ id: "friend_hookup", text: "🔥🤫 Yatak Arkadaşlığı / Kaçamak Teklif Et (Friends with Benefits)" });
            actions.push({ id: "confess_friend", text: "💘😭 Friendzone'u Kır & Aşkını İtiraf Et (Sevgili Ol)" });
            actions.push({ id: "modal_social_hangout", text: "🎉 Sosyal Etkinliğe Çıkar (Kahve, Maç, Konser...)" });
            actions.push({ id: "ask_matchmake", text: "💘 'Bana Birini Ayarla!' (Çöpçatanlık İste)" });
            actions.push({ id: "consolidated_chat", text: "💬 Samimi Sohbet & Dertleş" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Hediye Al" });
            actions.push({ id: "modal_detailed_kiss", text: "💋 Beklenmedik Bir Şekilde Öp (Aşka Çevirmeyi Dene)" });
            actions.push({ id: "modal_detailed_fight", text: "🤬 Yüzleş ve Hesap Sor" });
        } else if (isClassmate) {
            actions.push({ id: "school_crush", text: "💌 Sıra Altından Aşk Mektubu Ver (Okul Aşkı)", primary: true });
            actions.push({ id: "cheat_homework", text: "📝 Sınavda Dirseği Çek & Kopya İste (+Okul Başarısı)" });
            actions.push({ id: "hangout_canteen", text: "🥪 Kantinde Tost & Ayran Ismarla (80 TL)" });
            actions.push({ id: "prom_invitation", text: "💃 Mezuniyet Balosu Eşi Olmayı Teklif Et" });
            actions.push({ id: "stand_up_bully", text: "💥 Koridorda Laf Atarsa Dik Dur & Boyun Eğme" });
            actions.push({ id: "consolidated_chat", text: "💬 Teneffüste Sohbet Et & Dedikodu Yap" });
            actions.push({ id: "modal_detailed_fight", text: "🤬 Kavga Et & Tartış" });
        } else if (isTeacher) {
            actions.push({ id: "suck_up_teacher", text: "🍎 Tahtayı Sil & Hocaya Yağ Çek (+Sözlü Notu)", primary: true });
            actions.push({ id: "prank_teacher", text: "🤪 Sırasına Tebeşir / Raptiye Koy (Muziplik Yap)" });
            actions.push({ id: "consolidated_chat", text: "💬 Odasına Gidip Dersler Hakkında Akıl Danış" });
        } else if (isCoworker) {
            actions.push({ id: "modal_coworker_project", text: "💼📊 Ortak Projede Birlikte Çalış & Sunum Hazırla", primary: true });
            actions.push({ id: "modal_coworker_gossip", text: "☕🤫 Kahve Makinesinde Plaza Dedikodusu Yap", primary: true });
            actions.push({ id: "modal_coworker_hangout", text: "🎉🍻 Mesai Sonrası Sosyalleş & Dertleş (Kahve/Yemek/Pub)" });
            actions.push({ id: "office_romance", text: "☕🌹 Mesai Sonrası Kahveye Davet Et (Ofis Aşkı Başlat)" });
            actions.push({ id: "steal_credit", text: "😈 Sunumda Emeğini Çal & Patronun Gözüne Gir (+Performans, -Dostluk)" });
            actions.push({ id: "consolidated_chat", text: "💬 Kahve Molasında Sohbet Et & Dertleş" });
            actions.push({ id: "modal_detailed_fight", text: "🤬 Toplantıda Sert Tartış & Fikir Ayrılığı" });
        } else if (isBoss) {
            actions.push({ id: "modal_boss_mentorship", text: "👑🎓 Patrondan Mentorluk & Kariyer Koçluğu Al (1-e-1 Görüşme)", primary: true });
            actions.push({ id: "modal_boss_negotiation", text: "📈💼 Stratejik Maaş Zammı & Terfi Pazarlığı Yap", primary: true });
            actions.push({ id: "boss_annual_bonus", text: "💰🎉 Yıl Sonu Başarı Primi / İkramiye Talep Et (Yüksek Performans)" });
            actions.push({ id: "suck_up_boss", text: "☕ Özel Filtre Kahve Götür & Stratejisini Öv (+Performans)" });
            actions.push({ id: "flirt_with_boss", text: "💼🌹 Lüks Akşam Yemeğinde Yakınlaş (Patronla Flört / Zam Riski)" });
            actions.push({ id: "consolidated_chat", text: "💬 Odasında Şirket Vizyonu Hakkında Konuş" });
        } else {
            actions.push({ id: "modal_social_hangout", text: "🎉 Sosyal Etkinliğe Çıkar (Kahve, Maç, Konser...)", primary: true });
            actions.push({ id: "consolidated_chat", text: "💬 Samimi Sohbet & Hal Hatır Sor" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Özel Hediye Al" });
        }

        actions.forEach(act => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = act.primary ? "btn-primary" : "btn-choice";
            btn.style.textAlign = "left";
            btn.textContent = act.text;
            btn.onclick = () => handlePersonAction(act.id);
            actionsContainer.appendChild(btn);
        });
    }

    openDialogModal("personModal");
}

async function sendModalDm(personId, topicId) {
    await performActivity("send_dm", { person_id: personId, topic_id: topicId });
    openPersonModal(personId);
}

async function handlePersonAction(actId) {
    if (!activePersonId) return;
    const pid = activePersonId;

    if (actId === "modal_parent_care") {
        await closeTopLayer(document.getElementById("personModal"));
        openParentCareModal(pid);
        return;
    }
    if (actId === "modal_sibling_action") {
        await closeTopLayer(document.getElementById("personModal"));
        openSiblingActionModal(pid);
        return;
    }
    if (actId === "modal_parenting_crisis") {
        await closeTopLayer(document.getElementById("personModal"));
        openParentingCrisisModal(pid);
        return;
    }
    if (actId === "modal_friend_action") {
        await closeTopLayer(document.getElementById("personModal"));
        openFriendActionModal(pid);
        return;
    }
    if (actId === "consolidated_chat") {
        await performActivity("consolidated_chat", { person_id: pid });
        closeModal("personModal");
        return;
    }
    if (actId === "modal_intimacy" || actId === "intimacy") {
        await closeTopLayer(document.getElementById("personModal"));
        openIntimacyModal(pid);
        return;
    }
    if (actId === "modal_detailed_kiss") {
        await closeTopLayer(document.getElementById("personModal"));
        openDetailedKissModal(pid);
        return;
    }
    if (actId === "modal_detailed_date" || actId === "modal_date_venue") {
        await closeTopLayer(document.getElementById("personModal"));
        openDetailedDateModal(pid);
        return;
    }
    if (actId === "modal_detailed_fight" || actId === "argue") {
        await closeTopLayer(document.getElementById("personModal"));
        openDetailedFightModal(pid);
        return;
    }
    if (actId === "modal_couple_vacation") {
        await closeTopLayer(document.getElementById("personModal"));
        openCoupleVacationModal(pid);
        return;
    }
    if (actId === "modal_social_hangout") {
        await closeTopLayer(document.getElementById("personModal"));
        openSocialHangoutModal(pid);
        return;
    }
    if (actId === "modal_custom_gift") {
        await closeTopLayer(document.getElementById("personModal"));
        openCustomGiftModal(pid);
        return;
    }
    if (actId === "modal_propose_ring") {
        await closeTopLayer(document.getElementById("personModal"));
        openRingProposalModal(pid);
        return;
    }
    if (actId === "modal_plan_wedding") {
        await closeTopLayer(document.getElementById("personModal"));
        openWeddingModal(pid);
        return;
    }
    if (actId === "modal_couple_business") {
        await closeTopLayer(document.getElementById("personModal"));
        openCoupleBusinessModal(pid);
        return;
    }
    if (actId === "modal_rel_conflict") {
        await closeTopLayer(document.getElementById("personModal"));
        openRelConflictModal(pid);
        return;
    }
    if (actId === "modal_divorce_court") {
        await closeTopLayer(document.getElementById("personModal"));
        openDivorceCourtModal(pid);
        return;
    }
    if (actId === "situationship_talk") {
        await performActivity("situationship_talk", { person_id: pid });
        closeModal("personModal");
        return;
    }
    if (actId === "confess_love") {
        await performActivity("confess_love", { person_id: pid });
        closeModal("personModal");
        return;
    }
    if (actId === "hard_launch") {
        await performActivity("hard_launch", { person_id: pid });
        closeModal("personModal");
        return;
    }
    if (actId === "modal_handle_ex_text") {
        await closeTopLayer(document.getElementById("personModal"));
        openExMidnightTextModal(pid);
        return;
    }
    if (actId === "try_baby") {
        await performActivity("try_baby");
        closeModal("personModal");
        return;
    }
    if (["friend_hookup", "confess_friend"].includes(actId)) {
        await performActivity("friend_to_lover", { person_id: pid, action_id: actId });
        closeModal("personModal");
        return;
    }
    if (["school_crush", "cheat_homework", "hangout_canteen", "prom_invitation", "stand_up_bully", "suck_up_teacher", "prank_teacher"].includes(actId)) {
        await performActivity("classmate_action", { person_id: pid, action_id: actId });
        closeModal("personModal");
        return;
    }
    if (actId === "modal_coworker_project") {
        await closeTopLayer(document.getElementById("personModal"));
        openCoworkerProjectModal(pid);
        return;
    }
    if (actId === "modal_coworker_gossip") {
        await closeTopLayer(document.getElementById("personModal"));
        openCoworkerGossipModal(pid);
        return;
    }
    if (actId === "modal_coworker_hangout") {
        await closeTopLayer(document.getElementById("personModal"));
        openCoworkerHangoutModal(pid);
        return;
    }
    if (actId === "modal_boss_mentorship") {
        await closeTopLayer(document.getElementById("personModal"));
        openBossMentorshipModal(pid);
        return;
    }
    if (actId === "modal_boss_negotiation") {
        await closeTopLayer(document.getElementById("personModal"));
        openBossNegotiationModal(pid);
        return;
    }
    if (actId === "boss_annual_bonus") {
        await performActivity("boss_action", { person_id: pid, action_id: "annual_bonus" });
        closeModal("personModal");
        return;
    }
    if (["office_romance", "office_hookup", "happy_hour", "steal_credit"].includes(actId)) {
        await performActivity("coworker_action", { person_id: pid, action_id: actId });
        closeModal("personModal");
        return;
    }
    if (["suck_up_boss", "flirt_with_boss", "ask_raise"].includes(actId)) {
        await performActivity("boss_action", { person_id: pid, action_id: actId });
        closeModal("personModal");
        return;
    }

    await performActivity("interact_person", {
        person_id: pid,
        person_action: actId
    });
    closeModal("personModal");
}

function openParentCareModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.parent_care_options) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🤲 Yaşlı Bakım Masası: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    const statusNote = person.care_status ? `<div class="card-badge badge-green" style="margin-bottom:10px;">Mevcut Bakım Durumu: ${person.care_status}</div>` : "";

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            ${statusNote}
            Yaşlanan <b>${person.name}</b> (${person.relation}) için vefa borcunu nasıl ödemek istersin?
        </p>
        ${marketData.parent_care_options.map(opt => `
            <div class="panel-card" style="margin-bottom:10px;">
                <div class="card-title-row">
                    <span class="card-title">${opt.name}</span>
                    <span class="card-badge ${opt.cost > 0 ? 'badge-purple' : 'badge-green'}">${opt.cost > 0 ? '₺ ' + opt.cost.toLocaleString('tr-TR') : 'Ücretsiz (Vefa)'}</span>
                </div>
                <p class="card-desc" style="margin:6px 0;">${opt.desc}</p>
                <button type="button" class="btn-primary" style="margin-top:6px;" onclick="submitParentCare('${person.id}', '${opt.id}')">Bu Bakımı Seç & Uygula 🤲</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitParentCare(personId, careId) {
    await performActivity("parent_care", { person_id: personId, care_id: careId });
    closeModal("genericModal");
}

function openSiblingActionModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.sibling_interactions) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🤝 Kardeş Dayanışması: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    const estNote = person.is_estranged ? `<div class="card-badge badge-red" style="margin-bottom:10px;">⚠️ Şu an aranız açık/küs!</div>` : "";
    const debtNote = (person.lent_amount && person.lent_amount > 0) ? `<div class="card-badge badge-purple" style="margin-bottom:10px;">Borç Verdiğin: ₺ ${person.lent_amount.toLocaleString('tr-TR')}</div>` : "";

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            ${estNote}
            ${debtNote}
            Kan bağın olan <b>${person.name}</b> (${person.relation}) ile aile bağlarını ve dayanışmayı güçlendir:
        </p>
        ${marketData.sibling_interactions.map(item => `
            <div class="panel-card" style="margin-bottom:10px;">
                <div class="card-title-row">
                    <span class="card-title">${item.name}</span>
                    <span class="card-badge ${item.cost > 0 ? 'badge-purple' : 'badge-green'}">${item.cost > 0 ? '₺ ' + item.cost.toLocaleString('tr-TR') : 'Ücretsiz'}</span>
                </div>
                <p class="card-desc" style="margin:6px 0;">${item.desc}</p>
                <button type="button" class="btn-primary" style="margin-top:6px;" onclick="submitSiblingAction('${person.id}', '${item.id}')">Eylemi Gerçekleştir 🤝</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitSiblingAction(personId, actionId) {
    await performActivity("sibling_action", { person_id: personId, action_id: actionId });
    closeModal("genericModal");
}

function openParentingCrisisModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.parenting_crises) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🎓 Ebeveynlik & Kriz Masası: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">
            Çocuğun <b>${person.name}</b> (${person.age} Yaşında) için kritik ebeveynlik kararları. Yaklaşımın çocuğunun kişiliğini ve geleceğini şekillendirecek:
        </p>
        ${marketData.parenting_crises.map(crisis => `
            <div class="panel-card" style="margin-bottom:14px; border-left: 3px solid var(--accent, #6366f1);">
                <div class="card-title" style="margin-bottom:4px; font-weight:700;">${crisis.title}</div>
                <p class="card-desc" style="margin-bottom:10px;">${crisis.desc}</p>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    ${crisis.options.map(opt => `
                        <button type="button" class="btn-choice" style="text-align:left; padding:8px 12px;" onclick="submitParentingCrisis('${person.id}', '${crisis.id}', '${opt.id}')">
                            <div style="font-weight:600; color:#f8fafc;">${opt.text}</div>
                            <div style="font-size:11px; color:#94a3b8; margin-top:2px;">[${opt.style}] ${opt.desc}</div>
                        </button>
                    `).join("")}
                </div>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitParentingCrisis(personId, crisisId, choiceId) {
    await performActivity("parenting_crisis", { person_id: personId, crisis_id: crisisId, choice_id: choiceId });
    closeModal("genericModal");
}

function openFriendActionModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.friend_interactions) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🤝 Dostluk Sınavı & Sadakat: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    const loyaltyNote = `<div class="card-badge badge-green" style="margin-bottom:10px;">Sadakat Seviyesi: %${person.loyalty ?? 75}</div>`;
    const debtNote = (person.lent_amount && person.lent_amount > 0) ? `<div class="card-badge badge-purple" style="margin-bottom:10px;">Borç Verdiğin: ₺ ${person.lent_amount.toLocaleString('tr-TR')}</div>` : "";

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            ${loyaltyNote}
            ${debtNote}
            Dostun <b>${person.name}</b> ile gerçek hayatın içinden samimi ve riskli dostluk etkileşimleri:
        </p>
        ${marketData.friend_interactions.map(item => `
            <div class="panel-card" style="margin-bottom:10px;">
                <div class="card-title-row">
                    <span class="card-title">${item.name}</span>
                    <span class="card-badge ${item.cost > 0 ? 'badge-purple' : 'badge-green'}">${item.cost > 0 ? '₺ ' + item.cost.toLocaleString('tr-TR') : 'Ücretsiz'}</span>
                </div>
                <p class="card-desc" style="margin:6px 0;">${item.desc}</p>
                <button type="button" class="btn-primary" style="margin-top:6px;" onclick="submitFriendAction('${person.id}', '${item.id}')">Dostluk Adımını At 🤝</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitFriendAction(personId, actionId) {
    await performActivity("friend_action", { person_id: personId, action_id: actionId });
    closeModal("genericModal");
}

// ==================== İŞ ARKADAŞI & PATRON DİNAMİKLERİ MODALLARI ====================

function openCoworkerProjectModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.coworker_projects) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `💼📊 Ortak Proje Masası: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    const jobTitle = gameState.current_job ? gameState.current_job.title : "Şirket Projesi";
    const perfVal = gameState.current_job ? gameState.current_job.performance : 70;

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">
            <b>${jobTitle}</b> departmanında <b>${person.name}</b> ile büyük bir müşteri ihalesi ve sunum projesinde görevlendirildiniz. (Mevcut Performans: %${perfVal})<br>
            Bu projeyi nasıl yürütmek istersin?
        </p>
        ${marketData.coworker_projects.map(opt => `
            <div class="panel-card" style="margin-bottom:12px;">
                <div class="card-title-row">
                    <span class="card-title">${opt.name}</span>
                    <span class="card-badge ${opt.bonus_money > 0 ? 'badge-green' : 'badge-purple'}">
                        ${opt.bonus_money > 0 ? '+₺ ' + opt.bonus_money.toLocaleString('tr-TR') + ' Prim' : 'Standart'}
                    </span>
                </div>
                <p class="card-desc" style="margin:6px 0;">${opt.desc}</p>
                <div class="person-chip-row" style="margin:6px 0 10px;">
                    <span class="person-chip" style="color:#6ee7b7;">📈 Performans: +${opt.perf_boost}</span>
                    <span class="person-chip" style="color:${opt.stress_cost > 0 ? '#f87171' : '#6ee7b7'};">😰 Stres: ${opt.stress_cost > 0 ? '+' + opt.stress_cost : opt.stress_cost}</span>
                    <span class="person-chip" style="color:${opt.rel_boost > 0 ? '#60a5fa' : '#f87171'};">🤝 İlişki: ${opt.rel_boost > 0 ? '+' + opt.rel_boost : opt.rel_boost}</span>
                </div>
                <button type="button" class="btn-primary" style="margin-top:4px;" onclick="submitCoworkerAction('${person.id}', 'joint_project', '${opt.id}')">
                    Bu Stratejiyle Çalış 🚀
                </button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

function openCoworkerGossipModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.coworker_gossips || !marketData.coworker_gossip_reactions) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    const stories = marketData.coworker_gossips;
    const story = stories[Math.floor(Math.random() * stories.length)];

    document.getElementById("genericModalTitle").textContent = `☕🤫 Plaza Kulisleri & Dedikodu: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="margin-bottom:14px; background:rgba(30,41,59,0.7); border:1px solid rgba(245,158,11,0.3);">
            <div style="font-size:11px; font-weight:700; color:#f59e0b; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
                ☕ KAHVE MAKİNESİ BAŞINDA FISILTI
            </div>
            <div style="font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:6px;">
                ${story.title}
            </div>
            <p class="card-desc" style="color:#e2e8f0; font-size:13.5px; line-height:1.5; font-style:italic;">
                ${story.text}
            </p>
        </div>

        <p class="card-desc" style="margin-bottom:10px; font-weight:600; color:#cbd5e1;">
            Bu sıcak bilgi karşısında tutumun ne olacak?
        </p>

        ${marketData.coworker_gossip_reactions.map(r => `
            <div class="panel-card" style="margin-bottom:10px;">
                <div class="card-title-row">
                    <span class="card-title">${r.name}</span>
                </div>
                <p class="card-desc" style="margin:4px 0 8px;">${r.desc}</p>
                <button type="button" class="btn-primary" onclick="submitCoworkerAction('${person.id}', 'office_gossip', '${r.id}', '${story.id}')">
                    Tavrını Koy 🗣️
                </button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

function openCoworkerHangoutModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.coworker_hangouts) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🎉🍻 Mesai Sonrası Sosyalleşme: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">
            Mesai bitti, laptoplar kapandı! <b>${person.name}</b> ile iş stresini geride bırakıp kafa dağıtmak için bir plan seç:
        </p>
        ${marketData.coworker_hangouts.map(h => `
            <div class="panel-card" style="margin-bottom:10px;">
                <div class="card-title-row">
                    <span class="card-title">${h.name}</span>
                    <span class="card-badge ${gameState.money >= h.cost ? 'badge-green' : 'badge-danger'}">
                        ₺ ${h.cost.toLocaleString('tr-TR')}
                    </span>
                </div>
                <p class="card-desc" style="margin:6px 0;">${h.desc}</p>
                <div class="person-chip-row" style="margin:4px 0 10px;">
                    <span class="person-chip" style="color:#60a5fa;">🤝 İlişki: +${h.rel_boost}</span>
                    <span class="person-chip" style="color:#6ee7b7;">🧘 Stres: -${h.stress_relief}</span>
                    <span class="person-chip" style="color:#fcd34d;">😄 Mutluluk: +${h.hap_boost}</span>
                </div>
                <button type="button" class="btn-primary" style="margin-top:4px;" ${gameState.money < h.cost ? 'disabled style="opacity:0.5;"' : ''} onclick="submitCoworkerAction('${person.id}', 'afterwork_hangout', '${h.id}')">
                    ${gameState.money >= h.cost ? 'Davet Et & Git 🍻' : 'Yetersiz Bakiye'}
                </button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

function openBossMentorshipModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.boss_mentorships) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `👑🎓 Patrondan Mentorluk & Koçluk: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">
            Patronun <b>${person.name}</b>'in köşe ofisine girip kahve eşliğinde bire bir kariyer mentorluğu talep ediyorsun.<br>
            Hangi alanda vizyon ve tecrübe kazanmak istersin?
        </p>
        ${marketData.boss_mentorships.map(topic => `
            <div class="panel-card" style="margin-bottom:10px;">
                <div class="card-title-row">
                    <span class="card-title">${topic.name}</span>
                </div>
                <p class="card-desc" style="margin:6px 0;">${topic.desc}</p>
                <div class="person-chip-row" style="margin:4px 0 10px;">
                    <span class="person-chip" style="color:#6ee7b7;">📈 Performans: +${topic.perf_boost}</span>
                    <span class="person-chip" style="color:#93c5fd;">👔 Patron İlişkisi: +${topic.rel_boost}</span>
                    <span class="person-chip" style="color:#fcd34d;">🧠 Zeka/Yetenek Artışı</span>
                </div>
                <button type="button" class="btn-primary" style="margin-top:4px;" onclick="submitBossAction('${person.id}', 'boss_mentorship', '${topic.id}')">
                    Bu Konuda Akıl Danış 🎓
                </button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

function openBossNegotiationModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.boss_negotiations) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    const currentSal = gameState.current_job ? gameState.current_job.salary : 0;
    const currentTitle = gameState.current_job ? gameState.current_job.title : "Çalışan";
    const currentPerf = gameState.current_job ? gameState.current_job.performance : 70;

    document.getElementById("genericModalTitle").textContent = `📈💼 Maaş Zammı & Terfi Masası: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="margin-bottom:12px; background:rgba(30,41,59,0.7);">
            <div style="font-size:12px; color:#94a3b8; margin-bottom:4px;">MEVCUT KARİYER DURUMUN:</div>
            <div style="font-size:15px; font-weight:700; color:#f8fafc;">
                ${currentTitle} — ₺ ${currentSal.toLocaleString('tr-TR')} / yıl
            </div>
            <div class="person-chip-row" style="margin-top:6px;">
                <span class="person-chip" style="color:#6ee7b7;">📊 Performans: %${currentPerf}</span>
                <span class="person-chip" style="color:#93c5fd;">👔 Patronla İlişki: %${person.relationship_level}</span>
                <span class="person-chip" style="color:#fcd34d;">✨ Karizma: ${gameState.skills && gameState.skills.charisma ? gameState.skills.charisma : 25}</span>
            </div>
        </div>

        <p class="card-desc" style="margin-bottom:10px;">
            Patronun karşısına oturuyorsun. Masadaki kozunu ve ikna taktiğini seç:
        </p>

        ${marketData.boss_negotiations.map(tactic => `
            <div class="panel-card" style="margin-bottom:12px;">
                <div class="card-title-row">
                    <span class="card-title">${tactic.name}</span>
                    <span class="card-badge badge-green">Hedef: +%${tactic.raise_pct} Zam</span>
                </div>
                <p class="card-desc" style="margin:6px 0;">${tactic.desc}</p>
                <button type="button" class="btn-primary" style="margin-top:6px;" onclick="submitBossAction('${person.id}', 'boss_negotiation', '${tactic.id}')">
                    Pazarlığa Başla 💼
                </button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitCoworkerAction(personId, actionId, subId, storyId = "") {
    sound.playClick();
    await performActivity("coworker_action", {
        person_id: personId,
        action_id: actionId,
        sub_id: subId,
        story_id: storyId
    });
    closeModal("genericModal");
}

async function submitBossAction(personId, actionId, subId) {
    sound.playClick();
    await performActivity("boss_action", {
        person_id: personId,
        action_id: actionId,
        sub_id: subId
    });
    closeModal("genericModal");
}

let selectedHookupVenue = "nightclub";
let selectedHookupProtection = "protected";

function openHookupModal() {
    sound.playClick();
    if (!marketData || !marketData.hookup_venues) return;
    
    document.getElementById("genericModalTitle").textContent = "🍸 Gece Hayatı & Tek Gecelik Kaçamak";
    const body = document.getElementById("genericModalBody");

    selectedHookupVenue = marketData.hookup_venues[0].id;
    selectedHookupProtection = "protected";

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">
            Şehrin ışıkları altında hızlı, tutkulu ve anı yaşayacağın bir gece! Mekanını ve korunma tercihini seç:
        </p>
        <div style="font-size:12px; font-weight:700; color:#f8fafc; margin-bottom:6px;">1. Kaçamak Mekanını Seç:</div>
        <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
            ${marketData.hookup_venues.map((v, idx) => `
                <label class="panel-card" style="cursor:pointer; display:flex; align-items:flex-start; gap:10px; margin:0;">
                    <input type="radio" name="hookupVenueRadio" value="${v.id}" ${idx === 0 ? 'checked' : ''} onchange="selectedHookupVenue='${v.id}'" style="margin-top:4px;">
                    <div style="flex:1;">
                        <div class="card-title-row" style="margin-bottom:2px;">
                            <span class="card-title" style="font-size:13.5px;">${v.name}</span>
                            <span class="card-badge badge-purple">₺ ${v.cost.toLocaleString('tr-TR')}</span>
                        </div>
                        <p class="card-desc" style="margin:0; font-size:11.5px;">${v.desc}</p>
                    </div>
                </label>
            `).join("")}
        </div>

        <div style="font-size:12px; font-weight:700; color:#f8fafc; margin-bottom:6px;">2. Korunma Tercihin:</div>
        <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:16px;">
            ${(marketData.hookup_protection_choices || []).map((p, idx) => `
                <label class="panel-card" style="cursor:pointer; display:flex; align-items:flex-start; gap:10px; margin:0; border-left: 3px solid ${p.id === 'protected' ? '#10b981' : '#ef4444'};">
                    <input type="radio" name="hookupProtRadio" value="${p.id}" ${idx === 0 ? 'checked' : ''} onchange="selectedHookupProtection='${p.id}'" style="margin-top:4px;">
                    <div style="flex:1;">
                        <div class="card-title" style="font-size:13px; color:#f8fafc;">${p.name}</div>
                        <p class="card-desc" style="margin:2px 0 0; font-size:11px;">${p.desc}</p>
                    </div>
                </label>
            `).join("")}
        </div>

        <button type="button" class="btn-primary" style="width:100%; padding:10px;" onclick="submitHookup()">Geceye Ak & Kaçamağı Yaşa 🔥</button>
    `;
    openDialogModal("genericModal");
}

async function submitHookup() {
    const isProtected = (selectedHookupProtection === "protected");
    await performActivity("hookup", {
        venue_id: selectedHookupVenue,
        use_protection: isProtected
    });
    closeModal("genericModal");
}

function openExMidnightTextModal(personId) {
    sound.playClick();
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `📱 Gece 02:30 'Uyudun mu?' Krizi`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="margin-bottom:12px; text-align:center; padding:15px; border-left:3px solid #ec4899;">
            <div style="font-size:13px; color:#cbd5e1; font-style:italic;">
                "Uyudun mu? Kaç saattir eski fotoğraflarımıza bakıyorum... Seni hâlâ unutamadım 💔"
            </div>
            <div style="font-size:11px; color:#94a3b8; margin-top:6px;">— Gönderen: <b>${person.name}</b> (Eski Sevgili)</div>
        </div>
        <p class="card-desc" style="margin-bottom:12px;">Bu beklenmedik gece yarısı mesajı karşısında tavrın ne olacak?</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <button type="button" class="btn-primary" style="text-align:left;" onclick="submitExMidnightText('${person.id}', 'show_partner')">
                <b>🤝 Mevcut Sevgilime / Güvendiğim Arkadaşıma Göster (Dürüstlük)</b>
                <div style="font-size:11px; opacity:0.8;">Güven tazeler, ilişkiniz çelikleşir.</div>
            </button>
            <button type="button" class="btn-choice" style="text-align:left;" onclick="submitExMidnightText('${person.id}', 'reply_secretly')">
                <b>🤫 Gizlice Cevap Yaz: 'Uyumadım, ben de seni düşünüyordum...'</b>
                <div style="font-size:11px; color:#f87171;">Ateşle oynamak! Yakalanma riski %45!</div>
            </button>
            <button type="button" class="btn-choice" style="text-align:left;" onclick="submitExMidnightText('${person.id}', 'block_ex')">
                <b>🚫 Tek Kelime Etmeden Her Yerden Engeli Bas</b>
                <div style="font-size:11px; opacity:0.8;">Geçmişi tek hamlede arkanda bırak.</div>
            </button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function submitExMidnightText(personId, choiceId) {
    await performActivity("handle_ex_midnight_text", { person_id: personId, choice_id: choiceId });
    closeModal("genericModal");
}

function openCoupleVacationModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.couple_vacations) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `✈️ Romantik Tatil & Balayı: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            <b>${person.name}</b> (Sevgi Dili: <b>${person.love_language || "Kaliteli Zaman"}</b>) ile baş başa romantik bir kaçamak seç:
        </p>
        ${marketData.couple_vacations.map(v => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${v.name}</span>
                    <span class="card-badge badge-purple">₺ ${v.cost.toLocaleString('tr-TR')}</span>
                </div>
                <p class="card-desc">${v.desc}<br>İlişki: <b>+%${v.rel_boost}</b> • Mutluluk: <b>+%${v.hap_boost}</b></p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectCoupleVacation('${person.id}', '${v.id}')">Biletleri Al & Tatile Çık ✈️</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function selectCoupleVacation(personId, vacationId) {
    await performActivity("couple_vacation", { person_id: personId, vacation_id: vacationId });
    closeModal("genericModal");
}

function openSocialHangoutModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.social_hangouts) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🎉 Sosyal Etkinlik: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = marketData.social_hangouts.map(h => `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">${h.name}</span>
                <span class="card-badge badge-green">₺ ${h.cost.toLocaleString('tr-TR')}</span>
            </div>
            <p class="card-desc">${h.desc} (İlişki: <b>+%${h.rel_boost}</b>)</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectSocialHangout('${person.id}', '${h.id}')">Birlikte Git 🙌</button>
        </div>
    `).join("");
    openDialogModal("genericModal");
}

async function selectSocialHangout(personId, hangoutId) {
    await performActivity("social_hangout", { person_id: personId, hangout_id: hangoutId });
    closeModal("genericModal");
}

// ----------------- KISMETAPP (FLÖRT UYGULAMASI) & SOSYAL TANIŞMA MODALLARI -----------------

let kismetIndex = 0;
let activeKismetFilter = "standard";

async function openKismetAppModal(filterType = null) {
    sound.playClick();
    if (filterType) {
        activeKismetFilter = filterType;
    }
    document.getElementById("genericModalTitle").textContent = "📱 KısmetApp — Flört & Eşleşme";
    const body = document.getElementById("genericModalBody");

    // Eğer aday listesi boşsa veya yeni filtre seçildiyse sunucudan üret
    if (filterType || !gameState.dating_candidates || gameState.dating_candidates.length === 0) {
        body.innerHTML = `<p class="card-desc">Yakınındaki profiller taranıyor...</p>`;
        openDialogModal("genericModal");
        const res = await performActivity("kismet_generate", { filter_type: activeKismetFilter });
        if (!res || !res.success) {
            body.innerHTML = `<div class="panel-card"><p class="card-desc">${res ? res.message : "Aday bulunamadı."}</p></div>`;
            return;
        }
        kismetIndex = 0;
    } else {
        openDialogModal("genericModal");
    }

    renderKismetCandidateView();
}

function renderKismetCandidateView() {
    const body = document.getElementById("genericModalBody");
    const candidates = gameState.dating_candidates || [];

    const filterBarHtml = `
        <div class="kismet-filter-bar">
            <button type="button" class="filter-pill ${activeKismetFilter === 'standard' ? 'active' : ''}" onclick="openKismetAppModal('standard')">🔥 Standart (Ücretsiz)</button>
            <button type="button" class="filter-pill ${activeKismetFilter === 'vip_wealth' ? 'active' : ''}" onclick="openKismetAppModal('vip_wealth')">💎 Elit & Zengin (5.000₺)</button>
            <button type="button" class="filter-pill ${activeKismetFilter === 'vip_looks' ? 'active' : ''}" onclick="openKismetAppModal('vip_looks')">✨ Süper Model (3.000₺)</button>
            <button type="button" class="filter-pill ${activeKismetFilter === 'vip_smarts' ? 'active' : ''}" onclick="openKismetAppModal('vip_smarts')">🧠 Yüksek Zeka (3.000₺)</button>
        </div>
    `;

    if (candidates.length === 0 || kismetIndex >= candidates.length) {
        body.innerHTML = `
            ${filterBarHtml}
            <div class="panel-card" style="text-align:center; padding:22px;">
                <p class="card-desc" style="margin-bottom:12px;">Bu gruptaki tüm aday profillerini inceledin!</p>
                <button type="button" class="btn-primary" onclick="openKismetAppModal('${activeKismetFilter}')">🔄 Yeni Aday Profilleri Getir</button>
            </div>
        `;
        return;
    }

    const c = candidates[kismetIndex];
    const avatarEmoji = c.gender === "Erkek" ? "🧔" : "👩";

    body.innerHTML = `
        ${filterBarHtml}
        <div class="kismet-card">
            <div class="kismet-top-row">
                <div style="display:flex; gap:12px; align-items:center;">
                    <div class="kismet-avatar-circle">${avatarEmoji}</div>
                    <div>
                        <div style="font-size:16.5px; font-weight:800; color:#fff;">${c.name}, ${c.age}</div>
                        <div style="font-size:12px; color:#fbcfe8;">💼 ${c.job} • ✨ ${c.zodiac}</div>
                        <div style="font-size:11.5px; color:#cbd5e1; margin-top:2px;">${getPersonalityLabel(c.personality)}</div>
                    </div>
                </div>
                <span class="kismet-compat-badge">💞 %${c.compatibility} Uyum</span>
            </div>

            <div class="kismet-bio-box">"${c.bio}"</div>

            <div class="person-chip-row">
                ${(c.interests || []).map(i => `<span class="person-chip">${i}</span>`).join("")}
            </div>

            <div class="person-stats-grid">
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>✨ Görünüş</span><span>%${c.looks}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-looks" style="width:${c.looks}%"></div></div>
                </div>
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>🧠 Zeka</span><span>%${c.smarts}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-smarts" style="width:${c.smarts}%"></div></div>
                </div>
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>💰 Varlık</span><span>%${c.wealth}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-health" style="width:${c.wealth}%"></div></div>
                </div>
                <div class="person-stat-pill">
                    <div class="person-stat-pill-header"><span>🤪 Çılgınlık</span><span>%${c.craziness}</span></div>
                    <div class="stat-progress-bg"><div class="stat-progress-bar bar-happiness" style="width:${c.craziness}%"></div></div>
                </div>
            </div>

            <div style="margin: 10px 0 6px;">
                <div style="font-size:11.5px; font-weight:700; color:#cbd5e1; margin-bottom:4px;">💬 Özel Açılış Cümlesiyle Başla:</div>
                <div style="display:flex; flex-wrap:wrap; gap:4px;">
                    ${(marketData.dating_opening_lines || []).map(line => `
                        <button type="button" class="btn-dm-pill" style="font-size:11px;" onclick="sendFlirtOpening('${c.id}', '${line.id}')">
                            ${line.name}
                        </button>
                    `).join("")}
                </div>
            </div>

            <div class="kismet-swipe-bar">
                <button type="button" class="btn-swipe-pass" onclick="nextKismetCandidate()">❌ Pas Geç (${kismetIndex + 1}/${candidates.length})</button>
                <button type="button" class="btn-swipe-like" onclick="matchKismetCandidate('${c.id}', 'Flört')">🔥 Flört Et</button>
                <button type="button" class="btn-swipe-like" style="background:linear-gradient(135deg,#8b5cf6 0%,#6d28d9 100%);" onclick="matchKismetCandidate('${c.id}', 'Sevgili')">💘 Sevgili Ol</button>
            </div>
        </div>
    `;
}

async function sendFlirtOpening(candidateId, lineId) {
    const res = await performActivity("flirt_opening", {
        candidate_id: candidateId,
        line_id: lineId
    });
    if (res && res.success && res.candidate) {
        const cand = (gameState.dating_candidates || []).find(x => x.id === candidateId);
        if (cand) cand.compatibility = res.candidate.compatibility;
        renderKismetCandidateView();
    }
}

function nextKismetCandidate() {
    sound.playClick();
    kismetIndex++;
    renderKismetCandidateView();
}

async function matchKismetCandidate(candidateId, relationMode) {
    const res = await performActivity("kismet_swipe", {
        candidate_id: candidateId,
        relation_mode: relationMode
    });
    if (res && res.success) {
        closeModal("genericModal");
    }
}

function openMeetPlacesModal() {
    sound.playClick();
    if (!marketData || !marketData.meet_places) return;
    document.getElementById("genericModalTitle").textContent = "🥂 Sosyal Ortamlar & Görücü Usulü Tanışma";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">Gittiğin mekana göre tanışacağın kişilerin karakteri, zekası ve maddi durumu değişiklik gösterir:</p>
        ${marketData.meet_places.map(pl => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${pl.name}</span>
                    <span class="card-badge badge-green">${pl.cost === 0 ? 'Ücretsiz' : '₺ ' + pl.cost.toLocaleString('tr-TR')}</span>
                </div>
                <p class="card-desc">${pl.desc}</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectMeetPlace('${pl.id}')">Mekana Git & Tanış</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function selectMeetPlace(placeId) {
    await performActivity("meet_place", { place_id: placeId });
    closeModal("genericModal");
}

function openDateVenueModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.date_venues) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🌹 Randevu Mekanı Seç: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            <b>${person.name}</b> kişilik tipi: <b>${getPersonalityLabel(person.personality)}</b>. Onun ruhuna uygun bir mekan seçersen ekstra uyum kazanırsın!
        </p>
        ${marketData.date_venues.map(v => {
            const isFav = (v.best_for || []).includes(person.personality);
            return `
                <div class="panel-card" style="${isFav ? 'border-color:#f472b6;' : ''}">
                    <div class="card-title-row">
                        <span class="card-title">${v.name}</span>
                        <span class="card-badge ${isFav ? 'badge-purple' : 'badge-green'}">₺ ${v.cost.toLocaleString('tr-TR')}</span>
                    </div>
                    <p class="card-desc">
                        ${v.desc}
                        ${isFav ? `<br><b style="color:#f472b6;">✨ ${person.name}'ın kişiliğine tam uyumlu favori mekan!</b>` : ""}
                    </p>
                    <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectDateVenue('${person.id}', '${v.id}')">Randevuya Çıkar</button>
                </div>
            `;
        }).join("")}
    `;
    openDialogModal("genericModal");
}

async function selectDateVenue(personId, venueId) {
    await performActivity("venue_date", { person_id: personId, venue_id: venueId });
    closeModal("genericModal");
}

function openCustomGiftModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.romantic_gifts) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🎁 Hediye Seç: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = marketData.romantic_gifts.map(g => `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">${g.name}</span>
                <span class="card-badge badge-green">₺ ${g.cost.toLocaleString('tr-TR')}</span>
            </div>
            <p class="card-desc">İlişki Etkisi: <b>+%${g.rel_boost}</b></p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectCustomGift('${person.id}', '${g.id}')">Hediye Et</button>
        </div>
    `).join("");
    openDialogModal("genericModal");
}

async function selectCustomGift(personId, giftId) {
    await performActivity("custom_gift", { person_id: personId, gift_id: giftId });
    closeModal("genericModal");
}

function openRingProposalModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.engagement_rings) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `💍 Evlilik Teklifi Yüzüğü: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            <b>${person.name}</b> (${getPersonalityLabel(person.personality)}) önünde diz çökmek için bir yüzük seç:
        </p>
        ${marketData.engagement_rings.map(r => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${r.name}</span>
                    <span class="card-badge badge-yellow">₺ ${r.cost.toLocaleString('tr-TR')}</span>
                </div>
                <p class="card-desc">Kabul Şansı Bonusu: <b>+%${Math.round((r.bonus_chance || 0.1) * 100)}</b></p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitRingProposal('${person.id}', '${r.id}', ${r.cost})">Diz Çök & Teklif Et 💍</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitRingProposal(personId, ringId, ringCost) {
    await performActivity("propose_marriage", {
        person_id: personId,
        ring_id: ringId,
        ring_cost: ringCost
    });
    closeModal("genericModal");
}

function openWeddingModal(personId) {
    sound.playClick();
    if (!marketData || !marketData.wedding_venues) return;
    const person = gameState.relationships.find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `👰🤵 Düğün & Nikah Organizasyonu: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <label class="panel-card choice-card" style="margin-bottom:10px;">
            <input type="checkbox" id="chkPrenup" style="width:18px; height:18px; margin-top:2px; flex-shrink:0;">
            <div>
                <div style="font-size:13px; font-weight:700; color:#fde68a;">📜 Evlilik Sözleşmesi (Mal Ayrılığı) İmzalat</div>
                <p class="card-desc" style="margin-top:4px;">
                    Boşanma durumunda servetinin yarı yarıya bölünmesini engeller; ancak nişanlının kişiliğine göre biraz kırgınlık yaratabilir.
                </p>
            </div>
        </label>
        <div class="panel-card" style="margin-bottom:12px;">
            <label for="selGuestTier" style="font-size:12.5px; font-weight:800; color:#f9a8d4; display:block; margin-bottom:6px;">💌 Düğün Davetli Listesi Seçimi:</label>
            <select id="selGuestTier" class="form-select">
                <option value="family_friends">💃 Tüm Akrabalar, Komşular & Dostlar (Standart Takı)</option>
                <option value="vip_press">📸 VIP Cemiyet, Ünlüler & Magazin Basını (+%35 Takı & +15 Şöhret)</option>
                <option value="core_family">🤍 Sadece Çekirdek Aile & Yakın Şahitler (+18 Aile Onayı)</option>
            </select>
        </div>
        ${marketData.wedding_venues.map(w => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${w.name}</span>
                    <span class="card-badge badge-green">Maliyet: ₺ ${w.cost.toLocaleString('tr-TR')}</span>
                </div>
                <p class="card-desc">
                    ${w.desc}<br>
                    🎁 Beklenen Takı Merasimi Geliri: <b>₺ ${w.min_gifts.toLocaleString('tr-TR')} - ₺ ${w.max_gifts.toLocaleString('tr-TR')}</b>
                </p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitWeddingPlan('${person.id}', '${w.id}')">Bu Düğünü Yap & Evlen 🥂</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitWeddingPlan(personId, venueId) {
    const chk = document.getElementById("chkPrenup");
    const signPrenup = chk ? chk.checked : false;
    const guestSel = document.getElementById("selGuestTier");
    const guestTier = guestSel ? guestSel.value : "family_friends";
    await performActivity("plan_wedding", {
        person_id: personId,
        venue_id: venueId,
        sign_prenup: signPrenup,
        guest_tier: guestTier
    });
    closeModal("genericModal");
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
    document.getElementById("genericModalTitle").textContent = "📈 Borsa İstanbul, Kripto & Kaldıraç Piyasası";
    const body = document.getElementById("genericModalBody");
    body.innerHTML = "";

    if (!gameState.stocks) return;

    const headerActions = document.createElement("div");
    headerActions.style.cssText = "display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-bottom:12px;";
    headerActions.innerHTML = `
        <button type="button" class="btn-choice" onclick="openLeverageModal()">🚀 10x Kaldıraçlı İşlem (Long/Short)</button>
        <button type="button" class="btn-choice" onclick="openInsiderTradingModal()">🕵️‍♂️ İçeriden Bilgi (Insider)</button>
        <button type="button" class="btn-choice" style="grid-column: span 2;" onclick="openCryptoStakingModal()">🪙 Kripto Staking (%12 Yıllık Pasif Faiz)</button>
    `;
    body.appendChild(headerActions);

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

async function manageAssetExtra(assetId, subAction) {
    await performActivity("asset_manage", { asset_id: assetId, sub_action: subAction });
}

function openAuctionModal() {
    sound.playClick();
    if (!marketData || !marketData.auction_items) return;
    document.getElementById("genericModalTitle").textContent = "🖼️ VIP Sanat, Antika & Koleksiyon Müzayedesi";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">Müzayededen alınan nadir eserler her yıl <b>%10 ile %22</b> arasında değer kazanır ve cemiyette şöhretini artırır:</p>
        ${marketData.auction_items.map(item => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${item.name}</span>
                    <span class="card-badge badge-yellow">₺ ${item.price.toLocaleString("tr-TR")}</span>
                </div>
                <p class="card-desc">${item.desc}</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="buyAuctionItem('${item.id}')">🔨 Teklif Ver & Satın Al</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function buyAuctionItem(itemId) {
    await performActivity("buy_auction", { item_id: itemId });
    closeModal("genericModal");
}

function openFameModal() {
    sound.playClick();
    const awardsText = (gameState.fame_awards && gameState.fame_awards.length > 0)
        ? gameState.fame_awards.join(" • ")
        : "Henüz ödül kazanılmadı";

    document.getElementById("genericModalTitle").textContent = `🌟 Şöhret, Sahne & Magazin İmparatorluğu (%${gameState.fame || 0})`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f59e0b; margin-bottom:12px; background:linear-gradient(135deg, rgba(245,158,11,0.08), rgba(168,85,247,0.08));">
            <div class="card-title-row">
                <span class="card-title">👑 Yıldız Profilin: ${gameState.fame_archetype || "Arketip Seçilmedi"}</span>
                <span class="card-badge badge-yellow">Şöhret: %${gameState.fame || 0}</span>
            </div>
            <p class="card-desc" style="margin-top:4px;">
                Menajer: <b>${gameState.fame_manager || "Bağımsız / Kendi Kendini Yönetme"}</b><br>
                Ödüller: <b>${awardsText}</b>
            </p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:10px;">
                <button type="button" class="btn-choice" onclick="openFameArchetypeModal()">🎭 Şöhret Arketipini Seç</button>
                <button type="button" class="btn-choice" onclick="openFameManagerModal()">🤝 VIP Menajer / Ajans</button>
            </div>
            <button type="button" class="btn-choice" style="border-color:#ef4444; color:#ef4444; width:100%; margin-top:6px;" onclick="openFameCrisisModal()">📸💥 Magazin & Skandal Kriz Masası</button>
        </div>

        <div class="person-action-group-title" style="margin-bottom:8px;">Sahne, Performans & Global Şöhret:</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <div class="panel-card" style="border-color:#ec4899;">
                <div class="card-title-row"><span class="card-title">🎪 Harbiye Açıkhava Konseri & Stadyum Turnesi</span><span class="card-badge badge-green">Milyonluk Gişe</span></div>
                <p class="card-desc">En az %25 Şöhret gerekir. 15.000 kişilik Harbiye Açıkhava'da veya stadyumda biletleri tüket, dev gişe geliri elde et!</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerFameAction('harbiye_concert')">Harbiye'ye Çık 🎪🔥</button>
            </div>
            <div class="panel-card" style="border-color:#f59e0b;">
                <div class="card-title-row"><span class="card-title">🏆 Kırmızı Halı & Altın Kelebek Ödül Töreni</span><span class="card-badge badge-yellow">+25 Şöhret & Prestij</span></div>
                <p class="card-desc">En az %35 Şöhret gerekir. Yılın En İlham Veren Yıldızı ödülünü kazan, canlı yayında tüm Türkiye önünde konuşma yap!</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerFameAction('red_carpet_award')">Kırmızı Halıda Yürü 🏆✨</button>
            </div>
            <div class="panel-card" style="border-color:#a855f7;">
                <div class="card-title-row"><span class="card-title">👠 Paris & Milano Moda Haftası (Front Row)</span><span class="card-badge badge-purple">+16 Şöhret & Görünüş</span></div>
                <p class="card-desc">En az %30 Şöhret veya %80 Görünüş gerekir. Dünyaca ünlü tasarımcıların en ön sırasında otur, Vogue ve Elle kapağı ol!</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerFameAction('fashion_week')">Front Row'da Yerini Al 👠✨</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">🎭 Türkiye Yetenek & Ekran Seçmeleri</span><span class="card-badge badge-green">₺ 2.000</span></div>
                <p class="card-desc">Kamera karşısına çıkıp yeteneğini sergile, şöhret basamaklarını hızla tırman!</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerFameAction('audition_fame')">Seçmelere Katıl 🌟</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">🏆 Hit Albüm / Başrol Film / Şampiyonluk Maçı</span><span class="card-badge badge-yellow">+Telif & Şöhret</span></div>
                <p class="card-desc">En az %20 Şöhret veya Sanat/Spor kariyeri gerekir. Milyonluk telif ve prim kazandırır!</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerFameAction('release_work')">Yeni Eser / Performans Çıkar 🔥</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">📺 Prime-Time Talk Show Konuğu Ol</span><span class="card-badge badge-blue">+45B Takipçi</span></div>
                <p class="card-desc">Cuma gecesi canlı yayına konuk ol, hem şöhretini hem sosyal medya takipçilerini katla!</p>
                <button type="button" class="btn-choice" style="margin-top:8px;" onclick="triggerFameAction('tv_show')">Talk Show'a Çık 📺</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">💎 Dev Marka Reklam Anlaşması</span><span class="card-badge badge-green">Yüksek Gelir</span></div>
                <p class="card-desc">En az %30 Şöhret gerekir. Şöhret oranına göre yüz binlerce TL reklam ücreti al.</p>
                <button type="button" class="btn-choice" style="margin-top:8px;" onclick="triggerFameAction('brand_deal')">Reklam Sözleşmesi İmzala ✍️</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">📸 Magazin & Paparazzi Gündemi Yarat</span><span class="card-badge badge-purple">+18 Şöhret</span></div>
                <p class="card-desc">Bebek sahilinde paparazzilere sansasyonel röportaj vererek tüm manşetlere çık!</p>
                <button type="button" class="btn-choice" style="margin-top:8px;" onclick="triggerFameAction('paparazzi_stunt')">Manşetlere Çık 📸</button>
            </div>
            <div class="panel-card" style="border-color:#f472b6;">
                <div class="card-title-row"><span class="card-title">💘 VIP Ünlüler Kulübünde Yıldızla Tanış</span><span class="card-badge badge-purple">VIP Aşk</span></div>
                <p class="card-desc">Ünlü bir Dizi Yıldızı, Pop İkonu, Süpermodel veya Milli Futbolcu ile yılın aşkına başla!</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerFameAction('celebrity_date')">VIP Galaya Git & Tanış 🥂</button>
            </div>
        </div>
    `;
    openDialogModal("genericModal");
}

async function triggerFameAction(subAction, extraId = "") {
    await performActivity("fame_action", { sub_action: subAction, extra_id: extraId });
    closeModal("genericModal");
}

function openFameArchetypeModal() {
    sound.playClick();
    const archetypes = (marketData && marketData.fame_archetypes) || [];
    document.getElementById("genericModalTitle").textContent = "🎭 Şöhret Arketipini & İmajını Belirle";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Hangi alanda parlamak istiyorsun? Tarzını seçerek kariyerine güçlü bir kimlik kazandır:</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${archetypes.map(a => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${a.name}</span>
                        <span class="card-badge badge-yellow">${a.primary_skill.toUpperCase()}</span>
                    </div>
                    <p class="card-desc">${a.desc}</p>
                    <p class="card-desc" style="font-size:0.8rem; color:var(--text-muted);">Öne Çıkan Eser: <b>${a.work_name}</b></p>
                    <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitFameArchetype('${a.id}')">Bu İmajı Seç 🌟</button>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openFameModal()">← Şöhret Merkezine Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitFameArchetype(archId) {
    await performActivity("fame_action", { sub_action: "select_archetype", extra_id: archId });
    openFameModal();
}

function openFameManagerModal() {
    sound.playClick();
    const managers = (marketData && marketData.fame_managers) || [];
    document.getElementById("genericModalTitle").textContent = "🤝 VIP Menajer & PR Ajansı Seç";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Kariyerini zirveye taşıyacak profesyonel bir menajer veya uluslararası bir ajansla el sıkış:</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${managers.map(m => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${m.name}</span>
                        <span class="card-badge badge-green">${m.cost > 0 ? '₺ ' + m.cost.toLocaleString("tr-TR") : 'Ücretsiz'}</span>
                    </div>
                    <p class="card-desc">${m.desc}</p>
                    <p class="card-desc" style="font-size:0.8rem; color:var(--text-muted);">Komisyon: <b>%${m.commission}</b></p>
                    <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitFameManager('${m.id}')">Bu Ajansla Anlaş 🤝</button>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openFameModal()">← Şöhret Merkezine Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitFameManager(mgrId) {
    await performActivity("fame_action", { sub_action: "hire_manager", extra_id: mgrId });
    openFameModal();
}

function openFameCrisisModal() {
    sound.playClick();
    const crises = (marketData && marketData.fame_crises) || [];
    document.getElementById("genericModalTitle").textContent = "📸💥 Magazin & Skandal Kriz Masası";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Magazinciler peşinde! Ansızın patlak veren sansasyon ve skandallara karşı duruşunu seç:</p>
        <div style="display:flex; flex-direction:column; gap:12px;">
            ${crises.map(c => `
                <div class="panel-card" style="border-color:#ef4444;">
                    <div class="card-title-row">
                        <span class="card-title">${c.title}</span>
                    </div>
                    <p class="card-desc" style="margin-bottom:10px;">${c.desc}</p>
                    <div style="display:flex; flex-direction:column; gap:6px;">
                        ${c.options.map(opt => `
                            <button type="button" class="btn-choice" style="text-align:left; padding:8px 12px;" onclick="submitFameCrisis('${c.id}', '${opt.id}')">
                                <b>${opt.text}</b>
                            </button>
                        `).join("")}
                    </div>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openFameModal()">← Şöhret Merkezine Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitFameCrisis(crisisId, choiceId) {
    await performActivity("fame_action", { sub_action: "fame_crisis_choice", extra_id: `${crisisId}:${choiceId}` });
    closeModal("genericModal");
}

function openPoliticsModal() {
    sound.playClick();
    if (!marketData || !marketData.political_offices) return;
    document.getElementById("genericModalTitle").textContent = "🏛️ Siyaset, Seçim & Devlet Yönetimi";
    const body = document.getElementById("genericModalBody");

    let activeOfficeHtml = "";
    if (gameState.political_office) {
        activeOfficeHtml = `
            <div class="panel-card" style="border-color:var(--accent-blue); margin-bottom:12px;">
                <div class="card-title-row">
                    <span class="card-title">🇹🇷 Aktif Makam: ${gameState.political_office}</span>
                    <span class="card-badge badge-green">Halk Desteği: %${gameState.approval_rating}</span>
                </div>
                <p class="card-desc">Yıllık Makam Maaşı: <b>₺ ${(gameState.political_salary || 0).toLocaleString("tr-TR")}</b></p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:8px;">
                    <button type="button" class="btn-choice" onclick="triggerPoliticalAction('hold_rally')">📢 Meydan Mitingi (25B₺)</button>
                    <button type="button" class="btn-choice" onclick="triggerPoliticalAction('public_project')">🏗️ Altyapı & Hizmet Aç</button>
                    <button type="button" class="btn-choice" onclick="triggerPoliticalAction('tv_debate')">📺 Canlı Yayın Tartışması</button>
                    <button type="button" class="btn-choice" onclick="triggerPoliticalAction('corrupt_lobby')">💼 Gizli Lobi İhalesi (Riskli)</button>
                </div>
            </div>
        `;
    }

    body.innerHTML = `
        ${activeOfficeHtml}
        <div class="person-action-group-title" style="margin-bottom:8px;">🗳️ Seçim Adaylığı & Makamlar</div>
        ${marketData.political_offices.map(off => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${off.title}</span>
                    <span class="card-badge badge-yellow">Kampanya: ₺ ${off.campaign_cost.toLocaleString("tr-TR")}</span>
                </div>
                <p class="card-desc">
                    ${off.desc}<br>
                    Min. Yaş: <b>${off.min_age}</b> • Eğitim: <b>${off.req_edu}</b> • Maaş: <b>+₺ ${off.salary.toLocaleString("tr-TR")}/yıl</b>
                </p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="runForOffice('${off.id}')">🗳️ Aday Ol & Seçime Gir</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function runForOffice(officeId) {
    await performActivity("politics_run", { office_id: officeId });
    openPoliticsModal();
}

async function triggerPoliticalAction(subAction) {
    await performActivity("politics_action", { sub_action: subAction });
    openPoliticsModal();
}

function openBusinessModal() {
    sound.playClick();
    if (!marketData || !marketData.businesses) return;
    document.getElementById("genericModalTitle").textContent = "🏢 Girişimcilik & Kendi Şirketini Kur";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="margin-bottom:12px; background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.15);">
            <div style="font-size:12px; font-weight:700; color:#f8fafc; margin-bottom:6px;">✨ Şirketine Özel İsim Ver (İsteğe Bağlı):</div>
            <input type="text" id="customBizNameInput" placeholder="Örn: Demir Holding / Nova Burger (Boş bırakırsan varsayılan atanır)" style="width:100%; padding:9px 12px; border-radius:8px; border:1px solid rgba(255,255,255,0.2); background:rgba(15,23,42,0.85); color:#fff; font-size:13px; box-sizing:border-box;">
        </div>
        <p class="card-desc" style="margin-bottom:10px;">
            Kurmak istediğin sektörü ve şirket modelini seç:
        </p>
        <div style="display:flex; flex-direction:column; gap:10px;">
            ${marketData.businesses.map(b => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${b.name}</span>
                        <span class="card-badge ${gameState.money >= b.cost ? 'badge-green' : 'badge-danger'}">
                            Sermaye: ₺ ${b.cost.toLocaleString("tr-TR")}
                        </span>
                    </div>
                    <p class="card-desc" style="margin:4px 0 6px;">${b.desc || ''}</p>
                    <div class="person-chip-row" style="margin-bottom:8px;">
                        <span class="person-chip" style="color:#93c5fd;">🏢 Sektör: ${b.sector}</span>
                        <span class="person-chip" style="color:#6ee7b7;">📈 Beklenen Kâr: +₺ ${b.base_profit.toLocaleString("tr-TR")}/yıl</span>
                    </div>
                    <button type="button" class="btn-primary" ${gameState.money < b.cost ? 'disabled style="opacity:0.5;"' : ''} onclick="createBusiness('${b.id}')">
                        ${gameState.money >= b.cost ? 'Şirketi Kur 🚀' : 'Yetersiz Sermaye'}
                    </button>
                </div>
            `).join("")}
        </div>
    `;
    openDialogModal("genericModal");
}

async function createBusiness(bizId) {
    const customName = document.getElementById("customBizNameInput") ? document.getElementById("customBizNameInput").value : "";
    await performActivity("start_business", { biz_id: bizId, custom_name: customName });
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
    document.getElementById("genericModalTitle").textContent = "🦹 Yeraltı Dünyası, Mafya & Cezaevi";
    const body = document.getElementById("genericModalBody");

    if (gameState.is_in_prison) {
        body.innerHTML = `
            <div class="panel-card" style="border-color: var(--accent-red);">
                <h4>🚨 Cezaevindesin (Kalan: ${gameState.prison_years_left} Yıl)</h4>
                <p class="card-desc" style="margin: 8px 0;">Özgürlüğüne kavuşmak veya koğuşta racon kesmek için bir hamle seç:</p>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <button type="button" class="btn-primary" onclick="openPrisonModal()">⛓️ Koğuş Hayatı, Racon & Sigara Masası</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('escape_tunnel')">🏃💨 Havalandırma Tünelinden Firar Dene</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('escape_disguise')">🎭 Gardiyan Üniformasıyla Firar Dene</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('appeal_lawyer')">⚖️ Ünlü Ceza Avukatı Tut & Temyiz (60.000 TL)</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('bribe_guard')">👮 Gardiyana Rüşvet Ver (30.000 TL -> -1 Yıl)</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('library')">📖 Kütüphanede Hukuk Kitapları Oku</button>
                    <button type="button" class="btn-choice" onclick="doPrisonAction('yard_workout')">🏋️ Avluda Ağırlık Çalış</button>
                </div>
            </div>
        `;
    } else if (gameState.syndicate_id) {
        const ops = (marketData && marketData.syndicate_operations) || [];
        body.innerHTML = `
            <div class="panel-card" style="border-color:#ef4444; margin-bottom:12px; background:linear-gradient(135deg, rgba(239,68,68,0.12), rgba(0,0,0,0.4));">
                <div class="card-title-row">
                    <span class="card-title">${gameState.syndicate_name || "Gayrimeşru Aile"}</span>
                    <span class="card-badge badge-red">Korku / Saygınlık: %${gameState.syndicate_notoriety || 0}</span>
                </div>
                <p class="card-desc" style="margin-top:4px;">
                    Rütben: <b>${gameState.syndicate_rank || "Çırak"}</b><br>
                    Yıllık Harac Gelirin: <b>₺ ${(gameState.syndicate_racket_annual || 0).toLocaleString("tr-TR")}</b>
                </p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:8px;">
                    <button type="button" class="btn-primary" onclick="advanceSyndicateRank()">👑 Rütbe Atla</button>
                    <button type="button" class="btn-choice" onclick="openSyndicateSummitModal()">⚔️ Masada Zirve & Racon</button>
                </div>
            </div>

            <div class="person-action-group-title" style="margin-bottom:8px;">Yeraltı Operasyonları & Çökme:</div>
            <div style="display:flex; flex-direction:column; gap:8px;">
                ${ops.map(op => `
                    <div class="panel-card">
                        <div class="card-title-row">
                            <span class="card-title">${op.name}</span>
                            <span class="card-badge badge-yellow">${op.cost > 0 ? 'Bütçe: ₺ ' + op.cost.toLocaleString("tr-TR") : 'Ücretsiz'}</span>
                        </div>
                        <p class="card-desc">${op.desc}</p>
                        <button type="button" class="btn-primary" style="margin-top:6px;" onclick="doSyndicateOperation('${op.id}')">Operasyonu Başlat 💥</button>
                    </div>
                `).join("")}
            </div>
        `;
    } else {
        body.innerHTML = `
            <div class="panel-card" style="border-color:#ef4444; margin-bottom:12px; background:linear-gradient(135deg, rgba(239,68,68,0.08), rgba(0,0,0,0.2));">
                <div class="card-title-row">
                    <span class="card-title">🏛️ Gayrimeşru Aile & Yeraltı Masası</span>
                    <span class="card-badge badge-red">Yeraltı Dünyası</span>
                </div>
                <p class="card-desc" style="margin-top:4px;">Büyük bir mafya ailesine katılarak sokakları ve gece hayatını haraca bağla, racon kes!</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="openJoinSyndicateModal()">Yeraltı Masasına Otur 🗡️</button>
            </div>

            <div class="person-action-group-title" style="margin-bottom:8px;">Bireysel Suçlar:</div>
            <div style="display:flex; flex-direction:column; gap:8px;">
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
            </div>
        `;
    }
    openDialogModal("genericModal");
}

function openJoinSyndicateModal() {
    sound.playClick();
    const syns = (marketData && marketData.syndicates) || [];
    document.getElementById("genericModalTitle").textContent = "🏛️ Bir Gayrimeşru Aile Seç";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Hangi yeraltı teşkilatına biat edip masaya oturmak istiyorsun?</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${syns.map(s => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${s.name}</span>
                        <span class="card-badge badge-red">${s.territory}</span>
                    </div>
                    <p class="card-desc">Lider: <b>${s.leader}</b><br>${s.desc}</p>
                    <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitJoinSyndicate('${s.id}')">Bu Aileye Biat Et 🗡️</button>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openCrimeModal()">← Geri Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitJoinSyndicate(synId) {
    await performActivity("syndicate_join", { syndicate_id: synId });
    openCrimeModal();
}

async function doSyndicateOperation(opId) {
    await performActivity("syndicate_operation", { operation_id: opId });
    openCrimeModal();
}

async function advanceSyndicateRank() {
    await performActivity("syndicate_rank_up", {});
    openCrimeModal();
}

function openSyndicateSummitModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "⚔️ Yeraltı Masası Zirvesi";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Diğer suç örgütlerinin liderleri gizli bir yalıda toplandı. Kararını ver:</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">🗡️ Masaya Silahı Vur & Racon Kes</span></div>
                <p class="card-desc">Tüm şehirdeki haklarını talep et. Karizman ve korku seviyen güçlüyse payını katlarsın.</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitSyndicateSummit('racon_cut')">Racon Kes 🗡️</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">🤝 Barış Anlaşması İmzala</span></div>
                <p class="card-desc">Çatışmaları durdur, sınırları çiz ve yıllık 350.000 TL garanti bölge geliri bağla.</p>
                <button type="button" class="btn-choice" style="margin-top:8px;" onclick="submitSyndicateSummit('peace_treaty')">Barış İmzala 🤝</button>
            </div>
            <div class="panel-card">
                <div class="card-title-row"><span class="card-title">💣 Rakip Çetenin Deposuna Gece Baskını Yap</span></div>
                <p class="card-desc">Yüksek risk! Rakip kartelin ana lojistik kasasını patlatıp milyonlarca TL ganimet kap.</p>
                <button type="button" class="btn-primary" style="margin-top:8px; border-color:#ef4444;" onclick="submitSyndicateSummit('ambush_rival')">Gece Baskını Yap 💣</button>
            </div>
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openCrimeModal()">← Yeraltı Merkezine Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitSyndicateSummit(choiceId) {
    await performActivity("syndicate_summit", { choice_id: choiceId });
    openCrimeModal();
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
    document.getElementById("genericModalTitle").textContent = "📜 Noter & Resmi Vasiyetname";
    const body = document.getElementById("genericModalBody");

    const children = (gameState.relationships || []).filter(p => p.relation === "Çocuk" && p.is_alive && !p.is_disowned);
    const spouse = (gameState.relationships || []).find(p => p.relation === "Eş" && p.is_alive);

    body.innerHTML = `
        <div class="panel-card" style="border-color:var(--accent-yellow); margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">📜 Aktif Vasiyet Durumu</span>
                <span class="card-badge badge-yellow">Miras: ₺ ${(gameState.net_worth || 0).toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc">Vefat ettiğinde tüm mal varlığının, aile şirketinin ve nakdinin kime devredileceğini seç:</p>
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <button type="button" class="btn-choice" onclick="saveWill('all_children')">👶 Tüm Çocuklarıma Eşit Olarak Paylaştır</button>
            ${spouse ? `<button type="button" class="btn-choice" onclick="saveWill('spouse')">💍 Yalnızca Eşime (${spouse.name}) Bırak</button>` : ""}
            <button type="button" class="btn-choice" onclick="saveWill('charity')">🏛️ Mehmetçik Vakfı ve Sokak Hayvanları Derneğine Bağışla</button>
            ${children.length > 0 ? `
                <div class="person-action-group-title" style="margin-top:6px;">Tek Favori Çocuğunu Mirasçı Seç:</div>
                ${children.map(c => `
                    <button type="button" class="btn-choice" style="border-color:var(--accent-blue);" onclick="saveWill('child_${c.id}')">👑 Tüm Mirası Yalnızca ${c.name} Adlı Çocuğuma Bırak</button>
                `).join("")}
            ` : ""}
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

    const children = (gameState.relationships || []).filter(p => p.relation === "Çocuk" && p.is_alive && !p.is_disowned);
    const childContainer = document.getElementById("deathModalChildrenContainer");
    if (childContainer) {
        if (children.length > 0) {
            childContainer.innerHTML = `
                <p class="card-desc" style="margin:10px 0 6px;">👑 Nesiller Boyu Hanedanlık: Hangi çocuğunun hayatına geçip mirası devralmak istersin?</p>
                <div style="display:flex; flex-direction:column; gap:6px;">
                    ${children.map(c => `
                        <button type="button" class="btn-primary" onclick="continueAsChild('${c.id}')">👑 ${c.name} (${c.age} Yaş) Olarak Hayata Devam Et</button>
                    `).join("")}
                </div>
            `;
        } else {
            childContainer.innerHTML = `<p class="card-desc" style="margin-top:8px;">Yaşayan bir çocuğun olmadığı için hanedanlık bu kuşakta son buldu.</p>`;
        }
    }

    openDialogModal("deathModal");
}

async function continueAsChild(childId = null) {
    sound.playClick();
    try {
        const res = await fetch("/api/reincarnate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(childId ? { child_id: childId } : {})
        });
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
    // Kullanıcı talebi doğrultusunda ekranı kapatan ve rahatsız eden bildirimler devre dışı bırakıldı.
    return;
}

// ----------------- PAKET 2, 3, 4, 10: INSTASTORY, SOYAĞACI, GARDIROP, YKS/KPSS & ASKERLİK -----------------

function openInstaStoryModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "📸 InstaStory & Alev (🔥) Merkezi";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            Attığın hikayelere göre gizli hayranlar DM kutuna <b>🔥</b> atabilir, eski sevgilin gece yarısı yazabilir veya partnerinle aşkını herkese ilan edebilirsin:
        </p>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">💪 Spor & Ayna Selfiesi Paylaş</span>
                <span class="card-badge badge-purple">🔥 Yeni Flört & Görünüş</span>
            </div>
            <p class="card-desc">Gizli bir hayranın story'ne '🔥🔥' yanıtı gönderip DM'den tanışmak ister! (Kıskanç sevgilin varsa biraz kızabilir!)</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerInstaStory('gym_mirror')">Hikayeyi Paylaş 📸</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">🍸 Gece Gezmesi & Mekan Story'si</span>
                <span class="card-badge badge-yellow">🌙 Eski Sevgili Radarı</span>
            </div>
            <p class="card-desc">Eski sevgilin hikayeni görüp 'Seni hâlâ unutamadım' diye mesaj atabilir veya gece kulübünden yeni biriyle eşleşirsin!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerInstaStory('night_out')">Mekandan Story At 🍸</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">💑🧿 Partnerinle Romantik Çift Story'si</span>
                <span class="card-badge badge-green">+18 İlişki & +10 Sadakat</span>
            </div>
            <p class="card-desc">Sevgilin/eşinle el ele fotoğrafınızı nazar boncuğuyla (🧿) paylaşıp güven tazeleyin!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerInstaStory('couple_story')">Çift Story'si Paylaş 💖</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function triggerInstaStory(storyType) {
    await performActivity("insta_story", { story_type: storyType });
    closeModal("genericModal");
}

function openFamilyTreeModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = `🌳 ${gameState.last_name} Ailesi Soyağacı (${gameState.generation || 1}. Kuşak)`;
    const body = document.getElementById("genericModalBody");

    const rels = gameState.relationships || [];
    const parents = rels.filter(p => ["Anne", "Baba"].includes(p.relation));
    const partner = rels.find(p => p.is_alive && ["Eş", "Nişanlı", "Sevgili"].includes(p.relation));
    const siblings = rels.filter(p => ["Ağabey", "Abla", "Kardeş"].includes(p.relation));
    const children = rels.filter(p => p.relation === "Çocuk");

    const renderNode = (p, extraClass = "") => `
        <button type="button" class="tree-node ${extraClass} ${!p.is_alive ? 'tree-node-dead' : ''}" onclick="closeModal('genericModal'); openPersonModal('${p.id}')">
            <div class="tree-node-emoji">${getRelationEmoji(p.relation)}</div>
            <div class="tree-node-name">${p.name}</div>
            <div class="tree-node-role">${p.relation} • ${p.age} Yaş ${!p.is_alive ? '(Vefat)' : ''}</div>
        </button>
    `;

    const parentsHtml = parents.length > 0
        ? parents.map(p => renderNode(p)).join("")
        : `<div class="card-desc">Kayıtlı ebeveyn yok</div>`;

    const myNodeHtml = `
        <div class="tree-node tree-node-me">
            <div class="tree-node-emoji">${getCharacterAvatarEmoji(gameState)}</div>
            <div class="tree-node-name">${gameState.first_name} ${gameState.last_name}</div>
            <div class="tree-node-role">SEN (${gameState.age} Yaş)</div>
        </div>
    `;

    const partnerHtml = partner ? renderNode(partner, "tree-node-partner") : "";
    const siblingsHtml = siblings.map(s => renderNode(s)).join("");

    const childrenHtml = children.length > 0
        ? children.map(c => renderNode(c)).join("")
        : `<div class="card-desc" style="font-size:11.5px;">Henüz çocuk sahibi olmadın.</div>`;

    body.innerHTML = `
        <div class="family-tree-wrap">
            <div class="tree-tier-label">1. Kuşak — Anne & Baba</div>
            <div class="tree-tier">${parentsHtml}</div>
            <div class="tree-connector"></div>
            <div class="tree-tier-label">2. Kuşak — Sen, Partnerin & Kardeşlerin</div>
            <div class="tree-tier">
                ${myNodeHtml}
                ${partnerHtml}
                ${siblingsHtml}
            </div>
            <div class="tree-connector"></div>
            <div class="tree-tier-label">3. Kuşak — Çocukların (${children.length})</div>
            <div class="tree-tier">${childrenHtml}</div>
        </div>
    `;
    openDialogModal("genericModal");
}

function openWardrobeModal() {
    sound.playClick();
    if (!marketData || !marketData.outfit_styles) return;
    document.getElementById("genericModalTitle").textContent = "👔 Gardırop, Stil & Kombin Seçimi";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            Şu anki tarzın: <b>${gameState.outfit_style || "👕 Günlük & Rahat"}</b>. Seçtiğin kombin görünüşünü, karizmanı ve flört çekiciliğini doğrudan artırır:
        </p>
        ${marketData.outfit_styles.map(st => `
            <div class="panel-card" style="${gameState.outfit_style === st.name ? 'border-color:var(--accent-green);' : ''}">
                <div class="card-title-row">
                    <span class="card-title">${st.name}</span>
                    <span class="card-badge ${st.cost === 0 ? 'badge-blue' : 'badge-yellow'}">${st.cost === 0 ? 'Ücretsiz' : '₺ ' + st.cost.toLocaleString("tr-TR")}</span>
                </div>
                <p class="card-desc">
                    ${st.desc}<br>
                    ✨ Görünüş: <b>+%${st.looks_boost}</b> • 🗣️ Hitabet: <b>+%${st.charisma_boost}</b>
                </p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectOutfitStyle('${st.id}')">Kombini Giy ✨</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function selectOutfitStyle(styleId) {
    await performActivity("outfit_style", { style_id: styleId });
    closeModal("genericModal");
}

function openMilitaryModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = `🪖 Askerlik Şubesi & Kışla (${gameState.military_status})`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            Vatan borcunu ödemek için tercihini yap: Bedelli askerlik, 6 ay kışla görevi (ömürlük koğuş dostu kazandırır!) veya Üniversite mezunlarına özel maaşlı Yedek Subaylık!
        </p>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">💳 Bedelli Askerlik (28 Gün Kışla)</span><span class="card-badge badge-yellow">₺ 180.000</span></div>
            <p class="card-desc">180.000 TL bedelli ücretini yatırıp 28 günlük temel eğitimi tamamla ve hemen terhis ol.</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectMilitaryService('bedelli')">Bedelli Başvurusu Yap 💳</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">🪖 6 Ay Kışla Hizmeti (Erbaş / Çavuş)</span><span class="card-badge badge-green">Ücretsiz + Tertip Dostu</span></div>
            <p class="card-desc">Sağlık +12, Atletizm +15, Savunma +12 kazandırır ve aynı koğuştan ömürlük bir Asker Arkadaşı (Tertip) edinirsin!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectMilitaryService('erbas')">6 Ay Kışlaya Teslim Ol 🪖</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row"><span class="card-title">⭐ 12 Ay Yedek Subay (Asteğmen)</span><span class="card-badge badge-blue">+₺ 380.000 Maaş</span></div>
            <p class="card-desc">Üniversite mezunlarına özel! Hem subay olarak komuta et hem de toplam 380.000 TL asteğmen maaşı kazan!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectMilitaryService('yedek_subay')">Yedek Subay Olarak Katıl ⭐</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function selectMilitaryService(serviceType) {
    await performActivity("military_service", { service_type: serviceType });
    closeModal("genericModal");
}

function openExamsModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "📝 Ulusal Sınav Merkezi: LGS, YKS & KPSS";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">🎒 LGS (Liselere Geçiş Sınavı)</span>
                <span class="card-badge badge-yellow">Son Puan: ${gameState.lgs_score || "Girmedi"}</span>
            </div>
            <p class="card-desc">LGS'den 450+ puanla <b>Fen Lisesi</b>, 410+ ile <b>Köklü Özel Kolej</b> veya 340+ ile <b>Nitelikli Anadolu Lisesi</b> kazan!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="startExamQuiz('lgs')">🎒 LGS Sınavına Gir</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">🎓 YKS (Yükseköğretim Kurumları Sınavı)</span>
                <span class="card-badge badge-blue">Son Puan: ${gameState.yks_score || "Girmedi"}</span>
            </div>
            <p class="card-desc">2 soruluk YKS sınavında 410+ puan alırsan <b>Yıllık 45.000 TL Başarı & KYK Bursu</b> kazanırsın ve zekan +10 artar!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="startExamQuiz('yks')">📝 YKS Sınavına Gir</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">🏛️ KPSS (Kamu Personel Seçme Sınavı)</span>
                <span class="card-badge badge-green">Son Puan: ${gameState.kpss_score || "Girmedi"}</span>
            </div>
            <p class="card-desc">KPSS'den 80+ puan alarak mülakatsız doğrudan <b>Devlet Başmüfettişi / Kaymakam (980.000 TL/yıl)</b> veya <b>Kadrolu Memur</b> olarak atan!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="startExamQuiz('kpss')">🏛️ KPSS Sınavına Gir</button>
        </div>
    `;
    openDialogModal("genericModal");
}

function startExamQuiz(examType) {
    sound.playClick();
    const questions = (marketData && marketData.exam_questions && marketData.exam_questions[examType]) || [];
    if (questions.length < 2) return;

    document.getElementById("genericModalTitle").textContent = examType === "yks" ? "📝 YKS Sınav Kitapçığı" : (examType === "lgs" ? "🎒 LGS Sınav Kitapçığı" : "🏛️ KPSS Sınav Kitapçığı");
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card">
            <div style="font-size:13px; font-weight:800; color:#fff; margin-bottom:8px;">1) ${questions[0].q}</div>
            <select id="examAns1" class="form-select">
                ${questions[0].options.map((opt, idx) => `<option value="${idx}">${opt}</option>`).join("")}
            </select>
        </div>
        <div class="panel-card">
            <div style="font-size:13px; font-weight:800; color:#fff; margin-bottom:8px;">2) ${questions[1].q}</div>
            <select id="examAns2" class="form-select">
                ${questions[1].options.map((opt, idx) => `<option value="${idx}">${opt}</option>`).join("")}
            </select>
        </div>
        <button type="button" class="btn-primary" style="width:100%; margin-top:6px;" onclick="submitNationalExam('${examType}')">Optik Formu Teslim Et & Sonucu Gör 🎯</button>
    `;
}

async function submitNationalExam(examType) {
    const a1 = document.getElementById("examAns1")?.value || 0;
    const a2 = document.getElementById("examAns2")?.value || 0;
    await performActivity("national_exam", { exam_type: examType, ans1: Number(a1), ans2: Number(a2) });
    closeModal("genericModal");
}

function openStudentHousingModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = `🍜 Yurt & Öğrenci Evi Hayatı (${gameState.housing_type || "Aile Evi"})`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">🛏️ KYK Öğrenci Yurduna Yerleş</span>
                <span class="card-badge badge-green">Ücretsiz + Oda Arkadaşı</span>
            </div>
            <p class="card-desc">Yıllık yaşam giderini 35.000 TL'ye düşürür ve ranzada beraber sınavlara çalışacağın sıkı bir <b>Yurt Oda Arkadaşı</b> kazandırır!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectStudentHousing('kyk_dorm')">KYK Yurduna Kayıt Ol 🛏️</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">🍜 Arkadaşlarla Öğrenci Evine Çık</span>
                <span class="card-badge badge-purple">₺ 15.000 Depozito</span>
            </div>
            <p class="card-desc">Özgür öğrenci evi hayatı! Mutluluk +20, Hitabet +8 ve yeni bir <b>Ev Arkadaşı</b> kazandırır!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="selectStudentHousing('student_house')">Öğrenci Evine Taşın 🍜</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function selectStudentHousing(housingMode) {
    await performActivity("student_housing", { housing_mode: housingMode });
    closeModal("genericModal");
}

// ----------------- PAKET 11, 14, 15, 16: TV İZDİVAÇ ŞOVU, MÜZİK GRUBU, BANKA/OFFSHORE & YAŞAM GRAFİĞİ -----------------

async function handleFastAgeUp(years = 3) {
    if (!gameState || !gameState.is_alive) return;
    sound.playAgeUp();
    for (let i = 0; i < years; i++) {
        try {
            const res = await fetch("/api/age_up", { method: "POST" });
            const data = await res.json();
            if (!data.success) break;
            gameState = data.character;
            renderAll();
            if (data.character_died) {
                sound.playDeath();
                openDeathModal();
                break;
            }
            if (data.has_event) {
                openEventModal(data.event);
                break;
            }
        } catch (e) {
            break;
        }
    }
}

function openDramaIntrigueModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "📺 Kısmet Evi TV Şovu, Ofis Aşkı & Entrika";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f472b6;">
            <div class="card-title-row">
                <span class="card-title">📺 'Kısmet Evi' TV Evlilik Programına Katıl</span>
                <span class="card-badge badge-purple">+Ödül & TV Aşkı</span>
            </div>
            <p class="card-desc">Kameralar önünde 8 gelin ve damat adayıyla aynı evde yarış, halk oylamasıyla <b>180.000 - 450.000 TL</b> ödül kazan ve hayalindeki partnerle çık!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerDramaIntrigue('tv_dating_show')">Kısmet Evi'ne Katıl 📺</button>
        </div>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">💼❤️‍🔥 Plazada & İş Yerinde Gizli Ofis Aşkı</span>
                <span class="card-badge badge-yellow">+%28 Zam & Sevgili</span>
            </div>
            <p class="card-desc">Çalıştığın şirketteki üst düzey bir yöneticiyle tutkulu bir ofis aşkına başla! Başarılı olursa hem sevgili edinirsin hem de maaşına <b>%28 özel zam ve terfi</b> alırsın!</p>
            <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerDramaIntrigue('office_romance')">Ofiste Kıvılcım Başlat 💼</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function triggerDramaIntrigue(subAction) {
    await performActivity("drama_intrigue", { sub_action: subAction });
    closeModal("genericModal");
}

function openBandModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🎸 Müzik Grubu, Rap Kolektifi & Stadyum Turnesi";
    const body = document.getElementById("genericModalBody");

    let activeBandHtml = "";
    if (gameState.band) {
        const b = gameState.band;
        activeBandHtml = `
            <div class="panel-card" style="border-color:var(--accent-purple); margin-bottom:12px;">
                <div class="card-title-row">
                    <span class="card-title">🎸 ${b.name} (${b.genre})</span>
                    <span class="card-badge badge-green">Uyum: %${b.chemistry}</span>
                </div>
                <p class="card-desc">
                    Albüm Sayısı: <b>${b.albums_count}</b> • Hayran Kitlesi: <b>${b.fans.toLocaleString("tr-TR")}</b> • Yıllık Telif: <b>+₺ ${b.annual_royalties.toLocaleString("tr-TR")}/yıl</b>
                </p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:8px;">
                    <button type="button" class="btn-choice" onclick="triggerBandAction('rehearse')">🎶 Stüdyo Provası Yap</button>
                    <button type="button" class="btn-choice" onclick="triggerBandAction('record_album')">💿 Hit Albüm Çıkar</button>
                    <button type="button" class="btn-choice" onclick="triggerBandAction('stadium_tour')">🏟️ Stadyum Turnesi</button>
                    <button type="button" class="btn-choice" onclick="triggerBandAction('resolve_drama')">🤝 Grup Egosunu Çöz</button>
                </div>
            </div>
        `;
    }

    const genres = (marketData && marketData.band_genres) || [];
    body.innerHTML = `
        ${activeBandHtml}
        <div class="panel-card">
            <div class="form-group">
                <label for="inputBandName">Yeni Müzik Grubu / Kolektif Adı</label>
                <input type="text" id="inputBandName" class="form-input" placeholder="Örn: Dumanlı Geceler, Kadıköy Tayfa...">
            </div>
            <div class="form-group">
                <label for="selectBandGenre">Müzik Türü Seç</label>
                <select id="selectBandGenre" class="form-select">
                    ${genres.map(g => `<option value="${g.id}">${g.name} (Kurulum: ₺ ${g.cost.toLocaleString("tr-TR")})</option>`).join("")}
                </select>
            </div>
            <button type="button" class="btn-primary" onclick="submitCreateBand()">🎤 Grubu Kur & Sahneye Çık</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function submitCreateBand() {
    const name = document.getElementById("inputBandName")?.value || "";
    const genreId = document.getElementById("selectBandGenre")?.value || "anadolu_rock";
    await performActivity("create_band", { band_name: name, genre_id: genreId });
    openBandModal();
}

async function triggerBandAction(subAction) {
    await performActivity("band_action", { sub_action: subAction });
    openBandModal();
}

function openBankOffshoreModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🏦 Banka Kredisi & 🇨🇭 İsviçre Offshore Hesabı";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:var(--accent-blue);">
            <div class="card-title-row">
                <span class="card-title">🏦 Merkez & Konut Kredisi</span>
                <span class="card-badge badge-red">Mevcut Borç: ₺ ${(gameState.debt || 0).toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc">Emlak, araç veya şirket kurmak için anında nakit kredi çekebilir ya da mevcut kredi borcunu kapatabilirsin:</p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:8px;">
                <button type="button" class="btn-choice" onclick="triggerBankAction('take_loan', 250000)">💳 +250.000 TL Kredi Çek</button>
                <button type="button" class="btn-choice" onclick="triggerBankAction('take_loan', 1000000)">💳 +1.000.000 TL Kredi Çek</button>
                <button type="button" class="btn-choice" onclick="triggerBankAction('take_loan', 5000000)">💳 +5.000.000 TL Kredi Çek</button>
                <button type="button" class="btn-choice" style="border-color:var(--accent-green); color:#a7f3d0;" onclick="triggerBankAction('pay_debt', 0)">✅ Borcu Kapat</button>
            </div>
        </div>

        <div class="panel-card" style="border-color:var(--accent-yellow);">
            <div class="card-title-row">
                <span class="card-title">🇨🇭🔒 İsviçre Gizli Offshore Hesabı</span>
                <span class="card-badge badge-yellow">Bakiye: ₺ ${(gameState.offshore_balance || 0).toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc">
                Offshore hesabındaki servetin <b>boşanma mal paylaşımından (nafaka) ve hacizden %100 muaftır</b>, ayrıca her yıl <b>%8 döviz getirisi</b> kazandırır!
            </p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:8px;">
                <button type="button" class="btn-choice" onclick="triggerBankAction('deposit_offshore', 100000)">🇨🇭 100.000 TL Aktar</button>
                <button type="button" class="btn-choice" onclick="triggerBankAction('deposit_offshore', 1000000)">🇨🇭 1.000.000 TL Aktar</button>
                <button type="button" class="btn-choice" style="grid-column:span 2; border-color:var(--accent-green);" onclick="triggerBankAction('withdraw_offshore', 0)">💸 Tüm Offshore Bakiyesini Türkiye'ye Çek</button>
            </div>
        </div>
    `;
    openDialogModal("genericModal");
}

async function triggerBankAction(subAction, amount) {
    await performActivity("bank_action", { sub_action: subAction, amount });
    openBankOffshoreModal();
}

function createWideChartSvg(dataArr, strokeColor = "#10b981") {
    const arr = dataArr && dataArr.length >= 2 ? dataArr : [0, dataArr?.[0] || 0];
    const w = 360, h = 95;
    const min = Math.min(...arr);
    const max = Math.max(...arr);
    const range = max - min || 1;
    const pts = arr.map((val, idx) => {
        const x = (idx / (arr.length - 1)) * (w - 16) + 8;
        const y = h - 10 - ((val - min) / range) * (h - 20);
        return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(" ");
    return `
        <svg width="100%" height="${h}" viewBox="0 0 ${w} ${h}" style="background:rgba(15,23,42,0.75); border-radius:10px; border:1px solid rgba(255,255,255,0.08);">
            <polyline fill="none" stroke="${strokeColor}" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round" points="${pts}"/>
        </svg>
    `;
}

function openStatsChartModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = `📊 Yaşam & Servet Grafiği (${gameState.first_name} ${gameState.last_name})`;
    const body = document.getElementById("genericModalBody");

    const wHist = gameState.wealth_history || [gameState.net_worth];
    const hHist = gameState.happiness_history || [gameState.happiness];
    const peakWealth = Math.max(...wHist, gameState.net_worth);

    body.innerHTML = `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">📈 Net Servet Zaman Grafiği</span>
                <span class="card-badge badge-green">Zirve: ₺ ${peakWealth.toLocaleString("tr-TR")}</span>
            </div>
            <div style="margin:8px 0;">
                ${createWideChartSvg(wHist, "#10b981")}
            </div>
            <p class="card-desc">Güncel Net Servet: <b>₺ ${gameState.net_worth.toLocaleString("tr-TR")}</b> • Offshore: <b>₺ ${(gameState.offshore_balance || 0).toLocaleString("tr-TR")}</b></p>
        </div>

        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">😊 Yaşam Mutluluk Grafiği</span>
                <span class="card-badge badge-yellow">Güncel: %${gameState.happiness}</span>
            </div>
            <div style="margin:8px 0;">
                ${createWideChartSvg(hHist, "#f59e0b")}
            </div>
            <p class="card-desc">Yaş: <b>${gameState.age}</b> • Son Ödenen Vergi: <b>₺ ${(gameState.last_tax_paid || 0).toLocaleString("tr-TR")}</b> • Yıllık Nafaka: <b>₺ ${(gameState.alimony_annual || 0).toLocaleString("tr-TR")}</b></p>
        </div>
    `;
    openDialogModal("genericModal");
}

// ----------------- PAKET 17, 18, 19: ÇİFT ORTAKLIĞI, BOŞANMA MAHKEMESİ & PROFESYONEL SPOR KARİYERİ -----------------

function openCoupleBusinessModal(personId) {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `🤝🏪 ${person.name} ile Ortak Girişim Kur`;
    const body = document.getElementById("genericModalBody");
    const list = (marketData && marketData.couple_businesses) || [];

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:10px;">
            Sevgilin/eşin <b>${person.name}</b> sermayenin <b>%30'unu</b> karşılamaya hazır! Ortak iş yeriniz hem aşkınızı güçlendirir hem de her yıl ortak kâr getirir:
        </p>
        ${list.map(b => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${b.name}</span>
                    <span class="card-badge badge-yellow">Toplam: ₺ ${b.cost.toLocaleString("tr-TR")}</span>
                </div>
                <p class="card-desc">Yıllık Ortak Gelir: <b>+₺ ${b.annual_profit.toLocaleString("tr-TR")}/yıl</b></p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitCoupleBusiness('${person.id}', '${b.id}')">Ortaklığı Başlat 🤝</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitCoupleBusiness(personId, bizId) {
    await performActivity("couple_business", { person_id: personId, biz_id: bizId });
    closeModal("genericModal");
}

function openDivorceCourtModal(personId) {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = `⚖️ Aile & Boşanma Mahkemesi (${person.name})`;
    const body = document.getElementById("genericModalBody");
    const lawyers = (marketData && marketData.divorce_lawyers) || [];
    const hasEvidence = person.has_prenup || person.loyalty < 55;

    body.innerHTML = `
        <div class="panel-card" style="border-color:${hasEvidence ? 'var(--accent-green)' : 'var(--accent-red)'}; margin-bottom:10px;">
            <div class="card-title-row">
                <span class="card-title">📂 Dava Dosyası & Delil Durumu</span>
                <span class="card-badge ${hasEvidence ? 'badge-green' : 'badge-red'}">${hasEvidence ? 'Güçlü Kanıt / Sözleşme Var' : 'Kanıt Yok (Riskli!)'}</span>
            </div>
            <p class="card-desc">
                ${hasEvidence
                    ? "Elinde Evlilik Sözleşmesi veya Dedektif/Stalk sadakatsizlik kanıtı var! Mahkemede çok avantajlısın."
                    : "Elinde sözleşme veya sadakatsizlik kanıtı yok! İyi bir avukat tutmazsan servetinin %42'sini ve yıllık nafaka kaybedebilirsin!"}
            </p>
        </div>
        ${lawyers.map(lw => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${lw.name}</span>
                    <span class="card-badge badge-yellow">Vekalet: ₺ ${lw.cost.toLocaleString("tr-TR")}</span>
                </div>
                <p class="card-desc">${lw.desc}</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitDivorceCourt('${person.id}', '${lw.id}')">Bu Avukatla Duruşmaya Çık ⚖️</button>
            </div>
        `).join("")}
    `;
    openDialogModal("genericModal");
}

async function submitDivorceCourt(personId, lawyerId) {
    await performActivity("divorce_court", { person_id: personId, lawyer_id: lawyerId });
    closeModal("genericModal");
}

function openProSportsModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "⚽ Profesyonel Spor Kariyeri & Kulüp Başkanlığı";
    const body = document.getElementById("genericModalBody");
    const clubs = (marketData && marketData.sports_clubs) || [];
    const sc = gameState.sports_career;

    let activeCareerHtml = "";
    if (sc) {
        activeCareerHtml = `
            <div class="panel-card" style="border-color:var(--accent-green); margin-bottom:12px;">
                <div class="card-title-row">
                    <span class="card-title">🏟️ ${sc.team_name} (${sc.league_tier})</span>
                    <span class="card-badge badge-green">+₺ ${sc.salary.toLocaleString("tr-TR")}/yıl</span>
                </div>
                <p class="card-desc">
                    Gol/Sayı Katkısı: <b>${sc.goals_or_points}</b> • Kupalar: <b>🏆 ${sc.trophies}</b> • Milli Maç: <b>🇹🇷 ${sc.national_caps}</b>
                </p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:8px;">
                    <button type="button" class="btn-primary" onclick="triggerProSports('play_season_match')">⚽ Şampiyonluk Maçına Çık</button>
                    <button type="button" class="btn-choice" onclick="performActivity('gym_workout')">🏋️ Kondisyon Antrenmanı</button>
                </div>
            </div>
        `;
    }

    body.innerHTML = `
        ${activeCareerHtml}
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">🏃 Kulüp Altyapı Seçmeleri</span>
                <span class="card-badge badge-blue">Başlangıç</span>
            </div>
            <p class="card-desc">Gençlik akademisi seçmelerine katılarak atletizmini geliştir ve profesyonel lisansa adım at! (Mevcut Atletizm: <b>%${(gameState.skills && gameState.skills.athletics) || 15}</b>)</p>
            <button type="button" class="btn-choice" style="margin-top:8px;" onclick="triggerProSports('join_academy')">Altyapı Seçmelerine Gir 🏃</button>
        </div>

        <div class="person-action-group-title" style="margin:8px 0;">✍️ Süper Lig & Avrupa Transfer Teklifleri</div>
        ${clubs.map(c => `
            <div class="panel-card">
                <div class="card-title-row">
                    <span class="card-title">${c.name}</span>
                    <span class="card-badge badge-green">₺ ${c.salary.toLocaleString("tr-TR")}/yıl</span>
                </div>
                <p class="card-desc">Lig: <b>${c.tier}</b> • Gereken Atletizm: <b>%${c.req_ath}</b> (+%25 İmza Parası)</p>
                <button type="button" class="btn-primary" style="margin-top:8px;" onclick="triggerProSports('sign_club', '${c.id}')">Transfer Sözleşmesi İmzala ✍️</button>
            </div>
        `).join("")}

        <div class="panel-card" style="border-color:var(--accent-yellow);">
            <div class="card-title-row">
                <span class="card-title">👑 Süper Lig Kulübü Satın Al (Başkan Ol)</span>
                <span class="card-badge badge-yellow">₺ 20.000.000</span>
            </div>
            <p class="card-desc">Şehrinin takımını satın alarak Kulüp Başkanı ol! Protokol tribününde otur ve yıllık <b>+3.200.000 TL</b> yayın/gişe geliri kazan!</p>
            <button type="button" class="btn-choice" style="margin-top:8px;" onclick="triggerProSports('buy_sports_club')">Kulübü Satın Al & Başkan Ol 👑</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function triggerProSports(subAction, clubId = "anadolu_fk") {
    await performActivity("pro_sports", { sub_action: subAction, club_id: clubId });
    openProSportsModal();
}

// ----------------- MEVCUT ALANLARI GELİŞTİRME & DERİNLEŞTİRME MODALLARI -----------------

function openAnnualBudgetModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = `📑 Yıllık Finansal Bütçe Karnesi (${gameState.age} Yaş)`;
    const body = document.getElementById("genericModalBody");

    const summary = gameState.last_annual_summary || {};
    const incomes = summary.incomes || [];
    const expenses = summary.expenses || [];
    const totalInc = summary.total_income || gameState.annual_income_last || 0;
    const totalExp = summary.total_expense || gameState.annual_expense_last || 0;
    const net = summary.net !== undefined ? summary.net : (totalInc - totalExp);

    let incomeRows = incomes.length > 0
        ? incomes.map(i => `<div style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:12.5px;"><span>${i.label}</span><b style="color:var(--accent-green);">+₺ ${i.amount.toLocaleString("tr-TR")}</b></div>`).join("")
        : `<div style="font-size:12px; color:var(--text-secondary);">Aktif gelir kalemi bulunmuyor.</div>`;

    let expenseRows = expenses.length > 0
        ? expenses.map(e => `<div style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.06); font-size:12.5px;"><span>${e.label}</span><b style="color:var(--accent-red);">-₺ ${e.amount.toLocaleString("tr-TR")}</b></div>`).join("")
        : `<div style="font-size:12px; color:var(--text-secondary);">Aktif gider kalemi bulunmuyor.</div>`;

    body.innerHTML = `
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:12px;">
            <div class="panel-card" style="border-color:var(--accent-green); text-align:center; padding:10px;">
                <div style="font-size:11px; color:#a7f3d0; font-weight:700;">TOPLAM GELİR</div>
                <div style="font-size:16px; font-weight:800; color:var(--accent-green);">+₺ ${totalInc.toLocaleString("tr-TR")}</div>
            </div>
            <div class="panel-card" style="border-color:var(--accent-red); text-align:center; padding:10px;">
                <div style="font-size:11px; color:#fca5a5; font-weight:700;">TOPLAM GİDER</div>
                <div style="font-size:16px; font-weight:800; color:var(--accent-red);">-₺ ${totalExp.toLocaleString("tr-TR")}</div>
            </div>
        </div>

        <div class="panel-card" style="margin-bottom:10px;">
            <div class="card-title-row">
                <span class="card-title">💰 Yıllık Gelir Kalemleri</span>
                <span class="card-badge badge-green">Nakit Girişi</span>
            </div>
            <div style="margin-top:6px;">${incomeRows}</div>
        </div>

        <div class="panel-card" style="margin-bottom:10px;">
            <div class="card-title-row">
                <span class="card-title">🛒 Yıllık Gider & Vergi Kalemleri</span>
                <span class="card-badge badge-red">Nakit Çıkışı</span>
            </div>
            <div style="margin-top:6px;">${expenseRows}</div>
        </div>

        <div class="panel-card" style="border-color:${net >= 0 ? 'var(--accent-green)' : 'var(--accent-red)'}; text-align:center;">
            <div style="font-size:12px; color:var(--text-secondary);">Yıllık Net Bütçe Dengesi</div>
            <div style="font-size:20px; font-weight:900; color:${net >= 0 ? 'var(--accent-green)' : 'var(--accent-red)'}; margin:4px 0;">
                ${net >= 0 ? '+₺ ' + net.toLocaleString("tr-TR") : '-₺ ' + Math.abs(net).toLocaleString("tr-TR")}
            </div>
            <div style="font-size:11.5px; color:#cbd5e1;">Güncel Nakit: <b>₺ ${gameState.money.toLocaleString("tr-TR")}</b> • Net Servet: <b>₺ ${gameState.net_worth.toLocaleString("tr-TR")}</b></div>
        </div>
    `;
    openDialogModal("genericModal");
}

function openRelConflictModal(personId) {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === personId);
    if (!person) return;
    const conflicts = (marketData && marketData.relationship_conflicts) || [];
    if (conflicts.length === 0) return;
    const conflict = conflicts[Math.floor(Math.random() * conflicts.length)];

    document.getElementById("genericModalTitle").textContent = `${conflict.title}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:var(--accent-red); margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">🔥 ${person.name} ile Kriz Yaşanıyor!</span>
                <span class="card-badge badge-red">Gerginlik</span>
            </div>
            <p class="card-desc" style="font-size:13.5px; line-height:1.5; color:#f1f5f9; margin-top:6px;">
                ${conflict.desc}
            </p>
        </div>
        <div class="person-action-group-title" style="margin-bottom:8px;">Nasıl tepki vereceksin?</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${conflict.options.map(opt => `
                <button type="button" class="btn-choice" style="text-align:left; padding:10px 12px;" onclick="submitRelConflict('${person.id}', '${conflict.id}', '${opt.id}')">
                    <div style="font-weight:700; color:#fff;">${opt.text}</div>
                    <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">Taktik: <b>${opt.style}</b></div>
                </button>
            `).join("")}
        </div>
    `;
    openDialogModal("genericModal");
}

async function submitRelConflict(personId, conflictId, choiceId) {
    await performActivity("rel_conflict", { person_id: personId, conflict_id: conflictId, choice_id: choiceId });
    closeModal("genericModal");
}

function openCompanyDecisionsModal() {
    sound.playClick();
    if (!gameState.business) return;
    const b = gameState.business;
    const actions = (marketData && marketData.company_expansion_actions) || [];

    document.getElementById("genericModalTitle").textContent = `🏬 Patron Karar Odası: ${b.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:var(--accent-blue); margin-bottom:12px; background:linear-gradient(135deg, rgba(59,130,246,0.08), rgba(16,185,129,0.08));">
            <div class="card-title-row">
                <span class="card-title">🏢 ${b.name} (${b.sector})</span>
                <span class="card-badge badge-yellow">Değer: ₺ ${b.valuation.toLocaleString("tr-TR")}</span>
            </div>
            <p class="card-desc" style="margin-top:4px;">
                Aşama: <b>${b.stage || "Girişim"}</b> • Şube/Tesis: <b>${b.branches || 1}</b> • Pay: <b>%${b.shares_owned ?? 100}</b> • BIST Halka Açık: <b>${b.is_ipo ? "Evet 📈" : "Hayır"}</b> • CEO: <b>${b.has_manager ? "Profesyonel Yönetici 👔" : "Bizzat Siz"}</b><br>
                Yıllık Kâr: <b>₺ ${b.annual_profit.toLocaleString("tr-TR")}</b> • Çalışan: <b>${b.employees} Kişi</b> • İtibar: <b>%${b.reputation}</b>
            </p>
            <div style="display:flex; gap:8px; margin-top:10px;">
                <button type="button" class="btn-choice" style="border-color:#ef4444; color:#ef4444; width:100%;" onclick="openCompanyCrisisModal()">🚨 Şirket Kriz Masası</button>
            </div>
        </div>
        <div class="person-action-group-title" style="margin-bottom:8px;">Stratejik Yönetim & Büyüme Hamleleri:</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${actions.map(act => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${act.name}</span>
                        <span class="card-badge badge-green">Maliyet: ₺ ${act.cost.toLocaleString("tr-TR")}</span>
                    </div>
                    <p class="card-desc">${act.desc}</p>
                    <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitCompanyDecision('${act.id}')">Bu Kararı Uygula 🚀</button>
                </div>
            `).join("")}
        </div>
    `;
    openDialogModal("genericModal");
}

async function submitCompanyDecision(actionId) {
    await performActivity("company_manage", { action_id: actionId });
    openCompanyDecisionsModal();
}

function openCompanyCrisisModal() {
    sound.playClick();
    if (!gameState.business) return;
    const crises = (marketData && marketData.company_crises) || [];
    document.getElementById("genericModalTitle").textContent = `🚨 Şirket Kriz Masası & Risk Yönetimi`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Şirketinin karşılaşabileceği piyasa, denetim veya PR krizlerine karşı liderliğini göster ve kararlar al:</p>
        <div style="display:flex; flex-direction:column; gap:12px;">
            ${crises.map(c => `
                <div class="panel-card" style="border-color:#ef4444;">
                    <div class="card-title-row">
                        <span class="card-title">${c.title}</span>
                    </div>
                    <p class="card-desc" style="margin-bottom:10px;">${c.desc}</p>
                    <div style="display:flex; flex-direction:column; gap:6px;">
                        ${c.choices.map(choice => `
                            <button type="button" class="btn-choice" style="text-align:left; padding:8px 12px;" onclick="submitCompanyCrisis('${c.id}', '${choice.id}')">
                                <b>${choice.text}</b>
                            </button>
                        `).join("")}
                    </div>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openCompanyDecisionsModal()">← Patron Karar Odasına Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitCompanyCrisis(crisisId, choiceId) {
    await performActivity("company_crisis_choice", { crisis_id: crisisId, choice_id: choiceId });
    closeModal("genericModal");
}

function openTenantManageModal(assetId) {
    sound.playClick();
    const asset = (gameState.assets || []).find(a => a.id === assetId);
    if (!asset) return;
    const actions = (marketData && marketData.tenant_management_actions) || [];

    document.getElementById("genericModalTitle").textContent = `🔑 Kiracı Kriz Masası: ${asset.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:${asset.tenant_issue ? 'var(--accent-red)' : 'var(--accent-green)'}; margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">👤 Kiracı: ${asset.tenant_name || "Atanmadı"}</span>
                <span class="card-badge ${asset.tenant_issue ? 'badge-red' : 'badge-green'}">Güven: %${asset.tenant_reliability || 85}</span>
            </div>
            <p class="card-desc">
                ${asset.tenant_issue
                    ? `<b style="color:#fca5a5;">⚠️ Aktif Sorun:</b> ${asset.tenant_issue}`
                    : `Kiracın kiralarını düzenli ödüyor ve apartmanda huzur hakim.`}
            </p>
        </div>
        <div class="person-action-group-title" style="margin-bottom:8px;">Müdahale Seçenekleri:</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${actions.map(act => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${act.name}</span>
                        <span class="card-badge badge-yellow">${act.cost > 0 ? '₺ ' + act.cost.toLocaleString("tr-TR") : 'Ücretsiz'}</span>
                    </div>
                    <p class="card-desc">${act.desc}</p>
                    <button type="button" class="btn-primary" style="margin-top:8px;" onclick="submitTenantAction('${asset.id}', '${act.id}')">Uygula ⚖️</button>
                </div>
            `).join("")}
        </div>
    `;
    openDialogModal("genericModal");
}

async function submitTenantAction(assetId, actionId) {
    await performActivity("tenant_manage", { asset_id: assetId, action_id: actionId });
    openTenantManageModal(assetId);
}

function openWellnessModal(serviceId) {
    sound.playClick();
    const services = (marketData && marketData.wellness_services) || [];
    const serv = services.find(s => s.id === serviceId) || services[0];
    if (!serv) return;

    document.getElementById("genericModalTitle").textContent = serv.name;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">${serv.name}</span>
                <span class="card-badge badge-green">${serv.cost > 0 ? '₺ ' + serv.cost.toLocaleString("tr-TR") : 'Ücretsiz'}</span>
            </div>
            <p class="card-desc" style="font-size:13px; line-height:1.5; margin:8px 0;">${serv.desc}</p>
            <button type="button" class="btn-primary" style="width:100%; margin-top:8px;" onclick="submitWellnessAction('${serv.id}')">Hizmetten Yararlan ✨</button>
        </div>
    `;
    openDialogModal("genericModal");
}

async function submitWellnessAction(serviceId) {
    await performActivity("wellness_action", { action_id: serviceId });
    closeModal("genericModal");
}

// ----------------- DETAYLI İLİŞKİ SİSTEMLERİ: ÖP, DATE, KAVGA -----------------

function openDetailedKissModal(personId) {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === personId);
    if (!person) return;
    const styles = (marketData && marketData.kiss_styles) || [];

    document.getElementById("genericModalTitle").textContent = `💋 Romantik Yakınlaşma: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f472b6; margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">💑 ${person.name} (${person.relation})</span>
                <span class="card-badge badge-purple">İlişki: %${person.relationship_level}</span>
            </div>
            <p class="card-desc" style="margin-top:4px;">
                Sevgi Dili: <b>${person.love_language || "Fiziksel Temas"}</b> • Kişilik: <b>${getPersonalityLabel(person.personality)}</b>
            </p>
        </div>
        <div class="person-action-group-title" style="margin-bottom:8px;">Nasıl bir yakınlaşma seçeceksin?</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${styles.map(k => {
                const isFav = (k.preferred_personalities || []).includes(person.personality);
                return `
                    <button type="button" class="btn-choice" style="text-align:left; padding:10px 12px; ${isFav ? 'border-color:#f472b6; background:rgba(244,114,182,0.1);' : ''}" onclick="submitDetailedKiss('${person.id}', '${k.id}')">
                        <div style="font-weight:700; color:#fff; font-size:14px;">${k.name}</div>
                        <div style="font-size:11.5px; color:var(--text-secondary); margin-top:2px;">${k.desc}</div>
                        <div style="font-size:11px; color:#6ee7b7; margin-top:4px;">İlişki +${k.rel_boost} • Sadakat +${k.loyalty_boost} • Stres -${k.stress_relief}${isFav ? ' • <b style="color:#f472b6;">Tam Kişiliğine Uygun! 🔥</b>' : ''}</div>
                    </button>
                `;
            }).join("")}
        </div>
    `;
    openDialogModal("genericModal");
}

async function submitDetailedKiss(personId, kissId) {
    await performActivity("detailed_kiss", { person_id: personId, kiss_id: kissId });
    closeModal("genericModal");
}

let dateSimState = {
    personId: null,
    step: 1,
    venueId: "tea_simit",
    outfitId: "smart_casual",
    greetingId: "passionate_hug",
    dialogueId: "topic_destiny",
    dialogueChoiceId: null,
    tactileId: null,
    midEventId: "live_music_slow",
    midChoiceId: null,
    finaleId: null,
    chemistry: 50,
    cost: 0
};

function openDateSimPickerModal() {
    sound.playClick();
    const dateable = (gameState.relationships || []).filter(p => p.is_alive && ["Flört", "Sevgili", "Nişanlı", "Eş", "Sınıf Arkadaşı", "İş Arkadaşı", "Arkadaş"].includes(p.relation));
    document.getElementById("genericModalTitle").textContent = "🌹 Aşk & Randevu Simülatörü (Date Sim)";
    const body = document.getElementById("genericModalBody");

    if (dateable.length === 0) {
        body.innerHTML = `
            <div class="panel-card" style="text-align:center; padding:20px;">
                <div style="font-size:36px; margin-bottom:10px;">💔</div>
                <div class="card-title" style="margin-bottom:6px;">Buluşacak Kimse Yok</div>
                <p class="card-desc" style="margin-bottom:16px;">
                    Şu anda randevuya çıkabileceğin bir flörtün, sevgilin veya arkadaşın bulunmuyor.
                    Hemen KısmetApp'e girerek yeni biriyle tanışabilirsin!
                </p>
                <button type="button" class="btn-primary" onclick="closeModal('genericModal'); openKismetAppModal();">📱 KısmetApp'e Git</button>
            </div>
        `;
    } else {
        body.innerHTML = `
            <p class="card-desc" style="margin-bottom:12px;">
                Kiminle unutulmaz bir randevuya çıkmak istiyorsun? Kıyafetini seç, diyalogları yönet ve aranızdaki kimyayı zirveye taşı!
            </p>
            <div style="display:flex; flex-direction:column; gap:8px;">
                ${dateable.map(p => `
                    <button type="button" class="btn-choice" style="display:flex; align-items:center; justify-content:space-between; padding:12px;" onclick="closeModal('genericModal'); openDetailedDateModal('${p.id}');">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="font-size:24px;">${getRelationEmoji(p.relation)}</span>
                            <div style="text-align:left;">
                                <div style="font-weight:700; color:var(--text-primary);">${p.name}</div>
                                <div style="font-size:12px; color:var(--text-secondary);">${p.relation} • ${p.age} Yaş • ${getPersonalityLabel(p.personality)}</div>
                            </div>
                        </div>
                        <span class="card-badge badge-green">Sevgi: %${p.relationship_level}</span>
                    </button>
                `).join("")}
            </div>
        `;
    }
    openDialogModal("genericModal");
}

function openDetailedDateModal(personId) {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === personId);
    if (!person) return;

    const baseChem = Math.min(100, Math.max(30, Math.round((person.relationship_level || 50) * 0.4 + (gameState.looks || 50) * 0.3 + (gameState.skills?.charisma || 20) * 0.3)));
    const outfits = (marketData && marketData.date_outfits) || [];
    const greetings = (marketData && marketData.date_greetings) || [];
    const venues = (marketData && marketData.date_venues) || [];
    const convos = (marketData && marketData.date_conversations) || [];
    const midEvents = (marketData && marketData.date_mid_events) || [];

    dateSimState = {
        personId: personId,
        step: 1,
        venueId: venues[0]?.id || "tea_simit",
        outfitId: outfits[2]?.id || "smart_casual",
        greetingId: greetings[1]?.id || "passionate_hug",
        dialogueId: convos[Math.floor(Math.random() * (convos.length || 1))]?.id || "topic_destiny",
        dialogueChoiceId: null,
        midEventId: midEvents[Math.floor(Math.random() * (midEvents.length || 1))]?.id || "live_music_slow",
        midChoiceId: null,
        finaleId: null,
        chemistry: baseChem,
        cost: 0
    };

    renderDateSimStep1();
    openDialogModal("genericModal");
}

function renderDateSimStep1() {
    const person = (gameState.relationships || []).find(p => p.id === dateSimState.personId);
    if (!person) return;

    const outfits = (marketData && marketData.date_outfits) || [];
    const greetings = (marketData && marketData.date_greetings) || [];
    const venues = (marketData && marketData.date_venues) || [];

    document.getElementById("genericModalTitle").textContent = `🌹 Date Simülatörü: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f472b6; margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">✨ ${getRelationEmoji(person.relation)} ${person.name} ile Özel Randevu</span>
                <span class="card-badge badge-green">Nakit: ₺ ${gameState.money.toLocaleString('tr-TR')}</span>
            </div>
            <div style="font-size:12px; color:var(--text-secondary); margin-top:4px;">
                Kişilik: <b>${getPersonalityLabel(person.personality)}</b> • Görünüş: <b>%${person.looks ?? 70}</b> • Başlangıç Kimyası: <b>%${dateSimState.chemistry}</b>
            </div>
            <div class="stat-progress-bg" style="height:6px; margin-top:8px;">
                <div class="stat-progress-bar" style="width:${dateSimState.chemistry}%; background:linear-gradient(90deg, #ec4899, #f43f5e);"></div>
            </div>
        </div>

        <div class="person-action-group-title">1. Adım: Randevu Kıyafetin (Ne Giyiyorsun?)</div>
        <div class="form-group" style="margin-bottom:12px;">
            <select id="dateSimOutfit" class="form-select" style="font-size:13px; padding:10px;" onchange="updateDateSimTotalCost()">
                ${outfits.map(o => `
                    <option value="${o.id}" ${o.id === dateSimState.outfitId ? 'selected' : ''}>
                        ${o.name} (${o.cost === 0 ? 'Ücretsiz' : '₺ ' + o.cost.toLocaleString('tr-TR')})
                    </option>
                `).join("")}
            </select>
        </div>

        <div class="person-action-group-title">2. Adım: İlk Karşılama Jesti (Buluşma Anı)</div>
        <div class="form-group" style="margin-bottom:12px;">
            <select id="dateSimGreeting" class="form-select" style="font-size:13px; padding:10px;" onchange="updateDateSimTotalCost()">
                ${greetings.map(g => `
                    <option value="${g.id}" ${g.id === dateSimState.greetingId ? 'selected' : ''}>
                        ${g.name} (${g.cost === 0 ? 'Ücretsiz' : '₺ ' + g.cost.toLocaleString('tr-TR')})
                    </option>
                `).join("")}
            </select>
        </div>

        <div class="person-action-group-title">3. Adım: Randevu Mekanı Seç</div>
        <div class="form-group" style="margin-bottom:14px;">
            <select id="dateSimVenue" class="form-select" style="font-size:13px; padding:10px;" onchange="updateDateSimTotalCost()">
                ${venues.map(v => {
                    const isFav = (v.best_for || []).includes(person.personality);
                    return `
                        <option value="${v.id}" ${v.id === dateSimState.venueId ? 'selected' : ''}>
                            ${v.name} (${v.cost === 0 ? 'Ücretsiz' : '₺ ' + v.cost.toLocaleString('tr-TR')}) ${isFav ? '★ Uyumlu' : ''}
                        </option>
                    `;
                }).join("")}
            </select>
        </div>

        <div id="dateSimCostPreview" class="panel-card" style="margin-bottom:12px; background:rgba(255,255,255,0.03); text-align:center;">
            <!-- Dinamik Bütçe Hesabı -->
        </div>

        <button type="button" class="btn-primary" style="font-size:15px; padding:12px; width:100%;" onclick="startDateSimMeeting()">
            🚀 Randevuya Başla (Mekana Git)
        </button>
    `;
    updateDateSimTotalCost();
}

function updateDateSimTotalCost() {
    const outfitSelect = document.getElementById("dateSimOutfit");
    const greetingSelect = document.getElementById("dateSimGreeting");
    const venueSelect = document.getElementById("dateSimVenue");
    if (!outfitSelect || !greetingSelect || !venueSelect) return;

    dateSimState.outfitId = outfitSelect.value;
    dateSimState.greetingId = greetingSelect.value;
    dateSimState.venueId = venueSelect.value;

    const outfit = (marketData?.date_outfits || []).find(o => o.id === dateSimState.outfitId);
    const greeting = (marketData?.date_greetings || []).find(g => g.id === dateSimState.greetingId);
    const venue = (marketData?.date_venues || []).find(v => v.id === dateSimState.venueId);

    const total = (outfit?.cost || 0) + (greeting?.cost || 0) + (venue?.cost || 0);
    dateSimState.cost = total;

    const preview = document.getElementById("dateSimCostPreview");
    if (preview) {
        const affordable = gameState.money >= total;
        preview.innerHTML = `
            <div style="font-size:13px; font-weight:700; color:${affordable ? 'var(--accent-green)' : 'var(--accent-red)'};">
                Toplam Randevu Masrafı: ₺ ${total.toLocaleString('tr-TR')}
            </div>
            ${!affordable ? `<div style="font-size:11px; color:#f87171; margin-top:2px;">⚠️ Yetersiz bakiye! Daha uygun bir mekan veya kıyafet seç.</div>` : `<div style="font-size:11px; color:#94a3b8; margin-top:2px;">Kalan Nakit: ₺ ${(gameState.money - total).toLocaleString('tr-TR')}</div>`}
        `;
    }
}

function startDateSimMeeting() {
    sound.playClick();
    if (gameState.money < dateSimState.cost) {
        showToast("Bu randevu için yeterli paran yok!", "error");
        return;
    }

    const outfit = (marketData?.date_outfits || []).find(o => o.id === dateSimState.outfitId);
    const venue = (marketData?.date_venues || []).find(v => v.id === dateSimState.venueId);
    const greeting = (marketData?.date_greetings || []).find(g => g.id === dateSimState.greetingId);

    // Kıyafet & Mekan etkisi
    if (outfit?.id === "sloppy_tracksuit") {
        dateSimState.chemistry = Math.max(10, dateSimState.chemistry - 25);
    } else if (venue?.id && (outfit?.suitable_venues || []).includes(venue.id)) {
        dateSimState.chemistry = Math.min(100, dateSimState.chemistry + 14);
    } else {
        dateSimState.chemistry = Math.min(100, dateSimState.chemistry + 5);
    }

    // Karşılama etkisi
    if (greeting?.id === "flower_chocolate") {
        dateSimState.chemistry = Math.min(100, dateSimState.chemistry + 10);
    } else {
        dateSimState.chemistry = Math.min(100, dateSimState.chemistry + 6);
    }

    renderDateSimDialogue();
}

function renderDateSimDialogue() {
    const person = (gameState.relationships || []).find(p => p.id === dateSimState.personId);
    const convos = (marketData && marketData.date_conversations) || [];
    const topic = convos.find(c => c.id === dateSimState.dialogueId) || convos[0];
    const venue = (marketData?.date_venues || []).find(v => v.id === dateSimState.venueId);

    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f472b6; margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">🍷 ${venue?.name || 'Masa Sohbeti'}</span>
                <span class="card-badge badge-green">❤️ Kimya: %${dateSimState.chemistry}</span>
            </div>
            <div class="stat-progress-bg" style="height:7px; margin-top:8px;">
                <div class="stat-progress-bar" style="width:${dateSimState.chemistry}%; background:linear-gradient(90deg, #ec4899, #f43f5e); transition:width 0.4s ease;"></div>
            </div>
        </div>

        <div style="background:rgba(236,72,153,0.08); border-left:3px solid #ec4899; border-radius:8px; padding:12px; margin-bottom:14px;">
            <div style="font-size:11px; font-weight:700; color:#f472b6; text-transform:uppercase;">${person.name} Soruyor:</div>
            <div style="font-size:14px; font-weight:600; color:#f8fafc; font-style:italic; margin-top:4px;">
                "${topic.question}"
            </div>
        </div>

        <div class="person-action-group-title">Senin Yanıtın (Diyaloğu Yönet)</div>
        <div id="dateSimDialogueOptions" style="display:flex; flex-direction:column; gap:8px;">
            ${topic.options.map(opt => `
                <button type="button" class="btn-choice" style="text-align:left; padding:11px 13px;" onclick="chooseDateDialogueOption('${opt.id}')">
                    <div style="font-weight:600; color:#f1f5f9; font-size:13px;">${opt.text}</div>
                    <div style="font-size:11px; color:#cbd5e1; margin-top:2px;">Tarz: ${opt.type}</div>
                </button>
            `).join("")}
        </div>
        <div id="dateSimDialogueFeedback" style="display:none; margin-top:12px;"></div>
    `;
}

function chooseDateDialogueOption(optionId) {
    sound.playClick();
    dateSimState.dialogueChoiceId = optionId;
    const convos = (marketData && marketData.date_conversations) || [];
    const topic = convos.find(c => c.id === dateSimState.dialogueId) || convos[0];
    const opt = topic.options.find(o => o.id === optionId);
    const person = (gameState.relationships || []).find(p => p.id === dateSimState.personId);

    let delta = 8;
    if (person && (opt.favorite_personalities || []).includes(person.personality)) {
        delta = 18;
    } else if (["Toksik", "Soğuk", "Tembel"].includes(opt.type)) {
        delta = -18;
    }

    dateSimState.chemistry = Math.max(5, Math.min(100, dateSimState.chemistry + delta));

    const optionsContainer = document.getElementById("dateSimDialogueOptions");
    const feedbackBox = document.getElementById("dateSimDialogueFeedback");

    if (optionsContainer) optionsContainer.style.display = "none";
    if (feedbackBox) {
        feedbackBox.style.display = "block";
        feedbackBox.innerHTML = `
            <div class="panel-card" style="border-left:3px solid ${delta >= 0 ? '#4ade80' : '#f87171'}; padding:12px; margin-bottom:12px;">
                <div style="font-size:11px; font-weight:700; color:${delta >= 0 ? '#4ade80' : '#f87171'};">
                    ${person.name}'in Tepkisi (${delta >= 0 ? '+' + delta : delta}% Kimya):
                </div>
                <div style="font-size:13px; font-style:italic; color:#e2e8f0; margin-top:4px;">
                    "${opt.partner_reply}"
                </div>
            </div>
            <button type="button" class="btn-primary" style="width:100%; padding:11px;" onclick="renderDateSimTactile()">
                Devam Et (Tensel Yakınlaşma & Beden Dili) ➔
            </button>
        `;
    }
}

function renderDateSimTactile() {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === dateSimState.personId);
    const tactiles = (marketData && marketData.date_tactiles) || [];

    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f472b6; margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">💫 Tensel Çekim & Beden Dili</span>
                <span class="card-badge badge-green">❤️ Kimya: %${dateSimState.chemistry}</span>
            </div>
            <div class="stat-progress-bg" style="height:7px; margin-top:8px;">
                <div class="stat-progress-bar" style="width:${dateSimState.chemistry}%; background:linear-gradient(90deg, #ec4899, #f43f5e);"></div>
            </div>
        </div>

        <div style="background:rgba(236,72,153,0.08); border-left:3px solid #ec4899; border-radius:8px; padding:12px; margin-bottom:14px;">
            <div style="font-size:11px; font-weight:700; color:#f472b6; text-transform:uppercase;">Tensel Gerilim Yükseliyor</div>
            <div style="font-size:13.5px; font-weight:500; color:#e2e8f0; font-style:italic; margin-top:4px;">
                Diyalog ilerledikçe aranızdaki elektrik gözle görülür bir boyuta ulaştı. ${person?.name || 'Partnerin'} gözlerini gözlerinden kaçıramıyor. Aranızdaki dokunsal bağı ve tutkuyu başlatmak için nasıl bir temas seçeceksin?
            </div>
        </div>

        <div class="person-action-group-title">Dokunsal Hamleni Seç</div>
        <div id="dateSimTactileOptions" style="display:flex; flex-direction:column; gap:8px;">
            ${tactiles.map(t => `
                <button type="button" class="btn-choice" style="text-align:left; padding:11px 13px;" onclick="chooseDateTactileOption('${t.id}')">
                    <div style="font-weight:700; color:#f8fafc; font-size:13.5px;">${t.name}</div>
                    <div style="font-size:11.5px; color:#cbd5e1; margin-top:2px;">${t.short_desc} • <span style="color:#f472b6;">${t.style}</span></div>
                </button>
            `).join("")}
        </div>
        <div id="dateSimTactileFeedback" style="display:none; margin-top:12px;"></div>
    `;
}

function chooseDateTactileOption(optionId) {
    sound.playClick();
    dateSimState.tactileId = optionId;
    const tactiles = (marketData && marketData.date_tactiles) || [];
    const t = tactiles.find(item => item.id === optionId) || tactiles[0];
    const person = (gameState.relationships || []).find(p => p.id === dateSimState.personId);

    let delta = t.chemistry_boost || 20;
    if (person && ["Romantik", "Entelektüel"].includes(person.personality) && ["hair_tuck", "chin_lift_gaze"].includes(t.id)) {
        delta += 6;
    } else if (person && ["Kıskanç & Tutkulu", "Çapkın & Özgür Ruhlu"].includes(person.personality) && ["whisper_ear_neck", "thigh_touch_secret"].includes(t.id)) {
        delta += 8;
    }

    dateSimState.chemistry = Math.min(100, dateSimState.chemistry + delta);

    const optionsContainer = document.getElementById("dateSimTactileOptions");
    const feedbackBox = document.getElementById("dateSimTactileFeedback");

    if (optionsContainer) optionsContainer.style.display = "none";
    if (feedbackBox) {
        feedbackBox.style.display = "block";
        feedbackBox.innerHTML = `
            <div class="panel-card" style="border-left:3px solid #ec4899; padding:13px; margin-bottom:12px; background:rgba(236,72,153,0.06);">
                <div style="font-size:11px; font-weight:700; color:#f472b6; margin-bottom:4px;">
                    Tensel Uyum Patlaması (+${delta}% Kimya)
                </div>
                <div style="font-size:13px; color:#f1f5f9; line-height:1.5;">
                    ${t.sensory_log}
                </div>
                <div style="font-size:12.5px; font-style:italic; color:#cbd5e1; margin-top:6px; border-top:1px solid rgba(255,255,255,0.08); padding-top:6px;">
                    ${t.partner_reaction}
                </div>
            </div>
            <button type="button" class="btn-primary" style="width:100%; padding:11px;" onclick="renderDateSimMidEvent()">
                Devam Et (Randevu Ortası Sürprizi) ➔
            </button>
        `;
    }
}

function renderDateSimMidEvent() {
    sound.playClick();
    const midEvents = (marketData && marketData.date_mid_events) || [];
    const eventObj = midEvents.find(e => e.id === dateSimState.midEventId) || midEvents[0];

    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f472b6; margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">${eventObj.title}</span>
                <span class="card-badge badge-green">❤️ Kimya: %${dateSimState.chemistry}</span>
            </div>
            <div class="stat-progress-bg" style="height:7px; margin-top:8px;">
                <div class="stat-progress-bar" style="width:${dateSimState.chemistry}%; background:linear-gradient(90deg, #ec4899, #f43f5e);"></div>
            </div>
        </div>

        <div style="background:rgba(255,255,255,0.03); border-radius:8px; padding:12px; margin-bottom:14px; font-size:13px; color:#cbd5e1;">
            ${eventObj.desc}
        </div>

        <div class="person-action-group-title">Nasıl Tepki Vereceksin?</div>
        <div id="dateSimMidOptions" style="display:flex; flex-direction:column; gap:8px;">
            ${eventObj.options.map(opt => `
                <button type="button" class="btn-choice" style="text-align:left; padding:11px 13px;" onclick="chooseDateMidEventOption('${opt.id}')">
                    <div style="font-weight:600; color:#f1f5f9; font-size:13px;">${opt.text}</div>
                </button>
            `).join("")}
        </div>
        <div id="dateSimMidFeedback" style="display:none; margin-top:12px;"></div>
    `;
}

function chooseDateMidEventOption(optionId) {
    sound.playClick();
    dateSimState.midChoiceId = optionId;
    const midEvents = (marketData && marketData.date_mid_events) || [];
    const eventObj = midEvents.find(e => e.id === dateSimState.midEventId) || midEvents[0];
    const opt = eventObj.options.find(o => o.id === optionId);

    const delta = opt.effect_score || 10;
    dateSimState.chemistry = Math.max(5, Math.min(100, dateSimState.chemistry + delta));

    const optionsContainer = document.getElementById("dateSimMidOptions");
    const feedbackBox = document.getElementById("dateSimMidFeedback");

    if (optionsContainer) optionsContainer.style.display = "none";
    if (feedbackBox) {
        feedbackBox.style.display = "block";
        feedbackBox.innerHTML = `
            <div class="panel-card" style="border-left:3px solid ${delta >= 0 ? '#4ade80' : '#f87171'}; padding:12px; margin-bottom:12px;">
                <div style="font-size:13px; color:#e2e8f0;">
                    ${opt.note} (${delta >= 0 ? '+' + delta : delta}% Kimya)
                </div>
            </div>
            <button type="button" class="btn-primary" style="width:100%; padding:11px;" onclick="renderDateSimFinale()">
                Devam Et (Gecenin Kapanışı & Veda) ➔
            </button>
        `;
    }
}

function renderDateSimFinale() {
    sound.playClick();
    const finales = (marketData && marketData.date_finales) || [];
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:#f472b6; margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">🌙 Gecenin Sonu & Veda Hamlesi</span>
                <span class="card-badge badge-green">❤️ Kimya: %${dateSimState.chemistry}</span>
            </div>
            <div class="stat-progress-bg" style="height:7px; margin-top:8px;">
                <div class="stat-progress-bar" style="width:${dateSimState.chemistry}%; background:linear-gradient(90deg, #ec4899, #f43f5e);"></div>
            </div>
        </div>

        <p class="card-desc" style="margin-bottom:14px;">
            Kapının önünde göz göze duruyorsunuz. Gece sona eriyor; partnerinin gözlerinde beklenti dolu bir bakış var. Nasıl bir veda yapacaksın?
        </p>

        <div style="display:flex; flex-direction:column; gap:8px;">
            ${finales.map(f => `
                <button type="button" class="btn-choice" style="text-align:left; padding:12px;" onclick="submitDateSimFinale('${f.id}')">
                    <div style="font-weight:700; color:#f8fafc; font-size:13.5px;">${f.name}</div>
                    <div style="font-size:11px; color:#cbd5e1; margin-top:2px;">Gereken Asgari Kimya: %${f.chemistry_min}</div>
                </button>
            `).join("")}
        </div>
    `;
}

async function submitDateSimFinale(finaleId) {
    sound.playClick();
    dateSimState.finaleId = finaleId;

    const payload = {
        person_id: dateSimState.personId,
        venue_id: dateSimState.venueId,
        outfit_id: dateSimState.outfitId,
        greeting_id: dateSimState.greetingId,
        dialogue_id: dateSimState.dialogueId,
        dialogue_choice_id: dateSimState.dialogueChoiceId,
        tactile_id: dateSimState.tactileId || "hand_caress_table",
        mid_event_id: dateSimState.midEventId,
        mid_choice_id: dateSimState.midChoiceId,
        finale_id: dateSimState.finaleId
    };

    const res = await performActivity("run_date_simulation", payload);
    if (!res || !res.success) {
        closeModal("genericModal");
        return;
    }

    renderDateSimScorecard(res);
}

function renderDateSimScorecard(res) {
    const person = (gameState.relationships || []).find(p => p.id === dateSimState.personId);
    const body = document.getElementById("genericModalBody");
    document.getElementById("genericModalTitle").textContent = "🏆 Randevu Karnesi & Sonuç";

    body.innerHTML = `
        <div class="panel-card" style="text-align:center; padding:18px; border-color:#ec4899; margin-bottom:14px;">
            <div style="font-size:20px; font-weight:800; color:#fb7185; margin-bottom:6px;">
                ${res.rating_title || '🌹 Büyüleyici Randevu'}
            </div>
            <div style="font-size:13px; color:#cbd5e1;">
                Nihai Aşk Kimyası: <b style="color:#f43f5e;">%${res.chemistry || dateSimState.chemistry}</b> • İlişki: <b style="color:var(--accent-green);">${res.rel_boost > 0 ? '+' : ''}${res.rel_boost}</b>
            </div>
        </div>

        ${res.promoted_to_lover ? `
            <div class="panel-card" style="background:linear-gradient(135deg, rgba(236,72,153,0.2), rgba(244,63,94,0.3)); border-color:#f43f5e; text-align:center; padding:14px; margin-bottom:14px;">
                <div style="font-size:24px; margin-bottom:4px;">💘🎉</div>
                <div style="font-weight:800; color:#fff; font-size:15px;">GÖNLÜNÜ FETHETTİN! ARTIK SEVGİLİSİNİZ!</div>
                <div style="font-size:12px; color:#fbcfe8; margin-top:2px;">${person?.name || 'Partnerin'} ile birbirinize duyduğunuz aşk resmiyet kazandı!</div>
            </div>
        ` : ''}

        <div class="panel-card" style="margin-bottom:14px;">
            <div class="person-action-group-title" style="margin-top:0;">📖 Geceden Öne Çıkan Anlar</div>
            <div class="memories-timeline" style="margin-top:6px;">
                ${res.outfit_log ? `<div class="memory-item">• ${res.outfit_log}</div>` : ''}
                ${res.greeting_log ? `<div class="memory-item">• ${res.greeting_log}</div>` : ''}
                ${res.dialogue_log ? `<div class="memory-item">• "${res.dialogue_log}"</div>` : ''}
                ${res.tactile_log ? `<div class="memory-item" style="color:#fbcfe8;">• 💫 ${res.tactile_log}</div>` : ''}
                ${res.mid_log ? `<div class="memory-item">• ${res.mid_log}</div>` : ''}
                ${res.finale_log ? `<div class="memory-item">• ${res.finale_log}</div>` : ''}
            </div>
        </div>

        <button type="button" class="btn-primary" style="width:100%; padding:12px; font-size:14.5px;" onclick="closeModal('genericModal');">
            ✨ Harika! Hayata Devam Et
        </button>
    `;
}

function openDetailedFightModal(personId) {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === personId);
    if (!person) return;
    const topics = (marketData && marketData.detailed_fight_topics) || [];
    const attitudes = (marketData && marketData.detailed_fight_attitudes) || [];

    document.getElementById("genericModalTitle").textContent = `💥 Şiddetli Kavga & Hesaplaşma: ${person.name}`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
        <div class="panel-card" style="border-color:var(--accent-red); margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">🤬 ${person.name} ile Kriz & Hesaplaşma Masası</span>
                <span class="card-badge badge-red">Gerginlik Tavan</span>
            </div>
            <p class="card-desc" style="font-size:12.5px; margin-top:4px;">
                İçinde birikenleri masaya yatıracaksın. Partnerinin çılgınlığı ve sadakati sonucun boyutunu belirleyecek!
            </p>
        </div>

        <form id="detailedFightForm" onsubmit="event.preventDefault(); submitDetailedFightForm('${person.id}');">
            <div class="person-action-group-title">1. Adım: Hesap Sorma Nedeni & Konu</div>
            <div class="form-group" style="margin-bottom:12px;">
                <select id="fightTopicSelect" class="form-select" style="font-size:13px; padding:10px;">
                    ${topics.map(t => `<option value="${t.id}">${t.name}</option>`).join("")}
                </select>
            </div>

            <div class="person-action-group-title">2. Adım: Senin Kavga Yaklaşımın & Tavrın</div>
            <div class="form-group" style="margin-bottom:14px;">
                <select id="fightAttitudeSelect" class="form-select" style="font-size:13px; padding:10px;">
                    ${attitudes.map(a => `<option value="${a.id}">${a.name}</option>`).join("")}
                </select>
            </div>

            <button type="submit" class="btn-primary" style="background:var(--accent-red); border-color:#dc2626; font-size:15px; padding:12px; margin-top:6px;">💥 Yüzleşmeyi Başlat & Hesap Sor</button>
        </form>
    `;
    openDialogModal("genericModal");
}

async function submitDetailedFightForm(personId) {
    const topicId = document.getElementById("fightTopicSelect")?.value || "jealousy_dm";
    const attitudeId = document.getElementById("fightAttitudeSelect")?.value || "calm_ultimatum";
    await performActivity("detailed_fight", {
        person_id: personId,
        topic_id: topicId,
        attitude_id: attitudeId
    });
    closeModal("genericModal");
}

// ----------------- YATAK ODASI, İNTİMİTE & BİRLİKTE OL MOTORU -----------------

function openIntimacyPickerModal() {
    sound.playClick();
    const partners = (gameState.relationships || []).filter(p => p.is_alive && ["Sevgili", "Nişanlı", "Eş", "Flört", "Eski Sevgili", "Arkadaş"].includes(p.relation));
    document.getElementById("genericModalTitle").textContent = "🔥 Yatak Odası & Romantik Yakınlaşma";
    const body = document.getElementById("genericModalBody");

    if (partners.length === 0) {
        body.innerHTML = `
            <div class="panel-card" style="text-align:center; padding:20px;">
                <div style="font-size:36px; margin-bottom:10px;">💔</div>
                <div class="card-title" style="margin-bottom:6px;">Yakınlaşacak Partner Yok</div>
                <p class="card-desc" style="margin-bottom:16px;">
                    Şu anda birlikte olabileceğin bir sevgilin, flörtün veya partnerin bulunmuyor.
                    KısmetApp'e girerek yeni biriyle tanışabilir veya gece kulüplerinde kaçamak yapabilirsin!
                </p>
                <div style="display:flex; gap:8px; justify-content:center;">
                    <button type="button" class="btn-primary" onclick="closeModal('genericModal'); openKismetAppModal();">📱 KısmetApp</button>
                    <button type="button" class="btn-secondary" onclick="closeModal('genericModal'); openHookupModal();">🍸 Kaçamak Yap</button>
                </div>
            </div>
        `;
    } else {
        body.innerHTML = `
            <p class="card-desc" style="margin-bottom:12px;">
                Kiminle baş başa kalıp tutku dolu romantik anlar yaşamak istiyorsun? Partnerini seç, mekanı ve atmosferi belirle:
            </p>
            <div style="display:flex; flex-direction:column; gap:8px;">
                ${partners.map(p => `
                    <button type="button" class="btn-choice" style="display:flex; align-items:center; justify-content:space-between; padding:12px;" onclick="closeModal('genericModal'); openIntimacyModal('${p.id}');">
                        <div style="display:flex; align-items:center; gap:10px;">
                            <span style="font-size:22px;">${getRelationEmoji(p.relation)}</span>
                            <div style="text-align:left;">
                                <div style="font-weight:700; color:var(--text-primary); font-size:14px;">${p.name}</div>
                                <div style="font-size:12px; color:var(--text-secondary);">${p.relation} • ${p.age} Yaşında • ${p.personality || 'Romantik'}</div>
                            </div>
                        </div>
                        <div style="text-align:right;">
                            <div style="font-size:12px; font-weight:700; color:var(--accent-pink);">İlişki: %${p.relationship_level}</div>
                            <span class="status-chip" style="font-size:11px; padding:2px 8px; margin-top:2px; display:inline-block;">Seç 🔥</span>
                        </div>
                    </button>
                `).join("")}
            </div>
        `;
    }
    openDialogModal("genericModal");
}

let intimacySimState = {
    personId: null,
    step: 1,
    venueId: "bedroom_candlelight",
    musicId: "acoustic_jazz",
    outfitId: "natural_cozy",
    foreplayId: null,
    styleId: null,
    twistId: null,
    twistChoiceId: null,
    protectionId: "condom_safe",
    morningId: "breakfast_in_bed",
    passion: 60
};

function openIntimacyModal(personId) {
    sound.playClick();
    const person = (gameState.relationships || []).find(p => p.id === personId);
    if (!person) return;

    const basePassion = Math.min(100, Math.max(40, Math.round((person.relationship_level || 50) * 0.35 + (gameState.looks || 50) * 0.3 + (gameState.health || 80) * 0.2)));
    const venues = (marketData && marketData.intimacy_venues) || [];
    const musics = (marketData && marketData.intimacy_musics) || [];
    const outfits = (marketData && marketData.intimacy_outfits) || [];
    const foreplays = (marketData && marketData.intimacy_foreplays) || [];
    const styles = (marketData && marketData.intimacy_styles) || [];
    const twists = (marketData && marketData.intimacy_twists) || [];

    const randomTwist = twists[Math.floor(Math.random() * (twists.length || 1))] || twists[0];

    intimacySimState = {
        personId: personId,
        step: 1,
        venueId: venues[0]?.id || "bedroom_candlelight",
        musicId: musics[0]?.id || "acoustic_jazz",
        outfitId: outfits[3]?.id || "natural_cozy",
        foreplayId: foreplays[0]?.id || "massage_oil",
        styleId: styles[0]?.id || "tender_sensual",
        twistId: randomTwist?.id || "candle_magic",
        twistChoiceId: randomTwist?.options ? randomTwist.options[0]?.id : null,
        protectionId: "condom_safe",
        morningId: "breakfast_in_bed",
        passion: basePassion
    };

    renderIntimacyStep1();
    openDialogModal("genericModal");
}

function renderIntimacyHeader(person, stepTitle, stepNum) {
    const chemVal = person.intimacy_chemistry || 50;
    const countVal = person.intimacy_count || 0;
    const tierLabel = countVal === 0 ? "🌱 İlk Birliktelik" : (countVal < 4 ? `🌿 Gelişen Uyum (${countVal}. Gece)` : `🔥 Kusursuz Uyum (${countVal}. Gece)`);
    return `
        <div class="panel-card" style="margin-bottom:12px; background:linear-gradient(135deg, rgba(244,63,94,0.14), rgba(168,85,247,0.14)); border:1px solid rgba(244,63,94,0.35); padding:12px;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
                <div>
                    <h3 style="font-size:15px; font-weight:800; margin:0; color:#fda4af;">${getRelationEmoji(person.relation)} ${person.name}</h3>
                    <div style="font-size:11.5px; color:var(--text-secondary);">${person.relation} • ${tierLabel}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:11px; color:#fbcfe8;">Canlı Tutku & Arzu</div>
                    <div style="font-size:16px; font-weight:900; color:#fb7185;">%${intimacySimState.passion}</div>
                </div>
            </div>
            <div class="stat-progress-bg" style="height:6px; background:rgba(0,0,0,0.3);">
                <div class="stat-progress-bar" style="width:${intimacySimState.passion}%; background:linear-gradient(90deg, #ec4899, #f43f5e);"></div>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; font-size:11.5px; color:#cbd5e1; font-weight:600;">
                <span>Adım ${stepNum}/5: ${stepTitle}</span>
                <span style="color:#f43f5e;">Ten Uyumu: %${chemVal}</span>
            </div>
        </div>
    `;
}

function renderIntimacyStep1() {
    const person = (gameState.relationships || []).find(p => p.id === intimacySimState.personId);
    if (!person) return;

    document.getElementById("genericModalTitle").textContent = "🔥 Yatak Odası & İntimite Simülasyonu";
    const body = document.getElementById("genericModalBody");

    const venues = (marketData && marketData.intimacy_venues) || [];
    const musics = (marketData && marketData.intimacy_musics) || [];
    const outfits = (marketData && marketData.intimacy_outfits) || [];

    body.innerHTML = `
        ${renderIntimacyHeader(person, "Ambiyans, Müzik & Hazırlık", 1)}

        <form id="intimacyStep1Form" onsubmit="event.preventDefault(); proceedIntimacyStep2();">
            <div class="person-action-group-title">1. Mekan & Atmosfer</div>
            <div class="form-group" style="margin-bottom:12px;">
                <select id="simVenueSelect" class="form-select" style="font-size:12.5px; padding:9px;">
                    ${venues.map(v => `<option value="${v.id}" ${v.id === intimacySimState.venueId ? 'selected' : ''}>${v.name} ${v.cost > 0 ? `(${v.cost.toLocaleString('tr-TR')} ₺)` : '(Ücretsiz)'}</option>`).join("")}
                </select>
            </div>

            <div class="person-action-group-title">2. Arka Plan Müziği & Ambiyans</div>
            <div class="form-group" style="margin-bottom:12px;">
                <select id="simMusicSelect" class="form-select" style="font-size:12.5px; padding:9px;">
                    ${musics.map(m => `<option value="${m.id}" ${m.id === intimacySimState.musicId ? 'selected' : ''}>${m.name}</option>`).join("")}
                </select>
            </div>

            <div class="person-action-group-title">3. Kıyafet / İç Giyim & Cazibe</div>
            <div class="form-group" style="margin-bottom:16px;">
                <select id="simOutfitSelect" class="form-select" style="font-size:12.5px; padding:9px;">
                    ${outfits.map(o => `<option value="${o.id}" ${o.id === intimacySimState.outfitId ? 'selected' : ''}>${o.name} ${o.cost > 0 ? `(${o.cost.toLocaleString('tr-TR')} ₺)` : '(Ücretsiz)'}</option>`).join("")}
                </select>
            </div>

            <button type="submit" class="btn-primary" style="background:linear-gradient(135deg, #f43f5e, #e11d48); border:none; font-size:14.5px; padding:12px;">
                Baştan Çıkarmaya Başla ➡️ (Ön Sevişme)
            </button>
        </form>
    `;
}

function proceedIntimacyStep2() {
    intimacySimState.venueId = document.getElementById("simVenueSelect")?.value || intimacySimState.venueId;
    intimacySimState.musicId = document.getElementById("simMusicSelect")?.value || intimacySimState.musicId;
    intimacySimState.outfitId = document.getElementById("simOutfitSelect")?.value || intimacySimState.outfitId;
    intimacySimState.passion = Math.min(100, intimacySimState.passion + 8);
    renderIntimacyStep2();
}

function renderIntimacyStep2() {
    const person = (gameState.relationships || []).find(p => p.id === intimacySimState.personId);
    if (!person) return;

    const foreplays = (marketData && marketData.intimacy_foreplays) || [];
    const activeForeplay = foreplays.find(f => f.id === intimacySimState.foreplayId) || foreplays[0];

    const body = document.getElementById("genericModalBody");
    body.innerHTML = `
        ${renderIntimacyHeader(person, "Baştan Çıkarma & Ön Sevişme (Dokunsal Isınma)", 2)}

        <p class="card-desc" style="margin-bottom:12px; font-size:12.5px;">
            Partnerini nasıl baştan çıkarmak ve tenini ısıtmak istiyorsun? Bir hamle seçip canlı tepkisini hisset:
        </p>

        <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
            ${foreplays.map(f => `
                <button type="button" class="btn-choice ${f.id === intimacySimState.foreplayId ? 'selected-btn-choice' : ''}" style="text-align:left; padding:11px; border:1px solid ${f.id === intimacySimState.foreplayId ? '#f43f5e' : 'rgba(255,255,255,0.08)'}; background:${f.id === intimacySimState.foreplayId ? 'rgba(244,63,94,0.15)' : 'rgba(255,255,255,0.03)'};" onclick="chooseForeplayAction('${f.id}')">
                    <div style="font-weight:700; font-size:13.5px; color:#fda4af;">${f.name}</div>
                    <div style="font-size:11.5px; color:var(--text-secondary); margin-top:2px;">${f.desc}</div>
                </button>
            `).join("")}
        </div>

        <div style="background:rgba(255,255,255,0.04); border-radius:10px; padding:12px; margin-bottom:14px; border-left:3px solid #f43f5e;">
            <div style="font-size:11px; color:#f43f5e; font-weight:700; text-transform:uppercase; margin-bottom:4px;">✨ Dokunuş & Nefesler</div>
            <div style="font-size:12.5px; color:#f1f5f9; line-height:1.5;">${activeForeplay.sensory_log}</div>
            <div style="font-size:12px; color:#fbcfe8; font-style:italic; margin-top:6px;">${activeForeplay.partner_reply}</div>
        </div>

        <button type="button" class="btn-primary" style="background:linear-gradient(135deg, #f43f5e, #e11d48); border:none; font-size:14.5px; padding:12px;" onclick="renderIntimacyStep3()">
            Yakınlaşmayı Derinleştir ➡️ (Ritim & Dinamik)
        </button>
    `;
}

function chooseForeplayAction(foreplayId) {
    intimacySimState.foreplayId = foreplayId;
    intimacySimState.passion = Math.min(100, intimacySimState.passion + 10);
    renderIntimacyStep2();
}

function renderIntimacyStep3() {
    const person = (gameState.relationships || []).find(p => p.id === intimacySimState.personId);
    if (!person) return;

    const styles = (marketData && marketData.intimacy_styles) || [];
    const activeStyle = styles.find(s => s.id === intimacySimState.styleId) || styles[0];

    const body = document.getElementById("genericModalBody");
    body.innerHTML = `
        ${renderIntimacyHeader(person, "Yakınlaşma Ritmi & Ten Dinamiği", 3)}

        <p class="card-desc" style="margin-bottom:12px; font-size:12.5px;">
            Yatakta aranızdaki akışı hangi tempoda ve duyguda yönetmek istiyorsun?
        </p>

        <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
            ${styles.map(s => `
                <button type="button" class="btn-choice ${s.id === intimacySimState.styleId ? 'selected-btn-choice' : ''}" style="text-align:left; padding:11px; border:1px solid ${s.id === intimacySimState.styleId ? '#a855f7' : 'rgba(255,255,255,0.08)'}; background:${s.id === intimacySimState.styleId ? 'rgba(168,85,247,0.15)' : 'rgba(255,255,255,0.03)'};" onclick="chooseIntimacyStyle('${s.id}')">
                    <div style="font-weight:700; font-size:13.5px; color:#d8b4fe;">${s.name}</div>
                    <div style="font-size:11.5px; color:var(--text-secondary); margin-top:2px;">${s.desc}</div>
                </button>
            `).join("")}
        </div>

        <div style="background:rgba(255,255,255,0.04); border-radius:10px; padding:12px; margin-bottom:14px; border-left:3px solid #a855f7;">
            <div style="font-size:11px; color:#d8b4fe; font-weight:700; text-transform:uppercase; margin-bottom:4px;">🔥 Kalp Atışları & Ten Birleşimi</div>
            <div style="font-size:12.5px; color:#f1f5f9; line-height:1.5;">${activeStyle.narrative}</div>
        </div>

        <button type="button" class="btn-primary" style="background:linear-gradient(135deg, #a855f7, #9333ea); border:none; font-size:14.5px; padding:12px;" onclick="renderIntimacyStep4()">
            Gecenin Akışına Bırak ➡️ (Sürpriz An)
        </button>
    `;
}

function chooseIntimacyStyle(styleId) {
    intimacySimState.styleId = styleId;
    intimacySimState.passion = Math.min(100, intimacySimState.passion + 10);
    renderIntimacyStep3();
}

function renderIntimacyStep4() {
    const person = (gameState.relationships || []).find(p => p.id === intimacySimState.personId);
    if (!person) return;

    const twists = (marketData && marketData.intimacy_twists) || [];
    const activeTwist = twists.find(t => t.id === intimacySimState.twistId) || twists[0];
    const options = activeTwist.options || [];

    const body = document.getElementById("genericModalBody");
    body.innerHTML = `
        ${renderIntimacyHeader(person, "Yatak Odası Sürprizi & Anlık Reaksiyon", 4)}

        <div style="background:rgba(245,158,11,0.12); border-left:3px solid #f59e0b; border-radius:10px; padding:12px; margin-bottom:14px;">
            <div style="font-size:13px; font-weight:800; color:#fcd34d; margin-bottom:4px;">${activeTwist.title}</div>
            <div style="font-size:12.5px; color:#fef3c7; line-height:1.5;">${activeTwist.text}</div>
        </div>

        <p class="card-desc" style="margin-bottom:10px; font-size:12.5px;">Bu beklenmedik anda nasıl bir hamle yapıyorsun?</p>

        <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:16px;">
            ${options.map(opt => `
                <button type="button" class="btn-choice ${opt.id === intimacySimState.twistChoiceId ? 'selected-btn-choice' : ''}" style="text-align:left; padding:11px; border:1px solid ${opt.id === intimacySimState.twistChoiceId ? '#f59e0b' : 'rgba(255,255,255,0.08)'}; background:${opt.id === intimacySimState.twistChoiceId ? 'rgba(245,158,11,0.15)' : 'rgba(255,255,255,0.03)'};" onclick="chooseTwistChoice('${opt.id}')">
                    <div style="font-weight:700; font-size:13px; color:#fef08a;">${opt.text}</div>
                    <div style="font-size:11.5px; color:#cbd5e1; margin-top:3px; font-style:italic;">"${opt.reaction}"</div>
                </button>
            `).join("")}
        </div>

        <button type="button" class="btn-primary" style="background:linear-gradient(135deg, #f59e0b, #d97706); border:none; font-size:14.5px; padding:12px;" onclick="renderIntimacyStep5()">
            Gecenin Kapanışı & Sabah ➡️
        </button>
    `;
}

function chooseTwistChoice(choiceId) {
    intimacySimState.twistChoiceId = choiceId;
    intimacySimState.passion = Math.min(100, intimacySimState.passion + 8);
    renderIntimacyStep4();
}

function renderIntimacyStep5() {
    const person = (gameState.relationships || []).find(p => p.id === intimacySimState.personId);
    if (!person) return;

    const protections = (marketData && marketData.intimacy_protections) || [];
    const mornings = (marketData && marketData.intimacy_mornings) || [];

    const body = document.getElementById("genericModalBody");
    body.innerHTML = `
        ${renderIntimacyHeader(person, "Korunma & Sabah Uyanışı (Yastık Sohbeti)", 5)}

        <form id="intimacyStep5Form" onsubmit="event.preventDefault(); submitIntimacySimulation();">
            <div class="person-action-group-title">1. Korunma Yöntemi & Niyet</div>
            <div class="form-group" style="margin-bottom:12px;">
                <select id="simProtectionSelect" class="form-select" style="font-size:12.5px; padding:9px;">
                    ${protections.map(pr => `<option value="${pr.id}">${pr.name} - [${pr.safety_label}]</option>`).join("")}
                </select>
            </div>

            <div class="person-action-group-title">2. Sabah Uyanışı & Kapanış Jesti</div>
            <div class="form-group" style="margin-bottom:16px;">
                <select id="simMorningSelect" class="form-select" style="font-size:12.5px; padding:9px;">
                    ${mornings.map(m => `<option value="${m.id}">${m.name}</option>`).join("")}
                </select>
            </div>

            <button type="submit" class="btn-primary" style="background:linear-gradient(135deg, #f43f5e, #e11d48); border:none; font-size:15px; padding:12px; box-shadow:0 4px 15px rgba(244,63,94,0.4);">
                🔥 Birlikteliği Tamamla & Karneni Gör
            </button>
        </form>
    `;
}

async function submitIntimacySimulation() {
    intimacySimState.protectionId = document.getElementById("simProtectionSelect")?.value || intimacySimState.protectionId;
    intimacySimState.morningId = document.getElementById("simMorningSelect")?.value || intimacySimState.morningId;

    const res = await performActivity("do_intimacy", {
        person_id: intimacySimState.personId,
        venue_id: intimacySimState.venueId,
        music_id: intimacySimState.musicId,
        outfit_id: intimacySimState.outfitId,
        foreplay_id: intimacySimState.foreplayId,
        style_id: intimacySimState.styleId,
        twist_id: intimacySimState.twistId,
        twist_choice_id: intimacySimState.twistChoiceId,
        protection_id: intimacySimState.protectionId,
        morning_id: intimacySimState.morningId
    });

    if (res && res.success) {
        showIntimacyResultModal(res);
    } else {
        closeModal("genericModal");
    }
}

function showIntimacyResultModal(res) {
    document.getElementById("genericModalTitle").textContent = "🔥 Birliktelik Karnesi & Sabahın İlk Işıkları";
    const body = document.getElementById("genericModalBody");

    const starIcons = "⭐".repeat(res.stars || 4);
    body.innerHTML = `
        <div style="text-align:center; padding:8px 0;">
            <div style="font-size:24px; margin-bottom:2px;">${starIcons}</div>
            <h3 style="font-size:16.5px; font-weight:800; color:#fb7185; margin:0 0 4px 0;">${res.star_title || 'ÇOK TUTKULU BİR GECE!'}</h3>
            <div style="font-size:12px; color:#fbcfe8; font-weight:600; margin-bottom:12px;">${res.experience_tier || '🌿 Gelişen Ten Uyumu'} • ${res.venue}</div>
            
            <div style="background:rgba(255,255,255,0.05); border-radius:12px; padding:12px; margin-bottom:12px; text-align:left; border:1px solid rgba(255,255,255,0.1);">
                <div style="font-size:11px; color:#f43f5e; font-weight:700; text-transform:uppercase; margin-bottom:3px;">1. Ön Sevişme & Baştan Çıkarma</div>
                <div style="font-size:12px; color:#f1f5f9; line-height:1.45; margin-bottom:8px;">
                    ${res.foreplay_log || ''}
                </div>

                <div style="font-size:11px; color:#a855f7; font-weight:700; text-transform:uppercase; margin-bottom:3px;">2. Yakınlaşma & Tutku Doyumu</div>
                <div style="font-size:12px; color:#cbd5e1; line-height:1.45; margin-bottom:8px;">
                    ${res.narrative || ''}
                </div>

                ${res.twist_title ? `
                    <div style="background:rgba(245,158,11,0.1); border-left:3px solid #f59e0b; padding:7px 10px; border-radius:6px; margin-bottom:8px;">
                        <div style="font-size:11.5px; font-weight:700; color:#fcd34d;">${res.twist_title}</div>
                        <div style="font-size:11.5px; color:#fef3c7; line-height:1.35;">${res.twist_log}</div>
                    </div>
                ` : ""}

                <div style="font-size:11px; color:#38bdf8; font-weight:700; text-transform:uppercase; margin-bottom:3px;">3. Sabah Uyanışı & Yastık Sohbeti</div>
                <div style="font-size:12px; color:#e0f2fe; line-height:1.45;">
                    ${res.morning_log || ''}
                </div>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:12px;">
                <div class="person-stat-pill" style="padding:8px; text-align:center;">
                    <div style="font-size:10.5px; color:var(--text-secondary);">Ten Uyumu / Memnuniyet</div>
                    <div style="font-size:17px; font-weight:900; color:#f43f5e;">%${res.satisfaction || 85}</div>
                </div>
                <div class="person-stat-pill" style="padding:8px; text-align:center;">
                    <div style="font-size:10.5px; color:var(--text-secondary);">Ruh Hali & Bağ</div>
                    <div style="font-size:13px; font-weight:700; color:#4ade80;">İlişki +${res.rel_boost} • Stres -${res.stress_relief}</div>
                </div>
            </div>

            ${res.pregnancy_occurred ? `
                <div style="background:rgba(236,72,153,0.18); border:1px solid rgba(236,72,153,0.5); border-radius:12px; padding:10px; margin-bottom:12px; text-align:center;">
                    <div style="font-size:22px; margin-bottom:2px;">🍼👶</div>
                    <div style="font-size:13px; font-weight:700; color:#fbcfe8;">${res.pregnancy_msg}</div>
                </div>
            ` : ""}

            <button type="button" class="btn-primary" onclick="closeModal('genericModal');">
                ✨ Harika Bir Geceydi
            </button>
        </div>
    `;
    openDialogModal("genericModal");
}





function openLeverageModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🚀 10x Kaldıraçlı Vadeli İşlemler";
    const body = document.getElementById("genericModalBody");

    const stockKeys = Object.keys(gameState.stocks || {});
    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Vadeli işlem borsasında 10 kat kaldıraçla Long (Yükseliş) veya Short (Düşüş) pozisyonu aç (Yüksek kâr / Likidasyon riski!):</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <div>
                <label style="font-size:12px; color:var(--text-secondary);">İşlem Paritesi:</label>
                <select id="levSymbol" class="input-theme" style="width:100%; margin-top:4px;">
                    ${stockKeys.map(s => `<option value="${s}">${s} - ${(gameState.stocks[s]||{}).name}</option>`).join("")}
                </select>
            </div>
            <div>
                <label style="font-size:12px; color:var(--text-secondary);">Teminat Miktarı (₺):</label>
                <input id="levMargin" type="number" class="input-theme" style="width:100%; margin-top:4px;" value="50000" min="5000" step="5000" />
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px;">
                <button type="button" class="btn-primary" style="background:#10b981;" onclick="submitLeverageTrade('long')">🟢 10x LONG (Yükseliş)</button>
                <button type="button" class="btn-primary" style="background:#ef4444;" onclick="submitLeverageTrade('short')">🔴 10x SHORT (Düşüş)</button>
            </div>
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openStocksModal()">← Borsaya Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitLeverageTrade(direction) {
    const sym = document.getElementById("levSymbol").value;
    const margin = parseInt(document.getElementById("levMargin").value) || 50000;
    await performActivity("leverage_trade", { symbol: sym, direction: direction, leverage: 10, margin_amount: margin });
    openStocksModal();
}

function openInsiderTradingModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🕵️‍♂️ Plazada İçeriden Bilgi (Insider Trading)";
    const body = document.getElementById("genericModalBody");

    const stockKeys = Object.keys(gameState.stocks || {});
    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">100.000 TL bilgi rüşveti vererek holding yöneticilerinden gizli bilanço / birleşme istihbaratı al (%72 başarıyla tavan kilitler, SPK yakalarsa 3 yıl hapis!):</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${stockKeys.slice(0, 6).map(sym => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${sym}</span>
                        <span class="card-badge badge-yellow">Maliyet: ₺ 100.000</span>
                    </div>
                    <button type="button" class="btn-primary" style="margin-top:6px;" onclick="submitInsiderTrading('${sym}')">Kulis Bilgisi Al & Pozisyon Aç 🕵️‍♂️</button>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openStocksModal()">← Borsaya Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitInsiderTrading(symbol) {
    await performActivity("insider_trading", { symbol: symbol });
    openStocksModal();
}

function openCryptoStakingModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🪙 Kripto Staking (DeFi Havuzu)";
    const body = document.getElementById("genericModalBody");

    const cryptos = ["BTC", "ETH", "MEME", "MOONCOIN"];
    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Kripto varlıklarını akıllı sözleşmeye kilitleyip yıllık %12 pasif faiz geliri elde et:</p>
        <div style="display:flex; flex-direction:column; gap:8px;">
            ${cryptos.map(sym => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${sym} Havuzu</span>
                        <span class="card-badge badge-green">%12 Yıllık Getiri</span>
                    </div>
                    <div style="display:flex; gap:6px; margin-top:8px;">
                        <button type="button" class="btn-choice" style="flex:1;" onclick="submitCryptoStaking('${sym}', 50000)">50B ₺ Kilitle</button>
                        <button type="button" class="btn-choice" style="flex:1;" onclick="submitCryptoStaking('${sym}', 200000)">200B ₺ Kilitle</button>
                    </div>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="openStocksModal()">← Borsaya Dön</button>
    `;
    openDialogModal("genericModal");
}

async function submitCryptoStaking(sym, amount) {
    await performActivity("stake_crypto", { symbol: sym, amount: amount });
    openStocksModal();
}


// ==========================================
// 1. ESNAF & SANAYİ SİMÜLATÖRÜ MODALI
// ==========================================

function openTraditionalShopModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🥙 Esnaf & Sanayi Dükkanı Aç";
    const body = document.getElementById("genericModalBody");

    if (gameState.business) {
        body.innerHTML = `
            <div class="panel-card" style="border-color:var(--accent-yellow);">
                <h4>⚠️ Zaten Aktif Bir İşletmen Var</h4>
                <p class="card-desc" style="margin: 8px 0;">Şu anda '<b>${gameState.business.name}</b>' işletmesini yönetiyorsun. Yeni bir dükkan açabilmek için mevcut işletmeni devretmeli veya satmalısın.</p>
                <button type="button" class="btn-secondary" style="width:100%; margin-top:8px;" onclick="closeModal('genericModal')">Tamam</button>
            </div>
        `;
        openDialogModal("genericModal");
        return;
    }

    const shops = (marketData && marketData.traditional_shop_types) || [];
    body.innerHTML = `
        <p class="card-desc" style="margin-bottom:12px;">Kendi yağında kavrulan geleneksel bir Türk esnafı ol! Çırak yetiştir, gizli sosunu geliştir, zabıtayla anlaş ve motor kuryelerle sipariş yağdır:</p>
        <div style="display:flex; flex-direction:column; gap:10px;">
            ${shops.map(s => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${s.name}</span>
                        <span class="card-badge badge-green">Sermaye: ₺ ${s.capital_required.toLocaleString("tr-TR")}</span>
                    </div>
                    <p class="card-desc" style="margin:6px 0;">${s.desc}</p>
                    <div class="person-chip-row" style="margin-bottom:8px;">
                        <span class="person-chip" style="color:#6ee7b7;">📈 Başlangıç Kârı: +₺ ${s.base_annual_profit.toLocaleString("tr-TR")}/yıl</span>
                        <span class="person-chip">🏷️ Sektör: ${s.sector}</span>
                    </div>
                    <button type="button" class="btn-primary" style="width:100%;" onclick="startTraditionalShop('${s.id}')" ${gameState.money < s.capital_required ? 'disabled style="opacity:0.5;"' : ''}>
                        ${gameState.money >= s.capital_required ? '🥙 Dükkanı Aç (Siftah Yap)' : 'Yetersiz Para (₺ ' + s.capital_required.toLocaleString("tr-TR") + ' gerekli)'}
                    </button>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="closeModal('genericModal')">Vazgeç</button>
    `;
    openDialogModal("genericModal");
}

async function startTraditionalShop(shopId) {
    const res = await performActivity("shop_action", { action_id: "start_shop", shop_id: shopId });
    if (res && res.success) {
        closeModal("genericModal");
    }
}

async function performShopAction(actionId, params = {}) {
    await performActivity("shop_action", { action_id: actionId, ...params });
}

// ==========================================
// 2. KOĞUŞ HAYATI & CEZAEVİ HİYERARŞİSİ MODALI
// ==========================================

function openPrisonModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "⛓️ Koğuş Hayatı & Cezaevi Hiyerarşisi";
    const body = document.getElementById("genericModalBody");

    if (!gameState.is_in_prison) {
        body.innerHTML = `
            <div class="panel-card">
                <h4>🏛️ Şu Anda Özgürsün</h4>
                <p class="card-desc" style="margin: 8px 0;">Koğuş hiyerarşisi, karaborsa sigara ticareti ve ağalık mücadeleleri yalnızca cezaevinde hükümlüyken aktifleşir.</p>
                <div style="display:flex; gap:6px; margin-top:10px;">
                    <button type="button" class="btn-primary" style="flex:1;" onclick="openCrimeModal()">🦹 Suç & Yeraltı Masasına Git</button>
                    <button type="button" class="btn-secondary" style="flex:1;" onclick="closeModal('genericModal')">Kapat</button>
                </div>
            </div>
        `;
        openDialogModal("genericModal");
        return;
    }

    const role = gameState.prison_role || "Çaylak";
    const rep = gameState.prison_reputation || 10;
    const cigs = gameState.prison_contraband_cigarettes || 0;
    const yearsLeft = gameState.prison_years_left || 1;

    body.innerHTML = `
        <div class="panel-card" style="border-color:#ef4444; background:linear-gradient(135deg, rgba(239,68,68,0.15), rgba(15,23,42,0.6)); margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title" style="font-size:1.1rem;">🏢 Koğuş Rütben: <b>${role}</b></span>
                <span class="card-badge badge-red">⏳ ${yearsLeft} Yıl Ceza</span>
            </div>
            <div class="person-chip-row" style="margin:8px 0 4px;">
                <span class="person-chip" style="color:#fbbf24;">⭐ Koğuş Saygınlığı: %${rep}</span>
                <span class="person-chip" style="color:#60a5fa;">🚬 Kaçak Tütün/Sigara: ${cigs} Paket</span>
            </div>
            <p class="card-desc" style="margin-top:6px; color:#cbd5e1;">Koğuşta sözünün geçmesi ve ezilmemek için saygınlığını yükseltmeli, semaverin başına geçip raconunu kesmelisin.</p>
        </div>

        <div class="person-action-group-title" style="margin-bottom:8px;">Koğuş Eylemleri & Racon:</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <button type="button" class="btn-choice" onclick="performPrisonDeepAction('challenge_warden_boss')">
                👑 <b>Ağaya Meydan Oku / Racon Kes</b>
                <span style="font-size:0.75rem; color:#94a3b8; display:block; margin-top:2px;">Koğuş ağalığına oyna! Başarırsan mutlak lider olursun ve haracı sen toplarsın.</span>
            </button>
            <button type="button" class="btn-choice" onclick="performPrisonDeepAction('trade_contraband')">
                🚬 <b>Kantin & Karaborsa Sigara Ticareti</b>
                <span style="font-size:0.75rem; color:#94a3b8; display:block; margin-top:2px;">Kantin fişleriyle çay ve kaçak tütün toplayıp koğuşa dağıt, saygınlık ve sigara kazan.</span>
            </button>
            <button type="button" class="btn-choice" onclick="performPrisonDeepAction('yard_walk_allies')">
                🚶‍♂️ <b>Avluda Volta At & Tespih Sallayarak Dertleş</b>
                <span style="font-size:0.75rem; color:#94a3b8; display:block; margin-top:2px;">Temiz hava al, volta arkadaşı edin, stresini boşalt (-30 Stres).</span>
            </button>
            <button type="button" class="btn-choice" onclick="performPrisonDeepAction('petition_amnesty_appeal')">
                📜 <b>Yargı Paketi / İnfaz İndirimi Başvurusu</b>
                <span style="font-size:0.75rem; color:#94a3b8; display:block; margin-top:2px;">Adalet Bakanlığı yeni yargı paketine ve denetimli serbestliğe itiraz dilekçesi ver.</span>
            </button>
            <button type="button" class="btn-choice" style="border-color:#ef4444; color:#fca5a5;" onclick="performPrisonDeepAction('escape_laundry_tunnel')">
                🕳️ <b>Çamaşırhane Sepeti & Tünel Firarı</b>
                <span style="font-size:0.75rem; color:#94a3b8; display:block; margin-top:2px;">Yüksek riskli firar planı! Yakalanırsan cezan katlanır, başarırsan firarisin!</span>
            </button>
        </div>

        <div style="display:flex; gap:6px; margin-top:12px;">
            <button type="button" class="btn-action-outline" style="flex:1;" onclick="performActivity('prison_act', { activity: 'yard_workout' })">🏋️ Şınav & Barfiks</button>
            <button type="button" class="btn-action-outline" style="flex:1;" onclick="performActivity('prison_act', { activity: 'library' })">📖 Ceza Kanunu Oku</button>
        </div>
        <button type="button" class="btn-secondary" style="margin-top:10px; width:100%;" onclick="closeModal('genericModal')">Kapat</button>
    `;
    openDialogModal("genericModal");
}

async function performPrisonDeepAction(actionId, params = {}) {
    const res = await performActivity("prison_deep_action", { action_id: actionId, ...params });
    if (gameState.is_in_prison) {
        openPrisonModal();
    } else {
        closeModal("genericModal");
    }
}

// ==========================================
// 3. ALTERNATİF TIP & TERMAL KAPLICA MODALI
// ==========================================

function openAlternativeMedicineModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "♨️ Alternatif Tıp & Termal Şifa Kürleri";
    const body = document.getElementById("genericModalBody");

    const meds = (marketData && marketData.alternative_medicines) || [];
    const chronic = gameState.chronic_conditions || [];

    body.innerHTML = `
        ${chronic.length > 0 ? `
            <div class="panel-card" style="border-color:var(--accent-red); margin-bottom:12px;">
                <div class="card-title-row">
                    <span class="card-title">⚠️ Teşhis Konulan Kronik Rahatsızlıklar</span>
                    <span class="card-badge badge-red">${chronic.length} Rahatsızlık</span>
                </div>
                <div style="margin-top:6px; display:flex; flex-wrap:wrap; gap:6px;">
                    ${chronic.map(c => `<span class="person-chip" style="color:#fca5a5;">⚡ ${c}</span>`).join("")}
                </div>
                <p class="card-desc" style="margin-top:6px;">Kaplıca kürleri ve geleneksel şifa seansları ağrıları dindirir, stresini sıfırlar ve sağlığına can katar.</p>
            </div>
        ` : ''}

        <p class="card-desc" style="margin-bottom:12px;">Doğal termal sular, asırlık hacamat ve sülük terapileri ile nazar arınma ritüelleri:</p>
        <div style="display:flex; flex-direction:column; gap:10px;">
            ${meds.map(m => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${m.name}</span>
                        <span class="card-badge badge-yellow">₺ ${m.cost.toLocaleString("tr-TR")}</span>
                    </div>
                    <p class="card-desc" style="margin:6px 0;">${m.desc}</p>
                    <div class="person-chip-row" style="margin-bottom:8px;">
                        <span class="person-chip" style="color:#6ee7b7;">💚 Sağlık: +${m.health_gain}</span>
                        <span class="person-chip" style="color:#60a5fa;">🧘 Stres Azalması: -${m.stress_reduction}</span>
                    </div>
                    <button type="button" class="btn-primary" style="width:100%;" onclick="performHealthAgingAction('alternative_medicine', { treatment_id: '${m.id}' })" ${gameState.money < m.cost ? 'disabled style="opacity:0.5;"' : ''}>
                        ${gameState.money >= m.cost ? 'Şifa Seansına Başla ♨️' : 'Yetersiz Para (₺ ' + m.cost.toLocaleString("tr-TR") + ' gerekli)'}
                    </button>
                </div>
            `).join("")}
        </div>
        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="closeModal('genericModal')">Kapat</button>
    `;
    openDialogModal("genericModal");
}

// ==========================================
// 4. HUZUREVİ & YAŞLILIK BAKIMI MODALI
// ==========================================

function openElderlyCareModal() {
    sound.playClick();
    document.getElementById("genericModalTitle").textContent = "🏡 Huzurevi & Yaşlı Bakım Hizmetleri";
    const body = document.getElementById("genericModalBody");

    const homes = (marketData && marketData.nursing_homes) || [];
    const age = gameState.age;
    const isEnrolled = !!gameState.nursing_home;
    const hasCaregiver = !!gameState.elderly_caregiver;

    body.innerHTML = `
        <div class="panel-card" style="margin-bottom:12px;">
            <div class="card-title-row">
                <span class="card-title">👵 Yaşlılık Durum Özeti</span>
                <span class="card-badge ${age >= 60 ? 'badge-blue' : 'badge-yellow'}">${age} Yaşındasın</span>
            </div>
            <p class="card-desc" style="margin-top:6px;">
                ${isEnrolled ? `Şu an <b>${gameState.nursing_home}</b> bünyesinde kalıyorsun. Yemek ve sağlık takibin yapılıyor.` : 'Şu anda kendi evinde yaşıyorsun.'}
                <br>
                ${hasCaregiver ? '👩‍⚕️ <b>Yatılı hasta bakıcın</b> evde 7/24 yanında ve ilaçlarını aksatmıyor.' : 'Evde özel hasta bakıcın bulunmuyor.'}
            </p>
            ${isEnrolled ? `
                <button type="button" class="btn-action-outline" style="border-color:var(--accent-red); color:var(--accent-red); margin-top:8px; width:100%;" onclick="performHealthAgingAction('leave_nursing_home')">
                    🏡 Huzurevinden Ayrıl / Kendi Evine Geri Dön
                </button>
            ` : ''}
        </div>

        <div class="person-action-group-title" style="margin-bottom:8px;">Huzurevi Seçenekleri (60+ Yaş):</div>
        <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:16px;">
            ${homes.map(h => `
                <div class="panel-card">
                    <div class="card-title-row">
                        <span class="card-title">${h.name}</span>
                        <span class="card-badge badge-green">Yıllık ₺ ${h.cost_annual.toLocaleString("tr-TR")}</span>
                    </div>
                    <p class="card-desc" style="margin:6px 0;">${h.desc}</p>
                    <div class="person-chip-row" style="margin-bottom:8px;">
                        <span class="person-chip" style="color:#a78bfa;">⭐ Konfor Puanı: %${h.comfort}</span>
                    </div>
                    <button type="button" class="btn-primary" style="width:100%;" onclick="performHealthAgingAction('enroll_nursing_home', { home_id: '${h.id}' })" ${(age < 60 || gameState.nursing_home === h.name || gameState.money < h.cost_annual) ? 'disabled style="opacity:0.5;"' : ''}>
                        ${age < 60 ? '60 Yaşından Küçükler Başvuramaz' : (gameState.nursing_home === h.name ? 'Şu An Bu Huzurevindesin' : (gameState.money >= h.cost_annual ? 'Huzurevine Yerleş 🏡' : 'Yetersiz Para'))}
                    </button>
                </div>
            `).join("")}
        </div>

        <div class="person-action-group-title" style="margin-bottom:8px;">Eve Yatılı Hasta Bakıcı (65+ Yaş):</div>
        <div class="panel-card">
            <div class="card-title-row">
                <span class="card-title">👩‍⚕️ Yatılı Profesyonel Refakatçi & Bakıcı</span>
                <span class="card-badge badge-purple">Depozito: ₺ 45.000 / Yıl: ₺ 60.000</span>
            </div>
            <p class="card-desc" style="margin:6px 0;">Tansiyon, şeker, fıtık ve ilaç takiplerini aksatmaz; sıcak çorba pişirir, sağlığını güvenceye alır.</p>
            ${hasCaregiver ? `
                <button type="button" class="btn-action-outline" style="border-color:var(--accent-red); color:var(--accent-red); width:100%; margin-top:6px;" onclick="performHealthAgingAction('fire_elderly_caregiver')">
                    👩‍⚕️ Bakıcı ile Yolları Ayır
                </button>
            ` : `
                <button type="button" class="btn-primary" style="width:100%; margin-top:6px;" onclick="performHealthAgingAction('hire_elderly_caregiver')" ${(age < 65 || gameState.money < 45000) ? 'disabled style="opacity:0.5;"' : ''}>
                    ${age < 65 ? '65 Yaşından Küçükler Yararlanamaz' : (gameState.money >= 45000 ? 'Yatılı Hasta Bakıcı Tut (₺ 45.000)' : 'Yetersiz Para')}
                </button>
            `}
        </div>

        <button type="button" class="btn-secondary" style="margin-top:12px; width:100%;" onclick="closeModal('genericModal')">Kapat</button>
    `;
    openDialogModal("genericModal");
}

async function performHealthAgingAction(actionId, params = {}) {
    await performActivity("health_aging_action", { action_id: actionId, ...params });
    if (document.getElementById("genericModal") && document.getElementById("genericModal").classList.contains("modal-open")) {
        if (actionId.includes("nursing") || actionId.includes("caregiver")) {
            openElderlyCareModal();
        } else if (actionId.includes("alternative")) {
            openAlternativeMedicineModal();
        }
    }
}
