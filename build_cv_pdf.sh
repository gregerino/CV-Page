#!/bin/sh
# Renders the downloadable CVs from cv.html, so a PDF is always the CV page
# itself (see the PRINT rules at the end of style.css).
#
#   sh build_cv_pdf.sh                  # base CV: "CV Marcus Hultberg.pdf"
#   sh build_cv_pdf.sh sv               # base CV in Swedish: "... (sv).pdf"
#   sh build_cv_pdf.sh kunskapsgruppen  # one application, both languages
#   sh build_cv_pdf.sh all              # every application, both languages
#
# An application's CV is cv.html?job=<slug>, which job.js tailors from
# jobs/<slug>.json, and it is written to pdf/<slug>/. The job page and its CV
# page link there, so rebuild a pack's PDF whenever its JSON changes.
#
# Needs Google Chrome and Python 3. The page is served locally because it
# links its stylesheets from the site root.
set -e
cd "$(dirname "$0")"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT=3099
BASE="http://localhost:$PORT/cv.html"

python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null' EXIT
sleep 1

render() { # <url> <out>
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --run-all-compositor-stages-before-draw --virtual-time-budget=8000 \
    --print-to-pdf="$2" "$1" 2>/dev/null
  echo "Wrote $2"
}

pack() { # <slug>
  if [ ! -f "jobs/$1.json" ]; then echo "No pack jobs/$1.json" >&2; exit 1; fi
  mkdir -p "pdf/$1"
  render "$BASE?job=$1&lang=en" "pdf/$1/CV Marcus Hultberg.pdf"
  render "$BASE?job=$1&lang=sv" "pdf/$1/CV Marcus Hultberg (sv).pdf"
}

case "$1" in
  "")  render "$BASE" "CV Marcus Hultberg.pdf" ;;
  sv)  render "$BASE?lang=sv" "CV Marcus Hultberg (sv).pdf" ;;
  all)
    # exempel.json is the README's sample pack, not an application.
    for f in jobs/*.json; do
      slug=$(basename "$f" .json)
      [ "$slug" = exempel ] || pack "$slug"
    done ;;
  *)   pack "$1" ;;
esac
