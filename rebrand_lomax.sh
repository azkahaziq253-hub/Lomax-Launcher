#!/usr/bin/env bash
# Rebrand Amethyst-Android (fork PojavLauncher) menjadi "Lomax Launcher".
# Jalankan dari root repo. Aman dijalankan ulang setelah `git pull` upstream.
set -euo pipefail

APP_NAME="${APP_NAME:-Lomax Launcher}"
APP_ID="${APP_ID:-com.lomax.launcher}"
GAME_DIR="${GAME_DIR:-LomaxLauncher}"
HOME_URL="${HOME_URL:-https://github.com/YOUR_GITHUB/lomax-launcher}"
TARGET_SDK="${TARGET_SDK:-36}"

G=app_pojavlauncher/build.gradle
J=app_pojavlauncher/src/main/java/net/kdt/pojavlaunch
RES=app_pojavlauncher/src/main/res

echo ">> build.gradle: applicationId, nama app, authority, targetSdk"
sed -i \
  -e "s/org\.angelauramc\.amethyst/${APP_ID}/g" \
  -e "s/\"Amethyst (Debug)\"/\"${APP_NAME} (Debug)\"/g" \
  -e "s/\"app_name\", \"Amethyst\"/\"app_name\", \"${APP_NAME}\"/" \
  -e "s/\"app_short_name\", \"Amethyst\"/\"app_short_name\", \"${APP_NAME}\"/" \
  -e "s/targetSdkVersion [0-9]\+/targetSdkVersion ${TARGET_SDK}/" \
  -e "s/'amethyst-legacy-'/'lomax-'/" \
  "$G"

# Signing release & Play Store memakai keystore milik Anda sendiri (lewat env var)
python3 - "$G" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p).read()
new = '''        customRelease {
            storeFile file(System.getenv("LOMAX_KEYSTORE") ?: "lomax_upload.jks")
            storePassword System.getenv("LOMAX_KEYSTORE_PASSWORD")
            keyAlias System.getenv("LOMAX_KEY_ALIAS") ?: "upload"
            keyPassword System.getenv("LOMAX_KEY_PASSWORD") ?: System.getenv("LOMAX_KEYSTORE_PASSWORD")
        }
        googlePlayBuild {
            storeFile file(System.getenv("LOMAX_KEYSTORE") ?: "lomax_upload.jks")
            storePassword System.getenv("LOMAX_KEYSTORE_PASSWORD")
            keyAlias System.getenv("LOMAX_KEY_ALIAS") ?: "upload"
            keyPassword System.getenv("LOMAX_KEY_PASSWORD") ?: System.getenv("LOMAX_KEYSTORE_PASSWORD")
        }
    }
'''
s2 = re.sub(r"        customRelease \{.*?\n        googlePlayBuild \{.*?\n        \}\n    \}\n", new, s, count=1, flags=re.S)
open(p, "w").write(s2)
PY

echo ">> Teks yang tampil ke pengguna (semua bahasa)"
{ grep -rl "Amethyst" "$RES" --include=strings.xml || true; } | while read -r f; do
  sed -i "s/Amethyst/${APP_NAME}/g" "$f"
done

echo ">> Kode Java: nama app, folder game, URL"
sed -i \
  -e "s/APP_NAME = \"Amethyst\"/APP_NAME = \"${APP_NAME}\"/" \
  -e "s#games/Amethyst#games/${GAME_DIR}#g" \
  -e "s#URL_HOME = \"https://wiki.angelauramc.dev\"#URL_HOME = \"${HOME_URL}\"#" \
  "$J/Tools.java"
sed -i "s/\"Amethyst crash report/\"${APP_NAME} crash report/" "$J/PojavApplication.java"

echo ">> Ikon (jika folder branding/ ada)"
if [ -d branding/res ]; then cp -r branding/res/. "$RES/"; fi


echo ">> versionCode otomatis naik di setiap build GitHub Actions (wajib untuk Play Store)"
sed -i 's/versionCode [0-9]\+$/versionCode((System.getenv("GITHUB_RUN_NUMBER") ?: "1").toInteger() + 100)/' "$G"

echo ">> Submodule pakai HTTPS (agar bisa di-checkout GitHub Actions)"
sed -i 's#git@github.com:#https://github.com/#' .gitmodules

echo "Selesai: ${APP_NAME} (${APP_ID}), targetSdk ${TARGET_SDK}"
