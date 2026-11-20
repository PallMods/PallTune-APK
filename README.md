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


## File APK yang terbaru (unggahan pemilik)

- Nama release asset: `PallTune.apk`
- Ukuran: `37,550,424` bytes (~37.55 MB)
- SHA-256: `1202a104dbcebd5032f2f69611dce40d66dd2eefe668de9ae1adc997f68a3c7c`

File dikirim melalui ChatGPT. GitHub connector tidak dapat mengunggah binary APK sebagai release asset. Pemilik cukup mengunggah `PallTune.apk` ke draft release v4.3.5, lalu memilih Publish release.

**Jangan gunakan file MediaFire sebelumnya sebagai pengganti tanpa verifikasi SHA-256,** karena berkas APK terbaru memiliki ukuran dan hash yang berbeda.

## Release v4.3.5

Workflow GitHub Actions di `.github/workflows/publish-v4.3.5.yml` mencoba mengimpor APK dari MediaFire hanya jika ukuran dan SHA-256 cocok dengan unggahan paling baru. MediaFire saat ini mengembalikan 404, maka opsi tepercaya adalah mengunggah berkas yang sudah dikirim pemilik langsung ke draft release lalu mempublikasikannya.

**Penting:** Nama file APK harus **persis `PallTune.apk`** pada setiap release baru; bila tidak, URL permanen 404. Jangan tandai release sebagai pre-release.