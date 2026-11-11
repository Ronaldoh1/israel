"""Adds scene s00b0 ("'Antisemitism' — named by the haters, not the hated") after s00b in chapter 1,
and corrects the word's history in s00b (English, Spanish, Arabic). Idempotent.
Usage: python3 tools/patch_antisemitism_word.py [index.html]"""
import json, re, sys
IDX = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(IDX, encoding='utf-8').read()

def get(pattern):
    m = re.search(pattern, s, re.S); assert m, pattern; return m
def put(m, obj, compact=True):
    global s
    txt = json.dumps(obj, ensure_ascii=False, separators=(',', ':') if compact else None).replace('</', '<\\/')
    s = s[:m.start(1)] + txt + s[m.end(1):]

SID = 's00b0'
C = {
 'wiki_antisemitism_etym': ('https://en.wikipedia.org/wiki/Antisemitism', 'Antisemitism — etymology and usage'),
 'wiki_renan': ('https://en.wikipedia.org/wiki/Ernest_Renan', 'Ernest Renan'),
 'jvl_marr': ('https://www.jewishvirtuallibrary.org/wilhelm-marr', 'Wilhelm Marr — Jewish Virtual Library'),
 'jvl_pinsker': ('https://jewishvirtuallibrary.org/quot-auto-emancipation-quot-leon-pinsker', 'Pinsker, Auto-Emancipation (1882)'),
 'ihra_spelling_2015': ('https://holocaustremembrance.com/?p=1559', 'IHRA memo on the spelling of antisemitism (2015)'),
 'wjc_nyt_spelling': ('https://www.worldjewishcongress.org/en/news/nytimes-replaces-anti-semitism-with-antisemitism-in-updated-style-guidance', 'New York Times drops the hyphen (2021)'),
}

