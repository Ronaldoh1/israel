#!/usr/bin/env python3
"""Every Rothschild and the Zionist Organization (27 Nov 2026). Adds the documented ties the map lacked between the family's
branches and the Zionist movement, and gives the Balfour Declaration and the Mandate their documented causes in the
cause-and-effect reading (tools/patch_causes.py), so the London network's part in them is counted cause by cause.
Writes the page and the saved model. Idempotent.

Usage: python3 tools/patch_roth_wzo.py [road-network.html]"""
import json, os, sys
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'road-network.html')
SNAP = os.path.join(ROOT, 'book', 'plan', 'road_map', 'model_full.json')
J = lambda u, t: {'t': t, 'u': u}
JTA = 'https://www.jta.org/archive/'
B100 = J('https://www.balfour100.com/biography/lionel-walter-rothschild/', 'Balfour 100, Lionel Walter Rothschild')
HZ11 = J('https://www.herzlonline.org/en/diaries/h1-h82-diary-11/', 'Herzl, Diary 11 (April-July 1902), Herzl Online')
EJ_JAMES = J('https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/rothschild-james-armand-de', 'Encyclopaedia Judaica, Rothschild, James Armand de')
ZC = J('https://en.wikipedia.org/wiki/Zionist_Commission', 'Wikipedia, Zionist Commission')
EJ_ED = J('https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/rothschild-baron-edmond-james-de', 'Encyclopaedia Judaica, Rothschild, Baron Edmond James de')
WBD = 'https://en.wikipedia.org/wiki/Balfour_Declaration'
NODES = [{'id': 'zionist_comm_1918', 'name': 'Zionist Commission (1918)', 'kind': 'institution', 'cluster': 'zionist',
          'note': 'Sent to Palestine in March 1918, with the British government\'s consent, to advise the British authorities on carrying out the Balfour Declaration. Chaired by Weizmann.'}]
