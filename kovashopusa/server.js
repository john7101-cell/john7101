// Servidor de la maqueta KovaShopUSA: sirve la tienda (public/) y expone /api/usps/*.
// Sin dependencias: node server.js  →  http://localhost:3000
'use strict';

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { createUspsClient, UspsError } = require('./usps');

loadDotEnv(path.join(__dirname, '.env'));

const PUBLIC_DIR = path.join(__dirname, 'public');
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.ico': 'image/x-icon', '.json': 'application/json' };

function loadDotEnv(file) {
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && process.env[m[1]] === undefined) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
  }
}

function send(res, status, data) {
  res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(data));
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.on('data', (c) => { raw += c; if (raw.length > 1e5) req.destroy(); });
    req.on('end', () => { try { resolve(raw ? JSON.parse(raw) : {}); } catch { reject(new UspsError('JSON inválido')); } });
    req.on('error', reject);
  });
}

function createServer(usps = createUspsClient()) {
  return http.createServer(async (req, res) => {
    const url = new URL(req.url, 'http://localhost');
    try {
      if (url.pathname.startsWith('/api/usps/')) {
        const route = url.pathname.slice('/api/usps/'.length);
        if (req.method === 'GET' && route === 'status') return send(res, 200, usps.status());
        if (req.method === 'POST' && route === 'address') return send(res, 200, await usps.validateAddress(await readJson(req)));
        if (req.method === 'GET' && route === 'city-state') return send(res, 200, await usps.cityState(url.searchParams.get('zip')));
        if (req.method === 'POST' && route === 'rates') return send(res, 200, await usps.rates(await readJson(req)));
        if (req.method === 'GET' && route.startsWith('track/')) return send(res, 200, await usps.track(decodeURIComponent(route.slice(6))));
        return send(res, 404, { error: 'Ruta no encontrada' });
      }
      // Archivos estáticos
      const rel = url.pathname === '/' ? 'index.html' : decodeURIComponent(url.pathname).replace(/^\/+/, '');
      const file = path.normalize(path.join(PUBLIC_DIR, rel));
      if (!file.startsWith(PUBLIC_DIR + path.sep) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404); return res.end('Not found');
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    } catch (err) {
      const status = err instanceof UspsError ? err.status : 500;
      if (status === 500) console.error(err);
      send(res, status, { error: status === 500 ? 'Error interno' : err.message });
    }
  });
}

if (require.main === module) {
  const usps = createUspsClient();
  const port = Number(process.env.PORT) || 3000;
  createServer(usps).listen(port, () => {
    const s = usps.status();
    console.log(`KovaShopUSA → http://localhost:${port}`);
    console.log(s.mode === 'live' ? `USPS: API real (${s.environment}), origen ZIP ${s.originZIP}` : 'USPS: modo demo (configura USPS_CLIENT_ID y USPS_CLIENT_SECRET en .env para la API real)');
  });
}

module.exports = { createServer };
