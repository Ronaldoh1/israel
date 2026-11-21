# Brief: full candidate research (2026 Elections, Sophia)

Today is 2026-10-14. Produce a full candidate dossier exactly as specified in `/home/claude/el26/research/SCHEMA.md`.
Read all of it, including the v2.1 STRICT ADDENDUM; its rules are non-negotiable. For a model of finished depth, read
`/home/claude/el26/research/al-sen-barry-moore.json` and `/home/claude/el26/research/al-sen-everett-wess.json`.

You already have the public records for each candidate (do not re-research these, cite and use them):
`python3 -c "import json;d=json.load(open('/home/claude/el26/data_states.json'));c=d['cands']['<ID>'];print(json.dumps(d['rec'].get(c.get('rec',''),{}),indent=1)[:20000])"`
It holds FEC totals for every cycle, committee money by type, top committee donors, committees organized around another
country, 2026 outside spending, the FARA exact-name check (set checklist.fara "done"), certification votes, and House
disclosure links. House candidates' disclosure PDFs are on disk at `/home/claude/data26/x/<ST>/<ID>/house_disclosures/`
(read with `pdftotext -layout`). Cite these as FEC/FARA/Clerk sources with the fec.gov or disclosures-clerk URL.

Rules in brief: documented record only; every fact cited to a page you opened or that appeared in search results; same depth for
every party; charged is not convicted; a relative's record is not the candidate's; a donation is not a vote; "searched and found
nothing" is a finding; never the word "lie". Paraphrase; quotes under 25 words.

The web-search budget is shared with other researchers: use at most 12 WebSearch calls in total; prefer WebFetch of pages that
searches return (campaign site, Wikipedia, Ballotpedia, official bio, fec.gov, congress.gov, local press).

Write `/home/claude/el26/research/<ID>.json` per candidate (the id is the file name). Validate with `python3 -m json.tool`.
Reply in under 150 words: per candidate, the checklist values and the 2–3 most notable documented findings.
