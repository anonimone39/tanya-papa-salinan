# Tanya Papa: panduan kerja untuk Claude

Balas dalam bahasa Indonesia. Proyek ini adalah akun medsos edukasi dengan persona seorang papa yang mengajari anaknya, dibuat untuk anak muda (Gen Z dan non-Gen Z), terutama yang tumbuh tanpa sosok ayah. Topik: komunikasi, elektronik, komputer, pengetahuan umum, mekanik, dan lainnya.

Catatan sejarah dan preferensi lengkap ada di `Backup/memori/tanya-papa-rules.md`. Percakapan lama ada di `Backup/chat/`. Kalau isinya berbeda dengan file ini, file ini yang berlaku.

## Aturan wajib
1. Setiap topik baru dimulai dengan form 4 baris untuk diisi user. Jangan membuat apa pun sebelum terisi:
   ```text
   1. Detail materi   :
   2. Durasi video    :
   3. Rasio video     : Portrait 9:16 / Landscape 16:9 (YouTube)
   4. Kategori video  :
   ```
2. Setiap video punya kategori (contoh: Computer Things).
3. Tulis naskah dulu dalam tabel bernomor (nomor, adegan, kalimat), lalu tunggu persetujuan. Buat animasi hanya setelah naskah disetujui.
4. Setiap video wajib punya logo Tanya Papa di pojok kiri atas dan outro bermerek yang halus (tidak terpotong mendadak).
5. Setiap video selesai disertai judul per platform (YouTube Shorts, TikTok, Instagram Reels, Facebook Reels), caption, dan hashtag, disimpan di `Upload/<Judul>_judul-caption-hashtag.md`.
6. Format portrait: 1080x1920, 30 fps tetap, H.264 High, AAC 48 kHz. User memakai Android, jadi fps harus tetap.
7. Jangan menyalin atau mengunggah data pekerjaan kantor ke proyek ini.

## Gaya naskah
- Papa menjelaskan dengan santai ("gak", "tau"). Tanpa sapaan "Nak".
- Pembuka: pertanyaan penasaran, lalu "Sini, Papa jelasin!" yang bersemangat.
- Penutup (3 kalimat): "Nah... sekarang pengetahuanmu sudah bertambah." / "Kalau ada yang bikin kamu penasaran, tanya aja sama Papa yaa.." / "Tinggal komen di bawah, nanti Papa jelaskan di video berikutnya."
- Durasi suara kira-kira 2,6 kata per detik. Outro menambah 4,2 detik.

## Suara
- edge-tts `id-ID-ArdiNeural`, nada -10 Hz, kecepatan -5%. Dibuat per kalimat. Kalimat "Sini, Papa jelasin!" lebih cepat dan lebih keras dengan nada yang sama.
- "Nah," diberi jeda 0,5 detik. "yaa." tidak dijeda dan tidak diperlambat.
- Kata Inggris ditulis apa adanya (mouse, LED, chip, download, Print). Ejaan khusus yang sudah disetujui: USB = "yuesbi", GHz = "giga hertz", Ctrl = "kontrol".
- Caption di layar memakai ejaan normal. Jumlah kata caption harus sama dengan teks yang diucapkan, supaya sorotan per kata sinkron.

## Merek
- Logo dan banner di `Brand/`. Karakter Papa: kacamata bulat, rambut hitam rapi, baju biru, balon kuning bertanda tanya.
- Judul "Tanya Papa" (Tanya putih, Papa kuning), garis bawah koral, tagline "Sini Papa jelasin!".
- Warna: biru #1D4ED8 ke #14307A, kuning #FFD23F, koral #FF7A59, teks terang #DBEAFE. Font web Nunito 800/900.

## Gaya visual (isometrik, digambar dengan kode)
- Bentuk membulat, jangan mengkotak. Gunakan `rr`, `ext`, `rbox`, `extXZ` di template video 2.
- Kabel memakai lengkung (`spline`) dan konektor nyata (USB-A, USB-B, steker berkaki).
- Urutan gambar mengikuti kedalaman: benda dengan x+y lebih besar digambar belakangan, kalau tidak akan saling menimpa.
- Ukuran antar benda harus masuk akal (laptop jauh lebih besar dari mouse).
- Warna: kuning = sedang dijelaskan, hijau = menyala atau data, biru = sinyal atau tombol, merah = daya atau peringatan.
- Merek dan tipe perangkat di animasi memakai contoh rekaan.

## Cara membuat video baru
1. Salin folder video terakhir menjadi `NN Kategori - Judul` (contoh: `03 Computer Things - Keyboard`).
2. Ubah `naskah.py` (NAMA_FILE, kalimat `S`, jeda `GAP`, `CAPTIONS`).
3. Ubah `template.html` (adegan, kamera, label) dan `efek.py` (waktu efek suara). `Skrip/halaman.py` mengisi logo, caption, waktu, dan outro.
   Perhatikan: template video 2 punya judul, daftar adegan, dan teks halaman khusus printer yang harus diganti. Penanda `@@DEFS@@`, `@@CAPS@@`, `@@BRAND@@`, `@@DUR@@`, `@@VEND@@`, `@@AUDIO@@` dipertahankan.
4. Cek frame sebelum render penuh, lalu lihat gambarnya (label tidak terpotong, benda tidak saling menimpa, sorotan terlihat kamera):
   ```bash
   bash Skrip/buat_video.sh "03 Computer Things - Keyboard" cek 2,10,20,30,40
   ```
5. Render penuh ke `Upload/`:
   ```bash
   bash Skrip/buat_video.sh "03 Computer Things - Keyboard"
   ```
6. Periksa hasil dengan ffprobe dan beberapa frame. Claude tidak bisa mendengar audio, jadi minta user mendengarkan dan sebutkan nomor kalimat yang perlu diperbaiki.
7. Tulis paket unggah, lalu tawarkan commit dan push ke repo private `TanyaPapa/tanya-papa`.

Video 1 (mouse) hanya berupa HTML jadi di foldernya. Render ulang dengan `node Skrip/render.mjs full "<html>" <keluaran.mp4> "<mix-papa.mp3>" 61.3`.

## Efek suara dan musik
- Efek suara dibuat sintetis oleh `Skrip/efek.py` (whoosh, pop, klik, ding, chime). Tidak perlu mengunduh apa pun.
- User pernah menyebut Mixkit dan Envato Elements (berbayar). Mengunduh file hanya setelah user menyetujui nama, sumber, dan ukurannya.

## Ide topik berikutnya
Kenapa komputer lemot (RAM vs penyimpanan), kenapa flashdisk harus di-Eject, cara kerja keyboard, beda HDD dan SSD.
