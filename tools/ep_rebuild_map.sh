#!/bin/sh
# Rebuild the Epstein map data and write it into the live page.
# build_explorer.py keeps the live page's interface code and replaces only its DATA and the model and tests scripts
# (ep_viab_ui.js, ep_tests_ui.js); the link fixes of 27 Nov 2026 are reapplied after build_data.py.
set -e
cd "$(dirname "$0")/.."
( cd book/plan/epstein_map && python3 build_data.py )
python3 tools/patch_ep_links_nov27.py
( cd book/plan/epstein_map && python3 ep_viability.py >/dev/null && python3 build_explorer.py )
python3 tools/build_map_layouts.py epstein-network.html   # 27 Nov 2026: store the opening layout so phones skip the physics
