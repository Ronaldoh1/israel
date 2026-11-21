#!/bin/bash
# Talking-Point Radar: collect public posts from every platform at once, then build the report.
#
#   cd ~/Desktop/TalkingPointRadar
#   ./run.sh            check keys, then collect in the background (you can close Terminal) and build the report
#   ./run.sh status     what each collector is doing
#   ./run.sh stop       stop everything (collected posts are kept)
#   ./run.sh report     rebuild the report from what has been collected so far, and open it
#
# Safe to run again any time: only new posts are added. Run it weekly to see what is rising.

cd "$(dirname "$0")" || exit 1
mkdir -p logs run
JOBS="youtube reddit bluesky telegram gdelt inbox"
alive() { [ -f "run/$1.pid" ] && kill -0 "$(cat run/$1.pid)" 2>/dev/null; }

case "$1" in
  status)
    for J in $JOBS; do
      if alive "$J"; then S="running"; elif [ -f "run/$J.done" ]; then S="finished"; elif [ -f "run/$J.skip" ]; then S="skipped ($(cat run/$J.skip))"; elif [ -f "run/$J.fail" ]; then S="FAILED: $(tail -1 run/$J.fail)"; else S="not started"; fi
      N=$( [ -f data/posts/$J.jsonl ] && wc -l < data/posts/$J.jsonl | tr -d ' ' || echo 0); [ "$J" = gdelt ] && N=$( [ -f data/posts/news.jsonl ] && wc -l < data/posts/news.jsonl | tr -d ' ' || echo 0)
      printf "%-9s %-40s %s posts\n" "$J" "$S" "$N"
    done; exit 0;;
  stop)
    for J in $JOBS main; do alive "$J" && kill "$(cat run/$J.pid)" 2>/dev/null && echo "stopped $J"; done; pkill -f "radar.py collect" 2>/dev/null; exit 0;;
  report)
    python3 radar.py analyze && open output/report.html 2>/dev/null; exit 0;;
  __run)
    echo $$ > run/main.pid; [ -f keys.txt ] && . ./keys.txt
    rm -f run/*.done run/*.fail run/*.skip
    lane() {   # run one collector with up to 4 tries, waiting 5, 15, 30 minutes between them
      J=$1; (
        for W in 0 300 900 1800; do
          sleep $W; python3 radar.py collect $J >> logs/$J.log 2>&1; RC=$?
          [ $RC -eq 0 ] && { touch run/$J.done; exit 0; }
          [ $RC -eq 3 ] && { echo "daily limit reached, run again tomorrow" > run/$J.skip; exit 0; }
          tail -2 logs/$J.log > run/$J.fail
          grep -q "no YOUTUBE_API_KEY\|no REDDIT_CLIENT\|needs signing in" logs/$J.log && { echo "no key" > run/$J.skip; rm -f run/$J.fail; exit 0; }
        done ) &
      echo $! > run/$J.pid
    }
    [ -n "$YOUTUBE_API_KEY" ] && lane youtube || echo "no key" > run/youtube.skip
    [ -n "$REDDIT_CLIENT_ID" ] && lane reddit || echo "no key" > run/reddit.skip
    lane bluesky; lane telegram; lane gdelt; lane inbox
    wait
    python3 radar.py analyze >> logs/report.log 2>&1
    echo "Finished $(date). Report: output/report.html"; rm -f run/main.pid; exit 0;;
esac

# ---- default: keys, checks, then start in the background
if alive main; then echo "Already running. ./run.sh status to see progress."; exit 0; fi
command -v python3 >/dev/null || { echo "Python 3 is needed: run  xcode-select --install  then try again."; exit 1; }
python3 - <<'PY' 2>/dev/null || {
import urllib.request, urllib.error
try: urllib.request.urlopen('https://www.googleapis.com/', timeout=20)
except urllib.error.HTTPError: pass
PY
  echo "Python can't make secure connections. Open Finder > Applications > Python 3.x and double-click 'Install Certificates.command', then run this again."; exit 1; }
[ -f keys.txt ] && . ./keys.txt
ask() { V=${!1}; if [ -z "$V" ]; then printf "%s (press Enter to skip): " "$2"; read -r V; fi; printf -v "$1" '%s' "$V"; }
if [ ! -f keys.txt ]; then
  echo "Keys are optional; each one adds a platform. Details in START-HERE.txt."
  ask YOUTUBE_API_KEY "YouTube API key"
  ask REDDIT_CLIENT_ID "Reddit app client ID"; [ -n "$REDDIT_CLIENT_ID" ] && ask REDDIT_CLIENT_SECRET "Reddit app secret"
  ask BSKY_HANDLE "Bluesky handle (e.g. name.bsky.social)"; [ -n "$BSKY_HANDLE" ] && ask BSKY_APP_PASSWORD "Bluesky app password"
  { for K in YOUTUBE_API_KEY REDDIT_CLIENT_ID REDDIT_CLIENT_SECRET BSKY_HANDLE BSKY_APP_PASSWORD; do echo "export $K='${!K}'"; done; } > keys.txt; chmod 600 keys.txt
  echo "Saved to keys.txt (stays on this Mac). Edit or delete it to change keys."
fi
export YOUTUBE_API_KEY REDDIT_CLIENT_ID REDDIT_CLIENT_SECRET BSKY_HANDLE BSKY_APP_PASSWORD
# quick key checks, so a typo is caught now and not at 3 a.m.
if [ -n "$YOUTUBE_API_KEY" ]; then
  C=$(curl -s -o /dev/null -w '%{http_code}' "https://www.googleapis.com/youtube/v3/channels?part=id&forHandle=@YouTube&key=$YOUTUBE_API_KEY")
  [ "$C" = 200 ] && echo "YouTube key: OK" || { echo "YouTube key was refused (HTTP $C). Check it and that 'YouTube Data API v3' is enabled for it. Fix keys.txt and run again."; exit 1; }
fi
if [ -n "$REDDIT_CLIENT_ID" ]; then
  C=$(curl -s -o /dev/null -w '%{http_code}' -A "TalkingPointRadar/1.0" -u "$REDDIT_CLIENT_ID:$REDDIT_CLIENT_SECRET" -d grant_type=client_credentials https://www.reddit.com/api/v1/access_token)
  [ "$C" = 200 ] && echo "Reddit app: OK" || { echo "Reddit refused the app ID/secret (HTTP $C). Fix keys.txt and run again."; exit 1; }
fi
if [ -n "$BSKY_HANDLE" ]; then
  C=$(curl -s -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json' -d "{\"identifier\":\"$BSKY_HANDLE\",\"password\":\"$BSKY_APP_PASSWORD\"}" https://bsky.social/xrpc/com.atproto.server.createSession)
  [ "$C" = 200 ] && echo "Bluesky: OK" || { echo "Bluesky refused the handle/app password (HTTP $C). Fix keys.txt and run again."; exit 1; }
fi
nohup caffeinate -dims "$0" __run >> logs/run.log 2>&1 &
sleep 1; echo "Started in the background. You can close this window."
echo "  ./run.sh status    progress"
echo "  ./run.sh report    open the report (it is also built automatically at the end)"
