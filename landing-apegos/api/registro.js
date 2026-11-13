// Guarda cada registro del formulario como un archivo JSON privado en Vercel Blob.
import { put } from '@vercel/blob';
import { randomUUID } from 'node:crypto';

// Campo -> longitud máxima
const FIELDS = {
  nombre: 120,
  correo: 160,
  telefono: 30,
  ciudad: 80,
  origen: 60,
  expectativa: 600,
  consentimiento: 5,
};

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Método no permitido' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  // Trampa anti-spam: los bots llenan el campo oculto "website".
  if (body.website) return res.status(200).json({ ok: true });

  const data = {};
  for (const [key, max] of Object.entries(FIELDS)) {
    data[key] = String(body[key] ?? '').trim().slice(0, max);
  }

  if (!data.nombre || !EMAIL.test(data.correo) || !data.telefono || data.consentimiento !== 'Sí') {
    return res.status(400).json({ ok: false, error: 'Faltan datos obligatorios.' });
  }

  const now = new Date();
  data.fecha_registro = now.toISOString();

  const stamp = now.toISOString().replace(/[:.]/g, '-');
  const pathname = `registros/${stamp}-${randomUUID().slice(0, 8)}.json`;

  try {
    await put(pathname, JSON.stringify(data), {
      access: 'private',
      contentType: 'application/json',
      addRandomSuffix: false,
    });
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('No se pudo guardar el registro:', err);
    return res.status(500).json({ ok: false, error: 'No se pudo guardar el registro.' });
  }
}
