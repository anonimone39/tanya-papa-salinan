import subprocess, json, os, sys
WD, TMP, BASE, VOICE, OUT, PB = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6])
os.makedirs(TMP, exist_ok=True)
EDGE = os.path.expanduser("~/.claude/skill-packages/stick-figure/kit/.venv/bin/edge-tts")
# kalimat = daftar bagian: (teks, rate_offset, pitch_offset, volume, jeda_setelah_bagian)
S = [
 [("Pernah punya printer, tapi bingung cara menyambungkannya ke laptop?", 2, 0, 0, 0)],
 [("Sini, Papa jelasin!", 12, 0, 12, 0)],
 [("Pertama, colok kabel listrik printer, terus tekan tombol power.", 0, 0, 0, 0)],
 [("Habis itu, sambungkan kabel yuesbi dari printer ke laptop.", 0, 0, 0, 0)],
 [("Kedua, cek seri printernya. Biasanya ada di stiker, di bagian depan atau belakang printer.", 0, 0, 0, 0)],
 [("Catat tipenya, biasanya gabungan huruf dan angka.", 0, 0, 0, 0)],
 [("Ketiga, cari drivernya. Driver itu penerjemah, supaya laptop ngerti cara ngomong sama printer.", 0, 0, 0, 0)],
 [("Cara paling gampang, buka situs resmi merek printernya, ketik tipe tadi, lalu download drivernya.", 0, 0, 0, 0)],
 [("Kalau laptop kamu punya tempat CD, kamu bisa pakai kaset driver bawaan printernya. Kalau gak ada, tetap cari drivernya online ya.", 0, 0, 0, 0)],
 [("Setelah itu, jalankan file drivernya dan ikuti langkahnya sampai selesai.", 0, 0, 0, 0)],
 [("Keempat, buka dokumen yang mau dicetak, terus tekan kontrol dan P.", 0, 0, 0, 0)],
 [("Pilih nama printernya, atur jumlah salinan, lalu klik Print.", 0, 0, 0, 0)],
 [("Kalau kertasnya keluar, berarti printer kamu sudah siap dipakai!", 0, 0, 0, 0)],
 [("Nah,", 0, 0, 0, 0.5), ("sekarang pengetahuanmu sudah bertambah.", 0, 0, 0, 0)],
 [("Kalau ada yang bikin kamu penasaran, tanya aja sama Papa yaa.", 0, 0, 0, 0)],
 [("Tinggal komen di bawah, nanti Papa jelaskan di video berikutnya.", -2, 0, 0, 0)],
]
GAP = [0.14,0.10,0.18,0.14,0.18,0.14,0.16,0.14,0.16,0.14,0.14,0.14,0.16,0.20,0.14,0.0]
def sgn(n, u): return ("+" if n >= 0 else "-") + str(abs(n)) + u
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
def sil(path, d): subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(d),path],check=True)
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse"
t = 0.1; cues = []; lst = [f"{TMP}/lead.wav"]; sil(lst[0], 0.1)
for i, parts in enumerate(S):
    start = t
    for j, (txt, ro, po, vol, gap) in enumerate(parts):
        mp3 = f"{TMP}/s{i}_{j}.mp3"; wav = f"{TMP}/s{i}_{j}.wav"
        flags = [] if "Multilingual" in VOICE else [f"--rate={sgn(BASE+ro,'%')}", f"--pitch={sgn(PB+po,'Hz')}", f"--volume={sgn(vol,'%')}"]
        subprocess.run([EDGE, "--voice", VOICE] + flags + ["--text", txt, "--write-media", mp3], check=True, capture_output=True)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp3,"-ar","24000","-ac","1","-af",TRIM,wav], check=True)
        lst.append(wav); t += dur(wav)
        if gap > 0:
            g = f"{TMP}/pg{i}_{j}.wav"; sil(g, gap); lst.append(g); t += gap
    cues.append([round(start,3), round(t,3)])
    if GAP[i] > 0:
        g = f"{TMP}/g{i}.wav"; sil(g, GAP[i]); lst.append(g); t += GAP[i]
with open(f"{TMP}/list.txt","w") as f:
    for p in lst: f.write(f"file '{p}'\n")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",f"{TMP}/list.txt","-c","copy",f"{TMP}/all.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{TMP}/all.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=9","-ar","44100","-ac","1","-c:a","libmp3lame","-b:a","160k",f"{WD}/{OUT}"],check=True)
total = dur(f"{WD}/{OUT}")
json.dump({"cues":cues,"total":total}, open(f"{TMP}/timing.json","w"))
print(OUT, "total", round(total,2))
