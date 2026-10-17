# Baseline, ch01: lineages of the Jewish communities (research notes)

Verified 2026-10-17. Every claim in `ch01_lineages.json` comes from a page fetched in this session. WebFetch returns a model-written summary of each page, not the raw text, so quoted phrases are short. Check figures and quotations against the original pages before printing.

Companion files:
- `ch01_lineages.json`: 25 entries, 138 claims.
- `ch01_lineages-map.json`: 29 points and 11 routes. Points include route-only destinations: `poland_lithuania`, `ottoman`, `london`, `israel`, `americas`.

## Blocked or unread pages

- **Britannica "Ashkenazi":** only the summary and quick facts loaded.
- **Britannica "Bene Israel":** only the summary loaded.
- **Britannica "Sephardi" and "Mizrahi Jews":** the direct fetch was refused (provenance) and no search result supplied these URLs. JVL "Sephardim" and My Jewish Learning were used instead.
- **Wikipedia "Abayudaya" and "Mountain Jews (Juhuro)":** the fetch was refused. The Abayudaya entry rests on one news article (Intermountain Jewish News, 2021). The Mountain Jews entry uses the Endangered Language Alliance and JVL.
- **PubMed (Lemba genetics) and Project MUSE article pages:** captcha. Kaplan's book description on MUSE did load. Parfitt et al. (2000) is cited only through the Encyclopaedia Judaica "Lemba" entry.
- **ANU Museum (Beit Hatfutsot) Bene Israel page:** returned metadata only. No ANU or YIVO page was successfully read. The Ashkenazi entry uses JVL/EJ, Britannica and EGO (Leibniz Institute) instead.

## Not verified (deliberately left out of claims)

- **Map languages:**
  - Egyptian Jews: likely a mix of Arabic, French, Ladino and Italian, but no fetched page stated this.
  - Abayudaya and Lemba: no fetched page named their languages.
  - These fields read "not verified".
- **Map "today" field for Western Sephardim:** no source on where most descendants live today. The field says only "small historic congregations".
- **Map coordinates:** all are approximate centres I chose, not sourced. Iran is placed near Isfahan and Ethiopia near Gondar as regional centres; Karaites are placed in Crimea.
- **Yemenite language:** the only source is Wikipedia citing Ethnologue. The JLP or JVL pages were not found.
- **Western Sephardi New York (Shearith Israel, 1654):** not fetched, so not included.
- **Western Sephardi Hamburg:** appears only in JVL's list of Sephardi communities.
- **Abayudaya:** Jewish Agency recognition is undated in the source (2016 is often cited but not verified here). No numbers were sourced.

## Disputes and conflicts to handle in the text

1. **When "Mizrahi" became an umbrella term.**
   - My Jewish Learning: coined by the Ashkenazi establishment in the 1950s.
   - Wikipedia: Gil Eyal (2006) puts the invention in the Jewish Agency's 1940s "One Million Plan", and Bachi used the category in the 1940s.
   - Write "a modern Israeli category, from the 1940s–50s".
2. **North Africans as "Mizrahi".**
   - Maghrebi Jews were historically "Westerners" (Maghribiyyun).
   - They are often grouped with Sephardim in religious and rabbinic usage (Sephardi rite; Sephardi chief rabbinate).
   - The map colours them `mizrahi` as the brief instructed. Say so in the caption.
   - The "many object" statement on Wikipedia lacks a citation.
3. **Share of world Jewry that is Ashkenazi.** JVL/EJ says 90% before WWII; Britannica says more than 80% today. Both are estimates and depend on definition.
4. **Size of the 1492 expulsion.** JVL estimates 100,000. Scholarly estimates vary widely; for example, Wikipedia says North African arrival numbers "cannot be reliably estimated". Attribute any number you print.
5. **Haketia vs Judeo-Arabic in Morocco.**
   - JVL Morocco: "most of these communities" spoke Haketia until recently. This most likely means the northern, formerly Spanish-zone communities.
   - The toshavim/megorashim article and JLP: the majority spoke Judeo-Arabic or Judeo-Berber, and Haketia was a northern Moroccan (Tetouan) variety.
   - The claims follow the second reading. Do not print "most Moroccan Jews spoke Haketia".
6. **Iraqi airlift dates and figures.**
   - JVL dates the airlift from 18 May 1951 to early 1952 and gives "more than 120,000" and also "some 130,000".
   - Wikipedia gives 120,000–130,000 (about 75%) and dates emigration to the 1950 law.
   - The route label uses "1950–52". The brief's "1950–51" is too narrow.
   - Farhud deaths: Wikipedia gives about 200; other sources give 180 or more. Attribute the figure.
