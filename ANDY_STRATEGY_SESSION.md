# $ANDY Strategy Session Log
**Date:** Feb 20, 2026 | **Source:** Claude Code session (transferred here due to limit)

---

## Core Finding — What the Data Proves

| Token | Had a Hook? | Peak MC | Now | Verdict |
|-------|-------------|---------|-----|---------|
| PENGUIN | No (news event) | $180M | $8.5M | Dead -95% |
| UNSYS | No (ticker name) | $2M | $200K | Dead -90% |
| DORITO | No (cute image) | $200K | $20K | Dead -90% |
| PUNCH | Yes — burn game | $32M | $29.3M (2nd wave!) | Alive |
| PIPPIN | Yes — AI agent | $620M | $494M | Alive |
| VENICE | Yes — real product | $360M | $200M (recovered) | Alive |

**Rule: Launch fast like UNSYS. But build deep like PUNCH/PIPPIN.**

---

## The 3 Archetypes

**A — News Derivative** (PENGUIN, UNSYS, DORITO)
Launch on a headline. Lives hours to days. -90% inevitable.

**B — Gamified Community** (PUNCH, PIPPIN) ← **This is what we build**
Interactive mechanic keeps people coming back. Multi-wave potential.

**C — Product-Backed** (Venice)
Real product before token. Takes months of pre-work. Future direction.

---

## Channel Rules

| Channel | Rule |
|---------|------|
| X/Twitter | Non-negotiable. 100% of tokens live/die here |
| Website | All 3 survivors have one. All 3 dead ones don't. 100% correlation |
| Telegram | Use for memecoins/degens (PIPPIN model) |
| TikTok | Only if mechanic is visual/gamified |

**Maximum 3 channels.** No survivor used more than 3. Spreading kills momentum.

**For Andy: X + Website + Telegram**

---

## The Project: $ANDY — Talking Husky on Solana

**Concept synthesis:**
- PUNCH = Meme + Game mechanic → $29M, 2nd wave
- PIPPIN = Meme + AI Agent personality → $494M, still alive
- **Andy = Meme + AI Agent** (PIPPIN model — no game needed)

### Why This Works
- Huskies are the internet's most vocal dog breed — they "talk", argue, protest
- Real photos = content no other token can copy
- "Talk to Andy" chat on website IS the interactive hook
- PIPPIN proved: no game needed if the character is strong enough

### Andy's Character Voice
Dramatic. Stubborn. Complains about everything. Has opinions.

**Examples:**
- X post: *"they gave me the same food as yesterday. I sat and stared at them for 14 minutes. Nothing changed. This is not over."*
- Reply to GM: *"it is NOT a good morning. they made me wait 4 minutes for breakfast. 4 MINUTES."*
- To moon question: *"I cannot go to moon. I am watching the squirrel outside. This is more important."*

### Andy's Photos (saved at `4_Viral_Launch/andy/`)
| File | Use |
|------|-----|
| IMG_8129.jpg | **Profile pic** — serious side-eye face, big ears |
| IMG_8128.jpg | **X Banner** — tongue out chaos energy |
| IMG_8106.jpg | **First post** — sleeping with ice cream toy |
| IMG_8109.jpg | **Content** — sleeping photos |
| IMG_8127.MOV | **TikTok/content** — video |

**Decision: Use raw real photos.** Authenticity is the biggest advantage.

---

## Build Order (Pump.fun LAST)

| Step | Module | File | Status |
|------|--------|------|--------|
| 1 | X / Twitter Auto-Poster | `social/x_poster.py` | TODO |
| 2 | Landing Page (upgrade) | `generators/asset_gen.py` | TODO |
| 3 | Telegram Group + Bot | `social/telegram_group.py` | TODO |
| 4 | Andy AI Character | `social/ai_character.py` | TODO |
| 5 | Orchestrator | `run_andy_launch.py` | TODO |
| 6 | **Pump.fun Token Launch** | `solana/launcher.py` | **LAST** |

**Pump.fun is the trigger, not the foundation.** Deploy ONLY when all 5 modules are live.

---

## Andy's X Setup (Plan)

**Bio:**
```
i am andy. i have opinions about everything.
$ANDY on solana 🐺
[website] | [telegram]
```

**Pinned tweet (after CA):**
```
i heard you wanted to talk to a husky.
fine. i will allow it.

CA: [address]
[website] | [telegram]
```

**Content rhythm (handled by x_poster.py):**
- Morning: Andy GM complaint post
- Afternoon: reaction to price/news/random
- Evening: demand or observation
- Replies: respond to every mention in character

---

## What's Already Built vs What To Build

**Already built (reuse):**
- Twitter monitor (`monitor.py`)
- Gemini client (`gemini_client.py`)
- Twitter API client (`twitter_client.py`)
- HTML generator (`asset_gen.py`)
- Telegram bot config (token + chat ID in `settings.yaml`)
- Google Sheets logging

**To build:**
- `social/x_poster.py`
- `social/telegram_group.py`
- `social/ai_character.py`
- `run_andy_launch.py` (orchestrator)
- `solana/launcher.py` (last)

---

## Design References Saved
- https://godly.website/ — website design inspiration
- https://21st.dev/ — UI component references

---

## Checklist Location
Google Sheets → Tab: `Andy_Launch_Checklist`
URL: https://docs.google.com/spreadsheets/d/1xnIbQBVAmP1vpE9Id5lAcTflW0NLcM899oFKBXqqZNE/edit#gid=165181480

---

## Next Step (where session ended)
**Build `social/x_poster.py`** — the X auto-poster.
Prerequisite: Create the X account manually at x.com and get API keys from developer.x.com.

**X Account setup (manual):**
1. Create account at x.com
2. Username: @AndyOnSOL or @AndyHuskySOL or @talkingAndy
3. Profile pic: IMG_8129.jpg
4. Banner: IMG_8128.jpg
5. Bio: `i am andy. i have opinions. $ANDY on solana 🐺`
6. Apply for developer access at developer.x.com (Read+Write)
7. Get: API Key, API Secret, Access Token, Access Token Secret
8. Add all 4 keys to `settings.yaml`
