# Jax Tech social: daily posting playbook

Rudi's rule (24 Nov 2026): ONE post every day on the Jax Tech Facebook Page and Instagram (@jaxtech.co.za), fully automated, no input from him. Informative, genuinely helpful, with a hook that invites engagement every day.

## What the research says (24 Nov 2026)
- Carousels earn the most saves and shares on Instagram: Buffer's 2026 data shows a 6.90% median engagement rate for carousels vs 2.46–3.31% for Reels (smashballoon.com). Saves and DM shares now outweigh likes in ranking.
- Posts that ask a question draw about 37% more comments (eMarketer).
- Educational "answer the question buyers already ask" content earns the saves and shares that drive reach. Original content gets more distribution; reposted content gets cut.
- Facebook decision-makers skew 35–65; B2B on Facebook/Instagram works when it's human and helpful, not formal like LinkedIn.
- Best times (SAST): Facebook weekdays 12:00–20:00 (Sprout Social 2026); Instagram SA around lunchtime 11:00–14:00 and 19:00–21:00. We post at 12:30 every day.
- Competitors: Euphoria Telecom (Cape Town, 6,000+ business customers) leans on buyer's guides, "no long-term contract", local support, copper switch-off and load-shedding readiness, plus Takealot-voucher referrals. Switch Telecom runs flat-rate calling and like-and-share giveaways. Telviva targets Microsoft Teams calling. Gaps we fill: plain-language tips, transparent prices (R59 extension, 33c/min, per-second billing, no contract), softphone on your cellphone, free bill check.

## Daily schedule (Rudi 25 Nov: "busy every day")
- 12:30 carousel post (FB photo + IG carousel) — task 11:47.
- 18:30 Reel of the same day's slides (reel.py, 9:16, Mixkit music) on FB Reels + IG Reels — task 18:13. Reel caption: short new hook + clear-voice line + CTA, not a copy of the lunch caption.

## Format
- 4:5 carousel, 5–7 slides, rendered with render.py (cover with hook → 3–5 points → CTA). Facebook gets the cover image as a photo post with the same caption.
- Hook in the first line of the caption AND on the cover (problem, surprising number, myth, or "are you making this mistake?").
- End every caption with ONE easy question (either/or, yes/no or "tell us your…"). Never "comment YES to…" style bait (Meta demotes engagement bait).
- CTA line: "📲 Free bill check: WhatsApp us or call 021 002 5637 · 🌐 jaxtech.co.za". 4–6 hashtags.

## Key message (Rudi, 24 Nov 2026)
- HAMMER CLEAR VOICE QUALITY: most people expect VoIP to sound choppy/robotic/delayed. Our calls are crystal clear. Work this into hooks, captions and at least 2 posts a week (e.g. myth 'VoIP sounds bad', 'why some VoIP sounds bad and ours doesn't', 'can your clients hear you clearly?'). Never invent quotes; client reviews only once approved and listed in STRATEGY.md.

## Internet add-on (Rudi 25 Nov)
- Every caption (lunch post AND Reel) gets ONE line just above the CTA: "🌐 Need business internet too? Fibre & LTE for your office: send us your address and we'll check what reaches your building." Keep VoIP the main topic.
- Every Reel ends with the 'Need business internet too?' end card (built into reel.py). No internet prices/speeds (none published).

## Content pillars (rotate, never the same pillar two days running)
1. Landline → VoIP: Telkom copper switch-off, keeping your number (porting), what changes.
2. Save money: reading your phone bill, per-second vs per-minute billing, hidden line-rental costs, no-contract.
3. Never miss a call: softphone on cellphone, ring groups, after-hours routing, voicemail to email, missed-call cost.
4. Work from anywhere / resilience: power cuts, home office, internet fails → calls forward to cellphones.
5. Myth vs fact: "VoIP sounds bad", "I need new phones", "it's complicated", etc.
6. Quick wins & how-to: 3-step guides, checklists, glossary ("what is a PBX?").
7. For IT companies (1×/week, Thursday): reseller programme, set your own prices, we handle the platform.
8. Weekend (Sat/Sun): lighter, relatable "office life" or a quiz-style either/or question.

## Rules
- Verified facts only; name the source in the caption when citing a number. No invented stats, testimonials or reviews.
- Never name our suppliers (Herotel, Axxess, Bicom). Never say "small business". Company voice ("we"), no founder selfies.
- Prices: extension R59/month, app user R27/month, calls 33c/min billed per second, no contract. Partner (IT company) rates are not published on social.
- Phone 021 002 5637, WhatsApp via jaxtech.co.za, website jaxtech.co.za. Never post Rudi's cellphone number.
- No politics, no knocking competitors by name, no fear-mongering.

## Lessons log (newest first)
- 2026-11-26 (reel): Local `main` branch in the clone is an old, diverged history; work from a detached checkout of origin/main and push with `git push origin HEAD:main`. Either/or questions must spell out both options ("resell or refer?"), not "A or B" without labels.
- 2026-11-26: Cover sub-line gets hidden behind the photo when the title wraps to 4 lines; keep cover titles to ~3 lines (about 35 characters) and check slide 1 first.
- 2026-11-26 (analytics): FB Telkom copper-switch-off carousel (24 Nov) reached 20 vs 13 for the "VoIP sounds robotic" carousel and 2 for the same-topic Reel posted 6h later. Urgent, SA-news hooks ("your number is on borrowed time") beat myth-busting. Lead with a deadline/local-news angle where possible.
- 2026-11-26 (analytics): Two posts on the same topic the same day split reach (Reel got 2 on FB, 1 on IG). One topic per day; if a Reel and carousel both go out, use different hooks. Zero engagement on every post so far: end captions with a one-tap question (A or B?) instead of open-ended ones.
- 2026-11-25 (reel): git credential service returned 503 for ~10 min; raw.githubusercontent.com still worked for reads, so the Reel was built from raw-downloaded slides/music and pushed once git recovered. Retry git for several minutes before giving up.
- 2026-11-25: Out file names follow the JSON date; renamed the 24 Nov post's early renders to out/2026-11-24-N.jpg so today's slides could use 2026-11-25-N. Raw GitHub URLs served the new files immediately (hashes matched). FB scheduled posts return a photo id, not a post id; log that.
- 2026-11-24: Started. First post (25 Nov) = Telkom copper switch-off carousel.
