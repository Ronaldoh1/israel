#!/usr/bin/env python3
"""
OTS 2026 Elections: public-records pull for the candidate scorecards.

What it does (all free, public, no login, except the optional court search):
  1. FARA   - downloads the Justice Department's foreign-agent bulk files once and
              checks every candidate's name against them.
  2. HOUSE  - downloads the House Clerk's yearly financial-disclosure indexes,
     DISCLOSURES  finds each candidate's filings and downloads those PDFs.
  3. CERTIFICATION - downloads the official House and Senate roll calls on objections
              to certified electoral votes (2005 and 2021) and records how any candidate voted.
  4. COURTS - (only if you give it a free CourtListener token) searches federal dockets
              and court opinions for each candidate's name.

Run:   python3 ots_records_pull.py
       python3 ots_records_pull.py --state AZ             (one state only)
       COURTLISTENER_TOKEN=xxxx python3 ots_records_pull.py  (adds the court search)

It needs only Python 3.8+ (no installs). It is safe to stop and re-run: finished
downloads are reused. When it finishes, upload the files named upload_*.zip
from the ots_records folder back into the chat.
"""
import csv, io, json, os, re, ssl, sys, time, unicodedata, urllib.error, urllib.parse, urllib.request, zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# (id, first, last, state, office, district, research status)
CANDIDATES = [
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

OUT = os.path.abspath('ots_records')
RAW = os.path.join(OUT, 'raw')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

FARA_FILES = [   # Justice Department FARA eFile bulk data (efile.fara.gov, "Bulk Data")
    'https://efile.fara.gov/bulk/zip/FARA_All_Registrants.csv.zip',
    'https://efile.fara.gov/bulk/zip/FARA_All_ShortForms.csv.zip',
    'https://efile.fara.gov/bulk/zip/FARA_All_ForeignPrincipals.csv.zip',
]
FARA_PAGE = 'https://efile.fara.gov/ords/fara/f?p=API'
FD_ZIP = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{y}FD.zip'
FD_PDF = 'https://disclosures-clerk.house.gov/public_disc/{kind}/{y}/{doc}.pdf'
FD_YEARS = range(2008, datetime.now().year + 1)
FD_TYPES = {'C': 'Candidate report', 'O': 'Annual report', 'A': 'Amendment', 'T': 'Termination report',
            'P': 'Periodic transaction report (stock trades)', 'X': 'Extension request', 'D': 'Duplicate/other', 'W': 'Withdrawal', 'E': 'Electronic copy', 'N': 'New filer', 'B': 'Blind trust', 'H': 'Other', 'G': 'Gift/travel'}
CERT_VOTES = [   # objections to certified electoral votes that went to a recorded vote
    ('house', '2005-01-06', 'Ohio objection', 'https://clerk.house.gov/evs/2005/roll007.xml'),
    ('house', '2021-01-06', 'Arizona objection', 'https://clerk.house.gov/evs/2021/roll010.xml'),
    ('house', '2021-01-07', 'Pennsylvania objection', 'https://clerk.house.gov/evs/2021/roll011.xml'),
    ('senate', '2005-01-06', 'Ohio objection', 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1091/vote_109_1_00001.xml'),
    ('senate', '2021-01-06', 'Arizona objection', 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1171/vote_117_1_00001.xml'),
    ('senate', '2021-01-06', 'Pennsylvania objection', 'https://www.senate.gov/legislative/LIS/roll_call_votes/vote1171/vote_117_1_00002.xml'),
]
CL_SEARCH = 'https://www.courtlistener.com/api/rest/v4/search/'

# ---------------------------------------------------------------- helpers
def log(*a): print(*a, flush=True)

def ssl_ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()
CTX = ssl_ctx()

def fetch(url, dest=None, headers=None, tries=4):
    """GET a URL (to bytes, or to a file). Re-uses a finished file. Returns bytes or path, or None."""
    if dest and os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    h = {'User-Agent': UA, 'Accept': '*/*'}
    h.update(headers or {})
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), context=CTX, timeout=120) as r:
                data = r.read()
            if dest:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest + '.part', 'wb') as f: f.write(data)
                os.replace(dest + '.part', dest)
                return dest
            return data
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = 20 * (i + 1); log(f'    busy ({e.code}); waiting {wait}s'); time.sleep(wait); continue
            log(f'    HTTP {e.code} for {url}'); return None
        except ssl.SSLError as e:
            log('\n  SSL certificate problem. On a Mac, run the "Install Certificates.command" file in your'
                '\n  Applications > Python 3.x folder (or: pip3 install certifi), then run this again.\n')
            raise SystemExit(1)
        except urllib.error.URLError as e:
            if isinstance(getattr(e, 'reason', None), ssl.SSLError) or 'CERTIFICATE' in str(e):
                log('\n  SSL certificate problem. On a Mac, run the "Install Certificates.command" file in your'
                    '\n  Applications > Python 3.x folder (or: pip3 install certifi), then run this again.\n')
                raise SystemExit(1)
            log(f'    network error ({e}); retrying'); time.sleep(5 * (i + 1))
        except Exception as e:
            log(f'    error ({e}); retrying'); time.sleep(5 * (i + 1))
    return None

