# Brief: finish the due-diligence checks for fully researched candidates (2026 Elections, Sophia)

Today is 2026-10-14. These candidates already have full pages. Their overall score is held back until every check in the
checklist has been searched. Read `/home/claude/el26/research/SCHEMA.md` (the whole file, especially the v2.1 STRICT ADDENDUM):
its rules apply here unchanged. Same depth for every party; "searched and found nothing" is a valid finding.

For each candidate id you are given:
1. Read the candidate's current record: `python3 -c "import json;d=json.load(open('/home/claude/el26/data_states.json'));c=d['cands']['<ID>'];print(json.dumps({k:c.get(k) for k in ('name','race','checklist','checks','legal','democracy','finances','recordx','money_flags')},indent=1))"`
   and its public-records profile: `d['rec'][c['rec']]` (FEC every cycle, FARA exact-name check, certification votes, House disclosure links).
2. Work only on the checklist items that are not "done" or "na": courts, ethics, disclosures, democracy, money_history.
   - FARA is now done for everyone (the bulk FARA files were searched by exact name; none of these candidates matched). Set "fara": "done".
   - courts: CourtListener and Justia, or the court's own site, searched directly = "done". News only = "news". Record any case with its exact legal status.
   - disclosures: House candidates' filed reports are on disk at `/home/claude/data26/x/<ST>/<ID>/house_disclosures/*.pdf`
     (read them with `pdftotext -layout file.pdf -`). Reading the latest annual or candidate report = "done". Summarize assets,
     income, liabilities and positions in `finances` (net worth range, notable holdings, any foreign assets or income). Senate and
     state candidates: Senate eFD or the state ethics commission if reachable, else "news" or "no" honestly.
   - democracy: certification votes are in the records profile (`cert`). Add a `democracy` entry for each vote, with kind
     "objected" or "certified", plus any public statements on the 2020 and 2024 results you can source.
   - ethics, money_history: per SCHEMA.
3. Never mark anything "done" that you did not search directly. Never downgrade a finding.

Output one file per candidate: `/home/claude/el26/research/completion/<ID>.json`
```json
{"id": "<ID>", "cites": {"key": {"t": "Title — Outlet (date)", "u": "https://..."}},
 "checklist": {"fara": "done", "courts": "done|news|no", "...only the items you changed": "..."},
 "checks": {"legal": "what you searched", "foreign": "...", "democracy": "..."},
 "legal": [ ...the FULL updated list (existing entries kept, new ones added)... ],
 "democracy": [ ...FULL updated list... ],
 "finances": { ...FULL updated object, only if you read disclosures... },
 "research_notes": "anything still open"}
```
Omit a key you did not change. Citation keys are local to the file. Validate with `python3 -m json.tool`.

Reply in under 150 words: per candidate, the checklist after your pass, and anything notable you found.
