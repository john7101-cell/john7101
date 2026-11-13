// Descarga la lista de asistentes.
//   /api/exportar?key=CLAVE            -> archivo CSV (Excel / Google Sheets)
//   /api/exportar?key=CLAVE&ver=tabla  -> tabla para ver en el navegador
// La CLAVE es la variable de entorno EXPORT_KEY del proyecto en Vercel.
import { list, get } from '@vercel/blob';
import { timingSafeEqual } from 'node:crypto';

const COLUMNS = [
  ['fecha_registro', 'Fecha de registro'],
  ['nombre', 'Nombre'],
  ['correo', 'Correo'],
  ['telefono', 'Teléfono'],
  ['ciudad', 'Ciudad'],
  ['origen', '¿Cómo se enteró?'],
  ['expectativa', 'Qué quiere trabajar'],
  ['consentimiento', 'Consentimiento'],
];

const TIME_ZONE = 'America/Bogota';

function authorized(key) {
  const expected = process.env.EXPORT_KEY || '';
  const given = String(key || '');
  if (!expected || given.length !== expected.length) return false;
  return timingSafeEqual(Buffer.from(given), Buffer.from(expected));
}

function formatDate(iso) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso || '';
  return d.toLocaleString('es-CO', { timeZone: TIME_ZONE, dateStyle: 'short', timeStyle: 'short' });
}

// Evita que Excel interprete un valor como fórmula y escapa comillas.
function csvCell(value) {
  let s = String(value ?? '');
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return '"' + s.replace(/"/g, '""') + '"';
}

function htmlEscape(value) {
  return String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

async function loadRows() {
  const blobs = [];
  let cursor;
  do {
    const page = await list({ prefix: 'registros/', cursor, limit: 1000 });
    blobs.push(...page.blobs);
    cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor);

  blobs.sort((a, b) => a.pathname.localeCompare(b.pathname));

  const rows = await Promise.all(blobs.map(async (b) => {
    try {
      const result = await get(b.pathname, { access: 'private' });
      if (!result) return null;
      return JSON.parse(await new Response(result.stream).text());
    } catch (err) {
      console.error('No se pudo leer', b.pathname, err);
      return null;
    }
  }));
  return rows.filter(Boolean);
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('X-Robots-Tag', 'noindex');

  if (!authorized(req.query.key)) {
    return res.status(401).send('No autorizado');
  }

  let rows;
  try {
    rows = await loadRows();
  } catch (err) {
    console.error('Error al listar registros:', err);
    return res.status(500).send('No se pudieron leer los registros.');
  }

  const values = rows.map(r => COLUMNS.map(([k]) => (k === 'fecha_registro' ? formatDate(r[k]) : r[k] ?? '')));

  if (req.query.ver === 'tabla') {
    const head = COLUMNS.map(([, label]) => `<th>${htmlEscape(label)}</th>`).join('');
    const body = values.map(v => `<tr>${v.map(c => `<td>${htmlEscape(c)}</td>`).join('')}</tr>`).join('');
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.status(200).send(`<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Asistentes · Volver a mí</title>
<style>body{font-family:system-ui,Arial,sans-serif;margin:24px;color:#2B1A22;background:#F6EFEC}
h1{font-size:1.4rem}table{border-collapse:collapse;width:100%;background:#fff;font-size:.9rem}
th,td{border:1px solid #D9C3CA;padding:8px;text-align:left;vertical-align:top}th{background:#B5566B;color:#F6EFEC}
.wrap{overflow-x:auto}a{color:#8E3A50}</style></head><body>
<h1>Asistentes registrados: ${values.length}</h1>
<p><a href="?key=${encodeURIComponent(req.query.key)}">Descargar CSV</a></p>
<div class="wrap"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div></body></html>`);
  }

  const csv = '﻿' + [COLUMNS.map(([, label]) => csvCell(label)).join(','), ...values.map(v => v.map(csvCell).join(','))].join('\r\n');
  const today = new Date().toISOString().slice(0, 10);
  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', `attachment; filename="asistentes-apegos-${today}.csv"`);
  return res.status(200).send(csv);
}