def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z ]+', ' ', s.replace('-', ' ')).split()

class Cand:
    def __init__(self, t):
        self.id, self.first, self.last, self.state, self.office, self.district, self.status = t
        self.f = norm(self.first)[0] if norm(self.first) else ''
        self.l = norm(self.last)          # list of tokens (hyphenated names split)
    def name(self): return f'{self.first} {self.last}'
    def matches_tokens(self, toks):
        """first and last name both present among the tokens (first name may be an initial or nickname start)"""
        if not all(x in toks for x in self.l): return False
        return any(t == self.f or (len(t) >= 3 and (t.startswith(self.f[:3]) or self.f.startswith(t))) or t == self.f[:1] for t in toks)

# ---------------------------------------------------------------- 1. FARA
def run_fara(cands, R):
    log('\n[1/4] FARA foreign-agent records')
    by_last = {}
    for c in cands:
        by_last.setdefault(c.l[-1], []).append(c)
        R[c.id]['fara'] = {'searched': False, 'hits': []}
    got = []
    for url in FARA_FILES:
        dest = os.path.join(RAW, 'fara', url.rsplit('/', 1)[1])
        log('  downloading', url.rsplit('/', 1)[1])
        p = fetch(url, dest)
        if not p:
            log(f'  could not download it. Open {FARA_PAGE} in a browser, download the CSV bulk files there into'
                f'\n  {os.path.dirname(dest)} (keep the zip names), and run this again.')
            continue
        try:
            z = zipfile.ZipFile(p)
        except zipfile.BadZipFile:
            log('  the file is not a zip (the link may have moved):', url); os.remove(p); continue
        got.append(os.path.basename(p))
        for member in z.namelist():
            if not member.lower().endswith('.csv'): continue
            text = io.TextIOWrapper(z.open(member), encoding='utf-8', errors='replace')
            rd = csv.reader(text)
            head = next(rd, [])
            for row in rd:
                toks = set(norm(' '.join(row)))
                for last in toks & by_last.keys():
                    for c in by_last[last]:
                        if c.matches_tokens(toks):
                            R[c.id]['fara']['hits'].append({'file': member, 'row': dict(zip(head, row))})
    for c in cands:
        f = R[c.id]['fara']
        f['searched'] = len(got) == len(FARA_FILES)
        f['files'] = got
        f['note'] = ('Name matches only. A match may be a different person with the same name; each hit needs a human check.'
                     if f['hits'] else 'No row in the FARA bulk files names this person.')
    n = sum(1 for c in cands if R[c.id]['fara']['hits'])
    log(f'  done: searched {len(got)} of {len(FARA_FILES)} files; {n} candidate(s) have a name match to review')

