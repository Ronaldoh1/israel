"""Adds scene s00b1 ("The Shield — when the word is used to stop a question") after s00b0 in chapter 1 (EN/ES/AR). Idempotent.
Usage: python3 tools/patch_shield_scene.py [index.html]"""
import json, re, sys
IDX = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(IDX, encoding='utf-8').read()
def get(p):
    m = re.search(p, s, re.S); assert m, p; return m
def put(m, obj, compact=True):
    global s
    t = json.dumps(obj, ensure_ascii=False, separators=(',', ':') if compact else None).replace('</', '<\\/')
    s = s[:m.start(1)] + t + s[m.end(1):]

SID, AFTER = 's00b1', 's00b0'
C = {
 'ihra_text_safeguard': ('https://www.holocaustremembrance.com/resources/working-definitions-charters/working-definition-antisemitism', 'IHRA working definition — full text'),
 'stern_guardian_2019': ('https://www.bard.edu/news/bards-kenneth-stern-i-drafted-the-definition-of-anti-semitism-rightwing-jews-are-weaponizing-it-2019-12-18', "Kenneth Stern: 'I drafted the definition… it is being weaponized' (2019)"),
 'npr_stern_2024': ('https://www.kuow.org/stories/weaponizing-antisemitism-makes-students-less-safe-says-drafter-of-definition', "NPR: drafter says weaponizing it makes students 'less safe'"),
 'politifact_aaa_2024': ('https://www.politifact.com/article/2024/may/10/the-antisemitism-awareness-act-what-to-know/', 'PolitiFact: the Antisemitism Awareness Act, what to know (2024)'),
 'legiscan_s558': ('https://legiscan.com/US/bill/SB558/', 'S.558 (2025) — bill status'),
}

