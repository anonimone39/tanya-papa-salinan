---
name: tanya-papa-rules
description: "Project \"Tanya Papa\" (akun medsos edukasi, persona papa mengajari anak): aturan wajib tiap video, preferensi suara, gaya naskah, durasi, musik"
metadata:
  node_type: memory
  type: project
  originSessionId: 10c4aeec-1a21-42ff-b2f9-406b64282bba
  modified: 2026-11-24T16:38:42.246Z
---

Proyek: **Tanya Papa**. Akun medsos edukasi dengan persona seorang bapak yang mengajari anaknya tentang hidup. Dibuat karena banyak anak di Indonesia yang fatherless. Topik: cara berkomunikasi, elektronik, komputer, pengetahuan umum, mekanik, dan lainnya. Audiens: anak muda, baik Gen Z maupun non-Gen Z. Video pertama: "Cara kerja mouse wireless", kategori "Computer Things", animasi isometrik digambar dengan kode (artifact `mouse-wireless.html`, 2026-11-24).

**Aturan wajib (ditetapkan user, 2026-11-24):**
1. Setiap topik baru: wajib tentukan materi dan durasi dulu. Berikan form mini 4 baris untuk diisi user: (1) Detail materi, (2) Durasi video, (3) Rasio video (portrait, atau landscape untuk YouTube), (4) Kategori video.
2. Setiap video wajib punya kategori (contoh: mouse masuk "Computer Things").
3. Judul dikelompokkan dan dibuat menarik untuk upload ke YouTube, TikTok, Instagram, dan Facebook. Nada: papa yang mengajari anak, menarik untuk Gen Z dan non-Gen Z.
4. Buatkan juga kalimat postingan (caption) beserta hashtag.
5. Selalu kompres video dengan pengaturan terbaik untuk medsos. User memakai Android, jadi fps dan resolusi harus disesuaikan agar hasil upload ke FB/IG tetap bagus. Portrait 1080x1920, 30 fps tetap, H.264, AAC. Cek aturan resmi platform sebelum merender.

**Gaya naskah dan suara (preferensi user, 2026-11-24):**
- Gaya bicara papa menjelaskan ke anaknya (tanpa sapaan "Nak", lihat koreksi di bawah). Pembuka contoh dari user: "Pernah terlintas dalam pikiran, kenapa ... ? Sini papa jelasin!" Penutup contoh: ajak penonton komen pertanyaan, "nanti Papa jelaskan di video berikutnya". Kalimat "Sini Papa jelasin!" harus energik dan bersemangat.
- Suara: edge-tts `id-ID-ArdiNeural`, varian A (pitch -10Hz, lebih berat dari bawaan). Dibuat per kalimat (rate dasar sekitar -5%, kalimat energik lebih cepat dengan nada tetap sama) lalu digabung ffmpeg, agar timing kalimat pasti. Pelafalan dipandu lewat ejaan, tapi kata Inggris umum ditulis apa adanya (lihat koreksi di bawah).
- Durasi pilihan user untuk video mouse: sekitar 60 detik (agak cepat tidak apa).
- Musik latar: user menyarankan Envato Elements. Itu langganan berbayar, bukan gratis (cek lisensi resmi). User yang mengunduh trek, lalu mixing (ducking) dilakukan dengan ffmpeg.
- Referensi bentuk mouse dari user: mouse optik wireless kecil, atas abu-abu, sisi bawah hitam, roda scroll hitam bertekstur, garis pemisah tombol (tanpa logo merek).

**Why:** User ingin alur kerja konsisten dan hasil unggahan bagus dari perangkat Android.
**How to apply:** Di awal setiap topik baru, tampilkan form 4 baris dulu sebelum membuat apa pun. Di akhir setiap video, sertakan judul per platform, caption plus hashtag, dan perintah kompres sesuai spesifikasi platform.

**Koreksi pelafalan dari user (2026-11-24):** tulis kata Inggris apa adanya agar dibaca natural (mouse, LED, chip), jangan dieja per huruf atau diubah jadi "maus". Bahasa santai: "tau" bukan "tahu", "gak". Hindari sapaan "Nak" (suara Ardi membacanya kurang jelas). Jeda ~0,5 detik setelah "Nah"; "yaa" di akhir dipanjangkan agar ramah. Multilingual voice edge-tts tidak mendukung pengaturan rate/pitch dan sering gagal, jadi tetap pakai Ardi. Skrip pembuat suara dan penambal halaman ada di folder scratchpad sesi; naskah per kalimat disimpan di kolom caption halaman.