EN = {
 't': "'Antisemitism' — A Word Named by the Haters, Not the Hated",
 'sub': "1781 to 2015: a language label became a 'race,' then the name of a movement against Jews.",
 'n': "The word everyone argues about has a paper trail. A linguist named a family of languages in 1781. Race science turned it into a 'race' in the 1850s. A Jewish scholar first wrote 'antisemitic' in 1860 to attack that race theory. Then in 1879 a German agitator who was not Jewish made 'antisemitism' the name of his own movement against Jews. The name is a misnomer. Its meaning is not.",
 'tld': "'Anti-Semitism' is a precise term: the Semites are a people, and the word names hatred of them.",
 'rec': "'Semitic' was coined in 1781 for languages, not people. Nineteenth-century race science, led by Ernest Renan, recast it as an inferior 'Semitic race.' The adjective 'antisemitic' first appeared in 1860, when the Jewish scholar Moritz Steinschneider used it against Renan. In 1879 Wilhelm Marr, a Lutheran German journalist, made 'antisemitism' the banner of his League of Antisemites, aimed only at Jews. Jews named the same hatred 'Judeophobia' (Pinsker, 1882). Since 2015 the IHRA drops the hyphen because there is no 'Semitism.' The root is a misnomer; the meaning, set by use, is hatred of Jews.",
 'ents': [
  {'id':'schlozer','ic':'📚','fl':'🇩🇪','nm':'Schlözer, 1781','rl':"'Semitic' names a language family",'ty':'academic','x':16,'y':22,
   'dt':"In 1781 the Göttingen historian August Ludwig von Schlözer coined 'Semitic' (semitisch) for a family of related languages, borrowing the name of Shem, son of Noah, from Genesis 10. Today that family includes Hebrew, Aramaic, Arabic, Amharic, Tigrinya and Maltese. It is a classification of languages. It says nothing about blood, race or religion, and it has never belonged to one people. [cite:wiki_semitic_etymology]"},
  {'id':'renan','ic':'🧪','fl':'🇫🇷','nm':'Ernest Renan, 1855','rl':"Race science turns a language into a 'race'",'ty':'academic','x':50,'y':18,'pu':1,
   'dt':"The French scholar Ernest Renan's comparative history of the Semitic languages (1855) treated their speakers, Hebrews and Arabs alike, as a 'Semitic race' inferior to the 'Aryans.' This was the race science of the era: a label invented for grammar was turned into a ranking of peoples. Historians now call 'Semitic race' a discredited category, which is why the word causes confusion to this day. [cite:wiki_renan] [cite:wiki_antisemitism_etym]"},
  {'id':'steinschneider','ic':'✒️','fl':'🇩🇪','nm':'Moritz Steinschneider, 1860','rl':"The first 'antisemitic' — aimed at Renan",'ty':'academic','x':84,'y':24,
   'dt':"The adjective came first, and it came from a Jewish scholar. In 1860 the bibliographer Moritz Steinschneider wrote of 'antisemitic prejudices' (antisemitische Vorurteile) to rebut Renan's claim that Semitic peoples were inferior. In that first use, the target was the whole invented 'Semitic race.' Within twenty years, Jew-haters in Germany would take the word over and narrow it to one people. [cite:wiki_antisemitism_etym]"},
  {'id':'marr','ic':'📣','fl':'🇩🇪','nm':'Wilhelm Marr, 1879','rl':'A Lutheran Jew-hater names his movement','ty':'event','x':18,'y':58,'pu':1,
   'dt':"Wilhelm Marr (1819–1904) was a German journalist and a Lutheran, not a Jew as is sometimes claimed. In 1879 he published 'The Victory of Judaism over Germandom' and founded the League of Antisemites, the first German organization devoted to the alleged Jewish threat; it called for forcing Jews out of Germany. His 'Antisemitic Pamphlets' of 1881 spread the word. The point of 'antisemitism' was to make old Jew-hatred sound like modern science: if Jews were a foreign 'Semitic race,' no conversion and no centuries in Germany could make them German. The word was coined by the people doing the hating, about the people being hated. His biographer Moshe Zimmermann reports that near the end of his life Marr renounced antisemitism in a text he never published. [cite:wiki_marr_1879] [cite:jvl_marr]"},
  {'id':'pinsker','ic':'🩺','fl':'🇷🇺','nm':'Leon Pinsker, 1882','rl':"Jews called it 'Judeophobia'",'ty':'event','x':50,'y':54,
   'dt':"Jews had their own name for it. In 1882, after pogroms in the Russian Empire, the Odessa physician Leon Pinsker published 'Auto-Emancipation,' which called the hatred 'Judeophobia': an irrational fear of Jews that he described as an inherited disease. The name says plainly who the target is. Pinsker concluded that Jews needed a homeland of their own, which makes the pamphlet one of the founding texts of Zionism. [cite:jvl_pinsker] [cite:wiki_antisemitism_etym]"},
  {'id':'ihra2015','ic':'✂️','fl':'🌐','nm':'IHRA, April 2015','rl':"Drop the hyphen: there is no 'Semitism'",'ty':'academic','x':84,'y':58,
   'dt':"In April 2015 the International Holocaust Remembrance Alliance recommended writing 'antisemitism' without a hyphen. Its reason: the hyphen 'allows for the possibility of something called Semitism,' lending weight to a discredited racial classification. Style guides followed; The New York Times dropped the hyphen in 2021. Even the institutions most invested in the word agree the root is wrong. [cite:ihra_spelling_2015] [cite:wjc_nyt_spelling]"},
  {'id':'today','ic':'⚖️','fl':'🕊️','nm':'What the word means now','rl':'Misnomer in its root; settled in its meaning','ty':'contested','x':50,'y':86,'pu':1,
   'dt':"Two things are true together. The root is a misnomer: 'Semitic' describes languages, Palestinians who speak Arabic are as Semitic as anyone, and many Jews have never spoken a Semitic language at home. And the meaning is settled by use: since the 1880s 'antisemitism' has meant hostility to Jews, and nothing broader. That cuts both ways. 'Arabs are Semites too, so I can't be antisemitic' doesn't hold, because words mean what they are used to mean, not what their parts suggest. Stretching the word to cover political criticism of a state doesn't hold either; that dispute is documented in the scene before this one. The test is the target and the content of what is said, not the label. [cite:wiki_antisemitism_etym] [cite:ihra_spelling_2015]"},
 ],
 'cs': [
  {'f':'schlozer','t':'renan','ty':'formation'},
  {'f':'renan','t':'steinschneider','ty':'contested'},
  {'f':'renan','t':'marr','ty':'causal'},
  {'f':'marr','t':'pinsker','ty':'causal'},
  {'f':'marr','t':'ihra2015','ty':'formation'},
  {'f':'ihra2015','t':'today','ty':'causal'},
  {'f':'steinschneider','t':'today','ty':'formation'},
 ],
}

