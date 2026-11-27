#!/usr/bin/env python3
"""Epstein map: link the ties that named an outlet but carried no address (27 Nov 2026).
Every replacement below is a research key already in book/research or an address found by search on 27 Nov 2026.
Internal working notes ("to pull", "Project doc triangle", "inference", "Part Eight") are dropped or replaced with a real
record. Two ties are removed: Hillary Clinton -> Bill Clinton ("probably knew", an inference from marriage alone: a spouse's
record is never the subject's own) and Woody Allen -> Steve Bannon (no report of the offer could be found).
Family and appointment ties marked only "public record" get a reference page. Idempotent.
Run after build_data.py, before build_explorer.py."""
import json, os, re
ROOT = os.path.join(os.path.dirname(__file__), '..')
P = os.path.join(ROOT, 'book', 'plan', 'epstein_map', 'network.json')
W = 'https://en.wikipedia.org/wiki/'
USVI = 'https://www.justice.gov/epstein/doj-disclosures/court-records-government-united-states-virgin-islands-v-jpmorgan-chase-bank-na-no-122-cv-10904-sdny-2022'
KELLEN = 'Forbes, Epstein\'s longtime assistant Sarah Kellen testifies to Congress, 21 May 2026: https://www.forbes.com/sites/alisondurkee/2026/05/21/epsteins-longtime-assistant-sarah-kellen-testifies-to-congress-today-arguing-shes-also-a-victim/'
GETTY = 'Getty Images (Davidoff Studios), Trump, Knauss, Epstein and Maxwell at Mar-a-Lago, Feb 2000: https://www.gettyimages.com/detail/news-photo/american-real-estate-developer-donald-trump-and-his-news-photo/1192977800'
AJ66 = 'Al Jazeera, citing Drop Site, Israel installed security at Epstein\'s Manhattan apartment for ex-PM Barak, 19 Feb 2026: https://www.aljazeera.com/news/2026/2/19/israel-installed-security-at-epsteins-manhattan-apartment-for-ex-pm-barak'
REP = {  # source part -> replacement ('' drops it)
 'Reuters, Mar 2026': 'vt11_reuters_aidan',
 'Bloomberg/Reuters, Mar 2026': 'vt11_pnf_aidan; vt11_reuters_aidan',
 'The Star/AFP, 18 Feb 2026': 'Malay Mail/AFP, France orders probe after emails show French diplomat exchanged documents with Epstein, 12 Feb 2026: https://www.malaymail.com/news/world/2026/02/12/france-orders-probe-after-emails-show-french-diplomat-exchanged-documents-with-epstein/208927; French Foreign Ministry, Epstein files: situation of Fabrice Aidan, 24 Mar 2026: https://www.diplomatie.gouv.fr/en/the-ministry-and-its-network/news/article/epstein-files-situation-of-fabrice-aidan-24-03-26',
 'PBS/AP, Feb 2026': 'ep5_cnn_mandelson_arrest; ep5_itv_mandelson_bail',
 'Washington Times/AP, 19 Feb 2026': 'ep4_aj_arrests2026',
 'Fox/ABC, Feb 2026': 'ABC7/ABC News, Bill Clinton faces questions in House Oversight Epstein probe, 27 Feb 2026: https://abc7.com/post/bill-clinton-faces-questions-house-oversight-committee-epstein-probe/18657077/',
 'CBS, Feb 2026': 'ep4_ap_hillary2026',
 'her statement, 26 Feb 2026 (AOL/AP)': 'ep4_ap_hillary2026',
 '2019 unsealing': 'CBS News, newly unsealed documents in the Epstein case, 9 Aug 2019: https://cbsnews.com/news/jeffrey-epstein-case-newly-unsealed-documents-reveal-more-alleged-high-powered-connections-2019-08-09',
 'Gates statements': 'ep4_cbs_gates_musk',
 'ABC/AP, Aug 2025': 'ABC7/AP, Bureau of Prisons moves Ghislaine Maxwell to prison camp in Texas, 1 Aug 2025: https://abc7.com/post/bureau-prisons-moves-ghislaine-maxwell-prison-camp-texas/17391720/',
 'IBTimes, 29 Oct 2026': 'ep9_clearinghouse_phang',
 'AP, 10 Mar 2026': 'ep10_pbs_search2026', 'AP, Mar 2026': 'ep10_pbs_search2026',
 'Newsweek, 6 Oct 2026': 'ep11_newsweek_andriesz2026',
 'IBTimes, 5 Oct 2026': 'IBTimes UK, Epstein whistleblower dies after FBI declined to investigate his Lutnick tip, Oct 2026: https://www.ibtimes.co.uk/simon-andriesz-lutnick-epstein-files-1823598',
 'Irish Times, 22 Jul 2026': 'ep11_cp24_siad2026',
 'Washington Times, 18 May 2026': 'ep11_wt_noel2026',
 'NYT via NBC, Jun 2026': 'ep11_nyt_nbcps2026',
 'CBS, May 2026': 'ep4_ap_lutnick2026',
 'CBS, 11 Feb 2026': 'ep11_cbs_minute2026; Anadolu Agency, FBI destroyed original Epstein jail footage before releasing rebuilt version, Feb 2026: https://aa.com.tr/en/americas/fbi-destroyed-original-epstein-jail-footage-before-releasing-rebuilt-version/3827648',
 'Political.org, 2 Oct 2026': 'ep11_political_freeman2026',
 'Daily Beast 2019': 'The Daily Beast via Yahoo, Who murdered the lawyer of Victoria\'s Secret billionaire Les Wexner?, 2019: https://news.yahoo.com/murdered-lawyer-victoria-secret-billionaire-034921344.html',
 'PolitiFact, Feb 2023': 'ep11_politifact_middleton',
 'DOJ memo Dec 2019 via ABC, Jun 2026': KELLEN, 'Forbes, May 2026': KELLEN,
 'PBS, Jun 2026': 'PBS NewsHour, Who is Lesley Groff, Jun 2026: https://www.pbs.org/newshour/politics/who-is-lesley-groff-jeffrey-epsteins-former-assistant-being-interviewed-in-house-probe',
 '2010 conviction record': 'IBTimes UK, 2009 FBI sting video shows former butler selling the victim list, 2026: https://www.ibtimes.co.uk/epstein-butler-sting-video-reveals-network-1780349',
 'deposition': 'EFTA00159180', 'DOJ trial prep 2021': '',
 'ABC, 4 Jun 2026': 'ABC7/ABC News, Lawmakers ask DOJ to probe additional alleged abusers named by ex-Epstein assistant, 4 Jun 2026: https://abc7.com/post/lawmakers-ask-doj-probe-additional-alleged-abusers-named-ex-epstein-assistant/19234492/',
 'Getty/Davidoff': GETTY, 'Getty/Davidoff photo': GETTY,
 'Washington Times, 10 Apr 2026': 'The Washington Times, 9 Apr 2026: https://www.washingtontimes.com/news/2026/apr/9/melania-trump-not-epsteins-victim/; ABC7, What we know about Melania Trump and Jeffrey Epstein, Apr 2026: https://abc7ny.com/post/what-know-melania-trump-jeffrey-epstein/18866087/',
 '2002 email': 'AOL, Melania Trump denies ties to Epstein associate. What do emails show?, Apr 2026: https://www.aol.com/articles/melania-trump-denies-ties-epstein-215811225.html',
 'Fox Oct 2025': 'CBS News, Melania Trump denies relationship with Epstein, Apr 2026: https://www.cbsnews.com/news/melania-trump-jeffrey-epstein-relationship-denial/',
 'Spectrum Oct 2026': 'Spectrum News, House Judiciary Democrats\' report on Trump and Epstein, 26 Oct 2026: https://spectrumnews1.com/ky/louisville/politics/2026/10/26/trump-epstein-house-judiciary-committee-democrats-report',
 'Senate Finance (Wyden), Feb–Mar 2026': 'ep15_sfc_wydendea2026',
 'ABC, 25 Feb 2026': 'ep15_abc_evidence2026', 'Yahoo/ABC, 2026': 'ep15_abc_evidence2026',
 'NY1, 27 Mar 2026': 'NY1, computers taken from the Palm Beach home in 2005 before the police search, 27 Mar 2026: https://ny1.com/nyc/all-boroughs/politics/2026/03/27/epstein-files-computers-taken-palm-beach-home-2005-before-police-search-private-investigators-',
 'Kahn testimony via AOL, 2026': 'ep7_aol_kahn2026',
 'KOB, 5 Aug 2026': 'ep10_kob_interim2026',
 'Forbes, Jul 2025': 'Forbes, Epstein\'s properties have all been sold, 22 Jul 2025: https://www.forbes.com/sites/giacomotognini/2025/07/22/epsteins-properties-were-allegedly-the-sites-of-sexual-exploitation-now-theyve-all-been-sold/',
 'Bloomberg 2019': 'Bloomberg, The shell game: untangling Jeffrey Epstein\'s offshore money web, 2019: https://www.bloombergquint.com/onweb/the-shell-game-untangling-jeffrey-epstein-s-offshore-money-web',
 'Drop Site via Al Jazeera, 19 Feb 2026': AJ66, 'Drop Site via Al Jazeera': AJ66,
 'Telegraph via Yahoo, 2026': 'Yahoo News, Epstein email reveals plot to install hidden cameras, 2026: https://www.yahoo.com/news/articles/epstein-email-reveals-plot-install-202615670.html',
 'Hunterbrook, 4 Feb 2026': 'Hunterbrook, Ubiquiti Wi-Fi and a surveillance camera on Epstein\'s island, 4 Feb 2026: https://newsletter.hntrbrk.com/p/new-ubiquiti-wi-fi-and-surveillance',
 'Guardian': 'ep2_aj_brunel2022',
 'Part Eight': 'DOJ Office of Professional Responsibility, report on the 2007-08 Epstein investigation, Nov 2020: https://www.justice.gov/opr/page/file/1336471/dl',
 'USVI v. JPMorgan': 'DOJ Epstein Library, court records of USVI v. JPMorgan Chase (S.D.N.Y. 2022): ' + USVI,
 'JPMorgan Exhibit 175': 'USVI v. JPMorgan, Exhibit 175 (Doc. 285-41), in the DOJ Epstein Library\'s court records: ' + USVI, 'Doc. 285-41': '',
 'Pulitzer/WSJ summary': 'USVI v. JPMorgan, Doc. 238-31 (DOJ Epstein Library): https://www.justice.gov/multimedia/Court%20Records/Government%20of%20the%20United%20States%20Virgin%20Islands%20v.%20JPMorgan%20Chase%20Bank%2C%20N.A.%2C%20No.%20122-cv-10904%20%28S.D.N.Y.%202022%29/238-31.pdf',
 'CBS News reporting on DEA memo, 2026': 'ep15_cbs_dea_ice2026',
 'NYDFS Deutsche Bank consent order, paras. 28–30': 'NYDFS, press release on the Deutsche Bank consent order, 7 Jul 2020: https://www.dfs.ny.gov/reports_and_publications/press_releases/pr202007071; NYDFS consent order, paras. 28-30 (copy): https://www.nakedcapitalism.com/wp-content/uploads/2020/07/00-DFS-Deutsche-Bank-Order.pdf',
 'Fortune review of Deutsche Bank trust timeline and KYC records': 'Fortune, The Butterfly Trust: how Deutsche Bank kept Epstein as a client, 17 May 2026: https://fortune.com/2026/05/17/jeffrey-epstein-butterfly-trust-deutsche-bank-fraud-nydfs-christian-sewing/',
 'Valéria Chomsky public statement, 7 Feb 2026': 'Valéria Chomsky, official statement, 7 Feb 2026: https://starscholars.org/wp-content/uploads/2026/02/OFFICIAL-STATEMENT-FROM-VALERIA-CHOMSKY-REGARDING-JEFFREY-EPSTEIN-February.07.2026.pdf; The Irish Times, 9 Feb 2026: https://www.irishtimes.com/world/us/2026/02/09/noam-chomskys-wife-apologises-for-their-grave-mistake-in-epstein-ties/',
 # working notes
 'to pull': '', 'files to pull': '', 'FBI file to pull': '', 'originals to pull': '', 'Project doc triangle': '', 'release reporting': '',
}
PAIR = {  # per-tie replacements for "Maxwell trial record, 2021" and "public record"
 ('alessi', 'palm_beach'): 'ep15_upi_alessi2021',
 ('visoski', 'epstein'): 'NBC New York, Epstein\'s pilot testifies at the Maxwell trial, 30 Nov 2021: https://www.nbcnewyork.com/news/national-international/jeffrey-epstein-pilot-says-he-never-saw-sex-acts-on-flights-during-maxwell-trial-testimony/3426221/',
 ('visoski', 'flight_logs'): 'NBC New York, Epstein\'s pilot testifies at the Maxwell trial, 30 Nov 2021: https://www.nbcnewyork.com/news/national-international/jeffrey-epstein-pilot-says-he-never-saw-sex-acts-on-flights-during-maxwell-trial-testimony/3426221/',
 ('rodgers', 'flight_logs'): 'EFTA00159180',
 ('ferguson', 'andrew'): 'Wikipedia, Sarah, Duchess of York: ' + W + 'Sarah,_Duchess_of_York',
 ('trump', 'patel'): 'Wikipedia, Kash Patel: ' + W + 'Kash_Patel',
 ('patel', 'fbi'): 'Wikipedia, Director of the FBI: ' + W + 'Director_of_the_Federal_Bureau_of_Investigation',
 ('bop', 'doj'): 'Wikipedia, Federal Bureau of Prisons: ' + W + 'Federal_Bureau_of_Prisons',
 ('mcc', 'bop'): 'Wikipedia, Metropolitan Correctional Center, New York: ' + W + 'Metropolitan_Correctional_Center,_New_York',
 ('melania', 'trump'): 'Wikipedia, Melania Trump: ' + W + 'Melania_Trump',
 ('dpnr', 'usvi'): 'Wikipedia, Government of the United States Virgin Islands: ' + W + 'Government_of_the_United_States_Virgin_Islands',
 ('mark_epstein', 'epstein'): 'Wikipedia, Jeffrey Epstein: ' + W + 'Jeffrey_Epstein',
 ('kushner', 'trump'): 'Wikipedia, Jared Kushner: ' + W + 'Jared_Kushner',
 ('deutsche', 'deutsche_us'): 'Wikipedia, Deutsche Bank: ' + W + 'Deutsche_Bank',
 ('bofa', 'merrill'): 'Wikipedia, Merrill (company): ' + W + 'Merrill_(company)',
 ('hclinton', 'bclinton'): 'Wikipedia, Hillary Clinton: ' + W + 'Hillary_Clinton',
 ('bmo', 'ap_narrows_account'): 'EFTA00592208',
 ('jpm', 'bear'): 'Wikipedia, Bear Stearns: ' + W + 'Bear_Stearns',
}
LABEL = {  # wording that went past the record
 ('paris_prosecutor', 'aidan'): 'inquiry opened after the Foreign Ministry\'s referral, Feb 2026',
 ('uk_police', 'mandelson'): 'arrested Feb 2026; released under investigation, Mar 2026',
 ('andriesz', 'fbi'): 'tips 2020-21; "no interest" (his account)',
 ('npa', 'npa_deliberations'): 'deliberations reviewed by DOJ\'s Office of Professional Responsibility (2020); the internal records are not public',
}
DROP = {('hclinton', 'bclinton', "knowledge of spouse's connection"), ('allen', 'bannon', None)}
DOCTIE = re.compile(r'^doc_efta(\d{8})$')

