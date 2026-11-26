# Kejadian suara video ini. q(n)=awal kalimat ke-n, ev(n,f)=posisi f (0..1) di kalimat n.
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