7. **Operation Moses.** Weil (Encyclopedia of the Modern Middle East) gives 7,700. Other sources commonly give about 8,000. Operation Solomon: 14,400 (Weil).
8. **Beta Israel origins.**
   - Kaplan (1992): emerged as a group in the 14th–16th centuries.
   - My Jewish Learning: arrived between the 1st and 6th centuries.
   - Traditions: Dan; Menelik (rejected by the Beta Israel themselves).
   - The record does not settle the question.
9. **Kaifeng dating.**
   - Iranica and the majority view: Persian Jews who came in the 12th century under the Song dynasty.
   - Others: the Tang dynasty or earlier.
   - The synagogue's traditional date of 1163 is challenged by Yu (2017).
   - Wikipedia says the synagogue was destroyed by the flood of 1642 and dismantled between 1850 and 1866. The often-repeated "1860 flood" is not supported.
10. **Kerala dating.** The earliest document is the copper plates of about 1000 CE. Tradition and JLP say Jews were present "since at least the beginning of the common era". Keep documented and traditional dates separate.
11. **Georgian, Kurdish and Mountain Jewish origins (586 BCE, Ten Tribes, Lost Tribes).** These are traditions recorded in chronicles, not contemporary evidence, and are flagged `disputed`.
12. **Crimean Karaim identity.**
    - Crimean Karaim institutions adopted Khazar (non-Jewish) descent in 2000.
    - Genetics (Brook 2014) shows partial Middle Eastern ancestry.
    - Israel's Chief Rabbinate treats Karaites as Jews.
    - The Vytautas relocation to Trakai is a tradition, and its date is disputed (legend 1218 vs the usual c. 1397).
13. **Population estimates that conflict within a single source:**
    - Bukharan Jews worldwide: ELA "up to 200,000" vs Wikipedia 300,000–350,000.
    - Georgian Jews in Israel: 65,000 vs 75,000.
    - Iran: about 8,300–9,200 in JVL.
    - Yemen: fewer than 50 to about 100 in JVL.
    - Egypt: "a few dozen" in 2013 vs fewer than 10 in 2020 in JVL.
    - Algeria today: about 200 vs fewer than 5 in JVL.
14. **Bnei Menashe and Lemba descent claims.** These are flagged as disputed and not established.
    - Bnei Menashe: unpublished or non-peer-reviewed genetic tests found no clear Middle Eastern origin among men. Rabbinic recognition (Amar, 2005) still required conversion.
    - Lemba: early Y-chromosome findings rely on "Cohen Modal Haplotype" motifs, which Tofanelli et al. (2014) judge unreliable as predictors of Jewish ancestry.
15. **Abayudaya.** The Jewish Agency recognises them as Jews; Israel's Interior Ministry treats them as an "emerging community" not eligible under the Law of Return. Live status as of 2026 was not re-checked; verify before printing.

## Currency check (recent items, status as of 2026-10-17)

- **CBS Ethiopian-origin population:** 177,600 in 2024, released November 2025 and reported by JNS. The CBS release itself was not fetched.
- **Bnei Menashe:** Israeli approval (late November 2025) to bring about 5,800 over five years, reported by EastMojo (January 2026). Implementation status is not verified.

## Sources quality summary

- **Scholarly or encyclopaedic:**
  - Encyclopaedia Judaica via JVL (Ashkenaz, Kurdistan, Bene Israel, Djerba) and via Encyclopedia.com (Lemba)
  - Encyclopaedia Iranica (Kaifeng)
  - Jewish Language Project, HUC (Judezmo, Judeo-Persian, Judeo-Italian, Judeo-Georgian, Jewish Malayalam)
  - EGO / Leibniz Institute
  - Posen Library
  - USHMM, Yad Vashem
  - Kaplan (NYU Press)
  - Tofanelli et al. (Frontiers in Genetics)
- **Wikipedia, used with its cited sources noted in the label:**
  - Sepharad
  - Mizrahi Jews
  - Toshavim and Megorashim
  - History of the Jews in Iraq
  - Syrian Jews
  - Bukharan Jews
  - Georgian Jews
  - Yevanic
  - Kaifeng Jews
  - Crimean Karaites
  - Judeo-Yemeni Arabic
- **Romaniote entry:** rests entirely on Wikipedia "Yevanic". Upgrade it, for example with Kehila Kedosha Janina or the EJ "Ioannina" entry, if possible.
