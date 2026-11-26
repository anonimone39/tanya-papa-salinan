# Instalasi Tanya Papa di akun atau komputer baru (macOS)

Ikuti berurutan. Di komputer yang sama, sebagian besar alat mungkin sudah ada, dan skrip akan melewatinya.

## 1. Aplikasi dan akun
1. Pasang aplikasi Claude Desktop, lalu login dengan akun Claude baru. Pekerjaan dilakukan di tab **Code**.
2. Pasang Homebrew bila belum ada, dari https://brew.sh (ikuti perintah di halaman itu).
3. Pasang GitHub CLI dan login ke akun **TanyaPapa**:

```bash
brew install gh
```

```bash
gh auth login
```

Pilih GitHub.com, HTTPS, lalu login lewat browser.

## 2. Ambil proyek
Lewati langkah ini bila folder `Project Tanya Papa` masih ada di komputer.

```bash
gh repo clone TanyaPapa/tanya-papa "$HOME/Project Tanya Papa"
```

## 3. Pasang alat
```bash
bash "$HOME/Project Tanya Papa/setup.sh"
```

Skrip ini memasang:

| Alat | Versi yang dipakai saat dibuat | Fungsi |
|---|---|---|
| ffmpeg | 8.1.2 | Olah audio dan encode MP4 |
| Node.js | 22 | Menjalankan perender |
| Playwright + Chromium | 1.49.1 | Mengambil frame animasi |
| Python | 3.12 (di `.venv`) | Suara dan efek |
| edge-tts | 7.3.1 | Suara Papa (butuh internet) |
| numpy | 2.x | Efek suara |
| GitHub CLI | 2.x | Backup |

Perlu internet untuk instalasi, suara Papa, dan font (Google Fonts) saat render.

## 4. Periksa
```bash
bash "$HOME/Project Tanya Papa/Skrip/cek.sh"
```

Semua baris harus `OK`.

## 5. Coba alur (opsional tapi disarankan)
Membuat beberapa frame uji dari video 2, tanpa render penuh:

```bash
bash "$HOME/Project Tanya Papa/Skrip/buat_video.sh" "02 Computer Things - Printer USB" cek 3,12,30
```

Gambarnya ada di `02 Computer Things - Printer USB/build/`.

## 6. Mulai bekerja dengan Claude
Buka sesi baru di tab Code dan pilih folder `Project Tanya Papa`. File `CLAUDE.md` terbaca otomatis. Kirim pesan pertama:

> Baca CLAUDE.md dan Backup/memori/tanya-papa-rules.md, simpan aturannya ke memori, jalankan Skrip/cek.sh, lalu berikan form 4 baris untuk video berikutnya.

## Tambahan (opsional)
- **RTK** (hemat token untuk perintah terminal): `brew install rtk` lalu `rtk init -g`. Ini mengubah pengaturan global Claude Code.
- **Konektor Canva** untuk thumbnail: sambungkan lewat pengaturan Connectors di aplikasi Claude.
- **Skill stick-figure** tidak diperlukan untuk Tanya Papa.

## Kalau ada masalah
| Gejala | Solusi |
|---|---|
| `Belum terpasang. Jalankan dulu: bash setup.sh` | Jalankan langkah 3 |
| Suara gagal dibuat | Cek internet, coba lagi. edge-tts memakai layanan Microsoft yang bisa berubah |
| Font di video berbeda | Pastikan internet aktif saat render |
| Chromium tidak ditemukan | Di folder proyek: `npx playwright install chromium` |
| Push GitHub ditolak | Cek akun aktif: `gh auth status`, ganti dengan `gh auth switch` |
