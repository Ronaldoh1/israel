#!/usr/bin/env python3
"""
OTS 2026 Elections: records collector for every 2026 race, filed by state.

Run it on your own computer (it needs only Python 3.8+, nothing to install):
    python3 ots_2026_collect.py                  # every state
    python3 ots_2026_collect.py --state AZ       # one state (repeat --state for more)
    COURTLISTENER_TOKEN=xxxx python3 ots_2026_collect.py   # adds the court search

What it collects, all from free public records:
  FEC         every 2026 House and Senate candidate: their FEC IDs, money totals by cycle,
              every PAC/party/committee contribution to them since 2000 (with the donor
              committee's type: corporation, trade group, labor, ideological...), and outside
              spending for or against them in 2026
  DISCLOSURES House Clerk financial-disclosure filings, with the PDFs
  FARA        Justice Department foreign-agent records checked against every name
  CERTIFICATION  how sitting and former members voted on objections to certified electoral votes
  COURTS      (with a free CourtListener token) federal dockets and opinions naming them

Output: a folder called 2026elections-data with one folder per state, and inside it one
folder per candidate. The big national downloads go in 2026elections-data/_downloads and
are NOT meant to be shared (the .gitignore it writes leaves them out).

Safe to stop and re-run: anything already downloaded is reused.
When it finishes, push the folder to GitHub (the commands are printed at the end).
"""
import csv, io, json, os, re, ssl, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request, zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# Candidates already in the Sophia elections module: (id, first, last, state, office, district, status).
# Governors are only here (they don't file with the FEC); House and Senate candidates are also
# found automatically from the FEC's 2026 candidate list.
CURATED = [
    ("ak-gov-bernadette-wilson", "Bernadette", "Wilson", "AK", "governor", "", "complete"),
    ("ak-gov-dave-bronson", "Dave", "Bronson", "AK", "governor", "", "complete"),
    ("ak-gov-jonathan-kreiss-tomkins", "Jonathan", "Kreiss-Tomkins", "AK", "governor", "", "complete"),
    ("ak-gov-treg-taylor", "Treg", "Taylor", "AK", "governor", "", "complete"),
    ("ak-al-bill-hill", "Bill", "Hill", "AK", "house", "AL", "complete"),
    ("ak-al-eric-hafner", "Eric", "Hafner", "AK", "house", "AL", "complete"),
    ("ak-al-jim-mcdermott", "Jim", "McDermott", "AK", "house", "AL", "complete"),
    ("ak-al-nick-begich", "Nick", "Begich", "AK", "house", "AL", "complete"),
    ("ak-sen-dan-sullivan", "Dan", "Sullivan", "AK", "senate", "", "complete"),
    ("ak-sen-dan-sullivan-jr", "Dan", "Sullivan", "AK", "senate", "", "complete"),
    ("ak-sen-gerald-heikes", "Gerald", "Heikes", "AK", "senate", "", "complete"),
    ("ak-sen-mary-peltola", "Mary", "Peltola", "AK", "senate", "", "complete"),
    ("al-gov-doug-jones", "Doug", "Jones", "AL", "governor", "", "complete"),
    ("al-gov-tommy-tuberville", "Tommy", "Tuberville", "AL", "governor", "", "complete"),
    ("al-01-clyde-jones-jr", "Clyde", "Jones", "AL", "house", "01", "complete"),
    ("al-01-jerry-carl", "Jerry", "Carl", "AL", "house", "01", "complete"),
    ("al-02-rhett-marques", "Rhett", "Marques", "AL", "house", "02", "complete"),
    ("al-02-shomari-figures", "Shomari", "Figures", "AL", "house", "02", "complete"),
    ("al-03-lee-mcinnis", "Lee", "McInnis", "AL", "house", "03", "complete"),
    ("al-03-mike-rogers", "Mike", "Rogers", "AL", "house", "03", "complete"),
    ("al-04-amanda-pusczek", "Amanda", "Pusczek", "AL", "house", "04", "complete"),
    ("al-04-robert-aderholt", "Robert", "Aderholt", "AL", "house", "04", "complete"),
    ("al-05-andrew-sneed", "Andrew", "Sneed", "AL", "house", "05", "complete"),
    ("al-05-dale-strong", "Dale", "Strong", "AL", "house", "05", "complete"),
    ("al-06-gary-palmer", "Gary", "Palmer", "AL", "house", "06", "complete"),
    ("al-06-maurice-mercer", "Maurice", "Mercer", "AL", "house", "06", "complete"),
    ("al-07-ammie-akin", "Ammie", "Akin", "AL", "house", "07", "complete"),
    ("al-07-terri-sewell", "Terri", "Sewell", "AL", "house", "07", "complete"),
    ("al-sen-barry-moore", "Barry", "Moore", "AL", "senate", "", "complete"),
    ("al-sen-everett-wess", "Everett", "Wess", "AL", "senate", "", "complete"),
    ("ar-gov-fredrick-love", "Fredrick", "Love", "AR", "governor", "", "pending"),
    ("ar-gov-sarah-huckabee-sanders", "Sarah", "Sanders", "AR", "governor", "", "pending"),
    ("ar-sen-hallie-shoffner", "Hallie", "Shoffner", "AR", "senate", "", "pending"),
    ("ar-sen-jeff-wadlin", "Jeff", "Wadlin", "AR", "senate", "", "pending"),
    ("ar-sen-tom-cotton", "Tom", "Cotton", "AR", "senate", "", "pending"),
    ("az-gov-andy-biggs", "Andy", "Biggs", "AZ", "governor", "", "complete"),
    ("az-gov-katie-hobbs", "Katie", "Hobbs", "AZ", "governor", "", "complete"),
    ("az-gov-risa-lombardo", "Risa", "Lombardo", "AZ", "governor", "", "complete"),
    ("az-gov-teri-ann-hourihan", "Teri", "Hourihan", "AZ", "governor", "", "complete"),
    ("az-01-amish-shah", "Amish", "Shah", "AZ", "house", "01", "complete"),
    ("az-01-jay-feely", "Jay", "Feely", "AZ", "house", "01", "complete"),
    ("az-01-monica-alponte", "Monica", "Alponte", "AZ", "house", "01", "complete"),
    ("az-02-curtis-goodwin", "Curtis", "Goodwin", "AZ", "house", "02", "complete"),
    ("az-02-eli-crane", "Eli", "Crane", "AZ", "house", "02", "complete"),
    ("az-02-jonathan-nez", "Jonathan", "Nez", "AZ", "house", "02", "complete"),
    ("az-03-alan-aversa", "Alan", "Aversa", "AZ", "house", "03", "complete"),
    ("az-03-david-redkey", "David", "Redkey", "AZ", "house", "03", "complete"),
    ("az-03-yassamin-ansari", "Yassamin", "Ansari", "AZ", "house", "03", "complete"),
    ("az-04-greg-stanton", "Greg", "Stanton", "AZ", "house", "04", "complete"),
    ("az-04-tisha-benoit", "Tisha", "Benoit", "AZ", "house", "04", "complete"),
    ("az-04-zuhdi-jasser", "Zuhdi", "Jasser", "AZ", "house", "04", "complete"),
    ("az-05-elizabeth-lee", "Elizabeth", "Lee", "AZ", "house", "05", "complete"),
    ("az-05-mark-lamb", "Mark", "Lamb", "AZ", "house", "05", "complete"),
    ("az-06-gary-swing", "Gary", "Swing", "AZ", "house", "06", "complete"),
    ("az-06-jereme-peters", "Jereme", "Peters", "AZ", "house", "06", "complete"),
    ("az-06-joanna-mendoza", "JoAnna", "Mendoza", "AZ", "house", "06", "complete"),
    ("az-06-juan-ciscomani", "Juan", "Ciscomani", "AZ", "house", "06", "complete"),
    ("az-07-adelita-grijalva", "Adelita", "Grijalva", "AZ", "house", "07", "complete"),
    ("az-07-daniel-butierez", "Daniel", "Butierez", "AZ", "house", "07", "complete"),
    ("az-08-abe-hamadeh", "Abe", "Hamadeh", "AZ", "house", "08", "complete"),
    ("az-08-bernadette-greene-placentia", "Bernadette", "Greene-Placentia", "AZ", "house", "08", "complete"),
    ("az-09-danielle-sterbinsky", "Danielle", "Sterbinsky", "AZ", "house", "09", "complete"),
    ("az-09-paul-gosar", "Paul", "Gosar", "AZ", "house", "09", "complete"),
    ("ca-gov-steve-hilton", "Steve", "Hilton", "CA", "governor", "", "pending"),
    ("ca-gov-xavier-becerra", "Xavier", "Becerra", "CA", "governor", "", "pending"),
    ("co-gov-phil-weiser", "Phil", "Weiser", "CO", "governor", "", "pending"),
    ("co-gov-victor-marx", "Victor", "Marx", "CO", "governor", "", "pending"),
    ("co-sen-blake-huber", "Blake", "Huber", "CO", "senate", "", "pending"),
    ("co-sen-john-hickenlooper", "John", "Hickenlooper", "CO", "senate", "", "pending"),
    ("co-sen-mark-baisley", "Mark", "Baisley", "CO", "senate", "", "pending"),
    ("ct-gov-ned-lamont", "Ned", "Lamont", "CT", "governor", "", "pending"),
    ("ct-gov-ryan-fazio", "Ryan", "Fazio", "CT", "governor", "", "pending"),
    ("de-sen-chris-coons", "Chris", "Coons", "DE", "senate", "", "pending"),
    ("de-sen-michael-katz", "Michael", "Katz", "DE", "senate", "", "pending"),
    ("fl-sen-angie-nixon", "Angie", "Nixon", "FL", "senate", "", "pending"),
    ("fl-sen-ashley-moody", "Ashley", "Moody", "FL", "senate", "", "pending"),
    ("fl-sen-neil-gillespie", "Neil", "Gillespie", "FL", "senate", "", "pending"),
    ("ga-gov-keisha-lance-bottoms", "Keisha", "Bottoms", "GA", "governor", "", "pending"),
    ("ga-gov-rick-jackson", "Rick", "Jackson", "GA", "governor", "", "pending"),
    ("ga-sen-jon-ossoff", "Jon", "Ossoff", "GA", "senate", "", "pending"),
    ("ga-sen-mike-collins", "Mike", "Collins", "GA", "senate", "", "pending"),
    ("hi-gov-josh-green", "Josh", "Green", "HI", "governor", "", "pending"),
    ("ia-gov-rob-sand", "Rob", "Sand", "IA", "governor", "", "pending"),
    ("ia-gov-zach-lahn", "Zach", "Lahn", "IA", "governor", "", "pending"),
    ("ia-sen-ashley-hinson", "Ashley", "Hinson", "IA", "senate", "", "pending"),
    ("ia-sen-josh-turek", "Josh", "Turek", "IA", "senate", "", "pending"),
    ("ia-sen-thomas-laehn", "Thomas", "Laehn", "IA", "senate", "", "pending"),
    ("id-gov-brad-little", "Brad", "Little", "ID", "governor", "", "pending"),
    ("id-sen-jim-risch", "Jim", "Risch", "ID", "senate", "", "pending"),
    ("id-sen-matt-loesby", "Matt", "Loesby", "ID", "senate", "", "pending"),
    ("id-sen-natalie-fleming", "Natalie", "Fleming", "ID", "senate", "", "pending"),
    ("id-sen-todd-achilles", "Todd", "Achilles", "ID", "senate", "", "pending"),
    ("il-gov-darren-bailey", "Darren", "Bailey", "IL", "governor", "", "pending"),
    ("il-gov-jb-pritzker", "JB", "Pritzker", "IL", "governor", "", "pending"),
    ("il-sen-don-tracy", "Don", "Tracy", "IL", "senate", "", "pending"),
    ("il-sen-juliana-stratton", "Juliana", "Stratton", "IL", "senate", "", "pending"),
    ("il-sen-whitfield-harrington-jr", "Whitfield", "Harrington", "IL", "senate", "", "pending"),
    ("ks-gov-cindy-holscher", "Cindy", "Holscher", "KS", "governor", "", "pending"),
    ("ks-gov-ty-masterson", "Ty", "Masterson", "KS", "governor", "", "pending"),
    ("ks-sen-adam-hamilton", "Adam", "Hamilton", "KS", "senate", "", "pending"),
    ("ks-sen-david-graham", "David", "Graham", "KS", "senate", "", "pending"),
    ("ks-sen-roger-marshall", "Roger", "Marshall", "KS", "senate", "", "pending"),
    ("ky-sen-andy-barr", "Andy", "Barr", "KY", "senate", "", "pending"),
    ("ky-sen-charles-booker", "Charles", "Booker", "KY", "senate", "", "pending"),
    ("ky-sen-christopher-campbell", "Christopher", "Campbell", "KY", "senate", "", "pending"),
    ("la-sen-jamie-davis", "Jamie", "Davis", "LA", "senate", "", "pending"),
    ("la-sen-julia-letlow", "Julia", "Letlow", "LA", "senate", "", "pending"),
    ("ma-gov-maura-healey", "Maura", "Healey", "MA", "governor", "", "pending"),
    ("ma-sen-ed-markey", "Ed", "Markey", "MA", "senate", "", "pending"),
    ("ma-sen-john-deaton", "John", "Deaton", "MA", "senate", "", "pending"),
    ("ma-sen-shiva-ayyadurai", "Shiva", "Ayyadurai", "MA", "senate", "", "pending"),
    ("md-gov-dan-cox", "Dan", "Cox", "MD", "governor", "", "pending"),
    ("md-gov-wes-moore", "Wes", "Moore", "MD", "governor", "", "pending"),
    ("me-gov-hannah-pingree", "Hannah", "Pingree", "ME", "governor", "", "pending"),
    ("me-gov-robert-charles", "Robert", "Charles", "ME", "governor", "", "pending"),
    ("me-sen-susan-collins", "Susan", "Collins", "ME", "senate", "", "pending"),
    ("me-sen-troy-jackson", "Troy", "Jackson", "ME", "senate", "", "pending"),
    ("mi-gov-jocelyn-benson", "Jocelyn", "Benson", "MI", "governor", "", "pending"),
    ("mi-gov-john-james", "John", "James", "MI", "governor", "", "pending"),
    ("mi-sen-abdul-el-sayed", "Abdul", "El-Sayed", "MI", "senate", "", "pending"),
    ("mi-sen-douglas-p-marsh", "Douglas", "Marsh", "MI", "senate", "", "pending"),
    ("mi-sen-lydia-christensen", "Lydia", "Christensen", "MI", "senate", "", "pending"),
    ("mi-sen-mike-rogers", "Mike", "Rogers", "MI", "senate", "", "pending"),
    ("mn-gov-amy-klobuchar", "Amy", "Klobuchar", "MN", "governor", "", "pending"),
    ("mn-gov-lisa-demuth", "Lisa", "Demuth", "MN", "governor", "", "pending"),
    ("mn-sen-marisa-simonetti", "Marisa", "Simonetti", "MN", "senate", "", "pending"),
    ("mn-sen-michele-tafoya", "Michele", "Tafoya", "MN", "senate", "", "pending"),
    ("mn-sen-peggy-flanagan", "Peggy", "Flanagan", "MN", "senate", "", "pending"),
    ("mn-sen-rebecca-whiting", "Rebecca", "Whiting", "MN", "senate", "", "pending"),
    ("ms-sen-cindy-hyde-smith", "Cindy", "Hyde-Smith", "MS", "senate", "", "pending"),
    ("ms-sen-scott-colom", "Scott", "Colom", "MS", "senate", "", "pending"),
    ("ms-sen-ty-pinkins", "Ty", "Pinkins", "MS", "senate", "", "pending"),
    ("mt-sen-alani-bankhead", "Alani", "Bankhead", "MT", "senate", "", "pending"),
    ("mt-sen-kurt-alme", "Kurt", "Alme", "MT", "senate", "", "pending"),
    ("mt-sen-kyle-austin", "Kyle", "Austin", "MT", "senate", "", "pending"),
    ("mt-sen-seth-bodnar", "Seth", "Bodnar", "MT", "senate", "", "pending"),
    ("nc-sen-michael-dublin", "Michael", "Dublin", "NC", "senate", "", "pending"),
    ("nc-sen-michael-whatley", "Michael", "Whatley", "NC", "senate", "", "pending"),
    ("nc-sen-roy-cooper", "Roy", "Cooper", "NC", "senate", "", "pending"),
    ("nc-sen-shannon-bray", "Shannon", "Bray", "NC", "senate", "", "pending"),
    ("ne-gov-jim-pillen", "Jim", "Pillen", "NE", "governor", "", "pending"),
    ("ne-gov-lynne-walz", "Lynne", "Walz", "NE", "governor", "", "pending"),
    ("ne-sen-dan-osborn", "Dan", "Osborn", "NE", "senate", "", "pending"),
    ("ne-sen-pete-ricketts", "Pete", "Ricketts", "NE", "senate", "", "pending"),
    ("nh-gov-kelly-ayotte", "Kelly", "Ayotte", "NH", "governor", "", "pending"),
    ("nh-sen-chris-pappas", "Chris", "Pappas", "NH", "senate", "", "pending"),
    ("nh-sen-john-e-sununu", "John", "Sununu", "NH", "senate", "", "pending"),
    ("nj-sen-cory-booker", "Cory", "Booker", "NJ", "senate", "", "pending"),
    ("nj-sen-justin-murphy", "Justin", "Murphy", "NJ", "senate", "", "pending"),
    ("nj-sen-veronica-fernandez", "Veronica", "Fernandez", "NJ", "senate", "", "pending"),
    ("nm-gov-deb-haaland", "Deb", "Haaland", "NM", "governor", "", "pending"),
    ("nm-gov-gregg-hull", "Gregg", "Hull", "NM", "governor", "", "pending"),
    ("nm-sen-ben-ray-luj-n", "Ben", "Luján", "NM", "senate", "", "pending"),
    ("nm-sen-larry-marker", "Larry", "Marker", "NM", "senate", "", "pending"),
    ("nv-gov-aaron-ford", "Aaron", "Ford", "NV", "governor", "", "pending"),
    ("nv-gov-joe-lombardo", "Joe", "Lombardo", "NV", "governor", "", "pending"),
    ("ny-gov-bruce-blakeman", "Bruce", "Blakeman", "NY", "governor", "", "pending"),
    ("ny-gov-kathy-hochul", "Kathy", "Hochul", "NY", "governor", "", "pending"),
    ("oh-gov-amy-acton", "Amy", "Acton", "OH", "governor", "", "pending"),
    ("oh-gov-vivek-ramaswamy", "Vivek", "Ramaswamy", "OH", "governor", "", "pending"),
    ("oh-sen-greg-levy", "Greg", "Levy", "OH", "senate", "", "pending"),
    ("oh-sen-jon-husted", "Jon", "Husted", "OH", "senate", "", "pending"),
    ("oh-sen-sherrod-brown", "Sherrod", "Brown", "OH", "senate", "", "pending"),
    ("oh-sen-william-redpath", "William", "Redpath", "OH", "senate", "", "pending"),
    ("ok-sen-kevin-hern", "Kevin", "Hern", "OK", "senate", "", "pending"),
    ("ok-sen-n-kiyla-jasmine-thomas", "N’Kiyla", "Thomas", "OK", "senate", "", "pending"),
    ("or-gov-christine-drazan", "Christine", "Drazan", "OR", "governor", "", "pending"),
    ("or-gov-tina-kotek", "Tina", "Kotek", "OR", "governor", "", "pending"),
    ("or-sen-david-brock-smith", "David", "Smith", "OR", "senate", "", "pending"),
    ("or-sen-jeff-merkley", "Jeff", "Merkley", "OR", "senate", "", "pending"),
    ("pa-gov-josh-shapiro", "Josh", "Shapiro", "PA", "governor", "", "pending"),
    ("pa-gov-stacy-garrity", "Stacy", "Garrity", "PA", "governor", "", "pending"),
    ("ri-sen-jack-reed", "Jack", "Reed", "RI", "senate", "", "pending"),
    ("ri-sen-michael-bahry", "Michael", "Bahry", "RI", "senate", "", "pending"),
    ("ri-sen-raymond-mckay", "Raymond", "McKay", "RI", "senate", "", "pending"),
    ("sc-gov-alan-wilson", "Alan", "Wilson", "SC", "governor", "", "pending"),
    ("sc-gov-jermaine-johnson", "Jermaine", "Johnson", "SC", "governor", "", "pending"),
    ("sc-sen-annie-andrews", "Annie", "Andrews", "SC", "senate", "", "pending"),
    ("sc-sen-darline-graham", "Darline", "Graham", "SC", "senate", "", "pending"),
    ("sd-gov-dan-ahlers", "Dan", "Ahlers", "SD", "governor", "", "pending"),
    ("sd-gov-larry-rhoden", "Larry", "Rhoden", "SD", "governor", "", "pending"),
    ("sd-sen-brian-bengs", "Brian", "Bengs", "SD", "senate", "", "pending"),
    ("sd-sen-mike-rounds", "Mike", "Rounds", "SD", "senate", "", "pending"),
    ("tn-sen-bill-hagerty", "Bill", "Hagerty", "TN", "senate", "", "pending"),
    ("tn-sen-marquita-bradshaw", "Marquita", "Bradshaw", "TN", "senate", "", "pending"),
    ("tx-gov-gina-hinojosa", "Gina", "Hinojosa", "TX", "governor", "", "pending"),
    ("tx-gov-greg-abbott", "Greg", "Abbott", "TX", "governor", "", "pending"),
    ("tx-sen-james-talarico", "James", "Talarico", "TX", "senate", "", "pending"),
    ("tx-sen-ken-paxton", "Ken", "Paxton", "TX", "senate", "", "pending"),
    ("tx-sen-ted-brown", "Ted", "Brown", "TX", "senate", "", "pending"),
    ("va-sen-bert-mizusawa", "Bert", "Mizusawa", "VA", "senate", "", "pending"),
    ("va-sen-mark-warner", "Mark", "Warner", "VA", "senate", "", "pending"),
    ("vt-gov-amanda-janoo", "Amanda", "Janoo", "VT", "governor", "", "pending"),
    ("vt-gov-phil-scott", "Phil", "Scott", "VT", "governor", "", "pending"),
    ("wv-sen-rachel-fetty-anderson", "Rachel", "Anderson", "WV", "senate", "", "pending"),
    ("wv-sen-shelley-moore-capito", "Shelley", "Capito", "WV", "senate", "", "pending"),
    ("wy-sen-harriet-hageman", "Harriet", "Hageman", "WY", "senate", "", "pending"),
    ("wy-sen-james-w-byrd", "James", "Byrd", "WY", "senate", "", "pending"),
]

