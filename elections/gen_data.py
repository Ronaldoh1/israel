"""Generates the skeleton data for the 2026 Elections module.
Senate nominees: Wikipedia race table, headline-checked Oct 8, 2026 (SC, OK, ME verified
against wire reporting). Every state pass re-verifies before research fills in."""
import json, re
ASOF='2026-10-08'
STATES=[('AL','Alabama',7),('AK','Alaska',1),('AZ','Arizona',9),('AR','Arkansas',4),('CA','California',52),
('CO','Colorado',8),('CT','Connecticut',5),('DE','Delaware',1),('FL','Florida',28),('GA','Georgia',14),
('HI','Hawaii',2),('ID','Idaho',2),('IL','Illinois',17),('IN','Indiana',9),('IA','Iowa',4),('KS','Kansas',4),
('KY','Kentucky',6),('LA','Louisiana',6),('ME','Maine',2),('MD','Maryland',8),('MA','Massachusetts',9),
('MI','Michigan',13),('MN','Minnesota',8),('MS','Mississippi',4),('MO','Missouri',8),('MT','Montana',2),
('NE','Nebraska',3),('NV','Nevada',4),('NH','New Hampshire',2),('NJ','New Jersey',12),('NM','New Mexico',3),
('NY','New York',26),('NC','North Carolina',14),('ND','North Dakota',1),('OH','Ohio',15),('OK','Oklahoma',5),
('OR','Oregon',6),('PA','Pennsylvania',17),('RI','Rhode Island',2),('SC','South Carolina',7),('SD','South Dakota',1),
('TN','Tennessee',9),('TX','Texas',38),('UT','Utah',4),('VT','Vermont',1),('VA','Virginia',11),('WA','Washington',10),
('WV','West Virginia',2),('WI','Wisconsin',8),('WY','Wyoming',1)]
assert sum(s[2] for s in STATES)==435 and len(STATES)==50

