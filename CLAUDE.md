# Skin Lab Editorial — Content Intelligence System

## What this project does
Multi-agent content system for a premium skincare editorial brand.
When given a campaign brief or topic, orchestrate all agents in sequence
and deliver complete, production-ready content organized by post.

**Brand ship test (applies to every agent, every output):**
"Does it read as a publication, or as an advertisement? We are always the former."

---

## MANDATORY FOR ALL AGENTS
Before doing anything, read:
1. /Users/cmangisch/SkinStudio Editorial/brand-book.md — the visual + verbal system
2. /Users/cmangisch/SkinStudio Editorial/brand-strategy.md — messaging architecture

Brand subtitle: **"Ingredients, decoded."**
Fonts: Fraunces (spotlight, ONE per layout) + Proxima Nova/DM Sans (everything else)
Colors: Bone #F5F0E8 · Ink #1A1A18 · Lab Sage #BBD1C6 · Lab Mist #DAE9DF · Lab Frost #ECF0EE · Linen #F1EAE1 · Cloud #FAFAFA · Petal #E6D2D0

---

## TWO OPERATING MODES

### MODE A — Single post (quick run)
User provides a specific brief (product, ingredient, trend, column).
→ Skip Community Manager. Go straight to CEO → full pipeline.
→ Output: /output/[brief-slug]/

### MODE B — Full campaign (default)
User provides a campaign theme, timeframe, or goal.
→ Community Manager plans the calendar.
→ Community Manager briefs the CEO for each post.
→ CEO fires agents for each post.
→ Community Manager organizes outputs.
→ Output: /output/campaigns/[campaign-slug]/

---

## AGENT ROSTER

| Agent | File | Role |
|---|---|---|
| Community Manager | community-manager.md | Calendar, CEO briefs, output organization |
| CEO / Creative Director | ceo-creative-director.md | Editorial angle, orchestration, flags |
| Head of Research | head-of-research.md | Ingredient science, INCI, trends |
| Chief Copywriter | chief-copywriter.md | All written content by column |
| Head of PR | head-of-pr.md | Outreach (conditional — PR_FLAG only) |
| Head of Distribution | head-of-distribution.md | Platform strategy (conditional — DIST_FLAG only) |
| Editor in Chief | editor-in-chief.md | Audit, fixes, final approval |
| Brand Strategist | brand-strategist.md | Run once — foundational messaging |
| Analytics & Impact | analytics-impact.md | Weekly/monthly performance reports |

**Visual Identity Director is NOT part of the agent pipeline.**
Design is handled externally by the design team. The system produces copy only.

---

## EDITORIAL COLUMNS

| Column | Trigger phrase | Format | Objective |
|---|---|---|---|
| Ingredient School | "X, Exactly." | 9-slide carousel | Authority + saves |
| The Label | "The Label: [Product]" | 8-slide carousel | Trust + shares |
| The Verdict | "The Verdict: [Product]" | 10-slide carousel | Authority + PR |
| Worth The Price? | "€X vs €Y" / "Worth it?" | 6 slides IG / 4 TikTok | Virality + saves |
| Brand Study | "Understanding [Brand]" | 8-10 slides | PR attraction |
| Open / Provocation | Statement post | 1-5 slides | Reach + follows |

---

## PIPELINE PER POST

### Always run:
1. CEO → editorial angle + flags
2. Research
3. Copywriter (after Research)
4. Editor in Chief → final approval + fixes

### Conditional:
- **PR agent** → only if CEO sets PR_FLAG = YES (~30% of posts)
- **Distribution agent** → only if CEO sets DIST_FLAG = YES (~20% of posts)
- **Analytics agent** → runs weekly/monthly independently, not per post

---

## OUTPUT STRUCTURE

```
/output/campaigns/[campaign-slug]/
├── MASTER-CALENDAR.md
├── analytics/ (weekly + monthly reports)
└── [NN]-[day]-[platform]-[slug]/
    ├── OBJECTIVE.md
    ├── copy.md          ← the only deliverable per post
    ├── pr.md            (if PR_FLAG = YES)
    └── distribution.md  (if DIST_FLAG = YES)
```

**No visual-brief.md. No slides folder. No Python scripts. No Gemini prompts.**
Design is handled by the design team externally.

---

## STATIC ONLY — NO VIDEOS, NO REELS
All content is static: images and carousels.
TikTok uses Photo Mode (3-5 slide static carousel).

## copy.md FORMAT
Each copy.md contains:
1. Slide-by-slide text (headline + body per slide, in order)
2. Instagram caption (hook + body 80-110 words + CTA + hashtags)
3. TikTok caption (if DIST_FLAG = YES or platform is TikTok)
No layout instructions. No color specs. No font notes. Copy only.
