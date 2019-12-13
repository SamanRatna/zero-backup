#!/bin/bash
xset s noblank
xset s off
xset -dpms

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/'Local State'
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences
chromium-browser --kiosk --disable-overscroll-edge-effect --disable-pinch --disable-translate --no-first-run --fast --fast-start --disable-infobars --disable-features=TranslateUI "http://localhost:8000/index.html"
#chromium-browser --kiosk --disable-overscroll-edge-effect --disable-sync --disable-suggestions-ui --disable-signin-promo  --mmal-frame-copy --mmal-frame-buffers=4 --ignore-gpu-blacklist --enable-native-gpu-memory-buffers --start-maximized --disable-infobars 'http://your-url-here'