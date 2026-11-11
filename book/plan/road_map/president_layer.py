"""The presidents layer: Roosevelt's hidden illness and the 1944 vice-presidential choice, Wallace's documented position, Feinberg's
own account of the 1948 money, and Wilson's hidden stroke (1919) as the comparable case. Writes president_layer.json and
book/research/road_president_layer.json. 'reported' where the cited page reports a concern or claim rather than a documented act."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '../../..'))
sys.path.insert(0, HERE)
S = {
 'p_navy': ('US Navy Medicine: The President\'s Vital Signs, a look back at FDR\'s heart health', 'https://www.med.navy.mil/Media/News/Article/2609204/the-presidents-vital-signs-a-look-back-at-fdrs-heart-health/'),
 'p_hist_fdr': ('History.com: FDR\'s health in his final term', 'https://www.history.com/news/franklin-d-roosevelt-health-final-term'),
 'p_wp_1944': ('Wikipedia: 1944 Democratic National Convention', 'https://en.wikipedia.org/wiki/1944_Democratic_National_Convention'),
 'p_wp_wallace': ('Wikipedia: Henry A. Wallace', 'https://en.wikipedia.org/wiki/Henry_A._Wallace'),
 'p_aish_wallace': ('Aish: Stars of David, Henry Wallace', 'https://aish.com/stars-of-david-henry-wallace/'),
 'p_truman_feinberg': ('Truman Library: Oral history interview with Abraham Feinberg (23 Aug 1973)', 'https://trumanlibrary.gov/oralhist/feinberg.htm'),
 'p_hist_wilson': ('History.com: Woodrow Wilson\'s hidden stroke', 'https://www.history.com/articles/president-hidden-stroke-woodrow-wilson'),
}
V, R = 'verified', 'reported'
E = []
def add(f, t, ty, st, src, lab): E.append((f, t, ty, st, src, lab))
add('fdr', 'fdr_health', 'association', V, 'p_navy; p_hist_fdr', '28 Mar 1944: Navy cardiologist Howard Bruenn found hypertension and "acute congestive heart failure"; his condition was kept "a guarded secret". Blood pressure up to 240/130 in March 1945. Died 12 Apr 1945 of a cerebral hemorrhage, 82 days into his fourth term.')
add('fdr_health', 'conv1944', 'influence', R, 'p_hist_fdr', '"Concerns about Roosevelt\'s health among other Democratic leaders turned the question of his running mate in 1944 into a matter of much debate." A memo by Dr. Frank Lahey (10 July 1944), unpublished for six decades, predicted he would not finish another term.')
add('wallace', 'conv1944', 'association', V, 'p_wp_1944', 'Roosevelt\'s preferred running mate and popular with rank-and-file Democrats; first ballot Wallace 429.5, Truman 319.5. Party leaders thought him too far left and too close to labor.')
add('wallace', 'bengurion', 'meeting', V, 'p_aish_wallace', 'Oct 1947: on a trip to Palestine Wallace met Ben-Gurion and Begin and predicted the Zionists would make the Negev "a veritable garden".')
add('wallace', 'truman', 'pressure', V, 'p_wp_wallace; p_aish_wallace', '1948: "a supporter of Zionism", Wallace promised to end the arms embargo on Israel and accused Truman of "playing politics with the lives of the people of Israel".')
add('feinberg', 'truman', 'funding', V, 'p_truman_feinberg', 'Sept 1948, in Feinberg\'s own account: "I will pledge on behalf of Ed Kaufmann and myself that within two weeks we\'ll have $100,000 towards this trip"; donors understood that "without Truman, Israel would have had very difficult days". He also said the trip "would have been made one way or another".')
add('wilson', 'wilson_stroke', 'association', V, 'p_hist_wilson', '2 Oct 1919: a massive stroke left his left side paralyzed; the White House never acknowledged it, and it was hidden from the Cabinet, Congress and the public. Edith Wilson controlled access to him; he never fully resumed his duties and left office in 1921.')
NOTES = {
 'fdr_health': 'Roosevelt\'s heart failure, diagnosed in March 1944 and kept secret; he died on 12 April 1945. The closest earlier case is Woodrow Wilson\'s hidden stroke of 1919.',
 'wilson_stroke': 'Woodrow Wilson\'s stroke (2 Oct 1919), concealed from the Cabinet, Congress and the public; the comparable case to Roosevelt\'s hidden illness.',
}
NEW = '''fdr_health|Roosevelt's hidden heart failure (1944-45)|event|us government|congestive heart failure
wilson_stroke|Wilson's hidden stroke (1919)|event|us government|Wilson's stroke
'''

def main():
    import registry
    ids = {n['id'] for n in registry.load()}
    bad = [(f, t) for f, t, *_ in E if f not in ids or t not in ids]; assert not bad, bad
    json.dump({'_note': 'Presidents layer (Nov 2026). Built by president_layer.py; do not edit by hand.', 'node_notes': NOTES,
               'edges': [{'f': f, 't': t, 'type': ty, 'status': st, 'src': src, 'label': lab} for f, t, ty, st, src, lab in E]},
              open(os.path.join(HERE, 'president_layer.json'), 'w'), ensure_ascii=False, indent=1)
    entry = {'id': 'road_president_layer', 'stage': 'rd3', 'topic': 'Presidents layer: Roosevelt\'s hidden illness and the 1944 choice of running mate, Wallace\'s position, Feinberg\'s account of the 1948 money, Wilson\'s hidden stroke (Nov 2026)',
             'claims': [lab for *_, lab in E], 'sources': [{'key': k, 'url': u, 'label': l, 'kind': 'web'} for k, (l, u) in S.items()]}
    json.dump({'volume': 'road_president_layer', 'verified': '2026-11-05', 'entries': [entry]}, open(os.path.join(REPO, 'book/research/road_president_layer.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(E), 'ties')

if __name__ == '__main__':
    if '--registry' in sys.argv:
        s = open(os.path.join(HERE, 'registry.py')).read()
        if 'Presidents layer' not in s:
            i = s.rindex('"""'); s = s[:i] + '# ---------- Presidents layer (added Nov 2026) ----------\n' + NEW + s[i:]
            open(os.path.join(HERE, 'registry.py'), 'w').write(s); print('registry updated')
    else: main()
