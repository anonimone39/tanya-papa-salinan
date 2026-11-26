import json, re, sys
html_path, timing_path = sys.argv[1], sys.argv[2]
T = json.load(open(timing_path)); cues = T["cues"]; total = round(T["total"], 2)
texts = [
 "Pernah terlintas dalam pikiran, kenapa mouse gak ada kabel, tapi bisa menggerakkan kursor mouse di laptop?",
 "Sini, Papa jelasin!",
 "Coba kita lihat bagian bawahnya.",
 "Ada sensor kecil, isinya lampu LED sama kamera mini.",
 "Kamera itu memotret permukaan meja, ribuan kali dalam satu detik.",
 "Terus dia bandingkan foto yang satu dengan yang berikutnya, buat tau kamu geser ke arah mana.",
 "Selisihnya diubah sama chip di dalam jadi angka.",
 "Geser berapa ke kanan, berapa ke atas.",
 "Angka itu, ditambah klik tombolnya, dikirim lewat gelombang radio.",
 "Frekuensinya 2,4 GHz.",
 "Di colokan USB itu ada penerima kecil.",
 "Dia menangkap sinyalnya, lalu meneruskan ke komputer kamu.",
 "Komputer tinggal menggeser kursor sebesar angka tadi.",
 "Semuanya terjadi dalam hitungan milidetik, lebih cepat dari kedipan matamu.",
 "Nah... sekarang pengetahuanmu sudah bertambah.",
 "Kalau ada yang bikin kamu penasaran, tanya aja sama Papa yaa..",
 "Tinggal komen di bawah, nanti Papa jelaskan di video berikutnya.",
]
assert len(texts) == len(cues)
rows = []
for i, c in enumerate(cues):
    end = cues[i+1][0] if i+1 < len(cues) else total
    rows.append(" [%s,%s,'%s']" % (c[0], end, texts[i]))
h = open(html_path, encoding="utf-8").read()
h = re.sub(r"const CAPS=\[.*?\n\];", "const CAPS=[\n" + ",\n".join(rows) + "\n];", h, flags=re.S)
nb = [0] + [cues[k][0] for k in (2,4,6,8,10,12,14)] + [total]
h = re.sub(r"NEWB=\[[^\]]*\];", "NEWB=" + json.dumps(nb) + ";", h)
TAIL = 4.2
h = re.sub(r"DUR=[0-9.]+(,VEND=[0-9.]+)?;", "DUR=%s,VEND=%s;" % (round(total+TAIL,2), total), h)
h = re.sub(r'max="[0-9.]+" step="0.01"', 'max="%s" step="0.01"' % round(total+TAIL,2), h)
open(html_path, "w", encoding="utf-8").write(h)
print("patched, total", total, "NEWB", nb)
h=open(html_path,encoding="utf-8").read()
h=h.replace("wt=ws.map(w=>w.length+1)","wt=ws.map(w=>w.length+1+(w.includes('...')?9:0))")
open(html_path,"w",encoding="utf-8").write(h)
