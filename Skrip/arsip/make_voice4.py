# Suara per kalimat dengan waktu per kata dari edge-tts (WordBoundary), disusun ke satu file + timing.json
import asyncio, json, os, subprocess, sys, re
import edge_tts
WD, TMP, BASE, VOICE, OUT, PB, SRC = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7]
os.makedirs(TMP, exist_ok=True)
src = open(SRC, encoding="utf-8").read()
ns = {}
exec(re.search(r"S = \[\n.*?\n\]\nGAP = \[[^\]]*\]", src, re.S).group(0), ns)
S, GAP = ns["S"], ns["GAP"]
def sgn(n, u): return ("+" if n >= 0 else "-") + str(abs(n)) + u
def dur(p): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
def sil(path, d): subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(d),path],check=True)
async def tts(txt, rate, pitch, vol, mp3):
    c = edge_tts.Communicate(txt, VOICE, rate=sgn(rate,'%'), pitch=sgn(pitch,'Hz'), volume=sgn(vol,'%'), boundary="WordBoundary")
    words = []
    with open(mp3, "wb") as f:
        async for m in c.stream():
            if m["type"] == "audio": f.write(m["data"])
            elif m["type"] == "WordBoundary": words.append((m["text"], m["offset"]/1e7, m["duration"]/1e7))
    return words
t = 0.1; cues = []; cwords = []; lst = [f"{TMP}/lead.wav"]; sil(lst[0], 0.1)
for i, parts in enumerate(S):
    start = t; wl = []
    for j, (txt, ro, po, vol, gap) in enumerate(parts):
        mp3 = f"{TMP}/s{i}_{j}.mp3"; wav = f"{TMP}/s{i}_{j}.wav"
        words = asyncio.run(tts(txt, BASE+ro, PB+po, vol, mp3))
        lead = max(0.0, (words[0][1] if words else 0.0) - 0.04)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp3,"-ar","24000","-ac","1","-af",
            f"atrim=start={lead:.3f},asetpts=N/SR/TB,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse", wav], check=True)
        for w in words: wl.append([w[0], round(t + w[1] - lead, 3)])
        lst.append(wav); t += dur(wav)
        if gap > 0:
            g = f"{TMP}/pg{i}_{j}.wav"; sil(g, gap); lst.append(g); t += gap
    cues.append([round(start,3), round(t,3)]); cwords.append(wl)
    if GAP[i] > 0:
        g = f"{TMP}/g{i}.wav"; sil(g, GAP[i]); lst.append(g); t += GAP[i]
with open(f"{TMP}/list.txt","w") as f:
    for p in lst: f.write(f"file '{p}'\n")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",f"{TMP}/list.txt","-c","copy",f"{TMP}/all.wav"],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{TMP}/all.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=9","-ar","44100","-ac","1","-c:a","libmp3lame","-b:a","160k",f"{WD}/{OUT}"],check=True)
total = dur(f"{WD}/{OUT}")
json.dump({"cues":cues,"words":cwords,"total":total}, open(f"{TMP}/timing.json","w"), ensure_ascii=False)
print(OUT, "total", round(total,2), "cues", len(cues))
