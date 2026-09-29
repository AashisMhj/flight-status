#!/bin/bash
set -euo pipefail

# Resolve the directory this script lives in, regardless of where it's called from
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

VENV_DIR="$SCRIPT_DIR/.venv"
SPIDER_DIR="$SCRIPT_DIR/flight_status"


cd "$SPIDER_DIR"

"$VENV_DIR/bin/scrapy" crawl buddaair --loglevel=WARNING
"$VENV_DIR/bin/scrapy" crawl yetiairlines --loglevel=WARNING
"$VENV_DIR/bin/scrapy" crawl shreeairlines --loglevel=WARNING