VERSION = '1.0 (2026-10-12)'
ROOT = os.path.abspath('2026elections-data')
DL = os.path.join(ROOT, '_downloads')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
STATES = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY'.split()

FEC = 'https://www.fec.gov/files/bulk-downloads/{y}/{f}'
CYCLES = list(range(2000, 2028, 2))
FARA_FILES = ['https://efile.fara.gov/bulk/zip/FARA_All_Registrants.csv.zip',
              'https://efile.fara.gov/bulk/zip/FARA_All_ShortForms.csv.zip',
              'https://efile.fara.gov/bulk/zip/FARA_All_ForeignPrincipals.csv.zip']
FARA_PAGE = 'https://efile.fara.gov/ords/fara/f?p=API'
FD_ZIP = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{y}FD.zip'
FD_PDF = 'https://disclosures-clerk.house.gov/public_disc/{kind}/{y}/{doc}.pdf'
FD_TYPES = {'C': 'Candidate report', 'O': 'Annual report', 'A': 'Amendment', 'T': 'Termination report',
            'P': 'Periodic transaction report (stock trades)', 'X': 'Extension request', 'D': 'Other', 'W': 'Withdrawal',
            'E': 'Electronic copy', 'N': 'New filer', 'B': 'Blind trust', 'H': 'Other', 'G': 'Gift/travel'}