# ---------------------------------------------------------------- 2. House financial disclosures
def run_disclosures(cands, R, pdfs=True, ptr=False):
    log('\n[2/4] House financial disclosures (House Clerk)')
    idx = []
    for y in FD_YEARS:
        p = fetch(FD_ZIP.format(y=y), os.path.join(RAW, 'house_fd', f'{y}FD.zip'))
        if not p: continue
        try:
            z = zipfile.ZipFile(p)
        except zipfile.BadZipFile:
            continue
        xmln = [m for m in z.namelist() if m.lower().endswith('.xml')]
        if not xmln: continue
        root = ET.fromstring(z.read(xmln[0]))
        for m in root.iter('Member'):
            g = {ch.tag: (ch.text or '').strip() for ch in m}
            g['IndexYear'] = y
            idx.append(g)
    log(f'  index: {len(idx)} filings, {min(FD_YEARS)}-{max(FD_YEARS)}')
    for c in cands:
        hits = []
        for g in idx:
            if (g.get('StateDst') or '')[:2] != c.state: continue
            if norm(g.get('Last')) != c.l and ' '.join(c.l) not in ' '.join(norm(g.get('Last'))): continue
            if not c.matches_tokens(set(norm(g.get('First')) + c.l)): continue
            ft = g.get('FilingType', '')
            kind = 'ptr-pdfs' if ft == 'P' else 'financial-pdfs'
            yr = g.get('Year') or g['IndexYear']
            hits.append({'name': f"{g.get('First')} {g.get('Last')} {g.get('Suffix') or ''}".strip(), 'district': g.get('StateDst'),
                         'type': ft, 'type_label': FD_TYPES.get(ft, ft), 'year': yr, 'filed': g.get('FilingDate'), 'doc_id': g.get('DocID'),
                         'url': FD_PDF.format(kind=kind, y=yr, doc=g.get('DocID'))})
        hits.sort(key=lambda h: (str(h['year']), h['filed'] or ''))
        R[c.id]['house_disclosures'] = {'searched': bool(idx), 'filings': hits,
            'note': ('Senate candidates file with the Senate (efdsearch.senate.gov), and governors with their state; '
                     'only House filings appear here.') if c.office != 'house' else ''}
        if pdfs:
            for h in hits:
                if h['type'] == 'P' and not ptr: continue
                if h['type'] == 'X': continue
                dest = os.path.join(RAW, 'house_fd', 'pdf', c.id, f"{h['year']}_{h['type']}_{h['doc_id']}.pdf")
                if fetch(h['url'], dest): h['file'] = os.path.relpath(dest, OUT)
                time.sleep(0.3)
    n = sum(1 for c in cands if R[c.id]['house_disclosures']['filings'])
    log(f'  done: {n} candidate(s) have House filings')

# ---------------------------------------------------------------- 3. election-certification roll calls
def run_certification(cands, R):
    log('\n[3/4] Votes on objections to certified electoral votes')
    for c in cands: R[c.id]['certification_votes'] = []
    ok = 0
    for chamber, date, label, url in CERT_VOTES:
        b = fetch(url, os.path.join(RAW, 'certification', url.rsplit('/', 1)[1]))
        if not b: continue
        ok += 1
        root = ET.parse(b).getroot()
        rows = []
        if chamber == 'house':
            for rv in root.iter('recorded-vote'):
                lg = rv.find('legislator'); v = rv.find('vote')
                if lg is None or v is None: continue
                rows.append((lg.get('unaccented-name') or lg.text or '', lg.get('state', ''), lg.get('party', ''), v.text or ''))
        else:
            for m in root.iter('member'):
                rows.append(((m.findtext('last_name') or '') + ' ' + (m.findtext('first_name') or ''), m.findtext('state') or '', m.findtext('party') or '', m.findtext('vote_cast') or ''))
        for c in cands:
            for nm, st, party, vote in rows:
                if st != c.state: continue
                toks = norm(nm)
                if all(x in toks for x in c.l):
                    if len([1 for n2, s2, _, _ in rows if s2 == st and all(x in norm(n2) for x in c.l)]) > 1 and not c.matches_tokens(set(toks)):
                        continue
                    R[c.id]['certification_votes'].append({'chamber': chamber, 'date': date, 'objection': label, 'vote': vote,
                        'meaning': 'Yea = voted to sustain the objection (reject the certified electoral votes)', 'roll_call': url, 'listed_as': nm.strip()})
    log(f'  done: read {ok} of {len(CERT_VOTES)} roll calls; {sum(1 for c in cands if R[c.id]["certification_votes"])} candidate(s) voted on one')

