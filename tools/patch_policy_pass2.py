#!/usr/bin/env python3
"""Pass 2 of the coverage plan: policy instruments with documented effects, and a ninth channel,
Land held (thousands of dunams). Idempotent; run after patch_people_channel.py and patch_people_tests.py.

Land held: the Jewish National Fund's holdings (936,000 dunams by May 1948) are split into what it held
in 1920 (22,363) and what it bought under the Mandate's Land Transfer Ordinance (about 914,000); the rest
of Jewish-owned land (PICA and private buyers and companies) is counted without a policy share because
no source splits it by period. The channel is normalized to its own full record, so the baseline and
unrelated tests do not move.

Usage: python3 tools/patch_policy_pass2.py [road-network.html]"""
import json, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'road-network.html'
s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
V = D['viab']
if 'holdings' in V['channels']:
    print('pass 2 already applied'); sys.exit(0)
assert 'people' in V['channels'], 'run the people patch first'
R = {
 'pij': ("Dan Leon, 'The Jewish National Fund: How the Land Was Redeemed', Palestine-Israel Journal 12:4 (2005)", "https://www.pij.org/details.php?id=410"),
 'stein': ("Kenneth Stein, 'Zionist land acquisition: a core element in establishing Israel', Center for Israel Education", "https://israeled.org/ken-stein-zionist-land-acquisition-a-core-element-in-establishing-israel"),
 'sursock': ("Wikipedia, Sursock Purchases", "https://en.wikipedia.org/wiki/Sursock_Purchases"),
 'cojs1940': ("Center for Online Judaic Studies, February 28, 1940: British restrict land transfer", "https://cojs.org/february-28-1940-british-restrict-land-transfer/"),
 'macdonald': ("Wikipedia, MacDonald letter (13 Feb 1931)", "https://en.wikipedia.org/wiki/MacDonald_letter"),
 'wp1922': ("British White Paper of June 1922 (Boston University, Jerusalem sourcebook)", "https://www.bu.edu/mzank/Jerusalem/tx/whitepaper1922.htm"),
 'pmc1939': ("JTA, League body majority holds White Paper violates mandate (18 Aug 1939)", "https://www.jta.org/archive/league-body-majority-holds-white-paper-violates-mandate-partition-urged-as-solution"),
 'mandate_text': ("Mandate for Palestine, 1922 (Fordham Modern History Sourcebook)", "https://sourcebooks.web.fordham.edu/mod/1922mandate.asp"),
 'jta34': ("JTA, 'The Baron', 4 Nov 1934 (PICA owns about half a million dunams)", "https://www.jta.org/archive/the-baron"),
}
def refs(*keys): return [{"t": R[x][0], "u": R[x][1]} for x in keys]
NOTE = ' Added in November 2026 (policy pass).'
new_nodes = [
 ("other_holdings", "Land held by other Jewish owners (1948)", "population", "land", "Jewish-owned land outside the Jewish National Fund: PICA (about 500,000 dunams in 1934), private buyers and land companies. By May 1948 Jews had bought about 2 million dunams in all (Stein)."),
 ("private_land", "Private Jewish buyers and land companies", "organization", "land", "Individuals and companies such as the American Zion Commonwealth, which bought about 80,000 acres in the Jezreel Valley from the Sursock family in 1921-25."),
 ("macdonald_letter", "MacDonald letter (13 Feb 1931)", "document", "british state", "Prime Minister Ramsay MacDonald's letter to Chaim Weizmann, treated as withdrawing the Passfield White Paper's limits on immigration and land purchase; immigration then rose until the 1939 White Paper."),
 ("pmc", "Permanent Mandates Commission (League of Nations)", "institution", "international", "The League's supervisory body for the mandates. In 1939 four of its seven voting members found that the White Paper was not in conformity with the Mandate."),
]
have = {n['id'] for n in D['nodes']}
for i, nm, kind, cl, note in new_nodes:
    assert i not in have, i
    D['nodes'].append({"id": i, "name": nm, "kind": kind, "cluster": cl, "note": note + NOTE, "mentions": 0, "sections": []})
