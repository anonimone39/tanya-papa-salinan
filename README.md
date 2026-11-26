# Project Tanya Papa

Akun media sosial edukasi: Papa menjelaskan banyak hal ke anaknya (komunikasi, elektronik, komputer, pengetahuan umum, mekanik, dan lainnya).

## Isi folder
- `Upload/` : video siap unggah beserta judul, caption, dan hashtag per platform
- `Brand/` : logo, logo wajah, dan banner (SVG dan PNG)
- `01 Computer Things - Mouse Wireless/` : sumber video 1 (halaman animasi HTML, audio suara Papa, efek suara, waktu kalimat)
- `Skrip/` : skrip pembuat suara, efek suara, penambal halaman, dan perender MP4 (Playwright + ffmpeg)

## Aturan tiap video
1. Awal topik: isi form 4 baris (detail materi, durasi, rasio, kategori).
2. Setiap video punya kategori (contoh: Computer Things).
3. Judul per platform (YouTube, TikTok, Instagram, Facebook), caption, dan hashtag.
4. Kompres untuk medsos: 1080x1920, 30 fps tetap, H.264, AAC. Android: pastikan fps tetap.
5. Logo di pojok kiri atas dan outro bermerek yang halus.

## Mulai
- Instalasi di akun atau komputer baru: [INSTALL.md](INSTALL.md)
- Aturan dan alur kerja untuk Claude: [CLAUDE.md](CLAUDE.md)
- Membuat video: `bash Skrip/buat_video.sh "<folder video>"`