ES = {
 't': "«Antisemitismo»: una palabra puesta por quienes odiaban, no por los odiados",
 'sub': "De 1781 a 2015: una etiqueta lingüística se volvió «raza» y luego el nombre de un movimiento contra los judíos.",
 'n': "La palabra que todos discuten tiene un rastro documental. Un lingüista nombró una familia de lenguas en 1781. La ciencia racial la convirtió en una «raza» en la década de 1850. Un erudito judío escribió por primera vez «antisemita» en 1860 para atacar esa teoría racial. Y en 1879 un agitador alemán que no era judío convirtió «antisemitismo» en el nombre de su propio movimiento contra los judíos. El nombre es un error. Su significado, no.",
 'tld': "«Antisemitismo» es un término preciso: los semitas son un pueblo, y la palabra nombra el odio hacia ellos.",
 'rec': "«Semítico» se acuñó en 1781 para lenguas, no para personas. La ciencia racial del siglo XIX, con Ernest Renan a la cabeza, lo convirtió en una «raza semita» inferior. El adjetivo «antisemita» apareció en 1860, cuando el erudito judío Moritz Steinschneider lo usó contra Renan. En 1879 Wilhelm Marr, periodista alemán luterano, hizo del «antisemitismo» la bandera de su Liga de Antisemitas, dirigida solo contra los judíos. Los judíos llamaron a ese mismo odio «judeofobia» (Pinsker, 1882). Desde 2015 la IHRA omite el guion porque no existe el «semitismo». La raíz es un error; el significado, fijado por el uso, es el odio a los judíos.",
 'ents': {
  'schlozer': {'nm':'Schlözer, 1781','rl':'«Semítico» nombra una familia de lenguas','dt':"En 1781 el historiador de Gotinga August Ludwig von Schlözer acuñó «semítico» (semitisch) para una familia de lenguas emparentadas, tomando el nombre de Sem, hijo de Noé, del Génesis 10. Hoy esa familia incluye el hebreo, el arameo, el árabe, el amárico, el tigriña y el maltés. Es una clasificación de lenguas. No dice nada de sangre, raza ni religión, y nunca perteneció a un solo pueblo. [cite:wiki_semitic_etymology]"},
  'renan': {'nm':'Ernest Renan, 1855','rl':'La ciencia racial convierte una lengua en «raza»','dt':"La historia comparada de las lenguas semíticas del erudito francés Ernest Renan (1855) trató a sus hablantes, hebreos y árabes por igual, como una «raza semita» inferior a los «arios». Era la ciencia racial de la época: una etiqueta inventada para la gramática se convirtió en una jerarquía de pueblos. Los historiadores consideran hoy «raza semita» una categoría desacreditada, y por eso la palabra sigue causando confusión. [cite:wiki_renan] [cite:wiki_antisemitism_etym]"},
  'steinschneider': {'nm':'Moritz Steinschneider, 1860','rl':'El primer «antisemita», dirigido contra Renan','dt':"El adjetivo llegó primero, y lo escribió un erudito judío. En 1860 el bibliógrafo Moritz Steinschneider habló de «prejuicios antisemitas» (antisemitische Vorurteile) para refutar la tesis de Renan de que los pueblos semitas eran inferiores. En ese primer uso, el blanco era toda la inventada «raza semita». En veinte años, los antisemitas alemanes se apropiarían de la palabra y la reducirían a un solo pueblo. [cite:wiki_antisemitism_etym]"},
  'marr': {'nm':'Wilhelm Marr, 1879','rl':'Un luterano que odiaba a los judíos nombra su movimiento','dt':"Wilhelm Marr (1819–1904) fue un periodista alemán luterano, no judío como a veces se afirma. En 1879 publicó «La victoria del judaísmo sobre el germanismo» y fundó la Liga de Antisemitas, la primera organización alemana dedicada a la supuesta amenaza judía; pedía expulsar a los judíos de Alemania. Sus «Cuadernos antisemitas» de 1881 difundieron la palabra. El propósito de «antisemitismo» era que el viejo odio a los judíos sonara a ciencia moderna: si los judíos eran una «raza semita» extranjera, ninguna conversión ni siglos en Alemania podían hacerlos alemanes. La palabra la acuñaron quienes odiaban, sobre aquellos a quienes odiaban. Su biógrafo Moshe Zimmermann relata que al final de su vida Marr renegó del antisemitismo en un texto que nunca publicó. [cite:wiki_marr_1879] [cite:jvl_marr]"},
  'pinsker': {'nm':'Leon Pinsker, 1882','rl':'Los judíos lo llamaron «judeofobia»','dt':"Los judíos tenían su propio nombre para ello. En 1882, tras los pogromos en el Imperio ruso, el médico de Odesa Leon Pinsker publicó «Autoemancipación», que llamó a ese odio «judeofobia»: un miedo irracional a los judíos que describió como una enfermedad hereditaria. El nombre dice claramente quién es el blanco. Pinsker concluyó que los judíos necesitaban una patria propia, lo que convierte el folleto en uno de los textos fundacionales del sionismo. [cite:jvl_pinsker] [cite:wiki_antisemitism_etym]"},
  'ihra2015': {'nm':'IHRA, abril de 2015','rl':'Sin guion: no existe el «semitismo»','dt':"En abril de 2015 la Alianza Internacional para el Recuerdo del Holocausto recomendó escribir «antisemitismo» sin guion. Su razón: el guion «permite la posibilidad de algo llamado semitismo», lo que da peso a una clasificación racial desacreditada. Los manuales de estilo la siguieron; The New York Times eliminó el guion en 2021. Incluso las instituciones más comprometidas con la palabra admiten que la raíz es errónea. [cite:ihra_spelling_2015] [cite:wjc_nyt_spelling]"},
  'today': {'nm':'Qué significa hoy la palabra','rl':'Un error en su raíz; un significado asentado','dt':"Dos cosas son ciertas a la vez. La raíz es un error: «semítico» describe lenguas, los palestinos que hablan árabe son tan semitas como cualquiera, y muchos judíos nunca han hablado una lengua semítica en casa. Y el significado está fijado por el uso: desde la década de 1880 «antisemitismo» significa hostilidad hacia los judíos, y nada más amplio. Eso corta en ambas direcciones. «Los árabes también son semitas, así que no puedo ser antisemita» no se sostiene, porque las palabras significan lo que el uso les da, no lo que sugieren sus partes. Estirar la palabra para cubrir la crítica política a un Estado tampoco se sostiene; esa disputa se documenta en la escena anterior. La prueba es el blanco y el contenido de lo que se dice, no la etiqueta. [cite:wiki_antisemitism_etym] [cite:ihra_spelling_2015]"},
 },
}

