#!/usr/bin/env python3
"""Build the hosted version of Sophia: dist/web/index.html plus one small file per module.

dist/sophia.html (tools/build_sophia_dist.py) is one 11 MB file with every module inside it. Large
single uploads stall on Cloudflare, and every visitor downloads all 163 modules up front. This build
moves each module out into dist/web/m/<id>.z (its zlib bytes) and fetches it only when someone
opens that module, so the page itself is small and each upload piece is small.

The single-file dist/sophia.html stays the version for opening locally (fetch does not work from
file://). Run after tools/build_sophia_dist.py.
Usage: python3 tools/build_sophia_web.py"""
import base64, os, re, shutil, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'dist', 'sophia.html')
OUT = os.path.join(ROOT, 'dist', 'web')
s = open(SRC, encoding='utf-8').read()

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'm'))

# 1. modules (and the shared engine blocks) out to their own files
pat = re.compile(r'<script type="text/plain" id="([A-Za-z0-9_]+(?:_sim_b64)|ots_shared_blocks)" data-z="1">(.*?)</script>\n?', re.S)
n = total = 0
def out(m):
    global n, total
    raw = base64.b64decode(m.group(2))
    zlib.decompress(raw)                                   # must be a valid zlib stream
    open(os.path.join(OUT, 'm', m.group(1) + '.z'), 'wb').write(raw)
    n += 1; total += len(raw)
    return ''
s = pat.sub(out, s)
assert n > 100, 'expected the modules in dist/sophia.html; run tools/build_sophia_dist.py first'

# 2. the loader fetches a module file when it is opened
OLD = s[s.index('  function loadSimInto(frame, id){'):s.index('  /* The Israel simulation is hosted on its own')]
NEW = '''  /* Hosted build (tools/build_sophia_web.py): each module is its own file, m/<id>.z, fetched when opened. */
  var __zcache = {};
  function fetchZ(id){
    if(!__zcache[id]) __zcache[id] = fetch('m/' + id + '.z', {cache: 'force-cache'}).then(function(r){
      if(!r.ok) throw new Error('HTTP ' + r.status); return r.arrayBuffer();
    }).then(function(b){ return fflate.unzlibSync(new Uint8Array(b)); });
    __zcache[id].catch(function(){ delete __zcache[id]; });   /* let a later try fetch again */
    return __zcache[id];
  }
  function fetchModule(id){
    return fetchZ(id).then(function(raw){
      var html = new TextDecoder('utf-8').decode(raw);
      if(html.indexOf('<!--OTSB:') < 0) return raw;
      return fetchZ('ots_shared_blocks').then(function(sb){
        var shared = window.__otsShared || (window.__otsShared = JSON.parse(new TextDecoder('utf-8').decode(sb)));
        return new TextEncoder().encode(html.replace(/<!--OTSB:(\\d+)-->/g, function(m, k){ return shared[+k]; }));
      });
    });
  }
  var __loadSeq = 0;
  var MSG = function(t){ return '<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><body style="margin:0;height:100vh;display:flex;align-items:center;justify-content:center;background:#0B1530;color:#C8D3EA;font:16px system-ui,sans-serif;text-align:center;padding:24px">' + t + '</body>'; };
  function loadSimInto(frame, id){
    var seq = ++__loadSeq;
    frame.removeAttribute('src'); frame.srcdoc = MSG('Loading\\u2026');
    fetchModule(id).then(function(bytes){
      if(seq !== __loadSeq) return;                      /* another module was opened meanwhile */
      if(!OPAQUE_ORIGIN){
        try {
          var url = URL.createObjectURL(new Blob([bytes], {type:'text/html'}));
          frame.removeAttribute('srcdoc'); frame.src = url; currentUrl = url; return;
        } catch(e){ /* fall through to srcdoc */ }
      }
      frame.removeAttribute('src'); frame.srcdoc = new TextDecoder('utf-8').decode(bytes);
    }).catch(function(){
      if(seq === __loadSeq) frame.srcdoc = MSG('This module could not load. Check your connection and open it again.');
    });
    return null;
  }

'''
s = s.replace(OLD, NEW)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(s)
files = len(os.listdir(os.path.join(OUT, 'm')))
big = max(os.path.getsize(os.path.join(OUT, 'm', f)) for f in os.listdir(os.path.join(OUT, 'm')))
print('dist/web/index.html: %.2f MB; %d module files in dist/web/m (%.2f MB total, largest %.2f MB)'
      % (os.path.getsize(os.path.join(OUT, 'index.html')) / 1e6, files, total / 1e6, big / 1e6))
