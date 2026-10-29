set -eo pipefail
cd /home/claude/israel
S=/tmp/claude-0/-home-claude/e022d494-4813-5195-a8e3-0f7e50b32600/scratchpad
python3 tools/embed_book.py $S/index.before.html | tail -1
cp $S/index.before.html index.html
python3 tools/patch_record_fixes.py | tail -1
python3 tools/patch_four_words.py | tail -1
python3 tools/patch_lineages_map.py | tail -1
python3 tools/patch_scorecard22.py | tail -1
python3 tools/dream_dash.py | tail -1
python3 tools/patch_dream_dash.py | tail -1
for t in simplify_ux library_boot returning_visitors scene_controls patch_ui_flags_scheme; do python3 tools/$t.py | tail -1; done
python3 tools/build_dist.py | tail -1
python3 tools/build_israel_web.py | tail -1
