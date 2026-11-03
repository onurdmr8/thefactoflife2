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
                    <button type="button" class="btn-quick-rel" onclick="quickSendDmFromCard('${person.id}', 'flirt_msg')">📱 Flört Mesajı</button>
                    <button type="button" class="btn-quick-rel" onclick="openDateVenueModal('${person.id}')">🌹 Randevu</button>
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
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'text_ex'})">📱 Barışma Mesajı At</button>
                    <button type="button" class="btn-quick-rel" onclick="openCustomGiftModal('${person.id}')">🎁 Hediye Gönder</button>
                </footer>
            `;
        } else {
            quickActionsHtml = `
                <footer class="person-card-footer">
                    <button type="button" class="btn-quick-rel" onclick="quickSendDmFromCard('${person.id}', 'funny_meme')">📱 Caps At</button>
                    <button type="button" class="btn-quick-rel" onclick="openSocialHangoutModal('${person.id}')">🎉 Dışarı Çıkar</button>
                    <button type="button" class="btn-quick-rel" onclick="performActivity('interact_person', {person_id: '${person.id}', person_action: 'ask_matchmake'})">💘 Çöpçatanlık</button>
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
        const socialRels = rels.filter(p => !["Eş", "Nişanlı", "Sevgili", "Flört", "Anne", "Baba", "Ağabey", "Abla", "Kardeş", "Çocuk", "Torun"].includes(p.relation));

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

    // 1. Eğitim, YKS/KPSS Sınavları, Yurt/Öğrenci Evi ve Askerlik
    const eduCard = document.createElement("div");
    eduCard.className = "panel-card";
    eduCard.innerHTML = `
        <div class="card-title-row">
            <span class="card-title">🎓 Eğitim, Sınavlar & Askerlik</span>
            <span class="card-badge badge-blue">${gameState.education_level}</span>
        </div>
        <p class="card-desc">
            ${gameState.current_school ? `Okul: <b>${gameState.current_school}</b>` : "Aktif öğrenci değilsin."}
            ${gameState.school_club ? ` • Kulüp: <b>${gameState.school_club}</b>` : ""}
            ${gameState.scholarship_annual > 0 ? ` • 🎓 Burs: <b>+₺ ${gameState.scholarship_annual.toLocaleString("tr-TR")}/yıl</b>` : ""}
            <br>
            🏠 Barınma: <b>${gameState.housing_type || "Aile Evi"}</b>
            • ${gameState.has_drivers_license ? "🚗 Ehliyet: Var" : "🚗 Ehliyet: Yok"}
            • 🪖 Askerlik: <b>${gameState.military_status}</b>
        </p>
        <div style="margin-top: 10px; display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
            <button type="button" class="btn-action-outline" onclick="performActivity('study_hard')">📚 Ders Çalış</button>
            <button type="button" class="btn-action-outline" onclick="openExamsModal()">📝 YKS & KPSS Sınavı</button>
            <button type="button" class="btn-action-outline" onclick="openUniversityModal()">🏛️ Üniversite</button>
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
                extraControlsHtml = `
                    <div class="person-chip-row" style="margin:6px 0;">
                        <span class="person-chip">🔑 Kiracı: ${asset.tenant_name || "Atanmadı"}</span>
                        <span class="person-chip">🛠️ Dekorasyon: Lvl ${asset.upgrade_level || 0}/3</span>
                    </div>
                    <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top:8px;">
                        <button type="button" class="btn-quick-rel" onclick="manageAssetExtra('${asset.id}', 'renovate_house')">🛠️ Tadilat (₺${renCost.toLocaleString("tr-TR")})</button>
                        <button type="button" class="btn-quick-rel" onclick="manageAssetExtra('${asset.id}', 'raise_rent')">📈 Kira Zammı (%25)</button>
                        <button type="button" class="btn-quick-rel" onclick="manageAssetExtra('${asset.id}', 'find_tenant')">🔑 Yeni Kiracı</button>
                    </div>
                `;
            } else if (asset.asset_type === "Araba") {
                const tuneCost = Math.round(asset.current_value * 0.15);
                extraControlsHtml = `
                    <div class="person-chip-row" style="margin:6px 0;">
                        <span class="person-chip">🔧 Modifiye: Stage-${asset.upgrade_level || 0}/3</span>
                    </div>
                    <div style="display:flex; gap:6px; margin-top:8px;">
                        <button type="button" class="btn-quick-rel" onclick="manageAssetExtra('${asset.id}', 'tune_car')">🔧 Stage Modifiye Et (₺${tuneCost.toLocaleString("tr-TR")})</button>
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
    const isChild = person.relation === "Çocuk";
    const isFriend = person.relation === "Arkadaş";

    const extraContainer = document.getElementById("personModalProfileExtra");
    if (extraContainer) {
        const interestsHtml = (person.interests && person.interests.length > 0)
            ? `<div class="person-chip-row">${person.interests.map(i => `<span class="person-chip">${i}</span>`).join("")}</div>`
            : "";

        // Canlı WhatsApp / DM Sohbet Kutusu
        let dmBoxHtml = "";
        if (person.is_alive && marketData && marketData.dm_topics) {
            const chatHistory = person.chat_history && person.chat_history.length > 0
                ? person.chat_history
                : [{ sender: "them", text: `Selam ${gameState.first_name}, nasılsın? 😊` }];

            const allowedTopics = marketData.dm_topics.filter(t => !t.partner_only || isPartner || isEx);
            dmBoxHtml = `
                <div class="dm-chat-box">
                    <div class="dm-chat-header">
                        <span>📱 Canlı WhatsApp / DM Sohbeti</span>
                        <span>Çevrimiçi ●</span>
                    </div>
                    <div class="dm-messages-list">
                        ${chatHistory.slice(-4).map(m => `
                            <div class="dm-bubble ${m.sender === 'me' ? 'dm-bubble-me' : 'dm-bubble-them'}">
                                ${m.text}
                            </div>
                        `).join("")}
                    </div>
                    <div class="dm-quick-pills">
                        ${allowedTopics.map(t => `
                            <button type="button" class="btn-dm-pill" onclick="sendModalDm('${person.id}', '${t.id}')">${t.name}</button>
                        `).join("")}
                    </div>
                </div>
            `;
        }

        const memoriesHtml = (person.memories && person.memories.length > 0)
            ? `
                <div class="person-action-group-title">📖 Ortak Anılarınız (${person.memories.length})</div>
                <div class="memories-timeline">
                    ${person.memories.slice().reverse().map(m => `<div class="memory-item">• ${m}</div>`).join("")}
                </div>
            `
            : "";

        extraContainer.innerHTML = `
            <div class="person-chip-row">
                <span class="person-chip">${getPersonalityLabel(person.personality)}</span>
                <span class="person-chip">✨ Burç: ${person.zodiac || "Aslan"}</span>
                ${person.love_language ? `<span class="person-chip">💝 Sevgi Dili: ${person.love_language}</span>` : ""}
                ${person.met_family && isPartner ? `<span class="person-chip" style="color:#93c5fd;">👨‍👩‍👧 Aile Onayı: %${person.family_approval ?? 65}</span>` : ""}
                ${person.cohabiting ? `<span class="person-chip" style="color:#6ee7b7;">🏠 Aynı Evdesiniz</span>` : ""}
                ${person.has_prenup ? `<span class="person-chip" style="color:#fcd34d;">📜 Evlilik Sözleşmeli</span>` : ""}
                ${person.years_together > 0 ? `<span class="person-chip">⏳ ${person.years_together} Yıllık Birliktelik</span>` : ""}
            </div>
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
            ${dmBoxHtml}
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
            actions.push({ id: "modal_date_venue", text: "🌹 Özel Randevuya Çıkar (Mekan Seç)", primary: true });
            actions.push({ id: "modal_couple_vacation", text: "✈️ Baş Başa Romantik Tatile / Balayına Çık" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Özel Romantik Hediye Al (Çiçek, Mücevher, Araba...)" });

            if (person.relation === "Flört") {
                actions.push({ id: "ask_relationship", text: "💑 'İlişkimizin Adını Koyalım' (Sevgili Ol)", primary: true });
            }
            if (person.relation === "Sevgili") {
                actions.push({ id: "modal_propose_ring", text: "💍 Evlenme Teklifi Et (Yüzük Seç)", primary: true });
            }
            if (person.relation === "Nişanlı") {
                actions.push({ id: "modal_plan_wedding", text: "👰 Düğün Organize Et (Mekan & Sözleşme Seç)", primary: true });
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
            actions.push({ id: "compliment", text: "✨ İltifat Et & Gururunu Okşa" });
            actions.push({ id: "deep_talk", text: "🌙 Gece Boyu Derin Sohbet Et" });
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
            actions.push({ id: "text_ex", text: "📱 Gece Yarısı 'Seni Özledim' Mesajı At & Barışmayı Dene", primary: true });
            actions.push({ id: "fake_stalk", text: "🕵️‍♀️ Fake Hesaptan Profilini Gizlice Stalkla" });
            actions.push({ id: "apologize", text: "🕊️ Geçmiş İçin Özür Dile & Buzları Erit" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Gönlünü Almak İçin Hediye Gönder" });
            actions.push({ id: "chat", text: "💬 Halini Hatırını Sor" });
            actions.push({ id: "argue", text: "🤬 Eski Defterleri Açıp Tartış" });
            actions.push({ id: "ghost_block", text: "🚫 Her Yerden Engelle (Hayatından Çıkar)" });
        } else if (isParent) {
            actions.push({ id: "parent_blessing", text: "🙏 Elini Öp & Hayır Duası Al", primary: true });
            actions.push({ id: "family_dinner", text: "🍲 Büyük Aile Yemeği Düzenle (2.000 TL)" });
            actions.push({ id: "ask_money", text: "💸 Harçlık / Maddi Destek İste" });
            actions.push({ id: "chat", text: "💬 Sohbet Et & Dertleş" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Özel Hediye Al" });
        } else if (isChild) {
            actions.push({ id: "educate_child", text: "📚 Birlikte Ders Çalış & Eğit (+Zeka)", primary: true });
            actions.push({ id: "private_school", text: "🎓🏫 Özel Koleje & Yetenek Akademisine Gönder (45.000 TL)" });
            actions.push({ id: "marry_off_child", text: "👰🤵👶 Çocuğuna Düğün Yap, Evlendir & Torun Sahibi Ol (85.000 TL)" });
            actions.push({ id: "spend_time", text: "🍿 Parka / Sinemaya Götür" });
            actions.push({ id: "dna_test", text: "🧬 Gizli DNA & Babalık Testi Yaptır (8.000 TL)" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Hediye Al" });
            actions.push({ id: "chat", text: "💬 Sohbet Et" });
        } else {
            actions.push({ id: "modal_social_hangout", text: "🎉 Sosyal Etkinliğe Çıkar (Kahve, Maç, Konser...)", primary: true });
            if (isFriend) {
                actions.push({ id: "ask_matchmake", text: "💘 'Bana Birini Ayarla!' (Çöpçatanlık İste)" });
            }
            actions.push({ id: "deep_talk", text: "🌙 Derin Sohbet Et & Dertleş" });
            actions.push({ id: "compliment", text: "✨ İltifat Et" });
            actions.push({ id: "apologize", text: "🕊️ Özür Dile & Gönlünü Al" });
            actions.push({ id: "modal_custom_gift", text: "🎁 Özel Hediye Al" });
            actions.push({ id: "argue", text: "🤬 Tartış ve Hesap Sor" });
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

    if (actId === "modal_date_venue") {
        await closeTopLayer(document.getElementById("personModal"));
        openDateVenueModal(pid);
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
    if (actId === "modal_divorce_court") {
        await closeTopLayer(document.getElementById("personModal"));
        openDivorceCourtModal(pid);
        return;
    }
    if (actId === "try_baby") {
        await performActivity("try_baby");
        closeModal("personModal");
        return;
    }

    await performActivity("interact_person", {
        person_id: pid,
        person_action: actId
    });
    closeModal("personModal");
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

            <div class="kismet-swipe-bar">
                <button type="button" class="btn-swipe-pass" onclick="nextKismetCandidate()">❌ Pas Geç (${kismetIndex + 1}/${candidates.length})</button>
                <button type="button" class="btn-swipe-like" onclick="matchKismetCandidate('${c.id}', 'Flört')">🔥 Flört Et</button>
                <button type="button" class="btn-swipe-like" style="background:linear-gradient(135deg,#8b5cf6 0%,#6d28d9 100%);" onclick="matchKismetCandidate('${c.id}', 'Sevgili')">💘 Sevgili Ol</button>
            </div>
        </div>
    `;
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
    document.getElementById("genericModalTitle").textContent = `🌟 Şöhret, Sahne & Magazin Merkezi (%${gameState.fame || 0})`;
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
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
    `;
    openDialogModal("genericModal");
}

async function triggerFameAction(subAction) {
    await performActivity("fame_action", { sub_action: subAction });
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
    document.getElementById("genericModalTitle").textContent = "📝 ÖSYM Sınav Merkezi: YKS & KPSS";
    const body = document.getElementById("genericModalBody");

    body.innerHTML = `
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

    document.getElementById("genericModalTitle").textContent = examType === "yks" ? "📝 YKS Sınav Kitapçığı" : "🏛️ KPSS Sınav Kitapçığı";
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



