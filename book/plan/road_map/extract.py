"""Pass 1: split the Baseline (ch01) and Road to 1948 (rd0-rd6) text into cited sentences and run NER.
Writes mentions.json: [{sec, stage, sent, cites, ents:[[text,label]]}]"""
import json, os, re, glob, html, spacy
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
STAGES = ['ch01'] + ['rd%d' % i for i in range(7)] + ['cw%d' % i for i in range(1, 7)]
nlp = spacy.load('en_core_web_sm', disable=['lemmatizer'])
out = []
for st in STAGES:
    for f in sorted(glob.glob(os.path.join(ROOT, 'book/part1', st, '*.html'))):
        sec = os.path.basename(f)[:-5]
        if sec.startswith('_'): continue
        t = open(f, encoding='utf-8').read()
        t = re.sub(r'<(figure|table)[\s\S]*?</\1>', lambda m: ' '.join(re.sub(r'<[^>]+>', ' ', m.group(0)).split()) + '. ', t)
        for blk in re.findall(r'<(?:p|li|h2|h3|blockquote)[^>]*>([\s\S]*?)</(?:p|li|h2|h3|blockquote)>', t) or [t]:
            txt = html.unescape(re.sub(r'<[^>]+>', '', blk))
            txt = ' '.join(txt.split())
            if not txt: continue
            doc = nlp(re.sub(r'\[cite:[^\]]+\]|\[scene:[^\]]+\]', '', txt))
            cites_all = re.findall(r'\[cite:([^\]]+)\]', txt)
            for s in doc.sents:
                ents = [[e.text, e.label_] for e in s.ents if e.label_ in ('PERSON', 'ORG', 'GPE', 'NORP', 'LAW', 'EVENT', 'FAC', 'LOC', 'WORK_OF_ART')]
                if ents: out.append({'sec': sec, 'stage': st, 'sent': s.text.strip(), 'cites': cites_all, 'ents': ents})
json.dump(out, open('mentions.json', 'w'), ensure_ascii=False)
print(len(out), 'sentences with entities')