# state, incumbent, inc party, incumbent status, type, [(name, party, incumbent?)]
SEN=[
('AL','Tommy Tuberville','R','Not running — seeking governor','regular',[('Barry Moore','R'),('Everett Wess','D')]),
('AK','Dan Sullivan','R','Running','regular',[('Dan Sullivan','R',1),('Mary Peltola','D')]),
('AR','Tom Cotton','R','Running','regular',[('Tom Cotton','R',1),('Hallie Shoffner','D'),('Jeff Wadlin','L')]),
('CO','John Hickenlooper','D','Running','regular',[('John Hickenlooper','D',1),('Mark Baisley','R'),('Blake Huber','L')]),
('DE','Chris Coons','D','Running','regular',[('Chris Coons','D',1),('Michael Katz','R')]),
('FL','Ashley Moody','R','Appointed Jan 2025; running','special',[('Ashley Moody','R',1),('Angie Nixon','D'),('Neil Gillespie','I')]),
('GA','Jon Ossoff','D','Running','regular',[('Jon Ossoff','D',1),('Mike Collins','R')]),
('ID','Jim Risch','R','Running','regular',[('Jim Risch','R',1),('Todd Achilles','I'),('Natalie Fleming','I'),('Matt Loesby','L')]),
('IL','Dick Durbin','D','Retiring','regular',[('Juliana Stratton','D'),('Don Tracy','R'),('Whitfield Harrington Jr.','I')]),
('IA','Joni Ernst','R','Retiring','regular',[('Ashley Hinson','R'),('Josh Turek','D'),('Thomas Laehn','L')]),
('KS','Roger Marshall','R','Running','regular',[('Roger Marshall','R',1),('Adam Hamilton','D'),('David Graham','L')]),
('KY','Mitch McConnell','R','Retiring','regular',[('Andy Barr','R'),('Charles Booker','D'),('Christopher Campbell','I')]),
('LA','Bill Cassidy','R','Lost renomination','regular',[('Julia Letlow','R'),('Jamie Davis','D')]),
('ME','Susan Collins','R','Running','regular',[('Susan Collins','R',1),('Troy Jackson','D')]),
('MA','Ed Markey','D','Running','regular',[('Ed Markey','D',1),('John Deaton','R'),('Shiva Ayyadurai','I')]),
('MI','Gary Peters','D','Retiring','regular',[('Abdul El-Sayed','D'),('Mike Rogers','R'),('Lydia Christensen','L'),('Douglas P. Marsh','G')]),
('MN','Tina Smith','D','Retiring','regular',[('Peggy Flanagan','D'),('Michele Tafoya','R'),('Marisa Simonetti','I'),('Rebecca Whiting','L')]),
('MS','Cindy Hyde-Smith','R','Running','regular',[('Cindy Hyde-Smith','R',1),('Scott Colom','D'),('Ty Pinkins','I')]),
('MT','Steve Daines','R','Retiring','regular',[('Kurt Alme','R'),('Alani Bankhead','D'),('Seth Bodnar','I'),('Kyle Austin','L')]),
('NE','Pete Ricketts','R','Running','regular',[('Pete Ricketts','R',1),('Dan Osborn','I')]),
('NH','Jeanne Shaheen','D','Retiring','regular',[('Chris Pappas','D'),('John E. Sununu','R')]),
('NJ','Cory Booker','D','Running','regular',[('Cory Booker','D',1),('Justin Murphy','R'),('Veronica Fernandez','I')]),
('NM','Ben Ray Luján','D','Running','regular',[('Ben Ray Luján','D',1),('Larry Marker','R')]),
('NC','Thom Tillis','R','Retiring','regular',[('Roy Cooper','D'),('Michael Whatley','R'),('Shannon Bray','L'),('Michael Dublin','G')]),
('OH','Jon Husted','R','Appointed Jan 2025; running','special',[('Jon Husted','R',1),('Sherrod Brown','D'),('Greg Levy','I'),('William Redpath','L')]),
('OK','Alan Armstrong','R','Appointed Mar 2026 after Mullin left; not running','regular',[('Kevin Hern','R'),('N’Kiyla Jasmine Thomas','D')]),
('OR','Jeff Merkley','D','Running','regular',[('Jeff Merkley','D',1),('David Brock Smith','R')]),
('RI','Jack Reed','D','Running','regular',[('Jack Reed','D',1),('Raymond McKay','R'),('Michael Bahry','I')]),
('SC','Darline Graham','R','Appointed Jul 2026 after Sen. Lindsey Graham died','regular',[('Darline Graham','R',1),('Annie Andrews','D')]),
('SD','Mike Rounds','R','Running','regular',[('Mike Rounds','R',1),('Brian Bengs','I')]),
('TN','Bill Hagerty','R','Running','regular',[('Bill Hagerty','R',1),('Marquita Bradshaw','D')]),
('TX','John Cornyn','R','Lost renomination','regular',[('Ken Paxton','R'),('James Talarico','D'),('Ted Brown','L')]),
('VA','Mark Warner','D','Running','regular',[('Mark Warner','D',1),('Bert Mizusawa','R')]),
('WV','Shelley Moore Capito','R','Running','regular',[('Shelley Moore Capito','R',1),('Rachel Fetty Anderson','D')]),
('WY','Cynthia Lummis','R','Retiring','regular',[('Harriet Hageman','R'),('James W. Byrd','D')]),
]
assert len(SEN)==35
NOTES={
 'AK':'Top-four primary (Aug 18) with ranked-choice general election; four candidates advanced. The other two finalists are added in the state pass.',
 'ID':'No Democratic nominee after David Roth withdrew (Jul 28).',
 'NE':'No Democratic nominee after Cindy Burbank withdrew (Jul 17); the state Democratic Party endorsed independent Dan Osborn.',
 'SD':'No Democratic nominee on the ballot.',
 'NM':'Republican qualified as a write-in after the only other Republican filer was disqualified — confirm in the state pass.',
 'SC':'Nomination path after Sen. Graham’s death to be confirmed in the state pass.',
 'OK':'Democratic runoff held Aug 25 — confirm result in the state pass.',
 'ME':'Troy Jackson replaced Graham Platner as the Democratic nominee by party convention.',
}
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
races={}; cands={}
for st,inc,ip,istat,typ,cl in SEN:
    rid=f'{st}-SEN'
    ids=[]
    for c in cl:
        name,party=c[0],c[1]; isinc=len(c)>2
        cid=f'{st.lower()}-sen-{slug(name)}'
        cands[cid]=dict(id=cid,name=name,party=party,race=rid,incumbent=bool(isinc),research='pending')
        ids.append(cid)
    races[rid]=dict(id=rid,state=st,chamber='senate',type=typ,
        label=('Special election' if typ=='special' else 'Class II seat'),
        incumbent=dict(name=inc,party=ip,status=istat),candidates=ids,
        note=NOTES.get(st,''),research='pending',src=['wiki_sen26'])
for code,name,n in STATES:
    for d in range(1,n+1):
        rid=f'{code}-{"AL" if n==1 else str(d).zfill(2)}'
        races[rid]=dict(id=rid,state=code,chamber='house',district=(0 if n==1 else d),
            incumbent=None,candidates=[],note='',research='pending',src=[])

