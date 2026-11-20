import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
const [cmd, ...rest] = process.argv.slice(2);
const B={browserExecutable:"/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",chromeMode:"headless-shell"};
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const comp = await selectComposition({ serveUrl, id: "Promo", ...B });
if (cmd === "still") {
  for (const s of rest) await renderStill({ ...B, serveUrl, composition: comp, frame: Math.round(+s * 30), output: `out/still_${s}.png` });
} else {
  await renderMedia({ ...B, serveUrl, composition: comp, codec: "h264", crf: 18, audioBitrate: "192k", outputLocation: "out/promo.mp4", concurrency: 4,
    onProgress: ({ progress }) => { if (Math.round(progress * 100) % 10 === 0) process.stdout.write(`${Math.round(progress * 100)}% `); } });
}
