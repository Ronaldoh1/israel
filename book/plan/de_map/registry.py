"""Canonical nodes for the Dark Enlightenment network (the eight volumes of The Dark Enlightenment series).
Each line: id | name | kind | cluster | aliases (regex, ';'-separated; case-sensitive).
Kinds: person, company, institution, government, document, event.
An ideology map: nodes are named people, organizations, texts, funds, offices, cases and events. Never a group of
"followers", "believers" or an identity group; a person is tied to a text only by authorship, citation, publication,
funding, employment or their own statement. Journalists and outlets cited as sources are not nodes."""

RAW = r"""
# ---------- the thinkers and their texts ----------
yarvin|Curtis Yarvin (Mencius Moldbug)|person|thinkers|Curtis Yarvin;Yarvin;Mencius Moldbug;Moldbug
land|Nick Land|person|thinkers|Nick Land;Land(?=['’]s\b);Land(?= (?:wrote|argued|says|said|left|moved|was|is|called|calls|published|describes|described|taught|teaches|co-founded|founded|lived|lives|writes|had|has|put|treats|treated|added|coined|meant|means|uses|used|took|takes|named|names|framed|frames|answered|answers|did|does|never|also)\b)
hoppe|Hans-Hermann Hoppe|person|thinkers|Hans-Hermann Hoppe;Hoppe
carlyle|Thomas Carlyle|person|thinkers|Thomas Carlyle;Carlyle(?!['’]s Latter)
hirschman|Albert O. Hirschman|person|thinkers|Albert O\. Hirschman;Albert Hirschman;Hirschman
jburnham|James Burnham|person|thinkers|James Burnham
girard|René Girard|person|thinkers|René Girard;Rene Girard;Girard
schmitt|Carl Schmitt|person|thinkers|Carl Schmitt;Schmitt
strauss|Leo Strauss|person|thinkers|Leo Strauss
rothbard|Murray Rothbard|person|thinkers|Murray Rothbard;Rothbard
anton|Michael Anton|person|thinkers|Michael Anton;Anton(?=['’]s\b|\b (?:wrote|argued|said|was|is|called|published|became|served|left))
srinivasan|Balaji Srinivasan|person|exit|Balaji Srinivasan;Srinivasan
patri|Patri Friedman|person|exit|Patri Friedman
mfriedman|Milton Friedman|person|thinkers|Milton Friedman
plant|Sadie Plant|person|thinkers|Sadie Plant
ccru|Cybernetic Culture Research Unit (CCRU)|institution|thinkers|Cybernetic Culture Research Unit;CCRU
warwick|University of Warwick|institution|thinkers|University of Warwick;Warwick(?! Business)
ur|Unqualified Reservations (blog, 2007–2014)|document|texts|Unqualified Reservations
formalist|A Formalist Manifesto (Yarvin, 2007)|document|texts|A Formalist Manifesto;Formalist Manifesto
openletter|An Open Letter to Open-Minded Progressives (Yarvin, 2008)|document|texts|Open Letter to Open-Minded Progressives;Open-Minded Progressives
patchwork|Patchwork (Yarvin, 2008)|document|texts|Patchwork: A Positive Vision;Patchwork essay
whycarlyle|Why Carlyle Matters (Yarvin)|document|texts|Why Carlyle Matters
de_text|The Dark Enlightenment (Land, 2012)|document|texts|Land['’]s (?:2012 )?(?:text|essay|series)|The Dark Enlightenment(?= \((?:Land|2012))|The Dark Enlightenment['’]s? (?:essay|series|text)
graymirror|Gray Mirror (Yarvin's Substack)|document|texts|Gray Mirror
godthatfailed|Democracy: The God That Failed (Hoppe, 2001)|document|texts|Democracy: The God That Failed;The God That Failed
exitvoice|Exit, Voice, and Loyalty (Hirschman, 1970)|document|texts|Exit, Voice, and Loyalty
managerialrev|The Managerial Revolution (Burnham, 1941)|document|texts|The Managerial Revolution
eduoflib|The Education of a Libertarian (Thiel, 2009)|document|texts|The Education of a Libertarian
straussian|The Straussian Moment (Thiel, 2007)|document|texts|The Straussian Moment
zerotoone|Zero to One (Thiel, 2014)|document|texts|Zero to One
diversitymyth|The Diversity Myth (Thiel and Sacks, 1995)|document|texts|The Diversity Myth
hillbilly|Hillbilly Elegy (Vance, 2016)|document|texts|Hillbilly Elegy
networkstate|The Network State (Srinivasan, 2022)|document|texts|The Network State
technomanifesto|The Techno-Optimist Manifesto (Andreessen, 2023)|document|texts|Techno-Optimist Manifesto
cato_unbound|Cato Unbound|institution|texts|Cato Unbound
cato|Cato Institute|institution|think tanks|Cato Institute
tablet|Tablet (magazine)|institution|media|Tablet(?! (?:magazine reported|reported))
american_mind|The American Mind / Claremont Institute|institution|think tanks|Claremont Institute;Claremont;The American Mind
natcon|National Conservatism conference (Edmund Burke Foundation)|event|think tanks|National Conservatism(?: [Cc]onference)?;NatCon;Edmund Burke Foundation
heritage|Heritage Foundation|institution|think tanks|Heritage Foundation;Project 2025
technocracy_inc|Technocracy Incorporated|institution|thinkers|Technocracy Incorporated;Technocracy Inc\.?
haldeman|Joshua N. Haldeman|person|musk network|Joshua Haldeman;Joshua N\. Haldeman;Haldeman
# ---------- Thiel and his firms ----------
thiel|Peter Thiel|person|thiel network|Peter Thiel;Thiel(?! (?:Foundation|Capital|Fellowship|Fellows?)\b)
founders_fund|Founders Fund|company|thiel network|Founders Fund
thiel_capital|Thiel Capital|company|thiel network|Thiel Capital
clarium|Clarium Capital|company|thiel network|Clarium Capital;Clarium
mithril|Mithril Capital|company|thiel network|Mithril Capital;Mithril
valar|Valar Ventures|company|thiel network|Valar Ventures;Valar
narya|Narya Capital|company|thiel network|Narya Capital;Narya
thiel_found|Thiel Foundation|institution|thiel network|Thiel Foundation
thiel_fellow|Thiel Fellowship|institution|thiel network|Thiel Fellowship;Thiel Fellows?\b
per_aspera|Per Aspera Policy|institution|politics and money|Per Aspera Policy;Per Aspera
pronomos|Pronomos Capital|company|exit|Pronomos Capital;Pronomos
seasteading|Seasteading Institute|institution|exit|Seasteading Institute
gawker|Gawker Media|company|thiel network|Gawker
bollea|Bollea v. Gawker (Hogan case)|document|courts|Bollea v\. Gawker;Hulk Hogan;Terry Bollea;Bollea
stanford|Stanford University|institution|thiel network|Stanford(?! (?:Review|Law Review))
stanford_review|The Stanford Review|institution|thiel network|Stanford Review
lonsdale|Joe Lonsdale|person|palantir|Joe Lonsdale;Lonsdale
masters|Blake Masters|person|politics and money|Blake Masters;Masters(?= (?:ran|was|is|wrote|lost|won|co-wrote|said|left|served|worked)\b|['’]s\b)
howery|Ken Howery|person|paypal network|Ken Howery;Howery
rabois|Keith Rabois|person|paypal network|Keith Rabois;Rabois
sacks|David O. Sacks|person|paypal network|David Sacks;David O\. Sacks;Sacks(?=['’]s\b|\b (?:was|is|said|wrote|co-wrote|left|served|named|became|hosted|holds|held)\b)
hoffman|Reid Hoffman|person|paypal network|Reid Hoffman;Hoffman(?=['’]s\b)
levchin|Max Levchin|person|paypal network|Max Levchin;Levchin
nosek|Luke Nosek|person|paypal network|Luke Nosek;Nosek
chen|Steve Chen|person|paypal network|Steve Chen
paypal|PayPal|company|paypal network|PayPal
xcom|X.com (Musk's bank, 1999)|company|musk network|X\.com
confinity|Confinity|company|paypal network|Confinity
facebook|Facebook / Meta|company|platforms|Facebook;Meta(?![a-z])(?! (?:AI))
linkedin|LinkedIn|company|platforms|LinkedIn
youtube|YouTube|company|platforms|YouTube
# ---------- Palantir ----------
palantir|Palantir Technologies|company|palantir|Palantir
karp|Alex Karp|person|palantir|Alex Karp;Karp(?=['’]s\b|\b (?:was|is|said|wrote|told|called|has|had)\b)
scohen|Stephen Cohen (Palantir)|person|palantir|Stephen Cohen
gettings|Nathan Gettings|person|palantir|Nathan Gettings
sankar|Shyam Sankar|person|palantir|Shyam Sankar;Sankar
inqtel|In-Q-Tel|company|intelligence|In-Q-Tel;In Q Tel
immigrationos|ImmigrationOS (Palantir for ICE)|document|surveillance|ImmigrationOS
icm|Investigative Case Management (Palantir for ICE)|document|surveillance|Investigative Case Management;\bICM\b
falcon|FALCON (ICE system)|document|surveillance|FALCON
anduril|Anduril Industries|company|defense tech|Anduril
luckey|Palmer Luckey|person|defense tech|Palmer Luckey;Luckey
# ---------- Musk ----------
musk|Elon Musk|person|musk network|Elon Musk;Musk(?!['’]s (?:companies|firms))(?! Foundation)
spacex|SpaceX|company|musk network|SpaceX
starlink|Starlink / Starshield|company|musk network|Starlink;Starshield
tesla|Tesla|company|musk network|Tesla
twitter|Twitter / X|company|musk network|Twitter;X Corp\.?;\bX\b(?= \(formerly Twitter\)| Corp)
xai|xAI (Grok)|company|musk network|xAI;Grok
zip2|Zip2|company|musk network|Zip2
boring|The Boring Company|company|musk network|Boring Company
neuralink|Neuralink|company|musk network|Neuralink
america_pac|America PAC|institution|politics and money|America PAC
rbg_pac|RBG PAC|institution|politics and money|RBG PAC
# ---------- Vance ----------
vance|J.D. Vance|person|vance|J\.D\. Vance;JD Vance;J\. D\. Vance;Vance(?! (?:campaign committee))
protect_ohio|Protect Ohio Values PAC|institution|politics and money|Protect Ohio Values
narya_fund|Narya Capital Fund I|company|vance|Narya Capital Fund I
appharvest|AppHarvest|company|vance|AppHarvest
rumble|Rumble|company|platforms|Rumble
our_ohio|Our Ohio Renewal|institution|vance|Our Ohio Renewal
yale|Yale Law School|institution|vance|Yale Law School;Yale(?! University Press)
# ---------- money and politics ----------
andreessen|Marc Andreessen|person|money|Marc Andreessen;Andreessen(?! Horowitz)(?!['’]s firm)
a16z|Andreessen Horowitz (a16z)|company|money|Andreessen Horowitz;a16z
kupor|Scott Kupor|person|money|Scott Kupor;Kupor
horowitz|Ben Horowitz|person|money|Ben Horowitz
mercer|Robert Mercer|person|money|Robert Mercer;Rebekah Mercer;Mercer(?=['’]s\b|\b family)
uihlein|Richard Uihlein|person|money|Richard Uihlein;Uihlein
donorstrust|DonorsTrust|institution|money|DonorsTrust;Donors Trust
slf|Senate Leadership Fund|institution|politics and money|Senate Leadership Fund
club_growth|Club for Growth|institution|politics and money|Club for Growth
fec|Federal Election Commission|government|politics and money|Federal Election Commission;\bFEC\b
citizens_united|Citizens United v. FEC (2010)|document|courts|Citizens United
speechnow|SpeechNow.org v. FEC (2010)|document|courts|SpeechNow
trump|Donald Trump|person|executive|Donald Trump;President Trump;Trump(?! (?:Organization|Tower|v\.|administration))
trump_admin|Trump administration (2025–)|government|executive|Trump administration;the administration(?= (?:said|announced|argued))
bannon|Steve Bannon|person|politics and money|Steve Bannon;Bannon
rnc|Republican National Committee|institution|politics and money|Republican National Committee;\bRNC\b
# ---------- DOGE ----------
doge|Department of Government Efficiency (DOGE)|government|doge|Department of Government Efficiency;DOGE(?!['’]s? (?:staff|team))
usds|U.S. Digital Service / U.S. DOGE Service|government|doge|U\.S\. Digital Service;US Digital Service;U\.S\. DOGE Service;\bUSDS\b
eo14158|Executive Order 14158 (DOGE, 20 Jan 2025)|document|doge|Executive Order 14158;EO 14158;E\.O\. 14158
sdavis|Steve Davis|person|doge|Steve Davis
gleason|Amy Gleason|person|doge|Amy Gleason;Gleason
elez|Marko Elez|person|doge|Marko Elez;Elez
coristine|Edward Coristine|person|doge|Edward Coristine;Coristine
farritor|Luke Farritor|person|doge|Luke Farritor;Farritor
gracias|Antonio Gracias|person|doge|Antonio Gracias;Gracias
kliger|Gavin Kliger|person|doge|Gavin Kliger;Kliger
ramaswamy|Vivek Ramaswamy|person|doge|Vivek Ramaswamy;Ramaswamy
oneill|Jim O'Neill|person|doge|Jim O['’]Neill;O['’]Neill
kratsios|Michael Kratsios|person|executive|Michael Kratsios;Kratsios
vought|Russell Vought|person|executive|Russell Vought;Russ Vought;Vought
omb|Office of Management and Budget|government|executive|Office of Management and Budget;\bOMB\b
opm|Office of Personnel Management|government|executive|Office of Personnel Management;\bOPM\b
treasury|US Treasury (Bureau of the Fiscal Service)|government|executive|Treasury(?! Secretary)|Bureau of the Fiscal Service
ssa|Social Security Administration|government|executive|Social Security Administration;\bSSA\b
irs|Internal Revenue Service|government|executive|Internal Revenue Service;\bIRS\b
usaid|USAID|government|executive|USAID;U\.S\. Agency for International Development
cfpb|Consumer Financial Protection Bureau|government|executive|Consumer Financial Protection Bureau;\bCFPB\b
gao|Government Accountability Office|government|oversight|Government Accountability Office;\bGAO\b
cms|Centers for Medicare and Medicaid Services|government|executive|Centers for Medicare and Medicaid Services;\bCMS\b
hhs|Health and Human Services|government|executive|Health and Human Services;\bHHS\b
schedule_pc|Schedule Policy/Career (formerly Schedule F)|document|executive|Schedule Policy/Career;Schedule Policy;Schedule F
nspm7|NSPM-7 (Sept 2025)|document|executive|NSPM-7
insurrection|Insurrection Act|document|executive|Insurrection Act
pcast|President's Council of Advisors on Science and Technology|government|executive|PCAST;President['’]s Council of Advisors on Science and Technology
whitehouse|White House|government|executive|White House
# ---------- immigration, surveillance and data ----------
nro|National Reconnaissance Office|government|enforcement|National Reconnaissance Office;\bNRO\b
dhs|Department of Homeland Security|government|enforcement|Department of Homeland Security;\bDHS\b;Homeland Security(?! Investigations)
ice|Immigration and Customs Enforcement (ICE)|government|enforcement|Immigration and Customs Enforcement;\bICE\b(?!Block)
hsi|Homeland Security Investigations|government|enforcement|Homeland Security Investigations;\bHSI\b
ero|ICE Enforcement and Removal Operations|government|enforcement|Enforcement and Removal Operations;\bERO\b
cbp|Customs and Border Protection|government|enforcement|Customs and Border Protection;\bCBP\b;Border Patrol
tsa|Transportation Security Administration|government|enforcement|Transportation Security Administration;\bTSA\b
fbi|FBI|government|enforcement|\bFBI\b;Federal Bureau of Investigation
doj|Justice Department|government|enforcement|Justice Department;Department of Justice;\bDOJ\b
nsa|National Security Agency|government|intelligence|National Security Agency;\bNSA\b
cia|CIA|government|intelligence|\bCIA\b;Central Intelligence Agency
odni|Director of National Intelligence|government|intelligence|Director of National Intelligence;\bODNI\b
pentagon|Department of Defense / Pentagon|government|defense tech|Pentagon;Department of Defense;Department of War;\bDoD\b
army|US Army|government|defense tech|U\.S\. Army;US Army;the Army(?! Corps)
state_dept|State Department|government|executive|State Department;Department of State
geo|GEO Group|company|enforcement|GEO Group;GEO['’]s?\b
corecivic|CoreCivic|company|enforcement|CoreCivic
lexisnexis|LexisNexis Risk Solutions|company|surveillance|LexisNexis;Accurint
thomson|Thomson Reuters (CLEAR)|company|surveillance|Thomson Reuters;\bCLEAR\b
equifax|Equifax (The Work Number)|company|surveillance|Equifax;The Work Number
penlink|Penlink (Tangles, Webloc)|company|surveillance|Penlink;Tangles;Webloc
venntel|Venntel|company|surveillance|Venntel
babel|Babel Street|company|surveillance|Babel Street
clearview|Clearview AI|company|surveillance|Clearview
cellebrite|Cellebrite|company|surveillance|Cellebrite
graykey|Magnet Forensics / GrayKey|company|surveillance|GrayKey;Grayshift;Magnet Forensics
paragon|Paragon Solutions (Graphite)|company|surveillance|Paragon(?! of);Graphite
nso|NSO Group (Pegasus)|company|surveillance|NSO Group;\bNSO\b;Pegasus
flock|Flock Safety|company|surveillance|Flock Safety;Flock(?= (?:cameras|Safety|said|network))
xmode|X-Mode / Outlogic|company|surveillance|X-Mode;Outlogic
oracle|Oracle|company|platforms|Oracle(?!['’]s? (?:of))
microsoft|Microsoft|company|platforms|Microsoft
google|Google|company|platforms|Google
apple|Apple|company|platforms|Apple(?! Valley)
amazon|Amazon / AWS|company|platforms|Amazon(?! (?:rainforest|basin));\bAWS\b
openai|OpenAI|company|platforms|OpenAI
anthropic|Anthropic|company|platforms|Anthropic
hart|HART (DHS biometric system)|document|surveillance|\bHART\b;Homeland Advanced Recognition Technology
save|SAVE (USCIS verification system)|document|surveillance|\bSAVE\b(?! Act)
mobilefortify|Mobile Fortify (ICE face app)|document|surveillance|Mobile Fortify
fisa702|FISA Section 702|document|surveillance|Section 702;FISA
privacyact|Privacy Act of 1974|document|courts|Privacy Act
foia|Freedom of Information Act|document|oversight|Freedom of Information Act;\bFOIA\b
# ---------- exit, charter cities, crypto ----------
tlon|Tlon Corporation|company|exit|Tlon
urbit|Urbit|company|exit|Urbit(?! Foundation)
urbit_found|Urbit Foundation|institution|exit|Urbit Foundation
jburnham_tlon|John Burnham|person|exit|John Burnham
prospera|Próspera (Roatán, Honduras)|company|exit|Próspera;Prospera(?! Inc)
zede|ZEDE law (Honduras)|document|exit|ZEDE;ZEDEs;Zones for Employment and Economic Development
honduras_gov|Honduras (government)|government|foreign states|Honduran (?:government|Congress|Supreme Court);government of Honduras
castro|Xiomara Castro|person|foreign states|Xiomara Castro
milei|Javier Milei|person|foreign states|Javier Milei;Milei
bukele|Nayib Bukele|person|foreign states|Nayib Bukele;Bukele
argentina|Argentina (government)|government|foreign states|Argentine government;government of Argentina
el_salvador|El Salvador (government)|government|foreign states|El Salvador(?:['’]s)? government;Salvadoran government;CECOT
ethereum|Ethereum|company|exit|Ethereum
buterin|Vitalik Buterin|person|exit|Vitalik Buterin;Buterin
# ---------- abroad ----------
israel_gov|Israel (government)|government|foreign states|Israeli government;government of Israel;Israel Defense Forces;\bIDF\b
barak|Ehud Barak|person|foreign states|Ehud Barak;Barak(?=['’]s\b|\b (?:was|is|said|chaired|met)\b)
carbyne|Carbyne (Reporty)|company|surveillance|Carbyne;Reporty
uk_gov|United Kingdom (government)|government|foreign states|UK government;British government;\bNHS\b
epstein|Jeffrey Epstein|person|money|Jeffrey Epstein;Epstein(?!['’]s (?:estate))
china_gov|China (government)|government|foreign states|Chinese government;Chinese Communist Party;\bCCP\b;Beijing(?= (?:said|has|had))
singapore|Singapore (government)|government|foreign states|Singapore(?! (?:and Dubai))
# ---------- courts and cases ----------
scotus|US Supreme Court|government|courts|Supreme Court
slaughter|Trump v. Slaughter (29 June 2026)|document|courts|Trump v\. Slaughter;Slaughter(?= (?:ruling|decision|case))
humphreys|Humphrey's Executor v. US (1935)|document|courts|Humphrey['’]s Executor
chiafalo|Chiafalo v. Washington (2020)|document|courts|Chiafalo
carpenter|Carpenter v. United States (2018)|document|courts|Carpenter v\. United States;Carpenter(?= (?:ruling|decision))
chatrie|United States v. Chatrie|document|courts|Chatrie
murthy|Murthy v. Missouri (2024)|document|courts|Murthy v\. Missouri;Murthy
aclu|American Civil Liberties Union|institution|oversight|American Civil Liberties Union;\bACLU\b
aaup|American Association of University Professors|institution|oversight|American Association of University Professors;\bAAUP\b
congress|US Congress|government|oversight|Congress(?!ional Research)
senate|US Senate|government|oversight|the Senate|Senate(?= (?:confirmed|voted|Finance|Judiciary|Homeland))
house|US House of Representatives|government|oversight|House (?:Oversight|subcommittee|Judiciary|committee)|the House(?! of)
"""


def load():
    nodes = []
    for line in RAW.strip().splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        i, name, kind, cluster, al = [x.strip() for x in line.split('|', 4)]
        aliases = []
        for a in al.split(';'):
            a = a.strip()
            if not a: continue
            stage = None
            if '@' in a: a, stage = a.rsplit('@', 1)
            aliases.append((a, stage))
        nodes.append({'id': i, 'name': name, 'kind': kind, 'cluster': cluster, 'aliases': aliases})
    ids = [n['id'] for n in nodes]
    assert len(ids) == len(set(ids)), [x for x in ids if ids.count(x) > 1]
    return nodes