AR = {
 't': "«معاداة السامية»: كلمة صاغها الكارهون لا المكروهون",
 'sub': "من 1781 إلى 2015: تسمية لغوية صارت «عِرقًا»، ثم اسمًا لحركة ضد اليهود.",
 'n': "للكلمة التي يتجادل حولها الجميع أثرٌ موثَّق. سمّى عالِمٌ لغويّ عائلةً من اللغات عام 1781. ثم حوّلها «علم الأعراق» إلى «عِرق» في خمسينيات القرن التاسع عشر. وكتب عالِمٌ يهوديّ كلمة «معادٍ للسامية» لأول مرة عام 1860 ليهاجم تلك النظرية العرقية. ثم في عام 1879 جعل محرّضٌ ألمانيّ لم يكن يهوديًا «معاداة السامية» اسمًا لحركته ضد اليهود. الاسم تسمية خاطئة. أما معناه فليس كذلك.",
 'tld': "«معاداة السامية» مصطلح دقيق: الساميّون شعبٌ، والكلمة تسمّي كراهيتهم.",
 'rec': "صيغت كلمة «سامي» عام 1781 لوصف لغات لا أشخاص. ثم أعاد «علم الأعراق» في القرن التاسع عشر، وفي مقدّمته إرنست رينان، تشكيلها «عِرقًا ساميًا» أدنى منزلة. وظهرت صفة «معادٍ للسامية» أول مرة عام 1860 حين استخدمها العالِم اليهودي موريتس شتاينشنايدر ضد رينان. وفي عام 1879 جعل فيلهلم مار، الصحفي الألماني اللوثري، «معاداة السامية» شعارًا لـ«رابطة معادي السامية» الموجّهة ضد اليهود وحدهم. وسمّى اليهود الكراهية نفسها «رُهاب اليهود» (بينسكر، 1882). ومنذ 2015 تحذف IHRA الشرطة من الكلمة الإنجليزية لأنه لا وجود لشيء اسمه «السامية». الجذر تسمية خاطئة؛ أما المعنى الذي رسّخه الاستعمال فهو كراهية اليهود.",
 'ents': {
  'schlozer': {'nm':'شلوتسر، 1781','rl':'«سامي» اسمٌ لعائلة لغوية','dt':"في عام 1781 صاغ المؤرخ أوغست لودفيغ فون شلوتسر، من مدرسة غوتنغن، كلمة «سامي» (semitisch) لعائلة من اللغات المتقاربة، مستعيرًا اسم سام بن نوح من سفر التكوين (الإصحاح 10). وتضم هذه العائلة اليوم العبرية والآرامية والعربية والأمهرية والتغرينية والمالطية. إنها تصنيفٌ للغات، لا تقول شيئًا عن الدم أو العِرق أو الدين، ولم تكن يومًا ملكًا لشعب واحد. [cite:wiki_semitic_etymology]"},
  'renan': {'nm':'إرنست رينان، 1855','rl':'«علم الأعراق» يحوّل لغةً إلى «عِرق»','dt':"عامل كتاب العالِم الفرنسي إرنست رينان في التاريخ المقارن للغات السامية (1855) المتحدّثين بها، العبرانيين والعرب على السواء، بوصفهم «عِرقًا ساميًا» أدنى من «الآريين». كان ذلك «علم الأعراق» في ذلك العصر: تسميةٌ وُضعت للنحو تحوّلت إلى ترتيبٍ للشعوب. ويعدّ المؤرخون اليوم «العِرق السامي» فئةً فاقدة للمصداقية، ولهذا ما زالت الكلمة تثير اللَّبس. [cite:wiki_renan] [cite:wiki_antisemitism_etym]"},
  'steinschneider': {'nm':'موريتس شتاينشنايدر، 1860','rl':'أول «معادٍ للسامية»: موجّهة ضد رينان','dt':"جاءت الصفة أولًا، وجاءت من عالِم يهودي. ففي عام 1860 كتب الببليوغرافي موريتس شتاينشنايدر عن «أحكامٍ مسبقة معادية للسامية» (antisemitische Vorurteile) ليردّ على زعم رينان بأن الشعوب السامية أدنى منزلة. في ذلك الاستعمال الأول كان المستهدَف «العِرق السامي» المختلَق كله. وخلال عشرين عامًا استولى كارهو اليهود في ألمانيا على الكلمة وضيّقوها لتشمل شعبًا واحدًا. [cite:wiki_antisemitism_etym]"},
  'marr': {'nm':'فيلهلم مار، 1879','rl':'كارهٌ لوثريّ لليهود يسمّي حركته','dt':"كان فيلهلم مار (1819–1904) صحفيًا ألمانيًا لوثريًا، ولم يكن يهوديًا كما يُزعم أحيانًا. في عام 1879 نشر «انتصار اليهودية على الجرمانية» وأسّس «رابطة معادي السامية»، أول منظمة ألمانية مكرّسة لما سمّته الخطر اليهودي؛ ودعت إلى إخراج اليهود من ألمانيا قسرًا. ونشرت «كرّاساته المعادية للسامية» عام 1881 الكلمة على نطاق واسع. كان الهدف من «معاداة السامية» أن تبدو كراهية اليهود القديمة علمًا حديثًا: فإذا كان اليهود «عِرقًا ساميًا» أجنبيًا، فلا التنصّر ولا قرون في ألمانيا تجعلهم ألمانًا. صاغ الكلمةَ الكارهون أنفسهم، عن الذين يكرهونهم. ويروي كاتب سيرته موشيه تسيمرمان أن مار تبرّأ من معاداة السامية قرب نهاية حياته في نصٍّ لم ينشره قط. [cite:wiki_marr_1879] [cite:jvl_marr]"},
  'pinsker': {'nm':'ليون بينسكر، 1882','rl':'سمّاها اليهود «رُهاب اليهود»','dt':"كان لليهود اسمهم الخاص لها. ففي عام 1882، بعد مذابح في الإمبراطورية الروسية، نشر الطبيب ليون بينسكر من أوديسا كتيّب «التحرّر الذاتي» الذي سمّى تلك الكراهية «رُهاب اليهود»: خوفًا غير عقلاني من اليهود وصفه بأنه مرض موروث. يقول الاسم بوضوح من هو المستهدَف. وخلص بينسكر إلى أن اليهود يحتاجون وطنًا خاصًا بهم، ما يجعل الكتيّب من النصوص المؤسِّسة للصهيونية. [cite:jvl_pinsker] [cite:wiki_antisemitism_etym]"},
  'ihra2015': {'nm':'IHRA، أبريل 2015','rl':'احذفوا الشرطة: لا وجود لـ«السامية»','dt':"في أبريل 2015 أوصى التحالف الدولي لإحياء ذكرى الهولوكوست بكتابة الكلمة الإنجليزية antisemitism من دون شرطة. وسببه أن الشرطة «تفتح الباب لاحتمال وجود شيء اسمه السامية»، فتمنح وزنًا لتصنيف عرقي فاقد للمصداقية. وتبعته أدلة الأسلوب؛ وحذفت نيويورك تايمز الشرطة عام 2021. حتى أكثر المؤسسات تمسّكًا بالكلمة تقرّ بأن جذرها خاطئ. [cite:ihra_spelling_2015] [cite:wjc_nyt_spelling]"},
  'today': {'nm':'ماذا تعني الكلمة اليوم','rl':'جذرٌ خاطئ، ومعنى مستقرّ','dt':"أمران صحيحان معًا. الجذر تسمية خاطئة: «سامي» يصف لغات، والفلسطينيون الناطقون بالعربية ساميّون كأي أحد، وكثير من اليهود لم يتكلّموا لغةً سامية في بيوتهم قط. والمعنى رسّخه الاستعمال: منذ ثمانينيات القرن التاسع عشر تعني «معاداة السامية» العداء لليهود، ولا شيء أوسع. وهذا يسري في الاتجاهين. فقول «العرب ساميّون أيضًا، لذا لا يمكن أن أكون معاديًا للسامية» لا يصمد، لأن الكلمات تعني ما يستعملها الناس له، لا ما توحي به أجزاؤها. ولا يصمد كذلك مدّ الكلمة لتشمل النقد السياسي لدولة؛ وهذا الخلاف موثَّق في المشهد السابق. المعيار هو المستهدَف ومضمون ما يقال، لا التسمية. [cite:wiki_antisemitism_etym] [cite:ihra_spelling_2015]"},
 },
}

