# Lomax Launcher

Launcher Minecraft: Java Edition untuk Android. Dibangun dari
[Amethyst-Android](https://github.com/AngelAuraMC/Amethyst-Android) (turunan PojavLauncher),
lisensi **GNU LGPL v3**. Source code harus tetap publik.

> NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT.

## Isi kit

| File | Fungsi |
|---|---|
| `rebrand_lomax.sh` | Mengganti nama app, package `com.lomax.launcher`, teks semua bahasa, folder game, targetSdk 36, signing, versionCode otomatis |
| `branding/res/` | Ikon Lomax (adaptive + round) semua ukuran |
| `branding/make_icon.py` | Generator ikon (ubah warna/bentuk lalu jalankan ulang) |
| `branding/playstore_icon_512.png` | Ikon Play Store 512×512 |
| `branding/playstore_feature_1024x500.png` | Feature graphic Play Store |
| `branding/res/drawable*`, `branding/res/font` | Tema gaya game blok: tombol berbevel, tekstur latar, tombol MAIN oranye, font pixel Jersey 10 (OFL) |
| `branding/layout_overrides/fragment_launcher.xml` | Menu utama baru (grid 2 kolom). Hanya dipasang bila ID upstream masih cocok |
| `branding/assets/default.json` | Layout kontrol default Lomax: D-pad kiri, klaster aksi kanan, baris tombol atas, laci "⋯" |
| `branding/make_ui.py`, `make_controls.py`, `make_menu_preview.py` | Generator aset UI, kontrol, dan gambar pratinjau (ubah lalu jalankan ulang) |
| `branding/licenses/` | Lisensi font (wajib ikut disertakan) |
| `.github/workflows/lomax.yml` | Build otomatis gratis di GitHub Actions (APK tes + AAB Play Store) |
| `PRIVACY_POLICY_LOMAX.md` | Kebijakan privasi (wajib untuk Play Store) |

## Langkah 1 — Fork & pasang kit (gratis, tanpa install apa pun)

1. Login ke GitHub → buka `github.com/AngelAuraMC/Amethyst-Android` → **Fork**.
   Beri nama repo `lomax-launcher`. Biarkan **Public** (syarat LGPL + Actions gratis tanpa batas).
2. Di fork Anda, hapus file `.github/workflows/android.yml` (workflow lama, butuh keystore milik Amethyst).
3. **Add file → Upload files**: unggah `rebrand_lomax.sh`, folder `branding`, `README_LOMAX.md`,
   `PRIVACY_POLICY_LOMAX.md`.
4. **Add file → Create new file**, ketik nama `.github/workflows/lomax.yml`, tempel isi file `lomax.yml` dari kit.
   (Folder berawalan titik sering tidak ikut saat drag-and-drop, jadi buat lewat cara ini.)
5. Opsional: edit `HOME_URL` di `rebrand_lomax.sh` menjadi URL repo Anda.

## Langkah 2 — Build APK tes

1. Tab **Actions** → aktifkan workflow → pilih **Build Lomax Launcher** → **Run workflow**.
2. Tunggu ±20–40 menit. Unduh artifact **LomaxLauncher-debug-apk**, pasang di HP (Android 8+, 64-bit, RAM ≥4 GB disarankan).
3. Tes: login akun Microsoft, unduh versi, main. Akun tanpa pembelian Minecraft otomatis masuk mode **Demo**.

## Langkah 3 — Keystore untuk Play Store (sekali saja, SIMPAN BAIK-BAIK)

Di komputer yang ada Java (atau Android Studio):

```bash
keytool -genkeypair -v -keystore lomax_upload.jks -alias upload \
  -keyalg RSA -keysize 2048 -validity 10000
base64 -w0 lomax_upload.jks > lomax_upload.jks.b64      # Windows: certutil -encode lomax_upload.jks out.b64
```

Di repo: **Settings → Secrets and variables → Actions → New repository secret**:

| Nama secret | Isi |
|---|---|
| `LOMAX_KEYSTORE_BASE64` | isi file `.b64` |
| `LOMAX_KEYSTORE_PASSWORD` | password keystore |
| `LOMAX_KEY_ALIAS` | `upload` |
| `LOMAX_KEY_PASSWORD` | password key (biasanya sama) |
| `CURSEFORGE_API_KEY` | opsional, agar fitur unduh modpack CurseForge aktif |

Jalankan workflow lagi → muncul artifact **LomaxLauncher-playstore-aab**.
Jangan pernah commit file `.jks` ke repo.

## Langkah 4 — Rilis di Google Play

1. Daftar Google Play Console (biaya sekali bayar US$25).
   - Akun **pribadi** baru: wajib *closed testing* minimal 12 penguji aktif selama 14 hari sebelum boleh rilis produksi.
   - Akun **organisasi** (perlu nomor D-U-N-S perusahaan): tidak kena syarat 12 penguji.
2. Buat app: nama **Lomax Launcher** (jangan pakai kata "Minecraft" di nama/ikon).
3. Aktifkan **Play App Signing**, unggah file `.aab`.
4. Store listing: ikon 512, feature graphic, minimal 2 screenshot HP. Di deskripsi tulis disclaimer
   *"NOT AN OFFICIAL MINECRAFT PRODUCT. NOT APPROVED BY OR ASSOCIATED WITH MOJANG OR MICROSOFT."*
   dan sebutkan bahwa pengguna wajib memiliki Minecraft: Java Edition, serta credit ke Amethyst/PojavLauncher + link source.
5. Isi: Privacy policy URL (link ke `PRIVACY_POLICY_LOMAX.md` di repo Anda), Data safety, Content rating, Target audience (bukan untuk anak-anak).
6. Rilis ke Internal/Closed testing dulu → Production.

## Update dari upstream

Di GitHub fork: **Sync fork**. Workflow menjalankan `rebrand_lomax.sh` setiap build, jadi branding otomatis terpasang lagi.

## Catatan penting

- **Login Microsoft**: kode bawaan memakai client ID launcher resmi (`00000000402b5328`), sama seperti Amethyst/PojavLauncher.
  Untuk jangka panjang, daftarkan aplikasi Azure sendiri dan ajukan izin Minecraft API ke Microsoft,
  lalu ganti ID di `MicrosoftLoginFragment.java` dan `MicrosoftBackgroundLogin.java`.
- **targetSdk 36** dipasang karena itu syarat Play Store saat ini. Jika ada tampilan yang tertimpa status bar, laporkan/perbaiki di layout.
- Jangan pernah membundel file game Minecraft di APK; launcher mengunduhnya dari server Mojang setelah login.
