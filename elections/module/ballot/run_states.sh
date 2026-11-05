#!/bin/bash
# Vote America First: collect everything the scorecards need, one state at a time.
#
#   ./run_states.sh GA              one state
#   ./run_states.sh GA NC MI        several, one after another
#   ./run_states.sh next 5          the next 5 states not yet uploaded (closest races first)
#   ./run_states.sh ALL             every state not yet uploaded
#   ./run_states.sh status          what's done and what's left
#   add --redo to run states that were already uploaded again
#
# For each state: court records + Senate disclosures, then the research pack, then a check of every
# candidate against the scoring rubric (re-running once to fill anything that failed), then
# uploads/state-GA.zip goes to GitHub (release "states") and progress.csv records it.
# Safe to stop (Ctrl-C) and run again: finished work is kept and skipped.

cd "$(dirname "$0")" || exit 1
ORDER="GA MI NC ME NH TX OH IA AK AZ NE MN NV PA WI VA NM CO FL NY CA NJ IL KS MO MT SC KY LA MS AL AR CT DE HI ID IN MA MD ND OK OR RI SD TN UT VT WA WV WY"
REPO="Ronaldoh1/2026electiondata"; RELEASE="states"
export OTS_RECORDS_DIR="$PWD/data/ballot-records" OTS_RESEARCH_DIR="$PWD/data/research-pack"

[ $# -eq 0 ] && { sed -n '4,11p' "$0" | sed 's/^# \{0,1\}//'; exit 1; }
[ "$1" = "status" ] && { python3 scripts/check_state.py --status; exit 0; }

REDO=0; ARGS=()
for x in "$@"; do [ "$x" = "--redo" ] && REDO=1 || ARGS+=("$x"); done
uploaded() { [ -f progress.csv ] && awk -F, -v s="$1" '$1==s && $7!="" {f=1} END {exit !f}' progress.csv; }
if [ "${ARGS[0]}" = "ALL" ] || [ "${ARGS[0]}" = "next" ]; then
  N=${ARGS[1]:-99}; STATES=""
  for s in $ORDER; do uploaded "$s" && [ $REDO = 0 ] && continue; STATES="$STATES $s"; done
  STATES=$(echo $STATES | cut -d' ' -f1-"$N")
else
  STATES=$(echo "${ARGS[@]}" | tr '[:lower:]' '[:upper:]')
fi
[ -z "$STATES" ] && { echo "Nothing to do: every state is uploaded. (Use --redo to run one again.)"; exit 0; }

# keys: from the environment, or keys.txt in this folder (keys.txt is never uploaded)
[ -f keys.txt ] && source keys.txt
[ -z "$COURTLISTENER_TOKEN" ] && read -r -p "CourtListener token: " COURTLISTENER_TOKEN
[ -z "$FEC_API_KEY" ] && read -r -p "FEC / api.data.gov key: " FEC_API_KEY
printf 'COURTLISTENER_TOKEN=%s\nFEC_API_KEY=%s\n' "$COURTLISTENER_TOKEN" "$FEC_API_KEY" > keys.txt; chmod 600 keys.txt
export COURTLISTENER_TOKEN FEC_API_KEY

mkdir -p uploads data
UPLOAD=1
command -v gh >/dev/null || { echo "gh is not installed; zips are made but not uploaded."; UPLOAD=0; }
if [ $UPLOAD = 1 ] && ! gh release view "$RELEASE" -R "$REPO" >/dev/null 2>&1; then
  gh release create "$RELEASE" -R "$REPO" -t "State packs" -n "Courts, Senate disclosures and research pack, one zip per state" || UPLOAD=0
fi

collect() {   # $1 = state
  ( cd scripts && caffeinate -i python3 ots_ballot_records.py --state "$1" ) || return 1
  ( cd scripts && caffeinate -i python3 ots_research_pack.py --state "$1" ) || return 1
}

echo "States to run: $STATES"
for ST in $STATES; do
  if uploaded "$ST" && [ $REDO = 0 ]; then echo "$ST: already uploaded (use --redo to run it again)"; continue; fi
  echo; echo "================ $ST ================"
  collect "$ST" || { echo "$ST: stopped before finishing. Run ./run_states.sh $ST again to continue."; exit 1; }
  python3 scripts/check_state.py "$ST"
  if [ $? = 3 ]; then
    echo "$ST: filling what failed (one more pass)..."
    collect "$ST" || { echo "$ST: stopped before finishing. Run ./run_states.sh $ST again to continue."; exit 1; }
    python3 scripts/check_state.py "$ST" || echo "$ST: some downloads are still missing (listed above). Uploading what's there; run ./run_states.sh $ST --redo later to fill them."
  fi
  rm -f "uploads/state-$ST.zip"
  ( cd data && zip -qr "../uploads/state-$ST.zip" "ballot-records/$ST" "research-pack/$ST" )
  echo "$ST: packed uploads/state-$ST.zip ($(du -h "uploads/state-$ST.zip" | cut -f1))"
  if [ $UPLOAD = 1 ] && gh release upload "$RELEASE" "uploads/state-$ST.zip" -R "$REPO" --clobber; then
    python3 scripts/check_state.py "$ST" --uploaded >/dev/null; echo "$ST: uploaded"
  else
    echo "$ST: not uploaded yet. Run:  gh release upload $RELEASE uploads/state-$ST.zip -R $REPO --clobber"
  fi
done
echo; python3 scripts/check_state.py --status