# ---------- scene data ----------
m = get(r'<script id="scenedata" type="application/json">(.*?)</script>')
D = json.loads(m.group(1))
if not any(x['id'] == SID for x in D):
    i = next(k for k, x in enumerate(D) if x['id'] == 's00b')
    sc = {'id': SID, 'era': 'BASELINE', 'yr': '1781–2015'}
    sc.update({k: EN[k] for k in ('t', 'sub', 'n')})
    sc['ents'] = EN['ents']; sc['cs'] = EN['cs']; sc['tld'] = EN['tld']; sc['rec'] = EN['rec']
    sc.update({'ch': 'ch01', 'chn': D[i]['chn']})
    D.insert(i + 1, sc)
# s00b corrections (English)
b = next(x for x in D if x['id'] == 's00b')
b['n'] = "The word Semitic comes from Shem, son of Noah. It describes a family of languages and the peoples who speak them. It does not mean 'Jewish.' The conflation came out of nineteenth-century European race science, and it is load-bearing for the rest of the story."
for e in b['ents']:
    if e['id'] == 'marr':
        e['rl'] = "The word 'antisemitism' made a movement"
        e['dt'] = ("Wilhelm Marr — German journalist and agitator, a Lutheran, not Jewish — published 'Der Sieg des Judenthums über das Germanenthum' in 1879 and founded the Antisemiten-Liga (League of Antisemites) that same year. "
                   "He made 'antisemitismus' the name of his movement: a euphemism for Judenhass (Jew-hatred), meant to sound scientific and modern rather than crude and religious. "
                   "The adjective was older: in 1860 the Jewish scholar Moritz Steinschneider had written of 'antisemitic prejudices' to attack Ernest Renan's claim that Semitic peoples were inferior. "
                   "From Marr on, antisemitism meant hatred of Jewish people, and that is still what it means. The full history of the word is in the next scene. [cite:wiki_marr_1879] [cite:wiki_antisemitism_etym]")