EN = {
 't': 'The Shield — When the Word Is Used to Stop a Question',
 'sub': "The word means hatred of Jews. The fight is over whether criticizing a state counts.",
 'n': "Here is the line that matters. Hatred of Jewish people is antisemitism, and nothing in this simulation says otherwise. A question about what a government does is a question about a government, whether it's Canada, Mexico or Israel. The definition most institutions use says so in its own text. Its lead drafter says it has been turned into a weapon against critics of Israel anyway. This scene documents how that happens, what it costs the person asking, and what is also true on the other side.",
 'tld': "Questioning Israel is antisemitic.",
 'rec': "Antisemitism means hatred of Jews, and that hasn't changed. What changed is where the charge gets aimed. The IHRA definition's own text says criticism of Israel like that leveled at any other country is not antisemitic; its lead drafter, Kenneth Stern, says it has been weaponized against critics of Israel. Since 2019 it has been built into an executive order, state laws, campus enforcement and platform rules, and the ACLU warns that equating criticism of Israel's government with antisemitism chills speech. Real antisemitism is also at a record high. The test is the target: a government's actions, or Jewish people.",
 'ents': [
  {'id':'finetext','ic':'📄','fl':'🌐','nm':"The definition's own fine print",'rl':'Criticism like any other country’s is not antisemitic','ty':'political','x':16,'y':20,'pu':1,
   'dt':"The International Holocaust Remembrance Alliance's working definition, the one most governments and universities cite, contains this sentence in its own text: criticism of Israel similar to that leveled against any other country cannot be regarded as antisemitic. That is the standard the definition sets for itself. You can ask the same questions of Israel that you would ask of Canada, Mexico or any other state. What the definition's attached examples add, and what is disputed, is where criticism of Israel crosses into hostility to Jews (see the 'Semitic ≠ Jewish' scene and the IHRA chapter). [cite:ihra_text_safeguard]"},
  {'id':'stern','ic':'✍️','fl':'🇺🇸','nm':'Kenneth Stern, its lead drafter','rl':"'Never intended' to chill speech",'ty':'academic','x':50,'y':16,'pu':1,
   'dt':"Kenneth Stern was the American Jewish Committee's antisemitism expert and the lead drafter of the working definition. He has testified that it 'was not drafted, and was never intended, as a tool to target or chill speech on a college campus'; it was written to help governments collect data on antisemitism. In a December 2019 Guardian op-ed headlined 'I drafted the definition of antisemitism. Rightwing Jews are weaponizing it,' he called the executive order applying it to campuses an attack on academic freedom that would harm pro-Palestinian advocates and Jewish students alike. In 2024 he told NPR that weaponizing it makes students less safe. [cite:stern_guardian_2019] [cite:npr_stern_2024] [cite:politifact_aaa_2024]"},
  {'id':'law','ic':'⚖️','fl':'🇺🇸','nm':'From guideline to law','rl':'Executive order, 35 states, a House bill','ty':'political','x':84,'y':22,
   'dt':"A December 2019 executive order directed federal agencies, including the Education Department's civil rights office, to consider the definition when enforcing Title VI. By August 2024, 35 states and the District of Columbia had adopted it in some form. On May 1, 2024 the House passed the Antisemitism Awareness Act, which would write it into federal civil rights enforcement, 320 to 91, with members of both parties voting no. The ACLU urged a no vote, saying the bill would likely chill student speech by wrongly equating criticism of the Israeli government with antisemitism. Status as of October 2026: not law; the Senate version stalled in committee in 2025. [cite:politifact_aaa_2024] [cite:legiscan_s558]"},
  {'id':'cost','ic':'💸','fl':'🎓','nm':'What the label costs','rl':'Funding, visas, accounts','ty':'financial','x':18,'y':56,
   'dt':"A label works by raising the price of a question. The documented prices in this simulation: Columbia University lost $400 million in federal funding within four days of a task-force notice in 2025, and about 60 more universities got warning letters (see 'The Funding Threat as a Lever'). Five days after that notice, Mahmoud Khalil, a recent Columbia graduate who had negotiated for the protesters, was detained for deportation (see 'Mahmoud Khalil'). In July 2024 Meta began treating 'Zionist' as a stand-in for Jews in narrowly defined hate-speech cases after an advocacy campaign (see 'The Word Became the Trigger'). Each case has its own record, including real failures at Columbia that federal investigators documented. Together they show why many people choose not to ask."},
  {'id':'chill','ic':'🧊','fl':'🕊️','nm':'The chilling effect','rl':'Why people stop asking','ty':'contested','x':50,'y':52,'pu':1,
   'dt':"Being called antisemitic is a serious charge, because antisemitism is a serious hatred. That seriousness is exactly what gives the label force when it is aimed at a question about a government. The person asking risks their job, school, visa or account, so many stop asking, and the version they learned in school goes unexamined. This is what the ACLU and the definition's own drafter warned about. It is documented as an institutional effect, through rules and penalties; this simulation does not claim to measure what happens inside any individual's mind. [cite:politifact_aaa_2024] [cite:stern_guardian_2019]"},
  {'id':'alsotrue','ic':'⚠️','fl':'🌐','nm':'What is also true','rl':'Real antisemitism, at a record high','ty':'contested','x':84,'y':58,
   'dt':"The charge is sometimes misused, and antisemitism is also real and rising. The ADL counted 9,354 antisemitic incidents in the US in 2024, the most since it began counting in 1979. Federal investigators found Columbia had no reporting system until summer 2024 and left swastika vandalism uninvestigated. Some speech that calls itself anti-Zionist does cross into hatred of Jews, and even the Jerusalem Declaration, written to defend criticism of Israel, lists examples of it. Many of the strongest critics of Israeli policy are Jewish. Misusing the charge and ignoring real antisemitism both do damage, to Jews and to everyone asking honest questions. (See 'Is Anti-Zionism Antisemitism?')"},
  {'id':'test','ic':'🧭','fl':'🕊️','nm':'The test','rl':'Who is the target?','ty':'event','x':50,'y':86,'pu':1,
   'dt':"Two questions sort almost every case. First: is it aimed at Jewish people, or at what a government does? Second, the definition's own standard: would this criticism be fair if it were aimed at any other country? If it's about a government's actions and you'd say the same of Canada or Mexico, it's a political question, and asking it is not hatred. If it's about Jews as a people, holding them responsible for a state, or using old tropes, it's antisemitism, whatever it calls itself. [cite:ihra_text_safeguard]"},
 ],
 'cs': [
  {'f':'finetext','t':'stern','ty':'formation'},
  {'f':'stern','t':'law','ty':'contested'},
  {'f':'law','t':'cost','ty':'causal'},
  {'f':'cost','t':'chill','ty':'causal'},
  {'f':'chill','t':'test','ty':'causal'},
  {'f':'alsotrue','t':'test','ty':'contested'},
  {'f':'finetext','t':'test','ty':'formation'},
 ],
}

