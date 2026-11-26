import { chromium } from '/Users/steven.aprilianto/.claude/skill-packages/stick-figure/kit/node_modules/playwright/index.mjs';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
const [,, mode, outPath, audioPath] = process.argv;
const FPS = 30, DUR = Number(process.env.DUR), N = Math.round(DUR * FPS);
const url = 'file://' + process.argv[1].replace(/render\.mjs$/, 'index.html');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'networkidle' });
await page.addStyleTag({ content: `
  body{padding:0!important;margin:0!important;background:#0f1d2b}
  .wrap{display:block!important;max-width:none!important;margin:0!important}
  .wrap>div:not(.left){display:none!important}
  .left{max-width:none!important}
  .ctl{display:none!important}
  .stage{width:1080px!important;height:1920px!important;border-radius:0!important;border:0!important}` });
await page.evaluate(() => Promise.all([document.fonts.load('900 40px Nunito'),document.fonts.load('800 40px Nunito'),document.fonts.ready]));
const fonts = await page.evaluate(() => ({ nunito: document.fonts.check("900 40px Nunito"), grotesk: document.fonts.check("700 40px 'Space Grotesk'") }));
console.log('fonts', JSON.stringify(fonts));
const stage = page.locator('#stage');
if (mode === 'test') {
  for (const t of (process.env.TIMES||'3,12,40,59').split(',').map(Number)) {
    await page.evaluate(v => window.__seek(v), t);
    await stage.screenshot({ path: `${outPath}-${t}.png` });
  }
  await browser.close(); process.exit(0);
}
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-i', audioPath,
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
await new Promise(r => ff.on('close', r));
await browser.close();
console.log('done');