# renumber chapter positions
ch01 = [x for x in D if x['ch'] == 'ch01']
for k, x in enumerate(ch01): x['chpos'] = k + 1; x['chtotal'] = len(ch01)
put(m, D)

# ---------- chapters ----------
m = get(r'window\.CHAPTERS = (\[.*?\]);\n')
CH = json.loads(m.group(1))
c1 = next(c for c in CH if c['id'] == 'ch01')
if SID not in c1['scenes']:
    c1['scenes'].insert(c1['scenes'].index('s00b') + 1, SID)
put(m, CH, compact=False)

# ---------- citations + labels ----------
m = get(r'<script id="citationdata" type="application/json">(.*?)</script>')
CI = json.loads(m.group(1))
for k, (u, _) in C.items(): CI.setdefault(k, u)
put(m, CI)
m = get(r'window\.CITE_LABELS = (\{.*?\});\n')
CL = json.loads(m.group(1))
for k, (_, l) in C.items(): CL.setdefault(k, l)
CL['wiki_marr_1879'] = "Wilhelm Marr — made 'antisemitism' a movement (1879)"
put(m, CL, compact=False)

# ---------- expanded / deep dive fixes ----------
m = get(r'<script id="expanded-en" type="application/json">(.*?)</script>')
EX = json.loads(m.group(1))
sh = EX.get('s00b', {}).get('shem')
if sh: sh['dt'] = sh['dt'].replace('[cite:wiki_marr_1879]', '[cite:wiki_semitic_etymology]')
mr = EX.get('s00b', {}).get('marr')
if mr and 'Lutheran' not in mr['dt']:
    mr['dt'] = mr['dt'].replace('Wilhelm Marr — German journalist, agitator —', 'Wilhelm Marr — German journalist and agitator, a Lutheran, not Jewish —', 1)
    mr['dt'] += " The adjective was older: in 1860 the Jewish scholar Moritz Steinschneider wrote of 'antisemitic prejudices' to attack Ernest Renan's claim that Semitic peoples were inferior; Marr's movement took the word over and narrowed it to Jews. [cite:wiki_antisemitism_etym]"
