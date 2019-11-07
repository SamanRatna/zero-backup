#!/bin/bash
xset s noblank
xset s off
xset -dpms
chromium-browser --kiosk --incognito --disable-translate --no-first-run --fast --fast-start --disable-infobars --disable-features=TranslateUI "http://localhost:8000/index.html"