D = json.load(open(P, encoding='utf-8'))
out = []
for e in D['edges']:
    if any(e['f'] == a and e['t'] == b and (t is None or e['type'] == t) for a, b, t in DROP):
        if (e['f'], e['t']) == ('allen', 'bannon') and 'footage' not in e['label']: out.append(e); continue
        continue
    parts = [p.strip() for p in e['src'].split(';') if p.strip()]
    new = []
    for p in parts:
        if (p in ('Maxwell trial record, 2021', 'public record') or (e['f'], e['t']) == ('bmo', 'ap_narrows_account')) and (e['f'], e['t']) in PAIR: p = PAIR[(e['f'], e['t'])]
        elif p in REP: p = REP[p]
        elif p in ('inference', 'see ep_OPERATIONS Part E'): p = ''
        elif p in ('Yirah document index', 'Epstein-research repository', 'Yirah / DOJ document index'):
            m = DOCTIE.match(e['t']); p = p + ('; EFTA' + m.group(1) if m else '')
        new += [x.strip() for x in p.split(';') if x.strip()]
    seen = []; [seen.append(x) for x in new if x not in seen]
    if seen: e['src'] = '; '.join(seen)
    if (e['f'], e['t']) in LABEL: e['label'] = LABEL[(e['f'], e['t'])]
    out.append(e)
print('ties', len(D['edges']), '->', len(out))
D['edges'] = out
json.dump(D, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