ES = {
 't': 'El escudo: cuando la palabra se usa para frenar una pregunta',
 'sub': 'La palabra significa odio a los judíos. La disputa es si criticar a un Estado cuenta.',
 'n': "Esta es la línea que importa. El odio al pueblo judío es antisemitismo, y nada en esta simulación dice lo contrario. Una pregunta sobre lo que hace un gobierno es una pregunta sobre un gobierno, sea Canadá, México o Israel. La definición que usan la mayoría de las instituciones lo dice en su propio texto. Su redactor principal afirma que aun así se ha convertido en un arma contra quienes critican a Israel. Esta escena documenta cómo ocurre, lo que le cuesta a quien pregunta, y lo que también es cierto del otro lado.",
 'tld': 'Cuestionar a Israel es antisemita.',
 'rec': "Antisemitismo significa odio a los judíos, y eso no ha cambiado. Lo que cambió es hacia dónde se apunta la acusación. El propio texto de la definición de la IHRA dice que la crítica a Israel similar a la que se hace a cualquier otro país no es antisemita; su redactor principal, Kenneth Stern, dice que se ha usado como arma contra quienes critican a Israel. Desde 2019 se ha incorporado a una orden ejecutiva, a leyes estatales, a la aplicación de normas en universidades y a reglas de plataformas, y la ACLU advierte que equiparar la crítica al gobierno israelí con antisemitismo inhibe la libertad de expresión. El antisemitismo real también está en máximos históricos. La prueba es el blanco: las acciones de un gobierno, o el pueblo judío.",
 'ents': {
  'finetext': {'nm':'La letra pequeña de la propia definición','rl':'Criticar como a cualquier otro país no es antisemita','dt':"La definición de trabajo de la Alianza Internacional para el Recuerdo del Holocausto, la que citan la mayoría de gobiernos y universidades, contiene esta frase en su propio texto: la crítica a Israel similar a la que se hace a cualquier otro país no puede considerarse antisemita. Ese es el estándar que la definición se fija a sí misma. Puedes hacerle a Israel las mismas preguntas que le harías a Canadá, a México o a cualquier otro Estado. Lo que añaden los ejemplos adjuntos, y lo que está en disputa, es dónde la crítica a Israel se convierte en hostilidad hacia los judíos (ver la escena «Semita ≠ judío» y el capítulo de la IHRA). [cite:ihra_text_safeguard]"},
  'stern': {'nm':'Kenneth Stern, su redactor principal','rl':'«Nunca se pensó» para silenciar','dt':"Kenneth Stern era el experto en antisemitismo del Comité Judío Estadounidense y el redactor principal de la definición de trabajo. Ha declarado que «no se redactó, y nunca se pensó, como herramienta para atacar o silenciar la expresión en un campus universitario»; se escribió para ayudar a los gobiernos a recopilar datos sobre antisemitismo. En una columna de diciembre de 2019 en The Guardian, titulada «Yo redacté la definición de antisemitismo. La derecha judía la está usando como arma», calificó la orden ejecutiva que la aplica a las universidades de ataque a la libertad académica, que perjudicaría tanto a los defensores de Palestina como a estudiantes judíos. En 2024 dijo a NPR que usarla como arma hace a los estudiantes menos seguros. [cite:stern_guardian_2019] [cite:npr_stern_2024] [cite:politifact_aaa_2024]"},
  'law': {'nm':'De guía a ley','rl':'Orden ejecutiva, 35 estados, un proyecto de ley','dt':"Una orden ejecutiva de diciembre de 2019 indicó a las agencias federales, incluida la oficina de derechos civiles del Departamento de Educación, que tuvieran en cuenta la definición al aplicar el Título VI. Para agosto de 2024, 35 estados y el Distrito de Columbia la habían adoptado de alguna forma. El 1 de mayo de 2024 la Cámara de Representantes aprobó por 320 votos contra 91, con votos en contra de ambos partidos, la Ley de Concienciación sobre el Antisemitismo, que la incorporaría a la aplicación federal de los derechos civiles. La ACLU pidió votar en contra: dijo que probablemente inhibiría la expresión estudiantil al equiparar erróneamente la crítica al gobierno israelí con el antisemitismo. Estado a octubre de 2026: no es ley; la versión del Senado quedó estancada en comisión en 2025. [cite:politifact_aaa_2024] [cite:legiscan_s558]"},
  'cost': {'nm':'Lo que cuesta la etiqueta','rl':'Fondos, visados, cuentas','dt':"Una etiqueta funciona subiendo el precio de una pregunta. Los precios documentados en esta simulación: la Universidad de Columbia perdió 400 millones de dólares en fondos federales cuatro días después de un aviso de un grupo de trabajo en 2025, y unas 60 universidades más recibieron cartas de advertencia (ver «La amenaza de los fondos como palanca»). Cinco días después de ese aviso, Mahmoud Khalil, recién graduado de Columbia y negociador de los manifestantes, fue detenido para su deportación (ver «Mahmoud Khalil»). En julio de 2024 Meta empezó a tratar «sionista» como sustituto de «judío» en casos de discurso de odio definidos de forma restringida, tras una campaña de presión (ver «La palabra se convirtió en el detonante»). Cada caso tiene su propio expediente, incluidos fallos reales en Columbia documentados por investigadores federales. Juntos muestran por qué mucha gente elige no preguntar."},
  'chill': {'nm':'El efecto inhibidor','rl':'Por qué la gente deja de preguntar','dt':"Que te llamen antisemita es una acusación grave, porque el antisemitismo es un odio grave. Esa gravedad es justo lo que le da fuerza a la etiqueta cuando se dirige contra una pregunta sobre un gobierno. Quien pregunta arriesga su empleo, su universidad, su visado o su cuenta, así que muchos dejan de preguntar, y la versión que aprendieron en la escuela queda sin examinar. Es lo que advirtieron la ACLU y el propio redactor de la definición. Está documentado como un efecto institucional, mediante reglas y sanciones; esta simulación no pretende medir lo que ocurre dentro de la mente de nadie. [cite:politifact_aaa_2024] [cite:stern_guardian_2019]"},
  'alsotrue': {'nm':'Lo que también es cierto','rl':'Antisemitismo real, en máximos históricos','dt':"La acusación a veces se usa mal, y el antisemitismo también es real y va en aumento. La ADL contó 9.354 incidentes antisemitas en Estados Unidos en 2024, la cifra más alta desde que empezó a contarlos en 1979. Investigadores federales hallaron que Columbia no tuvo un sistema de denuncias hasta el verano de 2024 y dejó sin investigar pintadas de esvásticas. Parte del discurso que se presenta como antisionista sí cruza al odio a los judíos, e incluso la Declaración de Jerusalén, escrita para defender la crítica a Israel, enumera ejemplos. Muchos de los críticos más firmes de la política israelí son judíos. Usar mal la acusación e ignorar el antisemitismo real hacen daño, a los judíos y a todos los que hacen preguntas honestas. (Ver «¿Es antisemita el antisionismo?»)"},
  'test': {'nm':'La prueba','rl':'¿Quién es el blanco?','dt':"Dos preguntas resuelven casi todos los casos. Primera: ¿apunta al pueblo judío o a lo que hace un gobierno? Segunda, el propio estándar de la definición: ¿sería justa esta crítica si se dirigiera a cualquier otro país? Si trata de las acciones de un gobierno y dirías lo mismo de Canadá o de México, es una pregunta política, y hacerla no es odio. Si trata de los judíos como pueblo, los responsabiliza de un Estado o usa viejos estereotipos, es antisemitismo, se llame como se llame. [cite:ihra_text_safeguard]"},
 },
}

