# PallTune — Android APK

Repository resmi distribusi APK **PallTune**. Aplikasi musik gratis untuk Android.

**Website:** https://palltune.vercel.app/

## Download versi terbaru

Setelah rilis pertama selesai, tombol unduh di website dapat memakai URL permanen:

https://github.com/PallMods/PallTune-APK/releases/latest/download/PallTune.apk

Unduhan mengarah ke file APK, bukan halaman daftar rilis GitHub.

## Cara update aplikasi

1. Siapkan APK versi terbaru, **rename jadi `PallTune.apk`**.
2. Buka tab **Releases** di repository GitHub ini, pilih **Draft a new release**.
3. Buat tag baru, contoh `v4.3.6`. Set judul `PallTune V4.3.6`.
4. Upload file APK sebagai **release asset** (bukan commit file biasa).
5. Pastikan **Set as latest release** aktif, **Pre-release** nonaktif.
6. Klik **Publish release**.

Link permanen otomatis menunjuk asset `PallTune.apk` dari release terbaru tanpa mengubah website Vercel.

## Release v4.3.5

Workflow GitHub Actions di `.github/workflows/publish-v4.3.5.yml` mengimpor APK yang sudah diupload pemilik ke MediaFire. Importer hanya mempublikasikan jika ukuran dan checksum SHA-256 sesuai dengan APK asli yang diberikan pemilik. Bila MediaFire mengganti tata letak atau mengaktifkan CAPTCHA, workflow dapat gagal. Dalam keadaan itu upload APK secara manual pada halaman Releases.

**Penting:** Nama file APK harus **persis `PallTune.apk`** pada setiap release baru; bila tidak, URL permanen 404. Jangan tandai release sebagai pre-release.