CERT_VOTES = [
    ('house', '2005-01-06', 'Ohio objection', 'https://clerk.house.gov/evs/2005/roll007.xml'),
    ('house', '2021-01-06', 'Arizona objection', 'https://clerk.house.gov/evs/2021/roll010.xml'),
    ('house', '2021-01-07', 'Pennsylvania objection', 'https://clerk.house.gov/evs/2021/roll011.xml'),
    ('senate', '2005-01-06', 'Ohio objection', 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1091/vote_109_1_00001.xml'),
    ('senate', '2021-01-06', 'Arizona objection', 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1171/vote_117_1_00001.xml'),
    ('senate', '2021-01-06', 'Pennsylvania objection', 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1171/vote_117_1_00002.xml')]
CL_SEARCH = 'https://www.courtlistener.com/api/rest/v4/search/'

# FEC bulk-file columns (fec.gov/data/browse-data, "Bulk data" data descriptions)
CN_COLS = 'CAND_ID CAND_NAME CAND_PTY_AFFILIATION CAND_ELECTION_YR CAND_OFFICE_ST CAND_OFFICE CAND_OFFICE_DISTRICT CAND_ICI CAND_STATUS CAND_PCC CAND_ST1 CAND_ST2 CAND_CITY CAND_ST CAND_ZIP'.split()
WEBALL_COLS = 'CAND_ID CAND_NAME CAND_ICI PTY_CD CAND_PTY_AFFILIATION TTL_RECEIPTS TRANS_FROM_AUTH TTL_DISB TRANS_TO_AUTH COH_BOP COH_COP CAND_CONTRIB CAND_LOANS OTHER_LOANS CAND_LOAN_REPAY OTHER_LOAN_REPAY DEBTS_OWED_BY TTL_INDIV_CONTRIB CAND_OFFICE_ST CAND_OFFICE_DISTRICT SPEC_ELECTION PRIM_ELECTION RUN_ELECTION GEN_ELECTION GEN_ELECTION_PRECENT OTHER_POL_CMTE_CONTRIB POL_PTY_CONTRIB CVG_END_DT INDIV_REFUNDS CMTE_REFUNDS'.split()
CM_COLS = 'CMTE_ID CMTE_NM TRES_NM CMTE_ST1 CMTE_ST2 CMTE_CITY CMTE_ST CMTE_ZIP CMTE_DSGN CMTE_TP CMTE_PTY_AFFILIATION CMTE_FILING_FREQ ORG_TP CONNECTED_ORG_NM CAND_ID'.split()
PAS2_COLS = 'CMTE_ID AMNDT_IND RPT_TP TRANSACTION_PGI IMAGE_NUM TRANSACTION_TP ENTITY_TP NAME CITY STATE ZIP_CODE EMPLOYER OCCUPATION TRANSACTION_DT TRANSACTION_AMT OTHER_ID CAND_ID TRAN_ID FILE_NUM MEMO_CD MEMO_TEXT SUB_ID'.split()
ORG_TP = {'C': 'Corporation', 'L': 'Labor organization', 'M': 'Membership organization', 'T': 'Trade association',
          'V': 'Cooperative', 'W': 'Corporation without capital stock'}
CMTE_TP = {'Q': 'PAC (qualified)', 'N': 'PAC (nonqualified)', 'O': 'Super PAC', 'U': 'Single-candidate super PAC', 'V': 'Hybrid PAC (with non-contribution account)',
           'W': 'Hybrid PAC (with non-contribution account), nonqualified', 'X': 'Party (nonqualified)', 'Y': 'Party (qualified)', 'Z': 'National party nonfederal account',
           'H': 'House campaign', 'S': 'Senate campaign', 'P': 'Presidential campaign', 'C': 'Communication cost', 'D': 'Delegate committee', 'E': 'Electioneering communication', 'I': 'Independent expenditor (person or group)'}
CMTE_DSGN = {'A': 'Authorized by a candidate', 'B': 'Lobbyist/registrant PAC', 'D': 'Leadership PAC', 'J': 'Joint fundraiser', 'P': "Candidate's principal campaign committee", 'U': 'Unauthorized'}

# ---------------------------------------------------------------- helpers
def log(*a): print(*a, flush=True)

def ssl_ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()
CTX = ssl_ctx()
CERT_HELP = ('\n  SSL certificate problem. On a Mac, open Applications > Python 3.x and double-click'
             '\n  "Install Certificates.command" (or run: pip3 install certifi), then run this again.\n')

def fetch(url, dest=None, headers=None, tries=4, quiet=False):
    """GET a URL to bytes, or stream it to a file. Re-uses a finished file. Returns bytes/path or None."""
    if dest and os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    h = {'User-Agent': UA, 'Accept': '*/*'}
    h.update(headers or {})
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), context=CTX, timeout=180) as r:
                if not dest:
                    return r.read()
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                total = int(r.headers.get('Content-Length') or 0); got = 0; last = time.time()
                with open(dest + '.part', 'wb') as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b: break
                        f.write(b); got += len(b)
                        if total > 20e6 and time.time() - last > 5:
                            log(f'      {got / 1e6:.0f} of {total / 1e6:.0f} MB'); last = time.time()
            os.replace(dest + '.part', dest)
            return dest
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = 20 * (i + 1); log(f'    busy ({e.code}); waiting {wait}s'); time.sleep(wait); continue
            if not quiet: log(f'    HTTP {e.code}: {url}')
            return None
        except (ssl.SSLError, ssl.CertificateError):
            log(CERT_HELP); raise SystemExit(1)
        except urllib.error.URLError as e:
            if isinstance(getattr(e, 'reason', None), ssl.SSLError) or 'CERTIFICATE' in str(e).upper():
                log(CERT_HELP); raise SystemExit(1)
            log(f'    network error ({e.reason}); retrying'); time.sleep(5 * (i + 1))
        except Exception as e:
            log(f'    error ({e}); retrying'); time.sleep(5 * (i + 1))
    return None

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z ]+', ' ', s.replace('-', ' ')).split()

def slug(s): return '-'.join(norm(s)) or 'x'

def money(x):
    try: return round(float(x or 0), 2)
    except ValueError: return 0.0

def zip_lines(path):
    """yield decoded lines of the first .txt/.csv member of a zip"""
    z = zipfile.ZipFile(path)
    m = [n for n in z.namelist() if n.lower().endswith(('.txt', '.csv'))]
    if not m: return
    with z.open(m[0]) as f:
        for raw in io.TextIOWrapper(f, encoding='latin-1', newline=''):
            yield raw.rstrip('\r\n')

def wcsv(path, head, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(head); w.writerows(rows)

def wjson(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: json.dump(obj, f, indent=1, ensure_ascii=False)

class Cand:
    def __init__(self, cid, first, last, state, office, district, source):
        self.id, self.first, self.last, self.state, self.office, self.district, self.source = cid, first, last, state, office, district, source
        self.f = (norm(first) or [''])[0]
        self.l = norm(last) or ['?']
        self.fec_ids = set(); self.fec_rows = []; self.party = ''; self.ici = ''
    def name(self): return f'{self.first} {self.last}'
    def folder(self): return os.path.join(ROOT, self.state, self.id)
    def matches_tokens(self, toks):
        if not all(x in toks for x in self.l): return False
        f = self.f
        return any(t == f or t == f[:1] or (len(t) >= 3 and len(f) >= 3 and (t.startswith(f[:3]) or f.startswith(t))) for t in toks)

def fec_name(raw):
    """'GOSAR, PAUL ANTHONY DR.' -> ('Paul', 'Gosar')"""
    last, _, rest = (raw or '').partition(',')
    rest = [w for w in rest.replace('.', ' ').split() if w.upper() not in ('MR', 'MRS', 'MS', 'DR', 'JR', 'SR', 'II', 'III', 'IV', 'HON', 'REP', 'SEN')]
    return (rest[0].title() if rest else ''), last.strip().title()

# ---------------------------------------------------------------- 1. FEC: who is running, and the money
def fec_file(y, f):
    return fetch(FEC.format(y=y, f=f), os.path.join(DL, 'fec', str(y), f))

def run_fec(cands, states, since):
    log('\n[1/5] FEC: candidates and money')
    yy = lambda y: str(y)[2:]
    # 2026 candidate list
    p = fec_file(2026, 'cn26.zip')
    if not p: log('  could not download the 2026 FEC candidate list; skipping FEC.'); return cands
    by_key = {(c.state, c.office, c.l[-1]): c for c in cands if c.office in ('house', 'senate')}
    new = 0
    for line in zip_lines(p):
        r = dict(zip(CN_COLS, line.split('|')))
        if r.get('CAND_ELECTION_YR') != '2026' or r.get('CAND_OFFICE') not in ('H', 'S'): continue
        st = r['CAND_OFFICE_ST']
        if st not in states: continue
        office = 'house' if r['CAND_OFFICE'] == 'H' else 'senate'
        first, last = fec_name(r['CAND_NAME'])
        dist = (r.get('CAND_OFFICE_DISTRICT') or '').zfill(2) if office == 'house' else ''
        c = by_key.get((st, office, (norm(last) or ['?'])[-1]))
        if c and c.matches_tokens(set(norm(r['CAND_NAME']))):
            pass
        else:
            c = Cand(f"{st.lower()}-{'sen' if office == 'senate' else dist}-{slug(first + ' ' + last)}", first, last, st, office, dist, 'fec')
            cands.append(c); by_key[(st, office, c.l[-1])] = c; new += 1
        c.fec_ids.add(r['CAND_ID']); c.party = c.party or r.get('CAND_PTY_AFFILIATION', ''); c.ici = c.ici or r.get('CAND_ICI', '')
        c.fec_rows.append(r)
    log(f'  2026 list: {sum(1 for c in cands if c.fec_ids)} House/Senate candidates in the selected states ({new} not yet in the module)')
    # earlier IDs (e.g. a senator who served in the House) by name and state in older candidate lists
    idx = {}
    for c in cands:
        if c.office in ('house', 'senate'): idx.setdefault((c.state, c.l[-1]), []).append(c)
    for y in range(since, 2026, 2):
        p = fec_file(y, f'cn{yy(y)}.zip')
        if not p: continue
        for line in zip_lines(p):
            r = dict(zip(CN_COLS, line.split('|')))
            if r.get('CAND_OFFICE') not in ('H', 'S'): continue
            first, last = fec_name(r['CAND_NAME'])
            for c in idx.get((r['CAND_OFFICE_ST'], (norm(last) or ['?'])[-1]), []):
                if c.matches_tokens(set(norm(r['CAND_NAME']))): c.fec_ids.add(r['CAND_ID'])
    # committee master (who each donor committee is), all cycles
    cm = {}
    for y in range(since, 2028, 2):
        p = fec_file(y, f'cm{yy(y)}.zip')
        if not p: continue
        for line in zip_lines(p):
            r = dict(zip(CM_COLS, line.split('|')))
            cm[r['CMTE_ID']] = r
    log(f'  committee directory: {len(cm)} committees')
    ids = {}
    for c in cands:
        for i in c.fec_ids: ids[i] = c
    totals = {c.id: [] for c in cands}; contrib = {c.id: [] for c in cands}
    for y in range(since, 2028, 2):
        p = fec_file(y, f'weball{yy(y)}.zip')
        if p:
            for line in zip_lines(p):
                r = dict(zip(WEBALL_COLS, line.split('|')))
                c = ids.get(r['CAND_ID'])
                if c: totals[c.id].append({'cycle': y, 'fec_id': r['CAND_ID'], 'receipts': money(r['TTL_RECEIPTS']), 'individuals': money(r['TTL_INDIV_CONTRIB']),
                                           'pacs_and_committees': money(r['OTHER_POL_CMTE_CONTRIB']), 'party': money(r['POL_PTY_CONTRIB']), 'self': money(r['CAND_CONTRIB']),
                                           'candidate_loans': money(r['CAND_LOANS']), 'spent': money(r['TTL_DISB']), 'cash_on_hand': money(r['COH_COP']),
                                           'debts': money(r['DEBTS_OWED_BY']), 'through': r['CVG_END_DT'], 'general_result': r['GEN_ELECTION']})
        log(f'  committee contributions {y}')
        p = fec_file(y, f'pas2{yy(y)}.zip')
        if not p: continue
        for line in zip_lines(p):
            v = line.split('|')
            if len(v) < 17: continue
            c = ids.get(v[16])
            if not c: continue
            r = dict(zip(PAS2_COLS, v)); d = cm.get(r['CMTE_ID'], {})
            contrib[c.id].append([y, r['TRANSACTION_DT'], money(r['TRANSACTION_AMT']), r['TRANSACTION_TP'], r['CMTE_ID'], d.get('CMTE_NM', r['NAME']),
                                  CMTE_TP.get(d.get('CMTE_TP', ''), d.get('CMTE_TP', '')), CMTE_DSGN.get(d.get('CMTE_DSGN', ''), d.get('CMTE_DSGN', '')),
                                  ORG_TP.get(d.get('ORG_TP', ''), d.get('ORG_TP', '')), d.get('CONNECTED_ORG_NM', ''), r['CAND_ID'], r['IMAGE_NUM'],
                                  f"https://docquery.fec.gov/cgi-bin/fecimg/?{r['IMAGE_NUM']}" if r['IMAGE_NUM'] else ''])
    # outside spending (super PACs and others) for or against, 2026
    ie = {c.id: [] for c in cands}
    p = fetch('https://www.fec.gov/files/bulk-downloads/2026/independent_expenditure_2026.csv', os.path.join(DL, 'fec', '2026', 'independent_expenditure_2026.csv'))
    if p:
        with open(p, encoding='latin-1', newline='') as f:
            for r in csv.DictReader(f):
                c = ids.get(r.get('cand_id', ''))
                if c: ie[c.id].append([r.get('exp_date', ''), money(r.get('exp_amo')), r.get('sup_opp', ''), r.get('spe_id', ''), r.get('spe_nam', ''), r.get('pur', ''), r.get('pay', ''), r.get('image_num', '')])
    for c in cands:
        if not c.fec_ids: continue
        wjson(os.path.join(c.folder(), 'fec_totals.json'), {'fec_ids': sorted(c.fec_ids), 'cycles': sorted(totals[c.id], key=lambda t: t['cycle'])})
        wcsv(os.path.join(c.folder(), 'fec_committee_contributions.csv'),
             ['cycle', 'date', 'amount', 'transaction_type', 'donor_committee_id', 'donor_committee', 'donor_committee_type', 'donor_designation',
              'donor_organization_type', 'connected_organization', 'to_fec_id', 'image_num', 'filing_image'], sorted(contrib[c.id], key=lambda r: (r[0], r[1])))
        if ie[c.id]:
            wcsv(os.path.join(c.folder(), 'fec_outside_spending_2026.csv'),
                 ['date', 'amount', 'support_or_oppose', 'spender_id', 'spender', 'purpose', 'payee', 'image_num'], ie[c.id])
    log('  done')
    return cands

# ---------------------------------------------------------------- 2. House financial disclosures
def run_disclosures(cands, ptr=False):
    log('\n[2/5] House financial disclosures')
    idx = []
    for y in range(2008, datetime.now().year + 1):
        p = fetch(FD_ZIP.format(y=y), os.path.join(DL, 'house_fd', f'{y}FD.zip'), quiet=True)
        if not p: continue
        try: z = zipfile.ZipFile(p)
        except zipfile.BadZipFile: continue
        x = [m for m in z.namelist() if m.lower().endswith('.xml')]
        if not x: continue
        for m in ET.fromstring(z.read(x[0])).iter('Member'):
            g = {ch.tag: (ch.text or '').strip() for ch in m}; g['IndexYear'] = y; idx.append(g)
    log(f'  index: {len(idx)} filings')
    by = {}
    for g in idx: by.setdefault(((g.get('StateDst') or '')[:2], (norm(g.get('Last')) or ['?'])[-1]), []).append(g)
    n = 0
    for c in cands:
        hits = []
        for g in by.get((c.state, c.l[-1]), []):
            if not c.matches_tokens(set(norm(g.get('First'))) | set(c.l)): continue
            ft = g.get('FilingType', ''); yr = g.get('Year') or g['IndexYear']
            hits.append({'name': f"{g.get('First')} {g.get('Last')} {g.get('Suffix') or ''}".strip(), 'district': g.get('StateDst'), 'type': ft,
                         'type_label': FD_TYPES.get(ft, ft), 'year': yr, 'filed': g.get('FilingDate'), 'doc_id': g.get('DocID'),
                         'url': FD_PDF.format(kind='ptr-pdfs' if ft == 'P' else 'financial-pdfs', y=yr, doc=g.get('DocID'))})
        if not hits: continue
        n += 1
        hits.sort(key=lambda h: (str(h['year']), h['filed'] or ''))
        for h in hits:
            if h['type'] == 'X' or (h['type'] == 'P' and not ptr): continue
            dest = os.path.join(c.folder(), 'house_disclosures', f"{h['year']}_{h['type']}_{h['doc_id']}.pdf")
            if fetch(h['url'], dest, quiet=True): h['file'] = os.path.basename(dest)
            time.sleep(0.2)
        keys = ['year', 'type', 'type_label', 'filed', 'name', 'district', 'doc_id', 'url', 'file']
        wcsv(os.path.join(c.folder(), 'house_disclosures', 'index.csv'), keys, [[h.get(k, '') for k in keys] for h in hits])
    log(f'  done: {n} candidates have House filings')

# ---------------------------------------------------------------- 3. FARA
def run_fara(cands):
    log('\n[3/5] FARA foreign-agent records')
    by_last = {}
    for c in cands: by_last.setdefault(c.l[-1], []).append(c)
    hits = {c.id: [] for c in cands}; got = []
    for url in FARA_FILES:
        name = url.rsplit('/', 1)[1]; dest = os.path.join(DL, 'fara', name)
        p = fetch(url, dest)
        if not p:
            log(f'  could not download {name}. Open {FARA_PAGE} in a browser, save the CSV bulk files into\n  {os.path.dirname(dest)} with these names, and run again.'); continue
        try: z = zipfile.ZipFile(p)
        except zipfile.BadZipFile:
            log(f'  {name} is not a zip (the link may have moved)'); os.remove(p); continue
        got.append(name)
        for m in z.namelist():
            if not m.lower().endswith('.csv'): continue
            rd = csv.reader(io.TextIOWrapper(z.open(m), encoding='utf-8', errors='replace'))
            head = next(rd, [])
            for row in rd:
                toks = set(norm(' '.join(row)))
                for last in toks & by_last.keys():
                    for c in by_last[last]:
                        if c.matches_tokens(toks): hits[c.id].append({'file': m, 'row': dict(zip(head, row))})
    full = len(got) == len(FARA_FILES)
    for c in cands:
        wjson(os.path.join(c.folder(), 'fara.json'), {'searched': full, 'searched_on': NOW, 'files': got, 'name_matches': hits[c.id],
              'note': 'Name matches only; each needs a human check (same-name people are common).' if hits[c.id] else
                      ('No row in the FARA bulk files names this person.' if full else 'Search incomplete: not every FARA file downloaded.')})
    log(f'  done: {len(got)} of {len(FARA_FILES)} files; {sum(1 for c in cands if hits[c.id])} candidates have a name match to review')

# ---------------------------------------------------------------- 4. certification roll calls
def run_certification(cands):
    log('\n[4/5] Votes on objections to certified electoral votes')
    votes = {c.id: [] for c in cands}; ok = 0
    for chamber, date, label, url in CERT_VOTES:
        p = fetch(url, os.path.join(DL, 'certification', url.rsplit('/', 1)[1]))
        if not p: continue
        ok += 1; root = ET.parse(p).getroot(); rows = []
        if chamber == 'house':
            for rv in root.iter('recorded-vote'):
                lg, v = rv.find('legislator'), rv.find('vote')
                if lg is not None and v is not None: rows.append((lg.get('unaccented-name') or lg.text or '', lg.get('state', ''), v.text or ''))
        else:
            for m in root.iter('member'):
                rows.append(((m.findtext('first_name') or '') + ' ' + (m.findtext('last_name') or ''), m.findtext('state') or '', m.findtext('vote_cast') or ''))
        for c in cands:
            same = [r for r in rows if r[1] == c.state and all(x in norm(r[0]) for x in c.l)]
            if len(same) > 1: same = [r for r in same if c.matches_tokens(set(norm(r[0])))]
            for nm, st, vote in same[:1]:
                votes[c.id].append({'chamber': chamber, 'date': date, 'objection': label, 'vote': vote, 'listed_as': nm.strip(), 'roll_call': url,
                                    'meaning': 'Yea = voted to sustain the objection, i.e. to reject the certified electoral votes'})
    for c in cands:
        if votes[c.id] or c.office in ('house', 'senate'):
            wjson(os.path.join(c.folder(), 'certification_votes.json'), {'roll_calls_read': ok, 'of': len(CERT_VOTES), 'votes': votes[c.id],
                  'note': 'Only members who served on those dates appear in the roll calls; anyone else has no vote to record.'})
    log(f'  done: read {ok} of {len(CERT_VOTES)} roll calls; {sum(1 for c in cands if votes[c.id])} candidates voted on one')

# ---------------------------------------------------------------- 5. CourtListener
def run_courts(cands, token, scope):
    log('\n[5/5] Court records (CourtListener)')
    if not token:
        log('  skipped: no token. Make a free account at www.courtlistener.com, copy the API token from your profile,'
            '\n  then run:  COURTLISTENER_TOKEN=yourtoken python3 ots_2026_collect.py --only courts'); return
    todo = [c for c in cands if scope == 'all' or c.source == 'module' or c.ici == 'I']
    log(f'  searching {len(todo)} candidates ({"everyone" if scope == "all" else "module candidates and incumbents; use --courts all for everyone"})')
    H = {'Authorization': f'Token {token}', 'Accept': 'application/json'}
    for i, c in enumerate(todo, 1):
        out = {'searched_on': NOW, 'query': f'"{c.name()}"', 'note': 'Full-text name search; hits include namesakes and passing mentions and need a human check.'}
        for typ, label in (('r', 'federal_dockets'), ('o', 'opinions')):
            cache = os.path.join(DL, 'courtlistener', f'{c.id}_{typ}.json')
            if not os.path.exists(cache):
                q = urllib.parse.urlencode({'q': f'"{c.name()}"', 'type': typ, 'order_by': 'dateFiled desc'})
                b = fetch(f'{CL_SEARCH}?{q}', headers=H)
                if b is None: out[label] = 'search failed'; continue
                os.makedirs(os.path.dirname(cache), exist_ok=True)
                with open(cache, 'wb') as f: f.write(b)
                time.sleep(1.5)
            d = json.load(open(cache))
            out[label + '_count'] = d.get('count')
            out[label] = [{'case': x.get('caseName'), 'court': x.get('court') or x.get('court_id'), 'filed': x.get('dateFiled'), 'docket': x.get('docketNumber'),
                           'url': 'https://www.courtlistener.com' + (x.get('absolute_url') or '')} for x in (d.get('results') or [])[:20]]
        wjson(os.path.join(c.folder(), 'courts_courtlistener.json'), out)
        if i % 25 == 0: log(f'  {i} of {len(todo)}')
    log('  done')

# ---------------------------------------------------------------- index files
def write_indexes(cands, states, ran):
    for st in states:
        mine = sorted([c for c in cands if c.state == st], key=lambda c: (c.office, c.district, c.last))
        if not mine: continue
        wcsv(os.path.join(ROOT, st, 'candidates.csv'), ['id', 'name', 'office', 'district', 'party', 'incumbent_challenger_open', 'fec_ids', 'in_module'],
             [[c.id, c.name(), c.office, c.district, c.party, c.ici, ' '.join(sorted(c.fec_ids)), 'yes' if c.source == 'module' else 'no'] for c in mine])
    wjson(os.path.join(ROOT, 'manifest.json'), {'collector': 'ots_2026_collect.py ' + VERSION, 'run_at': NOW, 'states': states, 'steps': ran,
          'candidates': len(cands), 'sources': {'fec': FEC.format(y='{cycle}', f='...'), 'house_disclosures': FD_ZIP, 'fara': FARA_FILES,
                                                 'certification': [v[3] for v in CERT_VOTES], 'courts': CL_SEARCH}})
    with open(os.path.join(ROOT, '.gitignore'), 'w') as f: f.write('_downloads/\n*.part\n.DS_Store\n')
    with open(os.path.join(ROOT, 'README.md'), 'w') as f:
        f.write('# 2026 elections: public records by state\n\nCollected with `ots_2026_collect.py` ' + VERSION + ' on ' + NOW + '.\n\n'
                'Each state folder has `candidates.csv` and one folder per candidate:\n\n'
                '- `fec_totals.json` money by cycle; `fec_committee_contributions.csv` every PAC, party and committee contribution, with the donor type;\n'
                '  `fec_outside_spending_2026.csv` super PAC and other outside spending for or against\n'
                '- `house_disclosures/` House financial-disclosure filings (PDFs and index)\n'
                '- `fara.json` foreign-agent (FARA) name check\n'
                '- `certification_votes.json` votes on objections to certified electoral votes\n'
                '- `courts_courtlistener.json` federal dockets and opinions naming them\n\n'
                'Name matches (FARA, courts) are leads, not findings: each needs a human check.\n')

def main():
    a = sys.argv[1:]
    states = [a[i + 1].upper() for i, x in enumerate(a) if x == '--state'] or STATES
    bad = [s for s in states if s not in STATES]
    if bad: log('Unknown state code(s):', ', '.join(bad)); return
    only = set(a[a.index('--only') + 1].split(',')) if '--only' in a else {'fec', 'disclosures', 'fara', 'certification', 'courts'}
    since = int(a[a.index('--since') + 1]) if '--since' in a else 2000
    token = os.environ.get('COURTLISTENER_TOKEN') or (a[a.index('--token') + 1] if '--token' in a else None)
    scope = a[a.index('--courts') + 1] if '--courts' in a else 'module'
    os.makedirs(DL, exist_ok=True)
    cands = [Cand(t[0], t[1], t[2], t[3], t[4], t[5], 'module') for t in CURATED if t[3] in states]
    log(f'OTS 2026 collector {VERSION}: {len(states)} state(s), saving to {ROOT}')
    if 'fec' in only or not os.path.exists(os.path.join(ROOT, 'manifest.json')):
        cands = run_fec(cands, set(states), since)
    else:
        # re-load the FEC candidates found on an earlier run so the other steps cover them too
        for st in states:
            p = os.path.join(ROOT, st, 'candidates.csv')
            if not os.path.exists(p): continue
            have = {c.id for c in cands}
            for r in csv.DictReader(open(p, encoding='utf-8')):
                if r['id'] in have: continue
                first, _, last = r['name'].rpartition(' ')
                c = Cand(r['id'], first, last, st, r['office'], r['district'], 'fec'); c.fec_ids = set(r['fec_ids'].split()); c.party = r['party']; c.ici = r['incumbent_challenger_open']
                cands.append(c)
    if 'disclosures' in only: run_disclosures(cands, ptr='--with-trades' in a)
    if 'fara' in only: run_fara(cands)
    if 'certification' in only: run_certification(cands)
    if 'courts' in only: run_courts(cands, token, scope)
    write_indexes(cands, states, sorted(only))
    log(f'\nFinished: {len(cands)} candidates in {ROOT}.\n\nTo share it, run these from the folder you ran this script in:'
        f'\n  git add .gitignore 2>/dev/null; git add "{os.path.basename(ROOT)}"\n  git commit -m "Records pull {NOW}"\n  git push -u origin main'
        f'\n(The big national downloads in {os.path.basename(ROOT)}/_downloads are left out automatically.)')

if __name__ == '__main__':
    main()