EDGES = [
 ('walter_r', 'efz', 'leadership', 'President of the English Zionist Federation when the Balfour letter was addressed to him, November 1917; he had declared for Zionism in The Times on 28 May 1917.', [B100]),
 ('walter_r', 'balfour_decl', 'drafting', '19 June 1917: Balfour asked Walter and Weizmann for a formula acceptable to the Zionists; on 18 July Walter sent it, "the formula you asked me for". Balfour wrote the final text.', [B100]),
 ('natty', 'herzl', 'meeting', 'July 1902: Herzl met Lord Rothschild in London and laid out his plan and its finances to him; he also testified before the Royal Commission on Alien Immigration, on which Rothschild sat. Rothschild refused (his letter of 18 August).', [HZ11]),
 ('natty', 'walter_r', 'kinship', 'Natty came round to Zionism only shortly before his death in 1915; his sons Walter and Charles were Zionists.', [B100]),
 ('james_armand', 'zionist_comm_1918', 'membership', '1918: seconded to the Zionist Commission as its liaison officer when it reached Palestine.', [EJ_JAMES]),
 ('weizmann', 'zionist_comm_1918', 'leadership', 'Chaired the Commission.', [ZC]),
 ('zionist_comm_1918', 'wzo', 'branch', 'The Zionist movement\'s commission in Palestine, the forerunner of its executive there.', [ZC]),
 ('lionel_1882', 'jewish_agency', 'opposition', 'May 1929: as president of the anti-Zionist League of British Jews, declined to join the enlarged Jewish Agency.', [J(JTA + 'montefiore-and-rothschild-state-reasons-for-not-joining-agency', 'JTA, 9 May 1929')]),
 ('edmond_r', 'wzo', 'collaboration', 'May 1929: having opposed the plan a year before, congratulated Weizmann on enlarging the Jewish Agency; chosen its honorary president.', [J('https://jta.org/archive/baron-edmond-rothschild-concurs-in-plan-to-extend-jewish-agency', 'JTA, 27 May 1929'), EJ_ED]),
 ('edmond_r', 'jewish_agency', 'funding', 'February 1931: as honorary president, answered Weizmann\'s appeal for help with the Agency\'s finances favourably (sum not reported).', [J(JTA + 'baron-edmond-de-rothschild-responds-to-dr-weizmanns-appeal-for-help-for-jewish-agency-in-view-of-p', 'JTA, 3 Feb 1931')]),
]
CAUSES = [
 ['war_cabinet', 'balfour_decl', 1, 'The War Cabinet approved the declaration on 31 October 1917.', WBD],
 ['lloydgeorge', 'balfour_decl', 0, 'Lloyd George\'s government sought it for its war aims.', WBD],
 ['balfour', 'balfour_decl', 0, 'Balfour wrote and sent it.', WBD],
 ['sykes', 'balfour_decl', 0, 'Sykes brought the Zionist leaders and the government together in 1917.', WBD],
 ['samuel', 'balfour_decl', 0, 'Samuel\'s 1915 memorandum first put a Jewish Palestine under Britain to the Cabinet.', WBD],
 ['weizmann', 'balfour_decl', 0, 'Weizmann led the Zionist negotiation.', WBD],
 ['sokolow', 'balfour_decl', 0, 'Sokolow negotiated with London, Paris and Rome.', WBD],
 ['walter_r', 'balfour_decl', 0, 'Walter drafted the Zionist formula with Weizmann and received the letter, as head of the English Zionist Federation.', B100['u']],
 ['james_armand', 'balfour_decl', 0, 'James worked with Weizmann and brought him to the wider family.', 'https://www.ramat-hanadiv.org.il/en/content/generalpage/james-armand-de-rothschild-1878-1957'],
 ['rozsika_r', 'balfour_decl', 0, 'Rozsika brought Weizmann\'s case to Charles and Walter.', 'https://en.wikipedia.org/wiki/R%C3%B3zsika_Rothschild'],
 ['dorothy', 'balfour_decl', 0, 'Dorothy, enlisted by Weizmann in 1914, carried his letters into political circles.', 'https://www.thejc.com/news/features/a-family-that-helped-build-a-new-nation-kkakggbe'],
 ['edmond_r', 'balfour_decl', 0, 'After Weizmann\'s visit in 1914 Edmond aided him and Sokolow during the war (one reference account says he stayed apart).', EJ_ED['u']],
 ['balfour_decl', 'mandate', 0, 'The Mandate wrote the declaration into its preamble.', 'https://en.wikipedia.org/wiki/Mandate_for_Palestine'],
 ['san_remo', 'mandate', 0, 'The San Remo conference gave the mandate to Britain in 1920.', 'https://en.wikipedia.org/wiki/Mandate_for_Palestine'],
 ['league', 'mandate', 0, 'The League of Nations confirmed it in 1922.', 'https://en.wikipedia.org/wiki/Mandate_for_Palestine'],
]

def apply(D):
    ids = {n['id'] for n in D['nodes']}
    for n in NODES:
        if n['id'] not in ids: D['nodes'].append(dict(n))
    have = {(e['f'], e['t'], e['type']) for e in D['edges']}
    for f, t, ty, lab, refs in EDGES:
        if (f, t, ty) not in have:
            D['edges'].append({'n': 1, 'sec': '', 'f': f, 't': t, 'type': ty, 'status': 'verified', 'src': '', 'label': lab, 'refs': refs})
    C = D['viab'].setdefault('causes', [])
    seen = {(c[0], c[1]) for c in C}
    for c in CAUSES:
        if (c[0], c[1]) not in seen: C.append(c)
    D['roth_wzo'] = True

s = open(P, encoding='utf-8').read()
k = s.find('const DATA = ') + len('const DATA = ')
D, end = json.JSONDecoder().raw_decode(s, k)
if not D.get('roth_wzo'):
    apply(D); open(P, 'w', encoding='utf-8').write(s[:k] + json.dumps(D, ensure_ascii=False) + s[end:]); print('page updated')
S = json.load(open(SNAP, encoding='utf-8'))
if not S.get('roth_wzo'):
    apply(S); json.dump(S, open(SNAP, 'w', encoding='utf-8'), ensure_ascii=False); print('saved model updated')
