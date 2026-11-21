#!/usr/bin/env python3
"""Adds a "Yiddish" tab (a map of where Yiddish was spoken, by dialect, and where it is spoken now)
to the Jewish Lineages dashboard in index.html. Idempotent. Run after patch_lineages_map.py.
Usage: python3 tools/patch_yiddish_map.py [index.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(P, encoding='utf-8').read()
key = '"jewish_lineages": '
k = s.find(key + '{"title"')
assert k >= 0, 'jewish_lineages dashboard not found'
D, end = json.JSONDecoder().raw_decode(s, k + len(key))
if any(t['name'] == 'Yiddish' for t in D['tabs']):
    print('yiddish map already applied'); sys.exit(0)
F = {"west": ["Western Yiddish (faded by the 19th century)", "#8A5A2B"],
     "ne": ["Northeastern (Litvish)", "#1F3A68"],
     "ce": ["Central (Poylish)", "#B04E1C"],
     "se": ["Southeastern (Ukrainish)", "#1E6A6A"],
     "now": ["Where it is spoken daily today", "#6B3F86"]}
pts = [
 {"id": "y_rhine", "name": "Rhineland: Mainz, Worms, Speyer", "family": "west", "lat": 49.8, "lon": 8.3, "n": 1, "place": "Where most scholars place the language's formation", "lang": "Middle High German base, Hebrew-Aramaic and Romance words", "since": "named by the 12th c.; oldest dated text 1272 (Worms)", "today": "No longer spoken"},
 {"id": "y_alsace", "name": "Alsace and Switzerland", "family": "west", "lat": 47.9, "lon": 7.6, "n": 2, "place": "Southwestern dialects", "lang": "Western Yiddish", "since": "medieval", "today": "Faded with the 18th–19th-c. shift to German and French"},
 {"id": "y_holland", "name": "Netherlands and northern Germany", "family": "west", "lat": 52.4, "lon": 6.5, "n": 3, "place": "Northwestern dialects", "lang": "Western Yiddish", "since": "early modern", "today": "Faded by the 19th c."},
 {"id": "y_bohemia", "name": "Bohemia, Moravia, western Hungary", "family": "west", "lat": 49.6, "lon": 16.2, "n": 4, "place": "Transition zone between Western and Eastern Yiddish", "lang": "Transitional dialects", "since": "early modern", "today": "No longer spoken"},
 {"id": "y_litvish", "name": "Lithuania, Belarus, Latvia", "family": "ne", "lat": 54.7, "lon": 25.3, "n": 5, "place": "Vilnius region; also northeastern Poland", "lang": "Northeastern Yiddish (Litvish)", "since": "from the 14th–16th c. settlement", "today": "Communities destroyed in the Holocaust"},
 {"id": "y_poylish", "name": "Poland and western Galicia", "family": "ce", "lat": 52.2, "lon": 21.0, "n": 6, "place": "Warsaw, Łódź, Kraków; between the 1939 German border and the Vistula and San", "lang": "Central Yiddish (Poylish)", "since": "from the 13th–16th c. settlement", "today": "Communities destroyed in the Holocaust; the dialect of most Hasidim today"},
 {"id": "y_ukrainish", "name": "Ukraine and eastern Galicia", "family": "se", "lat": 49.9, "lon": 28.6, "n": 7, "place": "Most of Ukraine, eastern Galicia, southeastern Poland", "lang": "Southeastern Yiddish (Ukrainish)", "since": "early modern", "today": "Communities destroyed in the Holocaust"},
 {"id": "y_romania", "name": "Romania and Bessarabia", "family": "se", "lat": 47.2, "lon": 27.6, "n": 8, "place": "Moldavia, Bessarabia", "lang": "Southeastern Yiddish", "since": "early modern", "today": "Few speakers"},
 {"id": "y_antwerp", "name": "Antwerp", "family": "now", "lat": 51.2, "lon": 4.4, "n": 9, "place": "Hasidic community", "lang": "Yiddish at home and in school", "since": "after 1945", "today": "Spoken daily"},
 {"id": "y_london", "name": "London (Stamford Hill)", "family": "now", "lat": 51.6, "lon": -0.07, "n": 10, "place": "Hasidic community", "lang": "Yiddish at home and in school", "since": "after 1945", "today": "Spoken daily"},
 {"id": "y_israel", "name": "Israel: Bnei Brak and Jerusalem", "family": "now", "lat": 32.0, "lon": 34.95, "n": 11, "place": "Hasidic and other Haredi communities", "lang": "Yiddish at home and in school", "since": "20th c.", "today": "About 250,000 speakers (2021 estimate)"}
]
routes = [
 {"from": "y_rhine", "to": "y_poylish", "label": "Eastward settlement into Poland–Lithuania, 13th–16th c.", "family": "ce"},
 {"from": "y_poylish", "to": "y_litvish", "label": "Spread north into Lithuania and Belarus", "family": "ne"},
 {"from": "y_poylish", "to": "y_ukrainish", "label": "Spread south-east into Ukraine", "family": "se"},
 {"from": "y_poylish", "to": "y_israel", "label": "Emigration and survivors to Palestine and Israel, 20th c.", "family": "now"}
]
tab = {"name": "Yiddish", "sections": [
 {"type": "kpis", "items": [
   ["1272", "Oldest dated Yiddish text, a blessing in a prayer book from Worms"],
   ["11–13 million", "Yiddish speakers just before the Second World War"],
   ["about 85%", "Share of the Jews murdered in the Holocaust who spoke Yiddish, some five million people"],
   ["about 600,000", "Speakers today (2021 estimate): about 250,000 in the US, 250,000 in Israel; other estimates run higher"]]},
 {"type": "geomap", "title": "Where Yiddish was spoken, and where it is spoken now",
  "cap": "Yiddish is a Germanic language written in Hebrew letters, not a Semitic one. Dots mark the centre of each dialect region; the regions follow historical borders, not today's. New York (Brooklyn, Monsey, Kiryas Joel) and Montreal, the largest centres outside Israel today, lie off this map.",
  "view": [-12, 42, 28, 60], "families": F, "points": pts, "routes": routes}]}
names = [t['name'] for t in D['tabs']]
D['tabs'].insert(names.index('The Map') + 1, tab)
D['sources'] += [
 ["Wikipedia, Yiddish (origins, Western and Eastern dialects, speaker numbers, Hasidic communities)", "https://en.wikipedia.org/wiki/Yiddish"],
 ["Jewish Languages Project (William F. Weigel; Isaac Bleaman), Eastern Yiddish", "https://www.jewishlanguages.org/eastern-yiddish"],
 ["JewishGen, Yiddish dialects and their territories", "https://jewishgen.org/databases/givennames/yiddial.htm"]]
s = s[:k + len(key)] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
open(P, 'w', encoding='utf-8').write(s)
print('yiddish map applied')
