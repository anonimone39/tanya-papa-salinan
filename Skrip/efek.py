"""Pembuat efek suara sintetis. Pakai: python efek.py <folder_video/efek.py> <timing.json> <keluaran.wav>"""
import numpy as np, json, sys, wave
SR = 44100
kejadian_file, timing_file, out_wav = sys.argv[1:4]
timing = json.load(open(timing_file)); cues = timing["cues"]; total = timing["total"]
def whoosh(dur=.6, f0=300, f1=3800, gain=.5, seed=1):
    n = int(dur*SR); x = np.random.default_rng(seed).standard_normal(n)
    y = np.zeros(n); lp = bp = 0.0; q = .35
    for i in range(n):
        f = f0*(f1/f0)**(i/n); F = 2*np.sin(np.pi*f/SR)
        hp = x[i]-lp-q*bp; bp += F*hp; lp += F*bp; y[i] = bp
    y *= np.sin(np.pi*np.linspace(0,1,n))**1.6
    return y/(np.max(np.abs(y))+1e-9)*gain
def click(gain=.6):
    n = int(.05*SR); t = np.arange(n)/SR; r = np.random.default_rng(2).standard_normal(n)
    return (r*np.exp(-t/.004)*.5 + np.sin(2*np.pi*2200*t)*np.exp(-t/.012)*.5)*gain
def tick(gain=.25):
    n = int(.03*SR); t = np.arange(n)/SR
    return np.sin(2*np.pi*3200*t)*np.exp(-t/.006)*gain
def pop(gain=.5):
    n = int(.14*SR); t = np.arange(n)/SR; f = 250+450*np.exp(-t/.03)
    return np.sin(np.cumsum(2*np.pi*f/SR))*np.exp(-t/.05)*gain
def bell(freq, dur=.9, decay=.3, gain=.4):
    n = int(dur*SR); t = np.arange(n)/SR
    y = np.sin(2*np.pi*freq*t)+.4*np.sin(2*np.pi*freq*2.01*t)*np.exp(-t/.1)+.15*np.sin(2*np.pi*freq*3*t)*np.exp(-t/.05)
    return y*np.exp(-t/decay)*np.minimum(1, t/.004)*gain
def chime(gain=.45):
    y = np.zeros(int(1.6*SR))
    for k, f in enumerate([659.25, 783.99, 1046.5]):
        b = bell(f, 1.2, .4, gain); i = int(k*.09*SR); y[i:i+len(b)] += b[:len(y)-i]
    return y
TAIL = 4.2
buf = np.zeros(int((total+TAIL+1.0)*SR))
def add(snd, t):
    i = max(0, int(t*SR)); m = min(len(snd), len(buf)-i)
    if m > 0: buf[i:i+m] += snd[:m]
q = lambda n: cues[n-1][0]
qe = lambda n: cues[n][0] if n < len(cues) else total
ev = lambda n, f: q(n) + f*(qe(n)-q(n))
exec(open(kejadian_file, encoding="utf-8").read())
pk = np.max(np.abs(buf)); buf = buf/pk*.7
with wave.open(out_wav, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((buf*32767).astype(np.int16).tobytes())
print("sfx ok", round(len(buf)/SR,2))
