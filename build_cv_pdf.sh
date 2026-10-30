#!/bin/sh
# Renders "CV Marcus Hultberg.pdf" from cv.html, so the downloadable CV is
# the CV page itself (see the PRINT rules at the end of style.css).
#
#   sh build_cv_pdf.sh            # English
#   sh build_cv_pdf.sh sv         # Swedish, into "CV Marcus Hultberg (sv).pdf"
#
# Needs Google Chrome and Python 3. The page is served locally because it
# links its stylesheets from the site root.
set -e
cd "$(dirname "$0")"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT=3099
OUT="CV Marcus Hultberg.pdf"
URL="http://localhost:$PORT/cv.html"
if [ "$1" = "sv" ]; then
  OUT="CV Marcus Hultberg (sv).pdf"
  URL="$URL?lang=sv"
fi

python3 -m http.server "$PORT" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null' EXIT
sleep 1

"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw --virtual-time-budget=8000 \
  --print-to-pdf="$OUT" "$URL" 2>/dev/null

echo "Wrote $OUT"
