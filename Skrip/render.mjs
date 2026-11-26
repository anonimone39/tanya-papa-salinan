// Render halaman animasi menjadi MP4 (1080x1920, 30 fps) atau beberapa frame uji.
// node render.mjs full <halaman.html> <keluaran.mp4> <audio.mp3> <durasi>
// node render.mjs test <halaman.html> <awalan_png> [detik,detik,...]
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const [,, mode, htmlPath, outPath, arg4, arg5] = process.argv;
const FPS = 30;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: 'networkidle' });
await page.addStyleTag({ content: `
  body{padding:0!important;margin:0!important;background:#0f1d2b}
  .wrap{display:block!important;max-width:none!important;margin:0!important}
  .wrap>div:not(.left){display:none!important}
  .left{max-width:none!important}
  .ctl{display:none!important}
  .stage{width:1080px!important;height:1920px!important;border-radius:0!important;border:0!important}` });
await page.evaluate(() => Promise.all([document.fonts.load('900 40px Nunito'), document.fonts.load('800 40px Nunito'), document.fonts.ready]));
const stage = page.locator('#stage');
if (mode === 'test') {
  for (const t of (arg4 || '3,12,30').split(',').map(Number)) {
    await page.evaluate(v => window.__seek(v), t);
    await stage.screenshot({ path: `${outPath}-${t}.png` });
  }
  await browser.close(); process.exit(0);
}
const DUR = Number(arg5), N = Math.round(DUR * FPS);
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', arg4,
  '-vf', 'scale=out_color_matrix=bt709:flags=lanczos,format=yuv420p',
  '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'slow', '-crf', '18', '-maxrate', '12M', '-bufsize', '24M', '-g', '60',
  '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-r', String(FPS),
  '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-t', String(DUR), '-movflags', '+faststart', outPath],
  { stdio: ['pipe', 'inherit', 'inherit'] });
for (let i = 0; i < N; i++) {
  await page.evaluate(v => window.__seek(v), i / FPS);
  const buf = await stage.screenshot({ type: 'png' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % 100 === 0) console.log('frame', i, '/', N);
}
ff.stdin.end();
const code = await new Promise(r => ff.on('close', r));
await browser.close();
if (code !== 0) process.exit(code);
console.log('selesai:', outPath);
