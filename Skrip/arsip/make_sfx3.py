import numpy as np, json, sys, wave
SR = 44100
timing = json.load(open(sys.argv[1])); out_wav = sys.argv[2]
cues = timing["cues"]; total = timing["total"]
OLDB = [0,5,10,16,22,28,34,37.5,40]
NEWB = [0] + [cues[k][0] for k in (2,4,6,8,10,12,14)] + [total]
def real(o):
    for k in range(1, len(OLDB)):
        if o <= OLDB[k]:
            return NEWB[k-1] + (o-OLDB[k-1])/(OLDB[k]-OLDB[k-1])*(NEWB[k]-NEWB[k-1])
    return total
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
# pergantian adegan
for k, n in enumerate((3, 4, 5, 7, 8, 11, 13, 14)):
    add(whoosh(.5, 300+30*k, 3600, .38, 10+k), q(n)-.2)
# label muncul
for n, f in ((3,.08),(3,.62),(4,.45),(5,.15),(6,.2),(13,.4)): add(pop(.45), ev(n, f))
# colok listrik, tombol power
add(click(.55), ev(3,.32)); add(pop(.3), ev(3,.33))
pt = ev(3,.62); add(click(.6), pt); add(bell(1320, .35, .12, .28), pt+.12)
# kabel USB tersambung
add(whoosh(.35, 400, 1800, .25, 31), ev(4,.25)); add(click(.6), ev(4,.75)); add(bell(1568, .5, .2, .3), ev(4,.77)); add(bell(1760, .5, .2, .22), ev(4,.88))
# gelembung dan DRIVER
add(pop(.5), ev(7,.05)); add(pop(.45), ev(7,.12)); add(bell(1760, .8, .3, .35), ev(7,.45)); add(pop(.4), ev(7,.5))
# mengetik dan tombol Download
for i in range(7): add(tick(.3), ev(8,.45) + i*(ev(8,.8)-ev(8,.45))/6)
add(click(.6), ev(8,.88)); add(bell(1568, .5, .2, .3), ev(8,.9))
# kartu CD dan online
add(pop(.5), ev(9,.12)); add(pop(.5), ev(9,.58))
# pemasangan driver
for i in range(9): add(tick(.22), ev(10,.1) + i*(ev(10,.8)-ev(10,.1))/8)
add(chime(.4), ev(10,.85))
# Ctrl + P
add(click(.6), ev(11,.66)); add(click(.6), ev(11,.8))
# dialog Print
add(pop(.45), q(12)); add(click(.6), ev(12,.78))
# printer mencetak
add(whoosh(1.4, 120, 420, .35, 40), ev(13,.2)); add(whoosh(1.0, 150, 480, .3, 41), ev(13,.55))
add(bell(1568, .8, .3, .32), ev(13,.92)); add(bell(2093, .8, .3, .25), ev(13,.95))
# kartu penutup bermerek
add(whoosh(.6, 250, 3000, .38, 30), total+.1); add(pop(.55), total+.55); add(chime(.5), total+.6)
for d in (1.0, 1.4, 1.85): add(pop(.3), total+d)
pk = np.max(np.abs(buf)); buf = buf/pk*.7
with wave.open(out_wav, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((buf*32767).astype(np.int16).tobytes())
print("sfx ok", round(len(buf)/SR,2))
