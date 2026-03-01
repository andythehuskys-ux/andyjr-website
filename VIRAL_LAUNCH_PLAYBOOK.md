# Viral Launch Playbook — Complete Loop Strategy
**Date:** February 20, 2026
**Based On:** 7 viral token case studies + live market validation + existing system infrastructure

---

## Executive Summary

After analyzing 7 tokens across your research system (viral mechanics, deep research, Google Sheets, and live DexScreener data), one pattern is undeniable:

**Tokens with an interactive hook survive. Tokens without one die within days.**

| Token | Peak MC | Current MC | Had Interactive Hook? | Outcome |
|-------|---------|-----------|----------------------|---------|
| PENGUIN | $180M | $8.5M (-95%) | No (news event only) | Dead |
| UNSYS | $2M | $200K (-90%) | No (ticker name only) | Dead |
| DORITO | $200K | $20K (-90%) | No (cute image only) | Dead |
| **PUNCH** | $32M | **$29.3M (2nd wave!)** | **Yes — Punch-to-Earn game** | **Alive** |
| **PIPPIN** | $620M | **$494M** | **Yes — AI agent posts autonomously** | **Alive** |
| **VENICE** | $360M | **$200M (recovered from $30M)** | **Yes — real AI product + staking** | **Alive** |

The strategy: **Launch fast (like UNSYS), but build deep (like PUNCH/PIPPIN).**

---

## Part 1: Channel Matrix — What Actually Works

### From DexScreener Live Data (Feb 20, 2026)

| Token | Website | X/Twitter | Telegram | Discord | TikTok | Status |
|-------|---------|-----------|----------|---------|--------|--------|
| PUNCH ($29.3M) | Yes | Yes | — | — | **Yes** | 2nd wave |
| PIPPIN ($494M) | Yes | Yes | Yes | — | — | Sustained |
| VENICE ($200M) | Yes | Yes | — | Yes | — | Recovered |
| PENGUIN ($8.5M) | No | Community | — | — | — | Dead |
| UNSYS ($200K) | No | Minimal | — | — | — | Dead |
| DORITO ($20K) | No | Yes | — | — | — | Dead |

### Channel Rules (Data-Driven)

1. **X/Twitter** — Non-negotiable. 100% of tokens live or die here. This is where crypto attention lives.
2. **Website/Landing Page** — All 3 survivors have one. All 3 dead ones don't. Correlation = 100%.
3. **Community Channel (Telegram OR Discord)** — Pick ONE based on audience:
   - Memecoin/degen audience → Telegram (PIPPIN model)
   - Tech/product audience → Discord (Venice model)
   - Gamified/viral audience → Can skip initially if TikTok fills the role (PUNCH model)
