import json, os, re, runpy, sys
video_dir, timing_path, out_path, audio = sys.argv[1:5]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tpl_path = os.path.join(video_dir, "template.html")
full_svg = os.path.join(ROOT, "Brand", "logo-tanya-papa.svg"); face_svg = os.path.join(ROOT, "Brand", "logo-wajah-tanya-papa.svg")
TAIL = 4.2
T = json.load(open(timing_path)); cues = T["cues"]; total = round(T["total"], 2)
texts = runpy.run_path(os.path.join(video_dir, "naskah.py"))["CAPTIONS"]
assert len(texts) == len(cues), (len(texts), len(cues))
rows = []
for i, c in enumerate(cues):
    end = cues[i+1][0] if i+1 < len(cues) else total
    ws = T.get("words", [[]]*len(cues))[i]
    wl = [w[1] for w in ws] if len(ws) == len(texts[i].split(" ")) else []
    rows.append(" [%s,%s,'%s',%s]" % (c[0], end, texts[i], json.dumps(wl)))
def symbol(path, pre, sid):
    s = open(path, encoding="utf-8").read()
    inner = s[s.index(">", s.index("<svg")) + 1 : s.rindex("</svg>")]
    inner = re.sub(r'id="(bg|c|skin|shirt|arm|hair|dad)"', lambda m: 'id="%s_%s"' % (pre, m.group(1)), inner)
    inner = re.sub(r'url\(#(bg|c|skin|shirt|arm|hair)\)', lambda m: 'url(#%s_%s)' % (pre, m.group(1)), inner)
    return '<symbol id="%s" viewBox="0 0 1024 1024" overflow="hidden">%s</symbol>' % (sid, inner)
defs = symbol(full_svg, "lf", "logoF") + symbol(face_svg, "lw", "logoW") + \
 '<linearGradient id="endbg" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="#1D4ED8"/><stop offset="1" stop-color="#14307A"/></linearGradient>' + \
 '<clipPath id="clipAv"><circle cx="0" cy="0" r="165"/></clipPath><clipPath id="clipW"><circle cx="54" cy="62" r="32"/></clipPath>'
BRAND = r'''
const eob=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const FN="font-family:Nunito,'Arial Rounded MT Bold','Avenir Next Rounded',sans-serif;stroke:none;";
/* Logo pojok (setiap video) dan kartu penutup bermerek. rt = waktu sebenarnya. */
function brand(rt){
  let s='';
  const u=rt-VEND,ea=ss((u-.1)/.9),wa=(1-ea)*.95;
  if(wa>.02)s+=`<g opacity="${wa.toFixed(2)}"><circle cx="54" cy="62" r="35" fill="rgba(255,255,255,.92)"/><g clip-path="url(#clipW)"><use href="#logoW" x="22" y="30" width="64" height="64"/></g></g>`;
  if(ea>.01){
    s+=`<g opacity="${ea.toFixed(2)}"><rect width="540" height="960" fill="url(#endbg)"/>`;
    s+=`<circle cx="470" cy="120" r="200" fill="#fff" fill-opacity=".06"/><circle cx="60" cy="890" r="170" fill="#fff" fill-opacity=".05"/>`;
    s+=`<circle cx="70" cy="110" r="10" fill="#FFD23F"/><circle cx="470" cy="760" r="8" fill="#FF7A59"/><circle cx="500" cy="480" r="9" fill="#FFD23F"/>`;
    const ap=eob((u-.45)/.85);
    s+=`<g transform="translate(270 ${(330+(1-ap)*70).toFixed(1)}) scale(${Math.max(.001,ap).toFixed(3)})" opacity="${cl(ap*1.5).toFixed(2)}"><circle r="178" fill="rgba(255,255,255,.12)"/><g clip-path="url(#clipAv)"><use href="#logoF" x="-165" y="-165" width="330" height="330"/></g></g>`;
    const t1=eob((u-.95)/.7);
    s+=`<g opacity="${cl(t1*1.5).toFixed(2)}" transform="translate(0 ${((1-t1)*40).toFixed(1)})"><text x="270" y="640" text-anchor="middle" style="${FN}font-weight:900;font-size:88px;fill:#fff;letter-spacing:-1px">Tanya <tspan style="fill:#FFD23F">Papa</tspan></text><rect x="58" y="662" width="92" height="9" rx="4.5" fill="#FF7A59"/></g>`;
    const t2=eob((u-1.3)/.7);
    s+=`<g opacity="${cl(t2*1.5).toFixed(2)}" transform="translate(0 ${((1-t2)*30).toFixed(1)})"><text x="270" y="738" text-anchor="middle" style="${FN}font-weight:800;font-size:42px;fill:#DBEAFE">Sini Papa jelasin!</text></g>`;
    const t3=eob((u-1.8)/.7);
    s+=`<g opacity="${cl(t3*1.5).toFixed(2)}" transform="translate(0 ${((1-t3)*24).toFixed(1)})"><rect x="60" y="790" width="420" height="58" rx="29" fill="#FFD23F"/><text x="270" y="827" text-anchor="middle" style="${FN}font-weight:900;font-size:22px;fill:#14307A">Tulis pertanyaanmu di komentar</text></g>`;
    s+=`</g>`;
  }
  return s;
}
'''
h = open(tpl_path, encoding="utf-8").read()
for k, v in {"@@DEFS@@": defs, "@@CAPS@@": ",\n".join(rows), "@@BRAND@@": BRAND, "@@AUDIO@@": audio}.items():
    h = h.replace(k, v)
h = h.replace("@@VEND@@", str(total)).replace("@@DUR@@", str(round(total + TAIL, 2)))
open(out_path, "w", encoding="utf-8").write(h)
print("built", out_path, "total", total, "DUR", round(total + TAIL, 2))
