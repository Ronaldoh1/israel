#!/usr/bin/env python3
"""Adds an "On the Map" tab to the Four Words dashboard in index.html: where Zionism began (1838–1897)
and where the first settlers came from; where Jews leaving Eastern Europe went (1881–1914); and where
Jews live today. Idempotent. Run after patch_four_words.py.
Usage: python3 tools/patch_four_words_maps.py [index.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
key = '"four_words": '
k = s.find(key + '{"title"')
assert k >= 0, 'four_words dashboard not found'
D, end = json.JSONDecoder().raw_decode(s, k + len(key))
if any(t['name'] == 'On the Map' for t in D['tabs']):
    print('four words maps already applied'); sys.exit(0)

F1 = {"chr": ["Christian restorationists, 1830s–40s", "#8A5A2B"],
      "fore": ["Early calls for settlement, 1843–1862", "#1F3A68"],
      "hz": ["Lovers of Zion and the first wave, 1882–1884", "#B04E1C"],
      "org": ["Political Zionism organized, 1890–1897", "#6B3F86"],
      "ye": ["Yemenite immigration, 1881–82", "#1E6A6A"],
      "set": ["New settlements, 1882", "#2F6B45"]}
P1 = [
 {"id": "z_london", "n": 1, "name": "London", "family": "chr", "lat": 51.5, "lon": -0.1, "place": "Lord Shaftesbury lobbies Foreign Secretary Palmerston to encourage a Jewish return", "lang": "Christian restorationism", "since": "1838: a British consul is appointed in Jerusalem", "today": "Christian Zionism, later a mass movement in the US"},
 {"id": "z_semlin", "n": 2, "name": "Semlin (Zemun), near Belgrade", "family": "fore", "lat": 44.84, "lon": 20.4, "place": "Rabbi Yehuda Alkalai", "lang": "Calls for organized settlement in the land", "since": "1843", "today": "Alkalai later settled in Jerusalem"},
 {"id": "z_thorn", "n": 3, "name": "Thorn (Toruń)", "family": "fore", "lat": 53.0, "lon": 18.6, "place": "Rabbi Zvi Hirsch Kalischer, rabbi there for over forty years", "lang": "Derishat Zion: redemption can begin by human effort", "since": "1862", "today": "Now in Poland"},
 {"id": "z_kharkov", "n": 4, "name": "Kharkov (Kharkiv)", "family": "hz", "lat": 50.0, "lon": 36.23, "place": "Students found Bilu after the pogroms of 1881", "lang": "Bilu's first headquarters", "since": "January 1882", "today": "Now in Ukraine"},
 {"id": "z_odessa", "n": 5, "name": "Odessa", "family": "hz", "lat": 46.48, "lon": 30.73, "place": "Home of Leon Pinsker, a physician and author of Auto-Emancipation (1882)", "lang": "Seat of the Lovers of Zion central committee from 1884", "since": "1882–1884", "today": "Now in Ukraine"},
 {"id": "z_galati", "n": 6, "name": "Galați", "family": "hz", "lat": 45.43, "lon": 28.05, "place": "Romanian Jewish groups sail from this Danube port", "lang": "About 600 settle in new villages", "since": "1882", "today": "Now in Romania"},
 {"id": "z_kattowitz", "n": 7, "name": "Kattowitz (Katowice)", "family": "hz", "lat": 50.26, "lon": 19.02, "place": "Conference of the Lovers of Zion, chaired by Pinsker", "lang": "32 delegates, 22 of them from Russia", "since": "November 1884", "today": "Then in Germany, now in Poland"},
 {"id": "z_vienna", "n": 8, "name": "Vienna", "family": "org", "lat": 48.2, "lon": 16.37, "place": "Nathan Birnbaum coins the word \"Zionism\" (1890); Theodor Herzl writes Der Judenstaat (1896)", "lang": "From settlement societies to a political program", "since": "1890–1896", "today": ""},
 {"id": "z_basel", "n": 9, "name": "Basel", "family": "org", "lat": 47.56, "lon": 7.59, "place": "First Zionist Congress founds the Zionist Organization", "lang": "Program: a publicly and legally assured home in Palestine", "since": "August 1897", "today": ""},
 {"id": "z_sanaa", "n": 10, "name": "Sanaa", "family": "ye", "lat": 15.35, "lon": 44.2, "place": "A few hundred Jews leave Sanaa and nearby towns", "lang": "They arrive about seven months before most of the Eastern Europeans", "since": "1881–82", "today": "About a tenth of Yemen's Jews left by 1914"},
 {"id": "z_jaffa", "n": 11, "name": "Jaffa and Rishon LeZion", "family": "set", "lat": 31.96, "lon": 34.78, "place": "14 Bilu pioneers land at Jaffa on 6 July 1882; Rishon LeZion founded", "lang": "Bilu later settles Gedera (1884)", "since": "1882", "today": ""},
 {"id": "z_zikhron", "n": 12, "name": "Zikhron Ya'akov", "family": "set", "lat": 32.57, "lon": 34.95, "place": "Founded by settlers from Romania", "lang": "Later funded by Baron Edmond de Rothschild", "since": "1882", "today": ""},
 {"id": "z_roshpinna", "n": 13, "name": "Rosh Pinna", "family": "set", "lat": 32.97, "lon": 35.54, "place": "Settlers from Romania take over an earlier village, Gei Oni (1878)", "lang": "", "since": "1882", "today": ""},
 {"id": "z_jerusalem", "n": 14, "name": "Jerusalem", "family": "ye", "lat": 31.78, "lon": 35.22, "place": "Yemenite immigrants settle and work in construction", "lang": "Seat of the British consulate from 1838", "since": "1882", "today": ""}
]
R1 = [
 {"from": "z_kharkov", "to": "z_jaffa", "label": "Bilu pioneers, July 1882", "family": "hz"},
 {"from": "z_galati", "to": "z_roshpinna", "label": "Romanian groups, 1882", "family": "hz"},
 {"from": "z_sanaa", "to": "z_jerusalem", "label": "Yemenite Jews, 1881–82", "family": "ye"},
 {"from": "z_vienna", "to": "z_basel", "label": "Herzl calls the first Congress, 1897", "family": "org"}
]
F2 = {"from": ["Where they left from", "#1F3A68"], "eu": ["Western Europe", "#8A5A2B"],
      "pal": ["Palestine", "#2F6B45"], "am": ["The Americas", "#B04E1C"]}
P2 = [
 {"id": "m_pale", "n": 1, "name": "Russian Empire, Galicia, Romania", "family": "from", "lat": 51.5, "lon": 27.0, "place": "The Pale of Settlement and its neighbours", "lang": "Pushed by the pogroms of 1881–82, the May Laws and poverty: more than 2.5 million leave", "since": "1881–1914", "today": ""},
 {"id": "m_london", "n": 2, "name": "England", "family": "eu", "lat": 51.5, "lon": -0.1, "place": "Mainly London's East End", "lang": "About 300,000 arrive", "since": "1881–1914", "today": ""},
 {"id": "m_paris", "n": 3, "name": "France", "family": "eu", "lat": 48.86, "lon": 2.35, "place": "Mainly Paris", "lang": "About 80,000 arrive", "since": "1881–1914", "today": ""},
 {"id": "m_pal", "n": 4, "name": "Palestine", "family": "pal", "lat": 31.9, "lon": 34.9, "place": "Ottoman Palestine", "lang": "About 60,000 arrive; many later leave again", "since": "1881–1914", "today": ""},
 {"id": "m_atl", "name": "To the Americas", "family": "am", "lat": 46.0, "lon": -16.5, "dest": True, "side": "right"}
]
R2 = [
 {"from": "m_pale", "to": "m_atl", "label": "To the Americas: the great majority", "family": "am"},
 {"from": "m_pale", "to": "m_london", "label": "To England", "family": "eu"},
 {"from": "m_pale", "to": "m_paris", "label": "To France", "family": "eu"},
 {"from": "m_pale", "to": "m_pal", "label": "To Palestine", "family": "pal"}
]
tab = {"name": "On the Map", "sections": [
 {"type": "kpis", "items": [
   ["1843", "First call for organized settlement, by a rabbi near Belgrade; the movement is organized in Basel in 1897"],
   ["about 1.7 million", "Jews from Eastern Europe who went to the United States, 1881–1914"],
   ["about 60,000", "Who went to Palestine in the same years; many later left again"],
   ["1881–82", "Year the first Yemenite group set out, months before most of the Eastern Europeans"]]},
 {"type": "geomap", "title": "Where Zionism began, 1838–1897, and where the first settlers came from",
  "cap": "Numbers mark places in the order the ideas appeared, from London to Basel, then the arrivals. Most places are in Central and Eastern Europe, but the earliest British supporters were Christians, and one of the first groups of settlers came from Yemen.",
  "view": [-12, 50, 12, 57], "families": F1, "points": P1, "routes": R1},
 {"type": "geomap", "title": "Where Jews leaving Eastern Europe went, 1881–1914",
  "cap": "Approximate totals from the Posen Library. The Americas lie off this map; the arrow on the left stands for about 1.7 million Jews to the United States, 100,000 to Argentina and 60,000 to Canada. Other estimates put the United States at about two million.",
  "view": [-20, 42, 28, 60], "families": F2, "points": P2, "routes": R2},
 {"type": "hbar", "title": "Where they went, 1881–1914 (approximate)", "cap": "Posen Library estimates. Palestine took about one emigrant in thirty to forty; estimates for the first wave of settlers range from 25,000 to 60,000, and half or more left again.",
  "data": [["United States", 1700000, "", "about 1.7m"], ["England", 300000, "", "about 300,000"], ["Argentina", 100000, "", "about 100,000"], ["France", 80000, "", "about 80,000"], ["Canada", 60000, "", "about 60,000"], ["Palestine", 60000, "", "about 60,000"], ["South Africa", 50000, "", "about 50,000"]]},
 {"type": "hbar", "title": "Where Jews live today (2024)", "cap": "Jewish Agency figures from the demographer Sergio DellaPergola, using a \"core\" definition: people who identify as Jews, or have a Jewish parent and no other religion. Most of the world's Jews live outside Israel.",
  "data": [["Israel", 7300000, "", "7.3m"], ["United States", 6300000, "", "6.3m"], ["France", 438500, "", "438,500"], ["Canada", 400000, "", "400,000"], ["Britain", 313000, "", "313,000"], ["Argentina", 170000, "", "170,000"], ["Germany", 125000, "", "125,000"], ["Russia", 123000, "", "123,000"], ["Australia", 117000, "", "117,000"]]}]}
names = [t['name'] for t in D['tabs']]
D['tabs'].insert(names.index('Who Overlaps') + 1, tab)
D['sources'] += [
 ["Wikipedia, Christian Zionism in the United Kingdom (Shaftesbury; British consul in Jerusalem, 1838)", "https://en.wikipedia.org/wiki/Christian_Zionism_in_the_United_Kingdom"],
 ["Wikipedia, Zvi Hirsch Kalischer (Thorn; Derishat Zion, 1862)", "https://en.wikipedia.org/wiki/Zvi_Hirsch_Kalischer"],
 ["Jewish Virtual Library, Bilu (Kharkov, 1882; Jaffa, 6 July 1882)", "https://www.jewishvirtuallibrary.org/bilu-2"],
 ["Wikipedia, Katowice Conference (1884)", "https://en.wikipedia.org/wiki/Katowice_Conference"],
 ["Wikipedia, First Aliyah (numbers; Romanian and Yemenite settlers; settlements of 1882)", "https://en.wikipedia.org/wiki/First_Aliyah"],
 ["Posen Library, The Mass Migration of Jews (destinations, 1881–1914)", "https://www.posenlibrary.com/node/12125"],
 ["My Jewish Learning, Jewish Emigration in the 19th Century", "https://www.myjewishlearning.com/article/jewish-emigration-in-the-19th-century/"],
 ["JNS, Jewish population hits 15.8 million globally (2 Oct 2024; Jewish Agency, DellaPergola)", "https://www.jns.org/jewish-population-hits-15-8-million-globally/"]]
s = s[:k + len(key)] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(s)
print('four words maps applied')
