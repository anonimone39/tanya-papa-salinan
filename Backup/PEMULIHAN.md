# Memulihkan proyek Tanya Papa di akun atau komputer baru

## 1. Ambil kembali file
Login ke GitHub (`gh auth login`, akun TanyaPapa), lalu:

```bash
gh repo clone TanyaPapa/tanya-papa "$HOME/Project Tanya Papa"
```

## 2. Pasang alat dan lanjutkan
Ikuti [INSTALL.md](../INSTALL.md). Alur kerja untuk Claude ada di [CLAUDE.md](../CLAUDE.md). Riwayat percakapan ada di `Backup/chat/chat-tanya-papa.md` (teks saja).

## Yang tidak ikut dibackup
- Halaman artifact di claude.ai: tautannya terikat ke akun lama. Sumber HTML video 1 dan 2 sudah ada di folder masing-masing.
- Rekaman mentah sesi Claude Code (`~/.claude/projects`): tetap ada di komputer lama.
- Proyek lain di luar Tanya Papa.
- Paket skill stick-figure (sekitar 1,3 GB) dan model suaranya: pasang ulang bila diperlukan.
