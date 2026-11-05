# Brief: verify the November 3, 2026 U.S. House nominees, by district

Today is 2026-10-14. You are verifying who is on the general-election ballot for every U.S. House district in your assigned states, for the 2026 Elections module of Sophia (an evidence-first civic reference). The output feeds a public site, so every name must be checked.

## What to find, per district
- the incumbent (name, party) and whether they are running for re-election, retiring, running for another office, or lost renomination
- every general-election nominee on the ballot: major-party nominees, and independents or third-party candidates who have qualified for the ballot (list minor candidates when the source lists them; don't hunt beyond the main sources)
- the status of the race: `set` (nominees decided), or `pending` (a runoff, a top-two/jungle general, a court case or a late primary still to decide), with a one-line note
- for top-two (CA, WA) and other systems where two candidates of the same party face each other, list both
- Louisiana: state its 2026 system as the sources describe it, and list who is on the November ballot

## Sources, in order
1. Each state's "2026 United States House of Representatives elections in <State>" page on Wikipedia, and Ballotpedia's equivalent. Find them with WebSearch, then WebFetch the URL from the results (WebFetch only opens URLs that appeared in search results).
2. The state's election office (official certified candidate list) when you can reach it.
3. AP or major outlets for late primaries, runoffs and withdrawals.
Never rely on memory. Record every URL you used. Where two sources disagree, say so in the district note.

## Match to FEC ids
Each state has `/home/claude/data26/x/<ST>/candidates.csv` (columns id,name,office,district,party,incumbent_challenger_open,fec_ids,in_module): everyone who filed with the FEC for 2026. For each nominee, put the matching row's `id` in `rec` and its `fec_ids`. If you can't find a match (some ballot-qualified independents never file with the FEC), leave `rec` empty. Match carefully: same district, same person (watch nicknames and middle names).

## Output: one file per state
Write `/home/claude/el26/research/house/<ST>.json`:
```json
{"state": "AR", "checked": "2026-10-14",
 "cites": {"wiki_ar": {"t": "2026 United States House of Representatives elections in Arkansas — Wikipedia", "u": "https://..."}},
 "races": [
  {"race": "AR-01", "incumbent": {"name": "Rick Crawford", "party": "R", "status": "Running"},
   "nominees": [{"name": "Rick Crawford", "party": "R", "incumbent": true, "rec": "ar-01-rick-crawford", "fec": ["H0AR01083"]},
                {"name": "…", "party": "D", "incumbent": false, "rec": "…", "fec": ["…"]}],
   "status": "set", "note": "One line, only if useful (primary date and margin for an open seat, a pending runoff, a disputed result).",
   "c": ["wiki_ar"]}
 ]}
```
Race ids are `<ST>-<two-digit district>`; at-large seats are `<ST>-AL` (e.g. `WY-AL`, `VT-AL`, `ND-AL`, `SD-AL`, `DE-AL`, `AK-AL`). Party letters: D, R, L (Libertarian), G (Green), I (independent/no party), or the state party name in the note.

## Rules
- Documented facts only. Same care for every party.
- A district with no candidate of a party is fine; say "unopposed" in the note.
- If you cannot confirm a district, list what you have, set status `unconfirmed`, and say why in the note. Never guess.
- Validate the JSON with `python3 -m json.tool`. Check every district in the state is present (count against the state's number of seats).

Reply in under 200 words: districts per state, how many `set` / `pending` / `unconfirmed`, nominees without an FEC match, and any source conflict.
