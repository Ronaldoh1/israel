# Candidate research schema — 2026 Elections module (Sophia)

Output ONE JSON file per candidate. Today is 2026-10-08. Every fact must carry a citation key in `c` that you
define in the top-level `cites` map as {"t": "Title — Outlet (date)", "u": "https://..."}. Never invent a URL;
only cite pages you actually opened or that appeared in search results. If you can't find something, leave the
field out (or null) — do NOT guess. Paraphrase; quotes in `claim` may be verbatim but under ~25 words.

## Discipline (non-negotiable)
- Documented record only. Personal/biographical details need two independent sources or one primary record.
- Charged ≠ convicted. Use the exact legal status from the court/agency record.
- A spouse's, parent's or relative's record is NOT the candidate's; only include if the record shows joint action.
- A donation is not a vote: never write that money caused a position unless reporting documents that link.
- Same depth for every party. "Searched and found nothing" is a valid finding — record what you searched in `checks`.
- Claims check: use a FIXED sample — the candidate's own claims about their life/career/business (bio claims) plus
  up to 10 of their most-repeated campaign claims (site, ads, debates, speeches). Rate only checkable facts against
  records (primary sources first; AP/PolitiFact/FactCheck.org/WaPo as support). Verdicts: true | partly | misleading |
  false | unverifiable | opinion. Mark `repeated` only if you can cite BOTH the date it was publicly shown false and a
  later date they said it again. Never use the word "lie".
- Money: FEC candidate pages work via WebFetch, e.g. https://www.fec.gov/data/candidate/<ID>/?cycle=2026 and
  https://www.fec.gov/data/committee/<ID>/?cycle=2026 . OpenSecrets pages may also work via WebFetch
  (https://www.opensecrets.org/races/summary?cycle=2026&id=AL07 ; candidate pages /members-of-congress/... or
  /2026-races/...). Record the coverage end date (`thru`). If a breakdown isn't available, omit it — don't estimate.

## JSON shape
{
 "id": "<given id>",
 "cites": {"key": {"t": "...", "u": "..."}},
 "checked": "2026-10-08",
 "photo": {"src": "https://upload.wikimedia.org/...jpg (direct file URL)", "page": "https://commons.wikimedia.org/wiki/File:...", "credit": "Wikimedia Commons / U.S. Congress (public domain)"},
 "links": {"site": "official campaign site URL"},
 "profile": {
   "oneliner": {"t": "one sentence: who they are", "c": ["key"]},
   "born": {"t": "Month D, YYYY, City, State", "c": []}, "hometown": {"t":"...","c":[]}, "residence": "City, ST",
   "upbringing": {"t": "3-6 sentences from the record: family background, early life, how they came up", "c": []},
   "office_years": <number of years in any elected/appointed public office, integer>,
   "education": [{"level": "hs|ged|assoc|bach|grad", "deg": "B.A. Agriculture", "school": "...", "year": "1992", "c": []}],
   "career": [{"yrs": "1998–2010", "role": "...", "org": "...", "kind": "office|law|policy|admin|military|exec|econ|health|educ|business|other", "years": <int>, "c": []}]
 },
 "platform": [{"topic": "Economy", "t": "their stated position", "c": []}],
 "promises": [{"t": "specific promise for this campaign", "c": []}],
 "claims": [{"kind": "bio|campaign", "claim": "what they said", "short": "4-8 word label", "said": {"d": "YYYY-MM-DD", "where": "venue", "c": []},
             "verdict": "true|partly|misleading|false|unverifiable|opinion", "record": {"t": "what the documents show", "c": []},
             "repeated": {"corrected": "YYYY-MM-DD", "again": "YYYY-MM-DD", "c": []} }],
 "saydo": [{"topic": "...", "match": "consistent|partly|contradicts", "said": {"d": "", "t": "", "c": []}, "did": {"d": "", "t": "", "c": []}}],
 "promises_prev": [{"promise": "...", "made": "2022", "status": "DELIVERED|DELIVERED-MODIFIED|PARTIAL|ATTEMPTED-BLOCKED|REVERSED|NOT-ATTEMPTED|TOO-SOON-TO-CALL", "evidence": {"t":"","c":[]}, "complicating": {"t":"","c":[]}}],
 "positions": [{"topic": "...", "entries": [{"d": "YYYY", "t": "position then", "c": []}]}],
 "israel": {
   "aipac_endorse": {"t": "Yes — listed on AIPAC's endorsement page (date) | Not listed as of date", "c": []},
   "aipac_pac": {"amt": <dollars earmarked/bundled through AIPAC PAC this cycle or career — say which in note>, "note": "2026 cycle | career", "c": []},
   "udp": {"support": <$ United Democracy Project spent FOR them>, "oppose": <$ AGAINST>, "c": []},
   "others": [{"name": "e.g. NORPAC / Pro-Israel America / DMFI / J Street PAC", "amt": <$>, "kind": "direct|outside|earmark", "c": []}],
   "heritage": {"score": "87%", "period": "119th Congress", "c": []},
   "votes": [{"bill": "S.J.Res. 33 (block arms sale)", "d": "2025-04-03", "vote": "Yea|Nay", "what": "plain description", "c": []}],
   "statements": [{"d": "YYYY-MM-DD", "t": "paraphrase", "c": []}]
 },
 "fec": {
   "cid": "FEC candidate ID", "thru": "YYYY-MM-DD", "receipts": <$>, "disbursements": <$>, "coh": <$>, "debts": <$>,
   "instate_pct": <0-1 or omit>,
   "src": {"small": <unitemized indiv $>, "large": <itemized indiv $>, "pac_biz": <business/trade/union PAC $>, "pac_ideo": <ideological/single-issue/leadership PAC $>,
           "earmark": <$ bundled via interest-group conduits like AIPAC PAC, Club for Growth — NOT ActBlue/WinRed>, "party": <$>, "self": <candidate loans+contributions $>, "other": <$>},
   "industries": [["Industry", <$>]], "employers": [["Organization (PAC + employees)", <$>]],
   "quarters": [["Q1-25", <$ raised in period>]],
   "outside": {"support": [["Group", <$>, null, <true if a party committee>]], "oppose": [["Group", <$>, null, false]]},
   "c": []
 },
 "money2": {"top_donors": [["Name", <$>, "Occupation, Employer"]], "bundlers": [["Name", <$>]],
            "superpac_donors": [{"pac": "Super PAC name", "spent": <$ in this race>, "donors": [["Top donor", <$>]], "c": []}]},
 "finances": {"networth": {"min": <$>, "max": <$>, "year": 2024, "c": []},
              "trades": {"count": <int>, "period": "2023–2025", "overlap": [{"d": "YYYY-MM", "asset": "...", "amt": "$1K–$15K", "sector": "...", "committee": "...", "c": []}]},
              "note": {"t": "anything notable in disclosures", "c": []}},
 "effectiveness": {"sponsored": <int>, "law": <int>, "cel": {"score": "1.23", "benchmark": "Meets expectations", "congress": "118th", "c": []}, "committees": ["..."]},
 "revolving": [{"role": "...", "org": "...", "yrs": "...", "t": "...", "c": []}],
 "groups": [{"name": "House Freedom Caucus", "c": []}],
 "democracy": [{"kind": "certified|objected|statement", "d": "YYYY-MM-DD", "t": "...", "c": []}],
 "access": {"debates": {"accepted": <int>, "declined": <int>, "c": []}, "townhalls": {"n": <int>, "period": "...", "c": []}},
 "roots": {"years": <int>, "unit": "district|state", "note": {"t":"","c":[]}, "c": []},
 "checks": {"legal": "what you searched, e.g. PACER/CourtListener, Alabama courts (Alacourt via news), House Ethics, OCE, news archives",
            "foreign": "financial disclosures (assets/income by country), FARA database",
            "claims": "describe the fixed sample you used", "democracy": "what you searched"},
 "legal": [{"kind": "conviction-felony|conviction-misd|charge-pending|charge-dismissed|acquitted|civil-liability|civil-settled|ethics-finding|ethics-cleared|unpaid-obligation|disclosure-violation|bankruptcy|business-closure",
            "d": "YYYY", "t": "what happened, plain", "short": "4-8 word label", "status": "current status", "c": []}],
 "foreign": [{"kind": "foreign-govt|foreign-business", "d": "", "t": "", "short": "", "c": []}],
 "recordx": {"missed_pct": <number, sitting members only>, "period": "119th Congress", "disclosure": "on-time|extension|late|missing", "fec": "clean|notices|fined", "c": []},
 "research_notes": "anything you could not find or that needs a human check"
}