AR = {
 't': 'الدرع: حين تُستخدم الكلمة لإيقاف السؤال',
 'sub': 'الكلمة تعني كراهية اليهود. والخلاف هو: هل يُحسب انتقاد دولةٍ منها؟',
 'n': "هذا هو الخط الفاصل. كراهية الشعب اليهودي معاداةٌ للسامية، ولا شيء في هذه المحاكاة يقول غير ذلك. أما السؤال عمّا تفعله حكومة فهو سؤال عن حكومة، سواء كانت كندا أو المكسيك أو إسرائيل. والتعريف الذي تعتمده معظم المؤسسات يقول ذلك في نصّه نفسه. ومع ذلك يقول كاتبه الرئيسي إنه تحوّل إلى سلاح ضد منتقدي إسرائيل. يوثّق هذا المشهد كيف يحدث ذلك، وما يكلّفه للسائل، وما هو صحيح أيضًا في الجهة الأخرى.",
 'tld': 'التشكيك في إسرائيل معاداةٌ للسامية.',
 'rec': "معاداة السامية تعني كراهية اليهود، وهذا لم يتغيّر. ما تغيّر هو الوجهة التي تُصوَّب إليها التهمة. فنصّ تعريف IHRA نفسه يقول إن انتقاد إسرائيل بما يشبه انتقاد أي دولة أخرى ليس معاداةً للسامية؛ ويقول كاتبه الرئيسي كينيث ستيرن إنه استُخدم سلاحًا ضد منتقدي إسرائيل. ومنذ 2019 أُدرج في أمر تنفيذي وقوانين ولايات وإجراءات جامعية وقواعد منصّات، ويحذّر الاتحاد الأمريكي للحريات المدنية (ACLU) من أن مساواة انتقاد الحكومة الإسرائيلية بمعاداة السامية تكبح حرية التعبير. ومعاداة السامية الحقيقية أيضًا في أعلى مستوياتها. المعيار هو المستهدَف: أفعال حكومة، أم الشعب اليهودي.",
 'ents': {
  'finetext': {'nm':'ما ينصّ عليه التعريف نفسه','rl':'انتقادها كأي دولة أخرى ليس معاداةً للسامية','dt':"يتضمّن التعريف العملي للتحالف الدولي لإحياء ذكرى الهولوكوست، وهو الذي تستشهد به معظم الحكومات والجامعات، هذه الجملة في نصّه نفسه: لا يمكن اعتبار انتقاد إسرائيل المماثل لما يوجَّه إلى أي دولة أخرى معاداةً للسامية. هذا هو المعيار الذي يضعه التعريف لنفسه. يمكنك أن تطرح على إسرائيل الأسئلة نفسها التي تطرحها على كندا أو المكسيك أو أي دولة أخرى. أما ما تضيفه الأمثلة الملحقة به، وهو محلّ خلاف، فهو متى يتحوّل انتقاد إسرائيل إلى عداء لليهود (انظر مشهد «سامي ≠ يهودي» وفصل IHRA). [cite:ihra_text_safeguard]"},
  'stern': {'nm':'كينيث ستيرن، كاتبه الرئيسي','rl':'«لم يُقصد قط» لكبح التعبير','dt':"كان كينيث ستيرن خبير معاداة السامية في اللجنة اليهودية الأمريكية والكاتب الرئيسي للتعريف العملي. وقد شهد بأنه «لم يُصَغ، ولم يُقصد قط، أداةً لاستهداف التعبير أو كبحه في الحرم الجامعي»؛ بل كُتب لمساعدة الحكومات على جمع البيانات عن معاداة السامية. وفي مقال رأي في الغارديان في ديسمبر 2019 بعنوان «أنا صغتُ تعريف معاداة السامية. واليهود اليمينيون يحوّلونه إلى سلاح»، وصف الأمر التنفيذي الذي يطبّقه على الجامعات بأنه اعتداء على الحرية الأكاديمية سيضرّ المدافعين عن فلسطين والطلاب اليهود معًا. وفي 2024 قال لإذاعة NPR إن تحويله إلى سلاح يجعل الطلاب أقلّ أمانًا. [cite:stern_guardian_2019] [cite:npr_stern_2024] [cite:politifact_aaa_2024]"},
  'law': {'nm':'من إرشاد إلى قانون','rl':'أمر تنفيذي، 35 ولاية، مشروع قانون','dt':"وجّه أمر تنفيذي صدر في ديسمبر 2019 الوكالات الفدرالية، ومنها مكتب الحقوق المدنية في وزارة التعليم، إلى مراعاة التعريف عند تطبيق الباب السادس من قانون الحقوق المدنية. وبحلول أغسطس 2024 كانت 35 ولاية ومقاطعة كولومبيا قد تبنّته بشكل ما. وفي 1 مايو 2024 أقرّ مجلس النواب «قانون التوعية بمعاداة السامية» الذي يدرجه في تطبيق الحقوق المدنية الفدرالي، بأغلبية 320 مقابل 91، وصوّت ضده أعضاء من الحزبين. ودعا الاتحاد الأمريكي للحريات المدنية إلى التصويت ضده، قائلًا إنه سيكبح على الأرجح تعبير الطلاب بمساواته الخاطئة بين انتقاد الحكومة الإسرائيلية ومعاداة السامية. الوضع حتى أكتوبر 2026: لم يصبح قانونًا؛ وتعثّرت نسخة مجلس الشيوخ في اللجنة عام 2025. [cite:politifact_aaa_2024] [cite:legiscan_s558]"},
  'cost': {'nm':'ثمن التسمية','rl':'تمويل، تأشيرات، حسابات','dt':"تعمل التسمية برفع ثمن السؤال. والأثمان الموثَّقة في هذه المحاكاة: خسرت جامعة كولومبيا 400 مليون دولار من التمويل الفدرالي خلال أربعة أيام من إخطار فريق عمل عام 2025، وتلقّت نحو 60 جامعة أخرى رسائل تحذير (انظر «التهديد بالتمويل أداةً للضغط»). وبعد خمسة أيام من ذلك الإخطار احتُجز محمود خليل، الخرّيج الحديث من كولومبيا الذي تفاوض باسم المحتجّين، تمهيدًا لترحيله (انظر «محمود خليل»). وفي يوليو 2024 بدأت ميتا تعامل كلمة «صهيوني» بديلًا عن «يهودي» في حالات محدّدة بدقّة من خطاب الكراهية بعد حملة ضغط (انظر «الكلمة صارت الزناد»). لكل حالة سجلّها الخاص، بما في ذلك إخفاقات حقيقية في كولومبيا وثّقها محققون فدراليون. ومجتمعةً تُظهر لماذا يختار كثيرون ألّا يسألوا."},
  'chill': {'nm':'أثر الكبح','rl':'لماذا يتوقّف الناس عن السؤال','dt':"أن تُوصَف بمعاداة السامية تهمةٌ خطيرة، لأن معاداة السامية كراهيةٌ خطيرة. وهذه الخطورة بالضبط هي ما يمنح التسمية قوّتها حين تُصوَّب إلى سؤال عن حكومة. فالسائل يخاطر بعمله أو جامعته أو تأشيرته أو حسابه، فيتوقّف كثيرون عن السؤال، وتبقى الرواية التي تعلّموها في المدرسة بلا تمحيص. وهذا ما حذّر منه الاتحاد الأمريكي للحريات المدنية وكاتب التعريف نفسه. وهو موثَّق بوصفه أثرًا مؤسسيًا عبر القواعد والعقوبات؛ ولا تدّعي هذه المحاكاة قياس ما يحدث داخل عقل أي فرد. [cite:politifact_aaa_2024] [cite:stern_guardian_2019]"},
  'alsotrue': {'nm':'ما هو صحيح أيضًا','rl':'معاداة سامية حقيقية في أعلى مستوياتها','dt':"تُساء أحيانًا استخدام التهمة، ومعاداة السامية أيضًا حقيقية ومتصاعدة. فقد أحصت رابطة مكافحة التشهير (ADL) 9,354 حادثة معادية للسامية في الولايات المتحدة عام 2024، وهو الأعلى منذ بدأت الإحصاء عام 1979. ووجد محققون فدراليون أن كولومبيا لم يكن لديها نظام للبلاغات حتى صيف 2024 وتركت رسوم صلبان معقوفة دون تحقيق. وبعض الخطاب الذي يسمّي نفسه معاديًا للصهيونية يتجاوز فعلًا إلى كراهية اليهود، وحتى إعلان القدس، الذي كُتب للدفاع عن انتقاد إسرائيل، يسرد أمثلة على ذلك. وكثير من أشدّ منتقدي السياسة الإسرائيلية يهود. إن إساءة استخدام التهمة وتجاهل معاداة السامية الحقيقية كلاهما يُلحق الضرر، باليهود وبكل من يسأل بصدق. (انظر «هل معاداة الصهيونية معاداةٌ للسامية؟»)"},
  'test': {'nm':'المعيار','rl':'من المستهدَف؟','dt':"سؤالان يحسمان كل حالة تقريبًا. الأول: هل الكلام موجّه إلى الشعب اليهودي، أم إلى ما تفعله حكومة؟ والثاني، معيار التعريف نفسه: هل كان هذا الانتقاد سيُعدّ منصفًا لو وُجّه إلى أي دولة أخرى؟ إن كان عن أفعال حكومة وكنت ستقول الشيء نفسه عن كندا أو المكسيك، فهو سؤال سياسي، وطرحه ليس كراهية. وإن كان عن اليهود بوصفهم شعبًا، أو يحمّلهم مسؤولية دولة، أو يستخدم صورًا نمطية قديمة، فهو معاداة للسامية، أيًّا كان الاسم الذي يطلقه على نفسه. [cite:ihra_text_safeguard]"},
 },
}