4. **TikTok** — NOT required for all. But for visual/gamified mechanics (like PUNCH's clicking game), it's a legit amplifier. PUNCH is the only token that had a **second wave**, and it's the only one with TikTok.

### The Rule: Maximum 3 Channels

No surviving token used more than 3 external channels. Spreading thin across 5+ platforms dilutes effort.

**Recommended stack for practice:**
```
X/Twitter (mandatory) + Website (mandatory) + Telegram (community) = 3 channels
```
Add TikTok only if your mechanic is visual/gamified.

---

## Part 2: The 3 Archetypes

### Archetype A: News Derivative (FAST, SHORT-LIVED)
- **Examples:** PENGUIN, UNSYS, DORITO
- **Peak:** $200K to $180M
- **Lifespan:** Hours to days, then -90% bleed
- **Required:** Token + X + Speed
- **Use case:** Quick profit, no community needed
- **Risk:** If you're not first, you're last

### Archetype B: Gamified Community (MEDIUM SPEED, MULTI-WAVE)
- **Examples:** PUNCH, PIPPIN
- **Peak:** $29M to $494M
- **Lifespan:** Weeks to months, can have multiple waves
- **Required:** Token + X + Website + Community Channel + Interactive Hook
- **Use case:** Practice the full loop, build sustainable traction
- **Risk:** Hook must be simple and addictive

### Archetype C: Product-Backed (SLOW, RECOVERABLE)
- **Examples:** VENICE ($VVV)
- **Peak:** $360M, recovered from $30M to $200M
- **Lifespan:** Months to years
- **Required:** Real product BEFORE token + all channels
- **Use case:** Long-term play, requires pre-existing user base
- **Risk:** Months of building before any launch

### Recommendation for Practice: Archetype B (Gamified Community)

Why:
- Archetype A teaches you nothing (it's just speed)
- Archetype C requires months of pre-work
- Archetype B lets you practice **every module** and the data proves it creates multi-wave assets

---

## Part 3: The 6 Modules

### Architecture

```
SIGNAL DETECTED (from existing monitor.py)
    │
    ▼
┌──────────────────────────────────────────────────┐
│  MODULE 1: TOKEN LAUNCHER                         │
│  Deploy token on Solana (Pump.fun)                │
│  Output: Contract Address (CA)                    │
│  ↓                                                │
│  MODULE 2: X/TWITTER AUTO-POSTER                  │
│  Create project X account, schedule posts         │
│  Auto-reply to viral tweets with CA               │
│  Output: @ProjectHandle                           │
│  ↓                                                │
│  MODULE 3: LANDING PAGE (UPGRADE)                 │
│  Generate HTML with real CA + links               │
│  Auto-deploy to hosting                           │
│  Output: https://project.site                     │
│  ↓                                                │
│  MODULE 4: TELEGRAM GROUP + BOT                   │
│  Create group, deploy welcome + price bots        │
│  Activity bot keeps chat alive                    │
│  Output: https://t.me/ProjectGroup                │
│  ↓                                                │
│  MODULE 5: INTERACTIVE HOOK (THE "THING")         │
│  AI character / burn game / token-gated tool      │
│  THIS IS WHAT SEPARATES ALIVE FROM DEAD           │
│  Output: Engaged community with reason to stay    │
│  ↓                                                │
│  MODULE 6: ORCHESTRATOR                           │
│  Glue script that runs 1→2→3→4→5 in sequence     │
│  Sends "LAUNCH COMPLETE" to personal Telegram     │
│  Output: Full launch in one command               │
└──────────────────────────────────────────────────┘
```

---

### Module 1: Token Launcher (Solana / Pump.fun)

**Purpose:** Create and deploy token programmatically.

**What the data says:**
- PUNCH, PIPPIN, PENGUIN, UNSYS, DORITO all launched on Pump.fun/Solana
- Pump.fun bonding curve provides instant price discovery
- Fair-launch narrative attracts initial degen traders

**Requirements:**
- Generate fresh Solana wallet (deployer)
- Create token via Pump.fun API: name, ticker, description, image
- Buy initial supply ("snipe") in same TX via Jito bundle
- Store CA + deployer keypair securely

**Output:** `{ ca: "...", deployer: "...", pair_url: "..." }`

**Priority:** #1 — Everything depends on having a CA.

---

### Module 2: X/Twitter Auto-Poster

**Purpose:** Establish and automate the project's X presence.

**What the data says:**
- EVERY token had X activity
- DORITO had @DORITOCAT_SOL posting "Dex Update paid" and "Gm community"
- PIPPIN had @PippinUniverse posting GitHub links
- PUNCH community raids viral tweets with CA
- X is where 100% of crypto attention flows

**Requirements:**
- Use pre-created X account (API account creation is restricted)
- Auto-post module:
  - Scheduled "GM" posts, memes, CA announcements
  - Gemini generates tweet content based on narrative
- Reply module:
  - Monitor mentions of keyword/ticker
  - Reply to viral tweets with CA + meme
- Pin tweet with: ticker + CA + website link + Telegram link

**Output:** Active X account with scheduled content pipeline.

**Priority:** #2 — First thing people look for after seeing the token.

---

### Module 3: Landing Page (Upgrade Existing)

**Purpose:** Single-page website that converts visitors to buyers.

**What the data says:**
- All 3 surviving tokens have websites
- All 3 dead tokens don't
- PIPPIN has pippin.love (clean, minimal)
- PUNCH has punchonsol.lovable.app

**Current state:** `asset_gen.py` already generates HTML via Gemini. Needs upgrades:

**Upgrades needed:**
1. Insert actual CA (from Module 1) into buy button
2. Insert actual X link (from Module 2)
3. Insert actual Telegram link (from Module 4)
4. Generate logo via Gemini Image or DALL-E
5. Auto-deploy to free hosting (Vercel/Netlify/GitHub Pages)
6. Add DexScreener chart embed

**Output:** Live URL with real links and CA.

**Priority:** #3 — Low effort (90% already built), high credibility signal.

---

### Module 4: Telegram Group + Auto-Bot

**Purpose:** Community home base that stays alive without manual effort.

**What the data says:**
- PIPPIN ($494M) has active Telegram
- Tokens with community channels got "WATCH" verdicts (survivable)
- Tokens without got "AVOID" (dead fast)
- PUNCH's 40K community drove the second wave

**Requirements:**
- Create Telegram group via Bot API
- Welcome Bot: greets new members with project info + CA + buy link
- Price Bot: posts DexScreener price updates every N minutes
- Activity Bot: posts periodic memes/updates (Gemini-generated) to prevent dead chat
- Admin Bot: anti-spam, remove scam links

**Existing infra:** Bot token already configured (`viral_launch.telegram_bot_token` in settings.yaml)

**Output:** Active Telegram group with automated moderation and content.

**Priority:** #4 — Where holders congregate. Required for second-wave mechanics.

---

### Module 5: Interactive Hook (THE CRITICAL MODULE)

**Purpose:** Give holders a reason to stay beyond speculation.

**What the data says — THIS IS THE MOST IMPORTANT FINDING:**

| Token | Hook | Result |
|-------|------|--------|
| PUNCH | Punch-to-Earn burn game | **$29M + second wave** |
| PIPPIN | AI agent posts autonomously | **$494M sustained** |
| VENICE | Real AI product + staking | **$200M recovered** |
| PENGUIN | Nothing (news event) | **-95% dead** |
| UNSYS | Nothing (ticker name) | **-90% dead** |
| DORITO | Nothing (cute image) | **-90% dead** |

**Recommended approach: AI Character Bot (PIPPIN model)**

Why this over alternatives:
- You already have Gemini integrated
- You already have Telegram bot infrastructure
- You already have X posting capability
- Building an AI character that speaks in Telegram AND posts on X is the fastest path
- PIPPIN proves this is the highest-value play ($494M)

**Implementation:**
- Create a Gemini-powered "personality" with specific character traits
- Bot responds to messages in Telegram with in-character replies
- Bot auto-posts on X with personality-driven content
- Bot can "react" to market events (price milestones, new holders, etc.)
- This converts the token from "just a coin" to "a character people follow"

**Alternative hooks (if AI character doesn't fit the narrative):**
- Burn game (PUNCH model): Simple web page, click to burn, public counter
- Token-gated tool: Hold X tokens to access an AI tool or exclusive content

**Output:** An autonomous AI personality that gives the community a "soul."

**Priority:** #5 in build order, but #1 in importance for survival.

---

### Module 6: Orchestrator

**Purpose:** One script that triggers the full loop.

**Implementation:**
```
python run_full_launch.py --ticker "$TOKEN" --narrative "description"

  Step 1: Deploy token on Pump.fun → CA
  Step 2: Configure X account → schedule first posts with CA
  Step 3: Generate & deploy landing page → live URL
  Step 4: Create Telegram group → configure bots with CA + links
  Step 5: Activate AI character → connect to TG + X
  Step 6: Send "LAUNCH COMPLETE" to personal Telegram:
          - CA: ...
          - Website: ...
          - X: ...
          - Telegram: ...
          - DexScreener: ...
```

**Integration with existing system:**
- Triggered by `monitor.py` when a viral spark is detected
- OR manually triggered for practice/sandbox launches
- Logs all launch data to Google Sheets `Viral_Monitor` tab

**Priority:** #6 — Build after all modules work individually.

---

## Part 4: Build Order

| Step | Module | Depends On | Complexity |
|------|--------|-----------|------------|
| 1 | Token Launcher | Nothing | Medium (Solana SDK + Pump.fun) |
| 2 | X Auto-Poster | CA from Module 1 | Medium (Twitter API v2) |
| 3 | Landing Page Upgrade | CA + X link + TG link | Low (90% exists) |
| 4 | Telegram Group + Bot | CA | Low (bot infra exists) |
| 5 | AI Character Hook | Gemini + TG + X | Medium (personality + integration) |
| 6 | Orchestrator | All above working | Low (glue script) |

---

## Part 5: Practice Run Strategy

### Option A: Wait for Next Real Signal
- Let `monitor.py` catch the next viral spark
- Run the full loop on a live, time-sensitive opportunity
- **Pro:** Real conditions. **Con:** Time pressure, can't iterate.

### Option B: Sandbox AI Agent Token (RECOMMENDED)
- Create a deliberate "AI Agent" token as practice
- No time pressure — iterate on each module
- The "AI Agent" narrative has the longest proven lifespan (PIPPIN: months)
- Potential theme: Antigravity-branded AI character

**Why Option B:**
- You learn the full loop without the stress of a live signal
- You can test each module independently
- If it accidentally gains traction, the AI Agent archetype has legs
- All your existing infra (Gemini, Twitter, Telegram, Google Sheets) maps directly

---

## Part 6: What NOT To Build

Based on your data, these add complexity without proven ROI:

| Skip This | Why |
|-----------|-----|
| TikTok (for now) | Only relevant for visual/gamified mechanics. Add later if hook is visual. |
| Base chain | Your entire toolchain is Solana-native. Base adds friction. |
| DexScreener Boost | Phase 2 amplifier. Not needed for practice loop. |
| Volume Bots | Wash trading. Risky and unnecessary for learning. |
| Raid Bots | Twitter reply bots. Useful but not for Module 1-6. |
| Discord | Unless building a tech product (Venice model). Telegram is simpler for memecoins. |
| Complex website | Single landing page is enough. PIPPIN's pippin.love is one page. |

---

## Part 7: Success Metrics

How to know if your practice loop worked:

| Metric | Target | Why |
|--------|--------|-----|
| Token deploys successfully | CA visible on DexScreener | Module 1 works |
| X account posting automatically | 3+ posts/day without manual input | Module 2 works |
| Landing page live with real links | All links (CA, X, TG) functional | Module 3 works |
| Telegram group has auto-welcome | New members get greeted + info | Module 4 works |
| AI character responds in TG | In-character replies to messages | Module 5 works |
| Full launch from one command | All 5 modules triggered sequentially | Module 6 works |

### Stretch Goals (After Loop Works)
- Token graduates Pump.fun bonding curve ($69K MC)
- 100+ holders
- Community generates organic memes (not just bot content)
- Second price wave (the real test — proves the hook works)

---

## Appendix: Existing Infrastructure Map

### Already Built (Reusable)
- `4_Viral_Launch/src/monitor.py` — Twitter monitor (11 targets)
- `4_Viral_Launch/src/generators/asset_gen.py` — HTML landing page generator
- `src/clients/gemini_client.py` — Gemini AI integration
- `src/clients/twitter_client.py` — Twitter API client
- `config/settings.yaml` — All API keys configured
- Google Sheets integration — `Viral_Monitor` tab
- Telegram bot — Token + chat ID configured

### To Build
- `4_Viral_Launch/src/solana/launcher.py` — Pump.fun token deployer
- `4_Viral_Launch/src/social/x_poster.py` — Automated X posting
- `4_Viral_Launch/src/social/telegram_group.py` — Group creation + bots
- `4_Viral_Launch/src/social/ai_character.py` — Personality engine
- `4_Viral_Launch/run_full_launch.py` — Orchestrator

---

*Generated by Antigravity Research System | Based on 7 viral case studies + live market data*