## v2.1 STRICT ADDENDUM (applies to every candidate — read carefully)
Rubric v2.1 rewards only what is documented and never scores "unknown" as clean. So:

1. CHECKLIST — add "checklist" with one value per item: "done" (searched the primary source directly),
   "news" (only via news/secondary reporting), "na" (does not apply), "no" (not searched).
   Items: money_history, courts, ethics, disclosures, fara, claims, votes, democracy.
   Direct sources that count as "done":
   - money_history: FEC candidate+committee pages for EVERY cycle they ran (fec.gov works via WebFetch) + Track AIPAC
     (trackaipac.com) for pro-Israel career totals + funders of any super PAC that spent for them. State candidates:
     Alabama FCPA (fcpa.alabamavotes.gov) filings.
   - courts: CourtListener federal search (courtlistener.com/?q="Full Name") AND Justia/state appellate search; Alacourt is
     paywalled — note it, and this item may still be "done" if both free searches were run directly.
   - ethics: House Ethics (ethics.house.gov) / Senate Ethics / OCE reports; Alabama Ethics Commission for state officials.
   - disclosures: House disclosures (disclosures-clerk.house.gov), Senate eFD (efdsearch.senate.gov), or Alabama Ethics
     Commission statement of economic interests for state candidates.
   - fara: efile.fara.gov search for their name and companies.
   - votes: "na" if never in Congress; otherwise covered separately (key-vote roll calls).
   - democracy: certification votes (if served Jan 2017/Jan 2021) + public statements on 2020/2024 results.
2. CLAIMS — the sample is MECHANICAL, not chosen: (a) every checkable factual claim on the campaign's biography/about page,
   (b) the first 10 claims on its issues/platform page, (c) the two highest-spending ads (or, if spend is unknown, the two ads
   most covered in news). Record which page/ad each claim came from in said.where. Rate checkable facts only.
   Need ≥5 checkable claims; if the campaign publishes fewer, say so in research_notes.
3. MONEY FLAGS — "money_flags": {"corp": {"t","c"}, "lobby": {"t","c"}} whenever documented, ANY amount, ANY cycle:
   corp = business/trade PAC money, a super PAC funded by corporations, or ≥10% of itemized money from one company's or
   industry's employees; lobby = money from a PAC/conduit organized around another country's policy (pro-Israel or any other)
   or its super PAC. If you searched fully and found none, set money_flags to {} and checklist.money_history to "done".
4. RECORD — recordx needs at least two of: missed_pct (official, e.g. GovTrack's missed-votes figure), disclosure timeliness,
   fec ("clean"/"notices"/"fined" — from the FEC committee page's RFAI/notices tab).
5. DEMOCRACY — kind "objected" for any vote to reject certified electoral votes (any party, any year).
6. STOCK TRADES — finances.trades.overlap lists trades in industries their committee oversees.