H = 'holdings'
E = [  # f, t, label, type, status, refs, channel, weight
 ("jnf", "jnf_holdings", "Held by 1920: 22,363 dunams.", "land total", "verified", ['pij'], H, 22.4),
 ("lto_1920", "jnf_holdings", "Bought under the Mandate's land-transfer law, 1920 to May 1948: about 914,000 of the JNF's 936,000 dunams.", "legal route", "verified", ['pij'], H, 913.6),
 ("pica", "other_holdings", "PICA held about 500,000 dunams in 1934, roughly twice the JNF's holdings then.", "land total", "reported", ['jta34'], H, 500),
 ("private_land", "other_holdings", "Private buyers and companies: the rest of about 2 million dunams bought by May 1948, after the JNF and PICA (a remainder, not a measured figure).", "land total", "reported", ['stein', 'pij'], H, 564),
 ("sursock", "private_land", "The largest single seller: about 240,000 dunams in the Jezreel Valley (Shaw Commission table), much of it in 1921-25 to the American Zion Commonwealth; already counted in the buyers' totals.", "sale", "reported", ['sursock'], None, 0),
 ("ltr_1940", "jnf_holdings", "The 1940 regulations barred or restricted transfers in about 95% of the country; the JNF still acquired 390,000 dunams in 1940-46, 238,000 of them from Arab sellers, often through legal workarounds.", "restriction", "verified", ['cojs1940', 'stein'], None, 0),
 ("wp1922", "mandate_admin", "June 1922: the Jewish community is in Palestine 'as of right and not on the sufferance'; immigration not to exceed the country's 'economic capacity ... to absorb new arrivals', the rule for later certificate schedules.", "policy", "verified", ['wp1922'], None, 0),
 ("macdonald_letter", "wp1930", "13 Feb 1931: treated as withdrawing the Passfield White Paper's limits on immigration and land purchase.", "reversal", "verified", ['macdonald'], None, 0),
 ("macdonald_letter", "weizmann", "Addressed to Weizmann; reaffirmed British support for continued Jewish immigration and land purchase.", "policy", "verified", ['macdonald'], 'diplomacy', 1.5),
 ("pmc", "wp1939", "Aug 1939: four of seven voting members (Belgium, Switzerland, Norway, the Netherlands) could not find the White Paper in conformity with the Mandate; Britain, France and Portugal gave qualified approval. War stopped the League Council from ruling.", "review", "verified", ['pmc1939'], None, 0),
 ("mandate", "jewish_agency", "Article 4: an appropriate Jewish agency 'shall be recognised as a public body' to advise the administration.", "obligation", "verified", ['mandate_text'], 'organization', 1.5),
]
ids = {n['id'] for n in D['nodes']}
for f, t, *_ in E:
    assert f in ids and t in ids, (f, t)
V['channels'].append(H)
C = {c: i for i, c in enumerate(V['channels'])}
for f, t, lab, ty, st, rk, ch, w in E:
    D['edges'].append({"f": f, "t": t, "label": lab, "type": ty, "status": st, "src": "", "n": 1, "sec": "", "refs": refs(*rk), "ext": True})
    if ch and w:
        V['edges'].append([f, t, C[ch], 1.0 if st == 'verified' else 0.6, w if (st == 'verified' or ch == H) else round(w * 0.6, 4)])
        V['eyear'].append([0, 0])
V['labels'][H] = 'Land held'
V['need'][H] = 'another source of land on the same scale'
V['exp'].append(1)
V['tbuild'].append(66)
V['tfrom'].append('the first land purchases, 1882')
V['cap0'].append(round(sum(e[4] for e in V['edges'] if e[2] == C[H]), 4))
V['norm'].append(V['cal'])
V['incorp'] += [['jnf_holdings', 'jnf']]
D['viability_meta']['per_channel'][H] = sum(1 for e in V['edges'] if e[2] == C[H])
# the two weighted diplomacy/organization ties change those channels' full record: raise cap0 so the baseline holds
for ch in ('diplomacy', 'organization'):
    V['cap0'][C[ch]] = round(V['cap0'][C[ch]] + sum(e[4] for e in V['edges'][-12:] if e[2] == C[ch] and e[0] in ('macdonald_letter', 'mandate')), 4)
out = s[:k] + json.dumps(D, ensure_ascii=False).replace('</', '<\\/') + s[end:]
for a, b in [("<h4>The eight channels</h4>", "<h4>The nine channels</h4>"),
             ("<h3 class=\"vsec\">The eight channels</h3>", "<h3 class=\"vsec\">The nine channels</h3>")]:
    assert a in out, a
    out = out.replace(a, b)
open(P, 'w', encoding='utf-8').write(out)
print('pass 2 applied; land held', V['cap0'][-1], 'thousand dunams')