# ---------------------------------------------------------------- 4. CourtListener
def run_courts(cands, R, token):
    log('\n[4/4] Court records (CourtListener: federal dockets and court opinions)')
    if not token:
        log('  skipped: no token. Make a free account at www.courtlistener.com, copy your API token from your'
            '\n  profile, then run:  COURTLISTENER_TOKEN=yourtoken python3 ots_records_pull.py --only courts')
        for c in cands: R[c.id]['courts'] = {'searched': False}
        return
    H = {'Authorization': f'Token {token}', 'Accept': 'application/json'}
    for i, c in enumerate(cands, 1):
        res = {'searched': True, 'query': f'"{c.name()}"'}
        for typ, label in (('r', 'federal_dockets'), ('o', 'opinions')):
            dest = os.path.join(RAW, 'courtlistener', f'{c.id}_{typ}.json')
            if not os.path.exists(dest):
                q = urllib.parse.urlencode({'q': f'"{c.name()}"', 'type': typ, 'order_by': 'dateFiled desc'})
                b = fetch(f'{CL_SEARCH}?{q}', headers=H)
                if b is None: res['searched'] = False; continue
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, 'wb') as f: f.write(b)
                time.sleep(1.5)
            d = json.load(open(dest))
            res[label + '_count'] = d.get('count')
            res[label] = [{'case': x.get('caseName'), 'court': x.get('court') or x.get('court_id'), 'filed': x.get('dateFiled'),
                           'docket': x.get('docketNumber'), 'url': 'https://www.courtlistener.com' + (x.get('absolute_url') or '')}
                          for x in (d.get('results') or [])[:20]]
        res['note'] = 'Full-text name search: hits include namesakes and passing mentions, so each needs a human check.'
        R[c.id]['courts'] = res
        if i % 10 == 0: log(f'  {i} of {len(cands)}')
    log('  done')

# ---------------------------------------------------------------- output
def write_outputs(cands, R):
    json.dump({'pulled': NOW, 'candidates': R}, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, 'summary.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id', 'name', 'state', 'office', 'district', 'fara_searched', 'fara_name_matches', 'house_filings',
                    'certification_votes', 'courts_searched', 'federal_dockets', 'opinions'])
        for c in cands:
            r = R[c.id]; ct = r.get('courts', {})
            w.writerow([c.id, c.name(), c.state, c.office, c.district, r.get('fara', {}).get('searched'), len(r.get('fara', {}).get('hits', [])),
                        len(r.get('house_disclosures', {}).get('filings', [])),
                        '; '.join(f"{v['date']} {v['objection']}: {v['vote']}" for v in r.get('certification_votes', [])),
                        ct.get('searched'), ct.get('federal_dockets_count', ''), ct.get('opinions_count', '')])
    # upload bundles, 25 MB each: summary first, then the disclosure PDFs
    for old in os.listdir(OUT):
        if old.startswith('upload_') and old.endswith('.zip'): os.remove(os.path.join(OUT, old))
    files = [('summary.json', os.path.join(OUT, 'summary.json')), ('summary.csv', os.path.join(OUT, 'summary.csv'))]
    pdfdir = os.path.join(RAW, 'house_fd', 'pdf')
    for root, _, fs in os.walk(pdfdir):
        for fn in sorted(fs):
            if fn.endswith('.pdf'):
                files.append((os.path.relpath(os.path.join(root, fn), RAW), os.path.join(root, fn)))
    n, size, z = 0, 0, None
    for arc, path in files:
        s = os.path.getsize(path)
        if z is None or size + s > 25 * 1024 * 1024:
            if z: z.close()
            n += 1; size = 0
            z = zipfile.ZipFile(os.path.join(OUT, f'upload_{n}.zip'), 'w', zipfile.ZIP_DEFLATED)
        z.write(path, arc); size += s
    if z: z.close()
    return n

def main():
    a = sys.argv[1:]
    state = a[a.index('--state') + 1].upper() if '--state' in a else None
    only = set(a[a.index('--only') + 1].split(',')) if '--only' in a else {'fara', 'disclosures', 'certification', 'courts'}
    token = os.environ.get('COURTLISTENER_TOKEN') or (a[a.index('--token') + 1] if '--token' in a else None)
    cands = [Cand(t) for t in CANDIDATES if not state or t[3] == state]
    os.makedirs(RAW, exist_ok=True)
    log(f'OTS records pull: {len(cands)} candidates, saving to {OUT}')
    sp = os.path.join(OUT, 'summary.json')
    R = json.load(open(sp)).get('candidates', {}) if os.path.exists(sp) else {}
    for c in cands:
        R.setdefault(c.id, {}).update({'name': c.name(), 'state': c.state, 'office': c.office, 'district': c.district})
    if 'fara' in only: run_fara(cands, R)
    if 'disclosures' in only: run_disclosures(cands, R, pdfs='--no-pdfs' not in a, ptr='--with-ptr' in a)
    if 'certification' in only: run_certification(cands, R)
    if 'courts' in only: run_courts(cands, R, token)
    n = write_outputs(cands, R)
    log(f'\nFinished. Upload these {n} file(s) from {OUT} into the chat: ' + ', '.join(f'upload_{i}.zip' for i in range(1, n + 1)))

if __name__ == '__main__':
    main()
