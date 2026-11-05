"""Canonical nodes for the 1948 network (The Baseline + The Road to 1948).
Each line: id | name | kind | cluster | aliases (regex, ';'-separated; case-sensitive).
Kinds: person, institution, company, government, document, event.
Only actors, institutions, documents and events: no ethnic or religious group is ever a node
(ties come from documents, never identity). Historians and outlets cited as sources are not nodes."""

RAW = r"""
# ---------- the Zionist movement ----------
herzl|Theodor Herzl|person|zionist movement|Theodor Herzl;Herzl
weizmann|Chaim Weizmann|person|zionist movement|Chaim Weizmann;Weizmann
sokolow|Nahum Sokolow|person|zionist movement|Nahum Sokolow;Sokolow
wolffsohn|David Wolffsohn|person|zionist movement|David Wolffsohn;Wolffsohn
nordau|Max Nordau|person|zionist movement|Max Nordau;Nordau
bengurion|David Ben-Gurion|person|zionist movement|David Ben-Gurion;Ben-Gurion;Ben Gurion
jabotinsky|Ze'ev Jabotinsky|person|zionist movement|Ze'ev Jabotinsky;Ze’ev Jabotinsky;Vladimir Jabotinsky;Jabotinsky
ahadhaam|Ahad Ha'am|person|zionist movement|Ahad Ha'am;Ahad Ha’am;Asher Ginsberg
pinsker|Leon Pinsker|person|zionist movement|Leon Pinsker;Pinsker
hess|Moses Hess|person|zionist movement|Moses Hess
alkalai|Yehuda Alkalai|person|zionist movement|Alkalai
kalischer|Zvi Hirsch Kalischer|person|zionist movement|Kalischer
birnbaum|Nathan Birnbaum|person|zionist movement|Nathan Birnbaum;Birnbaum
zangwill|Israel Zangwill|person|zionist movement|Israel Zangwill;Zangwill
ruppin|Arthur Ruppin|person|zionist movement|Arthur Ruppin;Ruppin
hankin|Yehoshua Hankin|person|zionist movement|Yehoshua Hankin;Hankin
arlosoroff|Chaim Arlosoroff|person|zionist movement|Chaim Arlosoroff;Arlosoroff
sharett|Moshe Sharett|person|zionist movement|Moshe Sharett;Moshe Shertok;Sharett;Shertok
meir|Golda Meir|person|zionist movement|Golda Meir;Golda Meyerson;Golda Myerson;Meyerson
goldmann|Nahum Goldmann|person|zionist movement|Nahum Goldmann;Goldmann
benzvi|Yitzhak Ben-Zvi|person|zionist movement|Yitzhak Ben-Zvi;Ben-Zvi
begin|Menachem Begin|person|militias|Menachem Begin;Begin(?!ning|s\b)
dayan|Moshe Dayan|person|militias|Moshe Dayan;Dayan
allon|Yigal Allon|person|militias|Yigal Allon;Allon
rabin|Yitzhak Rabin|person|militias|Yitzhak Rabin;Rabin
magnes|Judah Magnes|person|zionist movement|Judah Magnes;Judah L. Magnes;Magnes
buber|Martin Buber|person|zionist movement|Martin Buber;Buber
rutenberg|Pinhas Rutenberg|person|finance|Pinhas Rutenberg;Rutenberg
thon|Jacob Thon|person|zionist movement|Jacob Thon
kahn_j|Jacobus Kahn|person|finance|Jacobus Kahn
warburg_o|Otto Warburg|person|zionist movement|Otto Warburg
wzo|World Zionist Organization|institution|zionist movement|World Zionist Organization;Zionist Organization(?! of America);WZO
congress1897|First Zionist Congress (Basel, 1897)|event|zionist movement|First Zionist Congress;Basel Congress;Zionist Congress of 1897;Basel Program;Basel Programme
zionist_congress|Zionist Congress|institution|zionist movement|(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|\d+th) Zionist Congress;Zionist Congress(?:es)?(?! of 1897);(?:Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Twentieth|Twenty-\w+) Congress@rd1;(?:Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth) Congress@rd0
actions_comm|Zionist Actions Committees|institution|zionist movement|Actions Committee;Zionist General Council
jewish_agency|Jewish Agency|institution|zionist movement|Jewish Agency
yishuv|Yishuv institutions (Va'ad Leumi)|institution|zionist movement|Va'ad Leumi;Vaad Leumi;National Council of the Yishuv
palestine_office|Palestine Office (Jaffa)|institution|zionist movement|Palestine Office
efz|English Zionist Federation|institution|zionist movement|English Zionist Federation
fedam|Federation of American Zionists|institution|us lobby|Federation of American Zionists
zoa|Zionist Organization of America|institution|us lobby|Zionist Organization of America;ZOA
hadassah|Hadassah|institution|us lobby|Hadassah
azec|American Zionist Emergency Council|institution|us lobby|American Zionist Emergency Council;AZEC;Emergency Committee for Zionist Affairs;American Zionist Emergency Committee
azcpa|American Zionist Committee for Public Affairs (later AIPAC)|institution|us lobby|American Zionist Committee for Public Affairs;AIPAC;American Israel Public Affairs Committee
apc|American Palestine Committee|institution|us lobby|American Palestine Committee
ccp|Christian Council on Palestine|institution|us lobby|Christian Council on Palestine
uja|United Jewish Appeal|institution|us lobby|United Jewish Appeal;UJA
upa|United Palestine Appeal|institution|us lobby|United Palestine Appeal
jdc|American Jewish Joint Distribution Committee|institution|us lobby|Joint Distribution Committee;\bJDC\b;the Joint\b
ajc|American Jewish Committee|institution|us lobby|American Jewish Committee
sonneborn_inst|Sonneborn Institute|institution|militias|Sonneborn Institute
biltmore|Biltmore Program (1942)|document|zionist movement|Biltmore Program;Biltmore Conference;Biltmore
ito|Jewish Territorial Organization|institution|zionist movement|Jewish Territorial Organization;\bITO\b
mizrachi|Mizrachi movement|institution|zionist movement|Mizrachi(?! Jews)
revisionists|Revisionist Zionist movement|institution|zionist movement|Revisionist Zionis[mt];New Zionist Organization;Revisionist movement;Revisionist party
betar|Betar|institution|militias|Betar
histadrut|Histadrut|institution|zionist movement|Histadrut;General Federation of Hebrew Workers
solel_boneh|Solel Boneh|company|finance|Solel Boneh
mapai|Mapai|institution|zionist movement|Mapai
brit_shalom|Brit Shalom|institution|zionist movement|Brit Shalom
hebrew_univ|Hebrew University|institution|zionist movement|Hebrew University
bilu|BILU|institution|zionist movement|\bBILU\b
hovevei|Hovevei Zion (Lovers of Zion)|institution|zionist movement|Hovevei Zion;Hibbat Zion;Lovers of Zion
derjudenstaat|Der Judenstaat (1896)|document|zionist movement|Der Judenstaat;The Jewish State\b
autoemancipation|Auto-Emancipation (1882)|document|zionist movement|Auto-Emancipation;Autoemancipation
# ---------- finance and land ----------
jct|Jewish Colonial Trust|company|finance|Jewish Colonial Trust
apc_bank|Anglo-Palestine Company (Bank Leumi)|company|finance|Anglo-Palestine Company;Anglo-Palestine Bank;Bank Leumi
jnf|Jewish National Fund|institution|finance|Jewish National Fund;\bJNF\b;Keren Kayemeth
keren_hayesod|Keren Hayesod|institution|finance|Keren Hayesod
pldc|Palestine Land Development Company|company|finance|Palestine Land Development Company;Palestine Land Development Co\.;\bPLDC\b
jca|Jewish Colonization Association|institution|finance|Jewish Colonization Association;\bJCA\b;\bICA\b
pica|Palestine Jewish Colonization Association (PICA)|institution|finance|Palestine Jewish Colonization Association;\bPICA\b
haavara|Haavara Agreement (1933)|document|finance|Haavara
pec|Palestine Electric Corporation|company|finance|Palestine Electric Corporation;Jaffa Electric Company;Rutenberg concession
sursock|Sursock family|company|land|Sursock
hirsch|Baron Maurice de Hirsch|person|finance|Maurice de Hirsch;Baron de Hirsch;Baron Maurice;Hirsch(?!feld)
montefiore|Moses Montefiore|person|finance|Moses Montefiore;Montefiore
feinberg|Abraham Feinberg|person|us lobby|Abraham Feinberg;Feinberg@rd4;Feinberg@rd5;Feinberg@rd6
sonneborn|Rudolf Sonneborn|person|militias|Rudolf Sonneborn;Sonneborn(?! Institute)
montor|Henry Montor|person|us lobby|Henry Montor;Montor
schwimmer|Al Schwimmer|person|militias|Al Schwimmer;Adolph Schwimmer;Schwimmer
warburg_f|Felix Warburg|person|finance|Felix Warburg
warburg_p|Paul Warburg|person|finance|Paul Warburg
schiff|Jacob Schiff|person|finance|Jacob Schiff;Schiff
# ---------- Rothschild family (documented individuals and firms only) ----------
mayer_amschel|Mayer Amschel Rothschild|person|rothschild|Mayer Amschel Rothschild;Mayer Amschel
nathan_r|Nathan Mayer Rothschild|person|rothschild|Nathan Mayer Rothschild;Nathan Rothschild;Nathan Mayer
james_mayer|James Mayer de Rothschild|person|rothschild|James Mayer de Rothschild;James Mayer
lionel_r|Lionel de Rothschild|person|rothschild|Lionel de Rothschild;Lionel
natty|Nathan "Natty" Rothschild, 1st Baron|person|rothschild|Natty;1st Baron Rothschild;Lord Rothschild@rd1
walter_r|Walter Rothschild, 2nd Baron|person|rothschild|Walter Rothschild;Lord Walter Rothschild;Lord Rothschild@rd2;Lionel Walter
edmond_r|Edmond de Rothschild|person|rothschild|Edmond de Rothschild;Baron Edmond;Edmond(?! Safra)
james_armand|James Armand de Rothschild|person|rothschild|James Armand;James de Rothschild@rd2;James de Rothschild@rd3;James de Rothschild@rd5;James de Rothschild@rd6
nm_rothschild|N M Rothschild & Sons|company|rothschild|N M Rothschild;N\. M\. Rothschild;NM Rothschild
rothschild_freres|de Rothschild Frères|company|rothschild|de Rothschild Frères;Rothschild Frères
torlonia|Torlonia bank|company|finance|Torlonia
# ---------- British state ----------
uk|British Government|government|british state|British government;British Government;His Majesty's Government;HM Government;Whitehall
war_cabinet|British War Cabinet|government|british state|War Cabinet
colonial_office|Colonial Office|government|british state|Colonial Office
foreign_office|Foreign Office|government|british state|Foreign Office
parliament|British Parliament|government|british state|House of Commons;House of Lords;Parliament
mandate_admin|British Mandate administration|government|british state|Mandate government;Mandatory government;Mandate administration;Mandatory administration;Palestine government
city_london|City of London Corporation|government|british state|City of London;Remembrancer
balfour|Arthur Balfour|person|british state|Arthur Balfour;Arthur James Balfour;Lord Balfour;Balfour(?! Declaration)
lloydgeorge|David Lloyd George|person|british state|Lloyd George
churchill|Winston Churchill|person|british state|Winston Churchill;Churchill(?! White Paper)
samuel|Herbert Samuel|person|british state|Herbert Samuel;Sir Herbert
montagu|Edwin Montagu|person|british state|Edwin Montagu;Montagu
chamberlain_j|Joseph Chamberlain|person|british state|Joseph Chamberlain
chamberlain_n|Neville Chamberlain|person|british state|Neville Chamberlain
sykes|Mark Sykes|person|british state|Mark Sykes;Sykes(?!-Picot)
mcmahon|Henry McMahon|person|british state|Henry McMahon;McMahon(?!-Hussein| correspondence)
allenby|Edmund Allenby|person|british state|Allenby
storrs|Ronald Storrs|person|british state|Ronald Storrs;Storrs
bevin|Ernest Bevin|person|british state|Ernest Bevin;Bevin
attlee|Clement Attlee|person|british state|Clement Attlee;Attlee
wingate|Orde Wingate|person|militias|Orde Wingate;Wingate
palmerston|Lord Palmerston|person|british state|Palmerston
shaftesbury|Lord Shaftesbury|person|british state|Shaftesbury
disraeli|Benjamin Disraeli|person|british state|Disraeli
cromer|Lord Cromer|person|british state|Cromer
peel|Peel Commission (1937)|institution|british state|Peel Commission;Peel Report;Peel(?! Street)
shaw|Shaw Commission (1930)|institution|british state|Shaw Commission;Shaw Report
hopesimpson|Hope Simpson Report (1930)|document|british state|Hope Simpson;Hope-Simpson
woodhead|Woodhead Commission (1938)|institution|british state|Woodhead
wp1922|Churchill White Paper (1922)|document|british state|Churchill White Paper;1922 White Paper
wp1930|Passfield White Paper (1930)|document|british state|Passfield
wp1939|White Paper of 1939|document|british state|1939 White Paper;White Paper of 1939;MacDonald White Paper;White Paper(?! of 1922)
bank_england|Bank of England|company|british state|Bank of England
jewish_legion|Jewish Legion / Zion Mule Corps|institution|militias|Jewish Legion;Zion Mule Corps;Royal Fusiliers
# ---------- documents and international decisions ----------
balfour_decl|Balfour Declaration (1917)|document|international|Balfour Declaration
sykes_picot|Sykes-Picot Agreement (1916)|document|international|Sykes-Picot;Sykes–Picot
mcmahon_corr|Hussein-McMahon Correspondence (1915-16)|document|international|McMahon[- ]Hussein;Hussein[- ]McMahon;McMahon correspondence
faisal_weizmann|Faisal-Weizmann Agreement (1919)|document|international|Faisal[- –]Weizmann
san_remo|San Remo Conference (1920)|event|international|San Remo
mandate|Mandate for Palestine (1922)|document|international|Mandate for Palestine;Palestine Mandate;British Mandate;the Mandate\b;Article 4 of the Mandate
league|League of Nations|institution|international|League of Nations;Permanent Mandates Commission;League Council
covenant22|League Covenant, Article 22|document|international|Article 22
paris_conf|Paris Peace Conference (1919)|event|international|Paris Peace Conference;Peace Conference
king_crane|King-Crane Commission (1919)|institution|international|King[- –]Crane
lausanne|Lausanne Conference (1949)|event|international|Lausanne
un|United Nations|institution|international|United Nations(?! Special| General| Relief| Security| Conciliation);\bUN\b(?! General| Security| Conciliation)
unga|UN General Assembly|institution|international|General Assembly
unsc|UN Security Council|institution|international|Security Council
unscop|UNSCOP|institution|international|UNSCOP;United Nations Special Committee
res181|UN Resolution 181 (Partition Plan)|document|international|Resolution 181;Partition Plan;partition resolution
res194|UN Resolution 194|document|international|Resolution 194
unrwa|UNRWA|institution|international|UNRWA
ccp_un|UN Conciliation Commission for Palestine|institution|international|Conciliation Commission
bernadotte|Folke Bernadotte|person|international|Folke Bernadotte;Count Bernadotte;Bernadotte
bunche|Ralph Bunche|person|international|Ralph Bunche;Bunche
anglo_am|Anglo-American Committee of Inquiry (1946)|institution|international|Anglo-American Committee
armistice49|1949 Armistice Agreements|document|international|Armistice Agreements?;armistice agreements?;Rhodes
decl_indep|Israeli Declaration of Independence (1948)|document|israel state|Declaration of Independence;Declaration of the Establishment
law_return|Law of Return (1950)|document|israel state|Law of Return
absentees|Absentees' Property Law (1950)|document|israel state|Absentees' Property Law;Absentees’ Property Law;Absentee Property Law
provisional|Provisional Government of Israel|government|israel state|Provisional Government;Provisional State Council;Provisional Council of State;People's Council
idf|Israel Defense Forces|institution|militias|Israel Defense Forces;\bIDF\b
knesset|Knesset|government|israel state|Knesset
israel_gov|Government of Israel|government|israel state|Israeli government;Government of Israel;government of Israel;Israeli cabinet
plan_dalet|Plan Dalet (1948)|document|militias|Plan Dalet;Plan D\b
# ---------- militias ----------
haganah|Haganah|institution|militias|Haganah
palmach|Palmach|institution|militias|Palmach
irgun|Irgun|institution|militias|Irgun;Etzel
lehi|Lehi (Stern Gang)|institution|militias|Lehi;Stern Gang;Stern Group
mossad_aliyah|Mossad LeAliyah Bet|institution|militias|Mossad LeAliyah Bet;Aliyah Bet
brihah|Brihah|institution|militias|Brihah;Bricha
nili|NILI|institution|militias|\bNILI\b
hashomer|Hashomer|institution|militias|Hashomer
rekhesh|Rekhesh (arms procurement)|institution|militias|Rekhesh
balak|Operation Balak (Czech arms airlift)|event|militias|Operation Balak;Balak
deir_yassin|Deir Yassin killings (April 1948)|event|1948 war|Deir Yassin
king_david|King David Hotel bombing (1946)|event|militias|King David Hotel
altalena|Altalena affair (1948)|event|militias|Altalena
lydda|Lydda and Ramle expulsions (July 1948)|event|1948 war|Lydda;Lod\b;Ramle;Ramla
tantura|Tantura (1948)|event|1948 war|Tantura
kafr_qasim|Kafr Qasim massacre (1956)|event|israel state|Kafr Qasim
# ---------- Ottoman ----------
ottoman|Ottoman Empire|government|ottoman|Ottoman Empire;Ottoman government;Sublime Porte;the Porte;Ottoman state
abdulhamid|Sultan Abdul Hamid II|person|ottoman|Abdul Hamid II;Abdülhamid;Abdul Hamid
land_code|Ottoman Land Code (1858)|document|ottoman|Ottoman Land Code;Land Code;1858 Land Law
mutasarrif|Mutasarrifate of Jerusalem|government|ottoman|Mutasarrifate
jamal_pasha|Jamal Pasha|person|ottoman|Jamal Pasha;Djemal Pasha
capitulations|Capitulations|document|ottoman|Capitulations
# ---------- Arab and Palestinian leadership ----------
husseini_amin|Hajj Amin al-Husseini|person|arab leadership|Hajj Amin al-Husseini;Hajj Amin al-Husayni;Amin al-Husseini;Amin al-Husayni;Hajj Amin;the Mufti;Grand Mufti
musa_kazim|Musa Kazim al-Husseini|person|arab leadership|Musa Kazim
jamal_h|Jamal al-Husseini|person|arab leadership|Jamal al-Husseini;Jamal al-Husayni
abd_qadir|Abd al-Qadir al-Husayni|person|arab leadership|Abd al-Qadir al-Husayni;Abd al-Qadir al-Husseini;Abd al-Qadir
nashashibi_r|Raghib al-Nashashibi|person|arab leadership|Raghib al-Nashashibi;Raghib Nashashibi;Nashashibi
ruhi_khalidi|Ruhi al-Khalidi|person|arab leadership|Ruhi al-Khalidi
yusuf_khalidi|Yusuf Diya al-Khalidi|person|arab leadership|Yusuf Diya al-Khalidi;Yusuf Diya
awni|Awni Abd al-Hadi|person|arab leadership|Awni Abd al-Hadi;Awni
qassam|Izz al-Din al-Qassam|person|arab leadership|Izz al-Din al-Qassam;al-Qassam;Qassam
ahc|Arab Higher Committee|institution|arab leadership|Arab Higher Committee
smc|Supreme Muslim Council|institution|arab leadership|Supreme Muslim Council
arab_exec|Arab Executive|institution|arab leadership|Arab Executive
arab_congress|Palestine Arab Congress|institution|arab leadership|Palestine Arab Congress;Arab Congress;(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh) Congress@rd2;(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh) Congress@rd3
pal_arab_deleg|Palestine Arab Delegation|institution|arab leadership|Palestine Arab Delegation
all_pal_gov|All-Palestine Government|government|arab leadership|All-Palestine Government
army_holy_war|Army of the Holy War|institution|arab leadership|Army of (?:the )?Holy War
filastin|Filastin (newspaper)|company|arab leadership|Filastin
alkarmil|al-Karmil (newspaper)|company|arab leadership|al-Karmil
revolt36|Arab Revolt (1936-39)|event|arab leadership|Arab Revolt;1936[–-]39 revolt;Great Revolt
# ---------- Arab states and leaders ----------
hussein_sharif|Sharif Hussein of Mecca|person|arab states|Sharif Hussein;Hussein bin Ali;Sharif of Mecca
faisal|Emir Faisal|person|arab states|Emir Faisal;Faisal(?![- –]Weizmann)
abdullah|King Abdullah I of Transjordan|person|arab states|Emir Abdullah;King Abdullah;Abdullah
ibn_saud|Ibn Saud|person|arab states|Ibn Saud;King Abdulaziz
transjordan|Transjordan / Jordan|government|arab states|Transjordan;Hashemite Kingdom
arab_legion|Arab Legion|institution|arab states|Arab Legion
glubb|John Bagot Glubb|person|arab states|Glubb
arab_league|Arab League|institution|arab states|Arab League
ala|Arab Liberation Army|institution|arab states|Arab Liberation Army
egypt|Egypt (government)|government|arab states|Egyptian government;Egypt(?:ian)? (?:army|forces)
iraq|Iraq (government)|government|arab states|Iraqi government;Iraqi (?:army|forces)
syria|Syria (government)|government|arab states|Syrian government;Syrian (?:army|forces)
zaim|Husni al-Za'im|person|arab states|Husni al-Za'im;Za'im;Za’im
farhud|Farhud (Baghdad, 1941)|event|arab states|Farhud
nasser|Gamal Abdel Nasser|person|arab states|Nasser
# ---------- United States ----------
us_gov|US Government|government|us government|US government;U\.S\. government;United States government;American government
white_house|White House|government|us government|White House
state_dept|State Department|government|us government|State Department;Department of State
jcs|Joint Chiefs of Staff|government|us government|Joint Chiefs
pentagon|War / Defense Department|government|us government|War Department;Defense Department;Pentagon;Department of Defense
cia|CIA|government|us government|\bCIA\b;Central Intelligence Agency
oss|OSS|government|us government|\bOSS\b;Office of Strategic Services
fbi|FBI|government|us government|\bFBI\b
doj|Justice Department|government|us government|Justice Department;Department of Justice
us_congress|US Congress|government|us government|US Congress;U\.S\. Congress;United States Congress;American Congress;House of Representatives;Senate Foreign Relations;the Senate\b;Congress(?! of| Committee|ional Research)@rd4;Congress(?! of| Committee|ional Research)@rd5;Congress(?! of| Committee|ional Research)@rd6
exim|Export-Import Bank|government|us government|Export-Import Bank
fara|Foreign Agents Registration Act|document|us government|Foreign Agents Registration Act;\bFARA\b
fdr|Franklin D. Roosevelt|person|us government|Franklin Roosevelt;Franklin D\. Roosevelt;FDR;President Roosevelt;(?<!Kermit )(?<!Theodore )(?<!Eleanor )Roosevelt(?! Jr)
truman|Harry Truman|person|us government|Harry Truman;Harry S\. Truman;Truman
wilson|Woodrow Wilson|person|us government|Woodrow Wilson;President Wilson;Wilson
marshall_g|George Marshall|person|us government|George Marshall;George C\. Marshall;Secretary Marshall;Marshall(?! Plan)@rd5;Marshall@rd6
forrestal|James Forrestal|person|us government|James Forrestal;Forrestal
lovett|Robert Lovett|person|us government|Robert Lovett;Lovett
henderson|Loy Henderson|person|us government|Loy Henderson;Henderson@rd5
clifford|Clark Clifford|person|us government|Clark Clifford;Clifford
niles|David Niles|person|us government|David Niles;Niles
jacobson|Eddie Jacobson|person|us lobby|Eddie Jacobson;Jacobson
stimson|Henry Stimson|person|us government|Henry Stimson;Stimson
wallace|Henry Wallace|person|us government|Henry Wallace;Wallace
kermit|Kermit Roosevelt Jr.|person|us government|Kermit Roosevelt
taft|Robert Taft|person|us government|Robert Taft;Taft
wagner|Robert Wagner|person|us government|Robert Wagner;Senator Wagner
bloom|Sol Bloom|person|us government|Sol Bloom
brandeis|Louis Brandeis|person|us lobby|Louis Brandeis;Brandeis
wise|Stephen Wise|person|us lobby|Stephen Wise;Stephen S\. Wise;Rabbi Wise
silver|Abba Hillel Silver|person|us lobby|Abba Hillel Silver;Hillel Silver;Rabbi Silver;Silver@rd4;Silver@rd5
neumann|Emanuel Neumann|person|us lobby|Emanuel Neumann;Neumann
bergson|Peter Bergson (Hillel Kook)|person|us lobby|Peter Bergson;Hillel Kook;Bergson Group;Bergson
kenen|Isaiah Kenen|person|us lobby|Isaiah Kenen;Si Kenen;Kenen
einstein|Albert Einstein|person|us lobby|Albert Einstein;Einstein
blackstone|William Blackstone|person|christian zionism|William Blackstone;Blackstone Memorial;Blackstone
scofield|Cyrus Scofield / Scofield Reference Bible|document|christian zionism|Scofield
darby|John Nelson Darby|person|christian zionism|John Nelson Darby;Darby
# ---------- Europe / Germany / USSR ----------
nazi_germany|Nazi Germany|government|nazi germany|Nazi Germany;Nazi government;Third Reich;Reich
hitler|Adolf Hitler|person|nazi germany|Adolf Hitler;Hitler
eichmann|Adolf Eichmann|person|nazi germany|Adolf Eichmann;Eichmann
heydrich|Reinhard Heydrich|person|nazi germany|Reinhard Heydrich;Heydrich
wannsee|Wannsee Conference (1942)|event|nazi germany|Wannsee
nuremberg_laws|Nuremberg Laws (1935)|document|nazi germany|Nuremberg Laws
evian|Évian Conference (1938)|event|international|Évian;Evian
kaiser|Kaiser Wilhelm II|person|europe|Kaiser Wilhelm;Wilhelm II;the Kaiser
plehve|Vyacheslav von Plehve|person|europe|Plehve
russia_imp|Imperial Russia|government|europe|Imperial Russia;Russian Empire;Tsarist;tsarist government
kishinev|Kishinev pogrom (1903)|event|europe|Kishinev
dreyfus|Dreyfus Affair|event|europe|Dreyfus
marr|Wilhelm Marr|person|europe|Wilhelm Marr;Marr\b
ussr|Soviet Union|government|soviet bloc|Soviet Union;USSR;Soviet government;Moscow
stalin|Joseph Stalin|person|soviet bloc|Stalin
gromyko|Andrei Gromyko|person|soviet bloc|Andrei Gromyko;Gromyko
czechoslovakia|Czechoslovakia (arms supplier)|government|soviet bloc|Czechoslovakia;Czechoslovak government
france_gov|French Government|government|europe|French government;France(?:'s)? government
napoleon|Napoleon Bonaparte|person|europe|Napoleon(?!ic)
# ---------- religious institutions and dissent ----------
vatican|Holy See / Vatican|government|religion|Holy See;Vatican;Papal States
pius10|Pope Pius X|person|religion|Pius X\b
pius12|Pope Pius XII|person|religion|Pius XII
gregory16|Pope Gregory XVI|person|religion|Gregory XVI
bund|Jewish Labor Bund|institution|religion|Jewish Labor Bund;\bBund\b
reform|Reform Judaism (Pittsburgh Platform, 1885)|institution|religion|Pittsburgh Platform;Reform Judaism;Reform movement
acj|American Council for Judaism|institution|religion|American Council for Judaism
agudah|Agudat Israel|institution|religion|Agudat Israel;Agudath Israel;Agudah
neturei|Neturei Karta|institution|religion|Neturei Karta
satmar|Satmar / Joel Teitelbaum|person|religion|Satmar;Teitelbaum;Vayoel Moshe;VaYoel Moshe
dehaan|Jacob Israel de Haan|person|religion|Jacob Israel de Haan;Jacob de Haan;de Haan;De Haan
kook|Rav Abraham Isaac Kook|person|religion|Rav Kook;Abraham Isaac Kook
# ---------- 1948 war and after ----------
nakba|Nakba / 1948 displacement|event|1948 war|Nakba
transfer_comm|Transfer Committee (1948)|institution|1948 war|Transfer Committee
military_gov|Military Government over Arab citizens (1948-66)|government|israel state|military government@rd6;military rule@rd6;Military Government@rd6
custodian|Custodian of Absentee Property|government|israel state|Custodian of Absentee Property;Custodian
ezra_nehemiah|Operation Ezra and Nehemiah (1950-51)|event|israel state|Ezra and Nehemiah;Operation Ezra
magic_carpet|Operation Magic Carpet (1949-50)|event|israel state|Magic Carpet;On Eagles' Wings
yachin|Operation Yachin (1961-64)|event|israel state|Operation Yachin;Yachin
yemenite_affair|Yemenite Children Affair|event|israel state|Yemenite Children

# ---------- colonies and Rothschild institutions (added Nov 2026) ----------
rishon|Rishon LeZion (colony, 1882)|place|settlement|Rishon LeZion;Rishon Lezion;Rishon le-Zion
zikhron|Zikhron Ya'akov (colony, 1882)|place|settlement|Zikhron Ya'akov;Zichron Ya'akov;Zikhron Yaakov
rosh_pinna|Rosh Pinna (colony, 1882)|place|settlement|Rosh Pinna
mazkeret|Mazkeret Batya (colony, 1883)|place|settlement|Mazkeret Batya
ekron|Ekron (colony, 1884)|place|settlement|Ekron@rd0;Ekron@ch01
metulla|Metulla (colony, 1896)|place|settlement|Metulla
mikveh|Mikveh Israel (agricultural school, 1870)|place|settlement|Mikveh Israel
mohilever|Rabbi Samuel Mohilever|person|zionist movement|Samuel Mohilever;Mohilever
dorothy|Dorothy de Rothschild|person|rothschild|Dorothy de Rothschild;Dorothy
yad_hanadiv|Yad Hanadiv (Rothschild charities in Israel)|institution|rothschild|Yad Hanadiv
ramat_hanadiv|Ramat HaNadiv (memorial and burial site)|place|rothschild|Ramat HaNadiv;Ramat Hanadiv
morgenthau|Henry Morgenthau Sr.|person|us government|Henry Morgenthau(?!,? Jr)

# ---------- American layer: organizations, intelligence, parties, money (added Nov 2026) ----------
shiloah|Reuven Shiloah (Zaslani)|person|intelligence|Reuven Shiloah;Reuven Zaslani;Shiloah;Zaslani
mossad|Mossad (founded 1949-51)|government|intelligence|\bMossad\b(?![ -]?[Ll]e)
ja_political|Jewish Agency Political Department|institution|intelligence|Jewish Agency's Political Department;Political Department of the Jewish Agency
kollek|Teddy Kollek|person|militias|Teddy Kollek;Kollek
hotel14|Hotel Fourteen (14 East 60th Street, New York)|place|militias|Hotel Fourteen
arazi|Yehuda Arazi|person|militias|Yehuda Arazi;Arazi
lansky|Meyer Lansky|person|militias|Meyer Lansky;Lansky
mickey_cohen|Mickey Cohen|person|militias|Mickey Cohen
siegel|Bugsy Siegel|person|militias|Bugsy Siegel;Benjamin Siegel
dafni|Reuven Dafni|person|militias|Reuven Dafni
americans_haganah|Americans for Haganah, Inc.|institution|us lobby|Americans for Haganah
voorhis|Voorhis Act|document|us government|Voorhis Act
neutrality|US Neutrality Acts|document|us government|Neutrality Acts?
hoover|J. Edgar Hoover|person|us government|J\. Edgar Hoover;Edgar Hoover
angleton|James Jesus Angleton|person|us government|James Jesus Angleton;James Angleton;Angleton
dnc|Democratic National Committee|institution|us parties|Democratic National Committee;\bDNC\b
conv1944|1944 Democratic National Convention|event|us parties|1944 Democratic (?:National )?[Cc]onvention
hannegan|Robert Hannegan|person|us parties|Robert Hannegan;Hannegan
pauley|Edwin Pauley|person|us parties|Edwin Pauley;Pauley
flynn_e|Edward J. Flynn|person|us parties|Edward J\. Flynn;Ed Flynn
walker_f|Frank C. Walker|person|us parties|Frank C\. Walker
kelly_e|Edward J. Kelly (Mayor of Chicago)|person|us parties|Edward J\. Kelly
allen_g|George E. Allen|person|us parties|George E\. Allen
byrnes|James F. Byrnes|person|us government|James F\. Byrnes;James Byrnes;Byrnes
kennan|George Kennan|person|us government|George Kennan;George F\. Kennan;Kennan
pps|State Department Policy Planning Staff|government|us government|Policy Planning Staff
pps_palestine|Policy Planning Staff report on Palestine (19 Jan 1948)|document|us government|PPS/19
mcclintock|Robert McClintock|person|us government|Robert McClintock;McClintock
connelly|Matthew Connelly|person|us government|Matthew Connelly
may12|White House meeting on Palestine (12 May 1948)|event|us government|meeting of 12 May 1948
recognition48|US recognition of Israel (14 May 1948)|event|us government|de facto recognition
fdr_letter45|Roosevelt letter to Ibn Saud (5 Apr 1945)|document|us government|letter of 5 April 1945
partition_notes|Truman administration notes on the partition vote (Nov 1947)|document|us government|notes on the partition vote
liberia|Liberia (government)|government|international|Liberian government;Liberian delegation
haiti|Haiti (government)|government|international|Haitian government;Haitian delegation
philippines|Philippines (government)|government|international|Philippine government;Philippine delegation
cuba|Cuba (government)|government|international|Cuban government;Cuban delegation
greece|Greece (government)|government|international|Greek government;Greek delegation
lansing|Robert Lansing|person|us government|Robert Lansing;Lansing
lansing_letter|Lansing letter to Wilson on Palestine (Dec 1917)|document|us government|Lansing's letter
frankfurter|Felix Frankfurter|person|us lobby|Felix Frankfurter;Frankfurter
faisal_frankfurter|Faisal-Frankfurter letter (3 Mar 1919)|document|international|Faisal[- –]Frankfurter;Feisal[- –]Frankfurter
gottheil|Richard Gottheil|person|us lobby|Richard Gottheil;Gottheil
pec_zionist|Provisional Executive Committee for General Zionist Affairs|institution|us lobby|Provisional Executive Committee
acpc|American Christian Palestine Committee|institution|christian zionism|American Christian Palestine Committee
azc|American Zionist Council|institution|us lobby|American Zionist Council
louis_marshall|Louis Marshall|person|us lobby|Louis Marshall
ajrc|American Jewish Relief Committee (1914)|institution|us lobby|American Jewish Relief Committee
technion|Technion (Haifa)|institution|zionist movement|Technion
belmont|August Belmont|person|finance|August Belmont
belmont_co|August Belmont & Co.|company|finance|Belmont & Co
josephs|J.L. & S.I. Joseph & Co.|company|finance|J\.L\. (?:and|&) S\.I\. Joseph
morgan|J. P. Morgan|person|finance|J\. ?P\. Morgan(?! &)(?! and Co);Pierpont Morgan
jpm_co|J.P. Morgan & Co.|company|finance|J\. ?P\. Morgan (?:&|and) Co
gold1895|Morgan-Belmont gold contract (8 Feb 1895)|document|finance|Morgan[- –]Belmont
cleveland|Grover Cleveland|person|us government|Grover Cleveland
treasury|US Treasury|government|us government|US Treasury;U\.S\. Treasury;Treasury Department
jekyll|Jekyll Island meeting (Nov 1910)|event|finance|Jekyll Island
aldrich|Nelson Aldrich|person|us government|Nelson Aldrich;Senator Aldrich
piatt_andrew|A. Piatt Andrew|person|us government|Piatt Andrew
davison|Henry P. Davison|person|finance|Henry P\. Davison;Henry Davison
vanderlip|Frank Vanderlip|person|finance|Frank Vanderlip;Vanderlip
national_city|National City Bank|company|finance|National City Bank
kuhn_loeb|Kuhn, Loeb & Co.|company|finance|Kuhn,? Loeb
aldrich_plan|Aldrich Plan (1911)|document|finance|Aldrich Plan
fed_act|Federal Reserve Act (Dec 1913)|document|finance|Federal Reserve Act
fed|Federal Reserve System|government|finance|Federal Reserve(?! Act)
glass|Carter Glass|person|us government|Carter Glass
owen_r|Robert L. Owen|person|us government|Robert L\. Owen
house_em|Edward M. House|person|us government|Colonel House;Edward M\. House
bernstein|Nahum (William) Bernstein|person|militias|William Bernstein;Nahum Bernstein
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