m = get(r'<script id="scenedata" type="application/json">(.*?)</script>')
D = json.loads(m.group(1))
if not any(x['id'] == SID for x in D):
    i = next(k for k, x in enumerate(D) if x['id'] == AFTER)
    sc = {'id': SID, 'era': 'BASELINE', 'yr': '2010–2026', 't': EN['t'], 'sub': EN['sub'], 'n': EN['n'], 'ents': EN['ents'], 'cs': EN['cs'], 'tld': EN['tld'], 'rec': EN['rec'], 'ch': 'ch01', 'chn': D[i]['chn']}
    D.insert(i + 1, sc)
ch01 = [x for x in D if x['ch'] == 'ch01']
for k, x in enumerate(ch01): x['chpos'] = k + 1; x['chtotal'] = len(ch01)
put(m, D)

m = get(r'window\.CHAPTERS = (\[.*?\]);\n')
CH = json.loads(m.group(1)); c1 = next(c for c in CH if c['id'] == 'ch01')
if SID not in c1['scenes']: c1['scenes'].insert(c1['scenes'].index(AFTER) + 1, SID)
put(m, CH, compact=False)

m = get(r'<script id="citationdata" type="application/json">(.*?)</script>')
CI = json.loads(m.group(1))
for k, (u, _) in C.items(): CI.setdefault(k, u)
put(m, CI)
m = get(r'window\.CITE_LABELS = (\{.*?\});\n')
CL = json.loads(m.group(1))
for k, (_, l) in C.items(): CL.setdefault(k, l)
put(m, CL, compact=False)

for lang, L in (('es', ES), ('ar', AR)):
    m = get(r'<script type="application/json" id="i18n-' + lang + r'">(.*?)</script>')
    d = json.loads(m.group(1))
    d['scenes'][SID] = {k: L[k] for k in ('t', 'sub', 'n', 'tld', 'rec')}; d['scenes'][SID]['ents'] = L['ents']
    put(m, d)

open(IDX, 'w', encoding='utf-8').write(s)
print('ok: scenes', len(D), '| ch01', len(ch01))