put(m, EX)
m = get(r'<script id="deepdive-en" type="application/json">(.*?)</script>')
DD = json.loads(m.group(1))
dm = DD.get('s00b', {}).get('marr')
if dm:
    dm['subtitle'] = "The Lutheran journalist who made 'antisemitism' the name of his movement in 1879 — not to describe hatred of Semitic peoples broadly, but as a euphemism for one specific, older hatred."
    dm['connections'] = [c for c in dm.get('connections', []) if c.get('scene') != SID] + [{'scene': SID, 'ent': 'marr', 'label': "The word's full history, 1781–2015"}]
put(m, DD)

# ---------- translations ----------
def tr(lang, L, s00b_n, marr_rl, marr_add):
    global s
    m = get(r'<script type="application/json" id="i18n-' + lang + r'">(.*?)</script>')
    d = json.loads(m.group(1))
    d['scenes'][SID] = {k: L[k] for k in ('t', 'sub', 'n', 'tld', 'rec')}
    d['scenes'][SID]['ents'] = L['ents']
    sb = d['scenes'].get('s00b')
    if sb:
        sb['n'] = s00b_n
        me = sb.get('ents', {}).get('marr')
        if me:
            me['rl'] = marr_rl
            if marr_add not in me.get('dt', ''): me['dt'] = me.get('dt', '') + ' ' + marr_add
    put(m, d)

