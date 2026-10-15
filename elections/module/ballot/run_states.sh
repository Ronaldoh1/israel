#!/bin/bash
# OTS 2026 Elections: collect everything for one or more states, zip each state, and upload it.
#
#   cd ~/Desktop/OTS-2026-Data
#   ./run_states.sh GA                 one state
#   ./run_states.sh GA NC MI ME        several, one after the other
#   ./run_states.sh ALL                every state, in the order below (closest races first)
#
# For each state it runs:
#   2-Ballot-records/ots_ballot_records.py   court records + Senate financial disclosures
#   4-Research-pack/ots_research_pack.py     Wikipedia, photos, Ballotpedia, campaign sites, votes, bills, committees, ethics
# then makes uploads/state-GA.zip and uploads it to the "states" release on GitHub.
# Safe to stop (Ctrl-C) and run again: finished work is kept and skipped.

cd "$(dirname "$0")" || exit 1
ORDER="GA MI NC ME NH TX OH IA AK AZ NE MN NV PA WI VA NM CO FL NY CA NJ IL KS MO MT SC KY LA MS AL AR CT DE HI ID IN MA MD ND OK OR RI SD TN UT VT WA WV WY"
REPO="Ronaldoh1/2026electiondata"
RELEASE="states"

[ $# -eq 0 ] && { echo "Usage: ./run_states.sh GA [NC MI ...]   or   ./run_states.sh ALL"; exit 1; }
STATES="$*"; [ "$1" = "ALL" ] && STATES="$ORDER"

# keys: read from the environment, or from keys.txt next to this script (never upload keys.txt)
[ -f keys.txt ] && source keys.txt
if [ -z "$COURTLISTENER_TOKEN" ]; then read -r -p "CourtListener token: " COURTLISTENER_TOKEN; fi
if [ -z "$FEC_API_KEY" ]; then read -r -p "FEC / api.data.gov key: " FEC_API_KEY; fi
printf 'COURTLISTENER_TOKEN=%s\nFEC_API_KEY=%s\n' "$COURTLISTENER_TOKEN" "$FEC_API_KEY" > keys.txt
chmod 600 keys.txt
export COURTLISTENER_TOKEN FEC_API_KEY

for f in 4-Research-pack/ballot_2026.csv; do [ -f "$f" ] || cp 2-Ballot-records/ballot_2026.csv "$f"; done
mkdir -p uploads
UPLOAD=1
command -v gh >/dev/null || { echo "gh is not installed; zips will be made but not uploaded."; UPLOAD=0; }
if [ $UPLOAD = 1 ] && ! gh release view "$RELEASE" -R "$REPO" >/dev/null 2>&1; then
  gh release create "$RELEASE" -R "$REPO" -t "State packs" -n "Courts, Senate disclosures and research pack, one zip per state" || UPLOAD=0
fi

for ST in $STATES; do
  ST=$(echo "$ST" | tr '[:lower:]' '[:upper:]')
  echo; echo "================ $ST ================"
  ( cd 2-Ballot-records && caffeinate -i python3 ots_ballot_records.py --state "$ST" ) || { echo "$ST: stopped. Run ./run_states.sh $ST again to continue."; exit 1; }
  ( cd 4-Research-pack && caffeinate -i python3 ots_research_pack.py --state "$ST" ) || { echo "$ST: stopped. Run ./run_states.sh $ST again to continue."; exit 1; }
  rm -f "uploads/state-$ST.zip"
  zip -qr "uploads/state-$ST.zip" "2-Ballot-records/ballot-records/$ST" "4-Research-pack/research-pack/$ST" 2>/dev/null
  echo "$ST: packed uploads/state-$ST.zip ($(du -h "uploads/state-$ST.zip" | cut -f1))"
  if [ $UPLOAD = 1 ]; then
    gh release upload "$RELEASE" "uploads/state-$ST.zip" -R "$REPO" --clobber && echo "$ST: uploaded" \
      || echo "$ST: upload failed; run later:  gh release upload $RELEASE uploads/state-$ST.zip -R $REPO --clobber"
  fi
done
echo; echo "Done: $STATES"