# ---------- Governors (Wikipedia 2026 gubernatorial table, retrieved Oct 8, 2026; nominees re-verified per state) ----------
GOV=[
('AL','Kay Ivey','R','Term-limited',[('Tommy Tuberville','R'),('Doug Jones','D')],''),
('AK','Mike Dunleavy','R','Term-limited',[],'Top-four primary Aug 18 with ranked-choice general; finalists to be confirmed. Independents Bill Walker and Meda DeWitt are listed.'),
('AZ','Katie Hobbs','D','Running',[('Katie Hobbs','D',1),('Andy Biggs','R')],'Also listed: Teri Hourihan (No Labels), Risa Lombardo (Green).'),
('AR','Sarah Huckabee Sanders','R','Running',[('Sarah Huckabee Sanders','R',1),('Fredrick Love','D')],'Also listed: Colt Shelby (Libertarian).'),
('CA','Gavin Newsom','D','Term-limited',[('Xavier Becerra','D'),('Steve Hilton','R')],'Top-two primary.'),
('CO','Jared Polis','D','Term-limited',[('Phil Weiser','D'),('Victor Marx','R')],'Also listed: Greg Lopez (I), Jeff Peckman (Unity).'),
('CT','Ned Lamont','D','Running',[('Ned Lamont','D',1),('Ryan Fazio','R')],''),
('FL','Ron DeSantis','R','Term-limited',[],'Primaries held Aug 18; nominees to be confirmed in the state pass.'),
('GA','Brian Kemp','R','Term-limited',[('Keisha Lance Bottoms','D'),('Rick Jackson','R')],''),
('HI','Josh Green','D','Running',[('Josh Green','D',1)],'Republican nominee to be confirmed.'),
('ID','Brad Little','R','Running',[('Brad Little','R',1)],'Democratic nominee to be confirmed.'),
('IL','JB Pritzker','D','Running',[('JB Pritzker','D',1),('Darren Bailey','R')],''),
('IA','Kim Reynolds','R','Retiring',[('Rob Sand','D'),('Zach Lahn','R')],'Also listed: Sondra Wilson (I).'),
('KS','Laura Kelly','D','Term-limited',[('Cindy Holscher','D'),('Ty Masterson','R')],''),
('ME','Janet Mills','D','Term-limited',[('Hannah Pingree','D'),('Robert Charles','R')],'Also listed: Rick Bennett (I).'),
('MD','Wes Moore','D','Running',[('Wes Moore','D',1),('Dan Cox','R')],''),
('MA','Maura Healey','D','Running',[('Maura Healey','D',1)],'Republican nominee to be confirmed (primary Sept 1).'),
('MI','Gretchen Whitmer','D','Term-limited',[('Jocelyn Benson','D'),('John James','R')],'Independent Mike Duggan suspended his campaign in May 2026.'),
('MN','Tim Walz','D','Retiring',[('Amy Klobuchar','D'),('Lisa Demuth','R')],''),
('NE','Jim Pillen','R','Running',[('Jim Pillen','R',1),('Lynne Walz','D')],''),
('NV','Joe Lombardo','R','Running',[('Joe Lombardo','R',1),('Aaron Ford','D')],''),
('NH','Kelly Ayotte','R','Running',[('Kelly Ayotte','R',1)],'Democratic nominee to be confirmed (primary Sept 8).'),
('NM','Michelle Lujan Grisham','D','Term-limited',[('Deb Haaland','D'),('Gregg Hull','R')],''),
('NY','Kathy Hochul','D','Running',[('Kathy Hochul','D',1),('Bruce Blakeman','R')],''),
('OH','Mike DeWine','R','Term-limited',[('Vivek Ramaswamy','R'),('Amy Acton','D')],''),
('OK','Kevin Stitt','R','Term-limited',[],'Nominees to be confirmed (runoffs Aug 25).'),
('OR','Tina Kotek','D','Running',[('Tina Kotek','D',1),('Christine Drazan','R')],''),
('PA','Josh Shapiro','D','Running',[('Josh Shapiro','D',1),('Stacy Garrity','R')],''),
('RI','Dan McKee','D','Running',[],'Primaries Sept 9; nominees to be confirmed.'),
('SC','Henry McMaster','R','Term-limited',[('Alan Wilson','R'),('Jermaine Johnson','D')],''),
('SD','Larry Rhoden','R','Running',[('Larry Rhoden','R',1),('Dan Ahlers','D')],''),
('TN','Bill Lee','R','Term-limited',[],'Primaries Aug 6; nominees to be confirmed.'),
('TX','Greg Abbott','R','Running',[('Greg Abbott','R',1),('Gina Hinojosa','D')],''),
('VT','Phil Scott','R','Running',[('Phil Scott','R',1),('Amanda Janoo','D')],''),
('WI','Tony Evers','D','Retiring',[],'Primaries Aug 11; nominees to be confirmed.'),
('WY','Mark Gordon','R','Term-limited',[],'Primaries Aug 18; nominees to be confirmed.'),
]
assert len(GOV)==36
for st,inc,ip,istat,cl,note in GOV:
    rid=f'{st}-GOV'; ids=[]
    for c in cl:
        name,party=c[0],c[1]; cid=f'{st.lower()}-gov-{slug(name)}'
        cands[cid]=dict(id=cid,name=name,party=party,race=rid,incumbent=len(c)>2,research='pending'); ids.append(cid)
    races[rid]=dict(id=rid,state=st,chamber='governor',incumbent=dict(name=inc,party=ip,status=istat),candidates=ids,note=note,research='pending',src=['wiki_gov26'])

