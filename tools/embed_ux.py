"""v1.3 reading upgrades for the Israel simulation (index.html). Idempotent: replaces its own block.
Injects tools/ux_block.html (chapter switcher, phone layout, resume, swipe, keyboard shortcuts)
and merges its interface strings into the Spanish and Arabic dictionaries.
Usage: python3 tools/embed_ux.py [index.html]"""
import json, os, re, sys
IDX = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
HERE = os.path.dirname(os.path.abspath(__file__))
block = open(os.path.join(HERE, 'ux_block.html'), encoding='utf-8').read().strip() + '\n'
s = open(IDX, encoding='utf-8').read()

UI = {  # English key: (Spanish, Arabic)
  'Chapters': ('Capítulos', 'الفصول'),
  'chapters': ('capítulos', 'فصلًا'),
  'scenes': ('escenas', 'مشهدًا'),
  'scenes read': ('escenas leídas', 'مشهدًا مقروءًا'),
  'Close': ('Cerrar', 'إغلاق'),
  'Search titles, people, years': ('Busca títulos, personas, años', 'ابحث في العناوين والأشخاص والسنوات'),
  'scene read': ('escena leída', 'مشهد مقروء'),
  'You’re here': ('Estás aquí', 'أنت هنا'),
  'Scenes': ('Escenas', 'المشاهد'),
  'Hide': ('Ocultar', 'إخفاء'),
  'No chapter or scene title matches': ('Ningún capítulo ni escena coincide con', 'لا يوجد فصل أو مشهد يطابق'),
  'Search the full text of every scene': ('Buscar en el texto completo de cada escena', 'ابحث في النص الكامل لكل مشهد'),
  'Pick up where you left off?': ('¿Seguir donde lo dejaste?', 'هل تتابع من حيث توقفت؟'),
  'Chapter': ('Capítulo', 'الفصل'),
  'Continue': ('Continuar', 'متابعة'),
  'Not now': ('Ahora no', 'ليس الآن'),
  'Tip': ('Consejo', 'نصيحة'),
  'Swipe the board left or right to change scenes. Tap the chapter label to jump anywhere.': (
      'Desliza el tablero a la izquierda o a la derecha para cambiar de escena. Toca la etiqueta del capítulo para saltar a cualquier parte.',
      'اسحب اللوحة يمينًا أو يسارًا لتغيير المشهد. انقر على اسم الفصل للانتقال إلى أي مكان.'),
  '📚 Chapters': ('📚 Capítulos', '📚 الفصول'),
  'Told vs. Record': ('Contado vs. registro', 'الرواية مقابل السجل'),
  'Keyboard shortcuts': ('Atajos de teclado', 'اختصارات لوحة المفاتيح'),
  'Next / previous scene': ('Escena siguiente / anterior', 'المشهد التالي / السابق'),
  'Next / previous chapter': ('Capítulo siguiente / anterior', 'الفصل التالي / السابق'),
  'Next / previous event': ('Evento siguiente / anterior', 'الحدث التالي / السابق'),
  'Open chapters': ('Abrir capítulos', 'فتح الفصول'),
  'Search': ('Buscar', 'بحث'),
  'Show this list': ('Mostrar esta lista', 'عرض هذه القائمة'),
  'Close any panel': ('Cerrar cualquier panel', 'إغلاق أي لوحة'),
}

def merge(lang, col):
    global s
    m = re.search(r'(<script type="application/json" id="i18n-' + lang + r'">)(.*?)(</script>)', s, re.S)
    assert m, lang
    d = json.loads(m.group(2))
    ui = d.setdefault('ui', {})
    for k, v in UI.items():
        ui.setdefault(k, v[col])
    payload = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + payload + s[m.end(2):]

merge('es', 0)
merge('ar', 1)
s = re.sub(r'<!--UX-START-->.*?<!--UX-END-->\n?', '', s, flags=re.S)
i = s.find('<!--ELEVEN-START-->')
if i < 0:
    i = s.rfind('</body>')
assert i > 0
s = s[:i] + block + s[i:]
open(IDX, 'w', encoding='utf-8').write(s)
print('ux block embedded ->', IDX, len(block), 'bytes')