**Efek suara (2026-11-24):** user menyarankan Mixkit (mixkit.co/free-sound-effects) dan minta efek suara ditambahkan. Dibuat sintetis dengan numpy/ffmpeg (whoosh antar adegan, pop label, klik tombol, ding sinyal, chime penutup) tanpa mengunduh file; hasil dicampur ke narasi sebagai `mix-papa.mp3`. Mengunduh dari Mixkit hanya setelah user menyetujui nama file, sumber, dan ukuran. Lisensi Mixkit: halaman menyebut boleh komersial tanpa atribusi, tapi teks lisensi lengkap belum diverifikasi.

**Merek dan outro (aturan user, 2026-11-24):** setiap video wajib punya logo Tanya Papa (pojok kiri atas, bulat) dan outro yang halus, tidak langsung terpotong. Outro: transisi memudar ke kartu penutup bermerek lalu ditahan ~4 detik, audio fade-out. Merek: karakter Papa (kacamata bulat, rambut hitam rapi, baju biru) dengan balon kuning bertanda tanya; judul "Tanya Papa" (Tanya putih, Papa kuning), garis bawah koral, tagline "Sini Papa jelasin!". Warna: biru #1D4ED8 ke #14307A, kuning #FFD23F, koral #FF7A59, teks terang #DBEAFE. Font: rounded bold (Avenir Next Rounded di Mac; Nunito 800/900 untuk web). File vektor logo dan banner dari user ada di folder sesi lain bernama scratch-2026-11-24-7d0a6e (logo-tanya-papa.svg, logo-wajah-tanya-papa.svg, banner-tanya-papa.svg); folder sesi bisa terhapus, jadi minta user menyimpannya di folder tetap.

**Pipeline render MP4 (2026-11-24, video 1 selesai):** halaman HTML/SVG dirender frame demi frame dengan Playwright Chromium (modul playwright ada di kit stick-figure: ~/.claude/skill-packages/stick-figure/kit/node_modules), viewport 1080x1920, memanggil window.__seek(t) lalu screenshot elemen #stage, dialirkan ke ffmpeg: libx264 High, crf 18, maxrate 12M, yuv420p, bt709, 30 fps tetap, AAC 192k 48 kHz stereo, +faststart. Hasil video mouse: 61,3 detik, 13 MB. Sebelum render penuh, selalu cek lembar kontak frame (label tidak terpotong). Audio: suara per kalimat (edge-tts Ardi) + efek suara sintetis + fade-out; durasi total = suara + ekor outro 4,2 detik.

**Lokasi file proyek (2026-11-25):** semua file penting disimpan di `/Users/steven.aprilianto/Project Tanya Papa/`. Video siap unggah (MP4, judul, caption, hashtag) ke subfolder `Upload/`. Subfolder lain: `Brand/` (logo, banner), `01 Computer Things - Mouse Wireless/` (sumber video 1), `Skrip/` (pembuat suara, efek, render). Video berikutnya: buat subfolder bernomor baru dengan pola "NN Kategori - Judul", dan simpan hasil jadi di `Upload/`.

**Video 2 selesai (2026-11-25):** "Cara Pakai Printer Lewat Kabel USB", Computer Things, 77 detik, 1080x1920 30 fps; file di `Project Tanya Papa/Upload/` dan sumbernya di `02 Computer Things - Printer USB/`. Topik berikutnya yang pernah diusulkan: kenapa komputer lemot (RAM vs penyimpanan), kenapa flashdisk harus di-Eject, cara kerja keyboard, beda HDD dan SSD.
**Pelajaran teknis penting:**
- Sinkron caption: pakai waktu per kata dari edge-tts (Communicate dengan boundary="WordBoundary"), bukan dibagi rata; skrip `Skrip/make_voice4.py`. Caption harus punya jumlah kata sama dengan teks yang diucapkan (ejaan pelafalan ditulis 1 kata per 1 kata caption).
- Urutan gambar isometrik harus berdasarkan kedalaman (x+y lebih besar = lebih dekat, digambar belakangan), kalau tidak benda saling menimpa.
- Bentuk benda jangan kotak: pakai persegi bersudut bulat (rr + ext), kabel pakai spline dengan colokan nyata (USB-A, USB-B, steker dengan kaki).
- Di zsh, tulis ${VAR} saat variabel diikuti tanda kurung siku di string ffmpeg (misal ${DUR}[v]); `rm` dengan glob yang tidak cocok membatalkan rantai perintah.

**Backup GitHub (2026-11-26):** repo private https://github.com/TanyaPapa/tanya-papa berisi seluruh folder `Project Tanya Papa` (termasuk `Backup/` dengan chat teks, memori, dan PEMULIHAN.md). User ingin hanya data Tanya Papa yang dibackup; data kantor tidak boleh disentuh. Setelah video baru selesai, tawarkan commit dan push ke repo ini.