states=[dict(code=c,name=n,house=h,senate=[r for r in races if r==f'{c}-SEN'],gov=[r for r in races if r==f'{c}-GOV'],redistricting='',research='pending') for c,n,h in STATES]
cites={'wiki_gov26':dict(t='2026 United States gubernatorial elections — Wikipedia (retrieved Oct 8, 2026)',u='https://en.wikipedia.org/wiki/2026_United_States_gubernatorial_elections'),'wiki_sen26':dict(t='2026 United States Senate elections — Wikipedia (race table, retrieved Oct 8, 2026)',
        u='https://en.wikipedia.org/wiki/2026_United_States_Senate_elections'),
       'fec_home':dict(t='Federal Election Commission — candidate and committee data',u='https://www.fec.gov/data/'),
       'fec_ie':dict(t='FEC — independent expenditures (Schedule E)',u='https://www.fec.gov/data/independent-expenditures/'),
       'os_home':dict(t='OpenSecrets — 2026 races and outside spending',u='https://www.opensecrets.org/races'),
       'ha_score':dict(t='Heritage Action for America — legislative scorecard',u='https://heritageaction.com/scorecard'),
       'aipac_pac':dict(t='AIPAC PAC — FEC committee filings (C00797670)',u='https://www.fec.gov/data/committee/C00797670/'),
       'udp':dict(t='United Democracy Project — FEC committee filings (C00799031)',u='https://www.fec.gov/data/committee/C00799031/'),
       'fara':dict(t='U.S. Department of Justice — FARA registration database',u='https://efile.fara.gov/ords/fara/f?p=1235:10'),
       'house_clerk':dict(t='Office of the Clerk — House roll call votes',u='https://clerk.house.gov/Votes'),
       'senate_votes':dict(t='U.S. Senate — roll call votes',u='https://www.senate.gov/legislative/votes_new.htm'),
       'sen_ap':dict(t='Darline Graham sworn in to finish Lindsey Graham’s term — Live 5 News (Jul 14, 2026)',u='https://www.live5news.com/2026/07/14/darline-graham-sworn-interim-us-senator/'),
       'ok_ap':dict(t='Oklahoma governor picks Alan Armstrong to fill Senate seat through end of year — PBS NewsHour (Mar 24, 2026)',u='https://www.pbs.org/newshour/amp/politics/energy-executive-alan-armstrong-picked-to-fill-mullins-senate-seat-through-end-of-year'),
       'me_ap':dict(t='Troy Jackson replaces Graham Platner as Maine Democrats’ Senate nominee — WJLA',u='https://wjla.com/news/nation-world/troy-jackson-replaces-graham-platner-as-maine-democrats-us-senate-nominee-politics-elections-voting-vote-polls-republican-sen-susan-collins-progressive-candidates-socialists-socialism-medicare-for-all-sexual-assault-allegation-accusation'),
       'tx_runoff':dict(t='Paxton defeats Cornyn in Texas GOP Senate runoff — Ballotpedia News (May 27, 2026)',u='https://news.ballotpedia.org/2026/05/27/ken-paxton-r-defeated-incumbent-john-cornyn-r-in-the-republican-primary-runoff-for-u-s-senate-in-texas-on-may-26-2026/'),
}
races['SC-SEN']['src']+= ['sen_ap']; races['OK-SEN']['src']+=['ok_ap']; races['ME-SEN']['src']+=['me_ap']; races['TX-SEN']['src']+=['tx_runoff']
data=dict(meta=dict(asof=ASOF,election='2026-11-03',version='0.1 skeleton'),states=states,races=races,cands=cands,cites=cites)
json.dump(data,open('/home/claude/el26/data.json','w'),ensure_ascii=False,indent=0)
print(len(races),len(cands))
