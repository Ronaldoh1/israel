# Baseline, ch01: "Semitic", a family of languages (research notes)

Verified 2026-10-17. Every claim in `ch01_semitic.json` comes from a page fetched in this session. WebFetch returns a model-written summary of each page, not the raw text, so check figures and wording against the original pages before printing.

Companion files:
- `ch01_semitic.json`: 8 entries, 70 claims. All source keys start with `sm_`.
- `ch01_semitic-map.json`: 26 points and 9 routes. Some points exist mainly as route ends: `imperial_aramaic` (Susa), `egyptian_arabic`, `maghreb_arabic` and `siculo_arabic`.

## Blocked or unread pages

- **Britannica "Semitic languages" (main article)** and **Wikipedia "Semitic languages"** could not be fetched directly at first because of the provenance check. The Wikipedia page loaded after it appeared in a search. The full Britannica adult article never loaded, so the Britannica students' edition and the separate Britannica language articles were used instead.
- **Britannica "Arabic language":** only the summary and family tree loaded, with no speaker figures or history. The Arabic history claims therefore rest on Wikipedia (Arabic, Levantine Arabic), the UN, Rubenson (1996) and Butts (preprint).
- **University of Reading PDF, "Why did Coptic fail":** blocked by bot protection. Rubenson was used instead.
- **UNESCO Silk Roads PDF on Arabic:** redirected and was not read.
- **Ethnologue and Glottolog:** not fetched directly. Ethnologue figures appear only as cited inside Wikipedia.

## Disputes and inconsistencies to keep visible

1. **Subgrouping.** The Hetzron/Huehnergard tree (East and West; Central and South) is the standard modern scheme, but several parts of it are contested:
   - **Arabic:** Central or South Semitic. Kitchen et al. found its placement statistically equivocal.
   - **Old South Arabian:** South Semitic, or Central Semitic per Hackett (2006).
   - **Modern South Arabian:** Militarev treats it as a separate third branch.
   - **The older Britannica scheme** (Northern and Southern, Peripheral and Central) is still used in Britannica articles. Its labels do not match the modern tree. For example, Britannica calls Aramaic, Canaanite and Eblaite "Northern Central".
2. **Eblaite.** Britannica classes it as Northern Central with Amorite. The common modern view (Wikipedia, "East Semitic languages") groups it with Akkadian as East Semitic. The family-tree diagram should use East Semitic and footnote the disagreement.
3. **Homeland.** There is no consensus.
   - The Levant date of c. 3750 BCE (Kitchen et al. 2009) dates the split among the attested branches. It does not date the split of Semitic from Afroasiatic, and it relies on a contested lexical clock.
   - The Britannica students' article says the parent language developed "between 8000 and 6000 BC". This is much earlier than Kitchen and is uncited. Do not use it.
   - The Afroasiatic homeland is mostly placed in Africa, but a Levantine minority view exists (Militarev).
4. **Ethiopian Semitic from South Arabia.** Kitchen gives a single introduction about 2,800 years ago, and Lipiński gives 1500–500 BCE (as summarized by Wikipedia). Other scholars propose an earlier presence in the Horn. The map route `sabaean → geez` is labelled DISPUTED. Kitchen says only "southern Arabia", not Sabaean specifically, so the route's start point is a stand-in.
5. **Is Ge'ez the ancestor of Tigrinya and Tigré?** Britannica's Ge'ez article says it is. Its Tigrinya and Tigré articles say only "closely related". This is not used as a claim; check it against specialist work (e.g. Weninger) before stating it.
6. **Moabite date.** Britannica "Canaanite languages" says an 8th-century BCE inscription. Britannica "Moabite language" and World History Encyclopedia say 9th century BCE (Mesha, c. 850 BCE onward). The JSON uses 9th century.
7. **Marr and "Antisemitismus".**
   - The pamphlet and the League of Antisemites date to 1879 (Wikipedia, JVL).
   - Wikipedia and Etymonline date Marr's popularisation of the term to 1881. Almog says "the 1870s".
   - The USHMM says only that the word was coined in German in the late 1800s.
   - The JSON says Marr popularised the term and flags the 1879/1881 split. Do not say he "coined" it outright. Earlier uses (e.g. Steinschneider, 1860) are widely reported but were not verified here.
8. **Speaker figures (all marked `reported`).**
   - **Arabic:** UN "more than 400 million" daily users. Wikipedia gives 411M L1 + 70M L2, and its body text says "as many as 380 million". UW-Madison says "more than 300 million".
   - **Amharic:** Britannica about 18.7M (early 21st c.) against Ethnologue 2025 about 33.7M L1 + 25.1M L2. Use a range or say which source.
   - **Hebrew:** about 9M (Wikipedia, 2018). EBSCO says about 5M in Israel plus 2M elsewhere.
   - **Neo-Aramaic:** 575k–1M is tagged "citation needed" on Wikipedia. Iranica's figures are old and Iran-only. Treat the number as weak.
   - **Mehri:** Leeds (2014) gives about 100k. Wikipedia (2024) gives about 250k.
   - **Maltese:** Wikipedia's 570k conflicts with Ethnologue's 530k.
9. **Ethiopia's working languages.** Article 5 of the 1995 Constitution (primary source) names Amharic as the federal working language. Wikipedia reports that in 2020 Oromo, Tigrinya, Somali and Afar were added as federal working languages. That was not verified against a primary decree, so the JSON states only the constitutional position.
10. **Arabic in North Africa.** The `arabic → maghreb_arabic` route rests only on Wikipedia's general statement that Arabic spread with the early Muslim conquests. No specialist source on the Maghreb's Arabisation (e.g. on the long Berber continuity) was fetched. The timing is gradual, not a 7th-century event; the label avoids dating the shift.
11. **Aramaic origin "in Syria".** Britannica says only "among the Aramaeans" (late 11th c. BCE) and does not name Syria. The map point at Damascus and the place label "Aramaean states of Syria" are standard but not sourced to a fetched page.
12. **Old Arabic map point.** Placing it in northern Arabia and the Syrian desert is inferred from the Safaitic and Hismaic attestation (Wikipedia) and from the Namara find site. No fetched page states a single "origin" location for Arabic.
13. **Syriac's earliest inscriptions.** e-GEDSH (Butts) gives the 1st–3rd centuries CE for non-Christian tomb inscriptions. The often-quoted "6 CE" first dated inscription was not verified.
14. **Afroasiatic: "only branch outside Africa".** Wikipedia states this directly. Britannica and BYU only imply it, by describing Semitic as the branch spoken in the Near East. Keep the wording as "described as".
15. **Race claims.** The JSON never says any people "is Semitic". Speakers are listed as speakers of Semitic languages.
   - The Encyclopaedia Judaica (Greenberg) supports the claim that careful usage of "Semitic" is linguistic only.
   - The USHMM supports the claim that there are no biological races.
   - Renan's racial ranking is sourced to the BnF.
   - No fetched page dated the racial extension to "the 19th century" in exactly those words. Etymonline dates "Semite" in the ethnic sense to 1847, and Renan's book is from 1855.

## Not verified / left out

- The Ugarit destruction "c. 1185 BCE": COJS says only "Sea Peoples" and gives a range ending in 1200 BCE. The JSON uses "around 1200 BCE".
- The exact 870 date of Arab rule in Malta comes from Brincat as "raided in 870". Wikipedia says only "9th century". Do not write "Arab rule from 870" without qualification.
- Kishite and Dilmunite as possible East Semitic languages were not included.
- Mandaic speaker numbers conflict: Iranica, citing Ethnologue, gives about 500; Wikipedia says "a few thousand". Both are left out of the claims.