tr('es', ES,
   "La palabra semita viene de Sem, hijo de Noé. Describe una familia de lenguas y a los pueblos que las hablan. No significa \"judío\". La confusión nació de la ciencia racial europea del siglo XIX, y sostiene buena parte del resto de la historia.",
   "La palabra \"antisemitismo\" se vuelve un movimiento",
   "Marr era luterano, no judío. El adjetivo era anterior: en 1860 el erudito judío Moritz Steinschneider habló de «prejuicios antisemitas» para atacar la tesis de Ernest Renan de que los pueblos semitas eran inferiores. La historia completa de la palabra está en la escena siguiente. [cite:wiki_antisemitism_etym]")
tr('ar', AR,
   "تأتي كلمة «سامي» من سام بن نوح. وهي تصف عائلة من اللغات والشعوب الناطقة بها، ولا تعني «يهودي». نشأ هذا الخلط من «علم الأعراق» الأوروبي في القرن التاسع عشر، وعليه يقوم كثير من بقية القصة.",
   "كلمة «معاداة السامية» تصبح حركة",
   "كان مار لوثريًا ولم يكن يهوديًا. والصفة أقدم منه: ففي عام 1860 كتب العالِم اليهودي موريتس شتاينشنايدر عن «أحكام مسبقة معادية للسامية» ليردّ على زعم إرنست رينان بأن الشعوب السامية أدنى منزلة. والتاريخ الكامل للكلمة في المشهد التالي. [cite:wiki_antisemitism_etym]")

open(IDX, 'w', encoding='utf-8').write(s)
print('ok: scenes', len(D), '| ch01', len(ch01))
