#!/usr/bin/env bash
# Rebrand Amethyst-Android (fork PojavLauncher) menjadi "Lomax Launcher".
# Jalankan dari root repo. Aman dijalankan ulang setelah `git pull` upstream.
set -euo pipefail

APP_NAME="${APP_NAME:-Lomax Launcher}"
APP_ID="${APP_ID:-com.lomax.launcher}"
GAME_DIR="${GAME_DIR:-LomaxLauncher}"
HOME_URL="${HOME_URL:-https://github.com/YOUR_GITHUB/lomax-launcher}"
TARGET_SDK="${TARGET_SDK:-36}"
DISCORD_URL="${DISCORD_URL:-$HOME_URL}"

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

echo ">> Ikon, tombol blok, tekstur latar, font pixel (folder branding/res)"
if [ -d branding/res ]; then cp -r branding/res/. "$RES/"; fi

echo ">> Tema warna gaya game blok"
C="$RES/values/colors.xml"
setcolor() { sed -i "s|<color name=\"$1\">[^<]*</color>|<color name=\"$1\">$2</color>|" "$C"; }
setcolor minebutton_color      "#E8922C"
setcolor background_app        "#1A262C"
setcolor background_overlay    "#3A5257"
setcolor background_status_bar "#12302F"
setcolor background_bottom_bar "#2A1E14"
setcolor control_button_color  "#66000000"

echo ">> Gaya tombol menu: blok + font pixel"
S="$RES/values/styles.xml"
sed -i 's#<item name="android:background">?android:attr/selectableItemBackground</item>#<item name="android:background">@drawable/lomax_block_button</item>#' "$S"
python3 - "$S" <<'PY'
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
if 'name="LomaxTile"' not in s:
    style = '''    <style name="LomaxTile" parent="LauncherMenuButton.Universal">
        <item name="android:layout_width">0dp</item>
        <item name="android:layout_height">@dimen/_52sdp</item>
        <item name="android:layout_margin">@dimen/_4sdp</item>
        <item name="android:background">@drawable/lomax_block_button</item>
        <item name="android:fontFamily">@font/lomax_pixel</item>
        <item name="android:textColor">#FFFFFFFF</item>
        <item name="android:shadowColor">#FF0C0E10</item>
        <item name="android:shadowDx">2</item>
        <item name="android:shadowDy">2</item>
        <item name="android:shadowRadius">0.01</item>
    </style>
'''
    i = s.rindex("</resources>")
    open(p, "w", encoding="utf-8").write(s[:i] + style + s[i:])
PY
sed -i 's/R\.font\.noto_sans_bold/R.font.lomax_pixel/' app_pojavlauncher/src/main/java/com/kdt/mcgui/MineButton.java

echo ">> Menu utama baru (grid blok) — hanya dipasang bila ID upstream masih cocok"
python3 - "$RES/layout/fragment_launcher.xml" branding/layout_overrides/fragment_launcher.xml app_pojavlauncher/src/main/java <<'PY'
import re, sys, os, shutil
up, ours, src = sys.argv[1:4]
ids = lambda p: set(re.findall(r'@\+id/(\w+)', open(p, encoding="utf-8").read()))
code = ""
for root, _, files in os.walk(src):
    for f in files:
        if f.endswith((".java", ".kt")):
            code += open(os.path.join(root, f), encoding="utf-8", errors="ignore").read()
needed = {i for i in ids(up) if re.search(r'R\.id\.' + re.escape(i) + r'\b', code)}
missing = needed - ids(ours)
if missing:
    print("   PERINGATAN: upstream memakai ID baru", sorted(missing), "- menu lama dipertahankan")
else:
    shutil.copy(ours, up); print("   menu blok terpasang")
PY

echo ">> Layout kontrol default Lomax"
if [ -f branding/assets/default.json ]; then cp branding/assets/default.json app_pojavlauncher/src/main/assets/default.json; fi

echo ">> Hapus font Mojang (Minecraft Ten) yang tidak dipakai"
rm -f "$RES/font/minecraft_ten.ttf"

echo ">> Link Discord diganti ke link Anda"
sed -i "s#<string name=\"discord_invite\" translatable=\"false\">[^<]*</string>#<string name=\"discord_invite\" translatable=\"false\">${DISCORD_URL}</string>#" "$RES/values/strings.xml"


echo ">> versionCode otomatis naik di setiap build GitHub Actions (wajib untuk Play Store)"
sed -i 's/versionCode [0-9]\+$/versionCode((System.getenv("GITHUB_RUN_NUMBER") ?: "1").toInteger() + 100)/' "$G"

echo ">> Submodule pakai HTTPS (agar bisa di-checkout GitHub Actions)"
sed -i 's#git@github.com:#https://github.com/#' .gitmodules

echo "Selesai: ${APP_NAME} (${APP_ID}), targetSdk ${TARGET_SDK}"
