// Cliente de la API v3 de USPS (https://developers.usps.com).
// - Si hay USPS_CLIENT_ID y USPS_CLIENT_SECRET usa la API real (OAuth 2.0 client_credentials).
// - Si no, responde en "modo demo" con datos simulados para poder probar la maqueta.
'use strict';

const HOSTS = {
  production: 'https://apis.usps.com',
  test: 'https://apis-tem.usps.com',
};

const { UspsError, MAIL_CLASSES, US_STATES, mock } = require('./public/usps-mock.js');

function createUspsClient(env = process.env, fetchImpl = globalThis.fetch) {
  const clientId = env.USPS_CLIENT_ID || '';
  const clientSecret = env.USPS_CLIENT_SECRET || '';
  const environment = env.USPS_ENV === 'production' ? 'production' : 'test';
  const baseUrl = env.USPS_BASE_URL || HOSTS[environment];
  const originZIP = env.SHIP_FROM_ZIP || '33166';
  const live = Boolean(clientId && clientSecret);
  let token = null;
  let tokenExpires = 0;

  async function getToken() {
    if (token && Date.now() < tokenExpires - 60_000) return token;
    const res = await fetchImpl(`${baseUrl}/oauth2/v3/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ grant_type: 'client_credentials', client_id: clientId, client_secret: clientSecret }),
    });
    if (!res.ok) throw new UspsError(`USPS OAuth falló (${res.status})`, 502);
    const data = await res.json();
    token = data.access_token;
    tokenExpires = Date.now() + (Number(data.expires_in) || 3600) * 1000;
    return token;
  }

  async function call(path, { method = 'GET', body } = {}) {
    const headers = { Authorization: `Bearer ${await getToken()}`, Accept: 'application/json' };
    if (body) headers['Content-Type'] = 'application/json';
    const res = await fetchImpl(`${baseUrl}${path}`, { method, headers, body: body ? JSON.stringify(body) : undefined });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      const msg = data?.error?.message || data?.message || `USPS respondió ${res.status}`;
      throw new UspsError(msg, res.status === 404 ? 404 : 502);
    }
    return data;
  }

  // ---------- Direcciones ----------
  async function validateAddress(input) {
    const a = normalizeAddressInput(input);
    if (!live) return mock.validateAddress(a);
    const q = new URLSearchParams({ streetAddress: a.street, state: a.state });
    if (a.secondary) q.set('secondaryAddress', a.secondary);
    if (a.city) q.set('city', a.city);
    if (a.zip) q.set('ZIPCode', a.zip);
    const data = await call(`/addresses/v3/address?${q}`);
    const ad = data.address || {};
    return {
      valid: true,
      address: {
        street: ad.streetAddress || a.street,
        secondary: ad.secondaryAddress || '',
        city: ad.city || a.city,
        state: ad.state || a.state,
        zip: ad.ZIPCode || a.zip,
        zip4: ad.ZIPPlus4 || '',
      },
      corrections: data.corrections || [],
      source: 'usps',
    };
  }

  async function cityState(zip) {
    if (!/^\d{5}$/.test(String(zip))) throw new UspsError('El ZIP debe tener 5 dígitos');
    if (!live) return mock.cityState(zip);
    const data = await call(`/addresses/v3/city-state?ZIPCode=${zip}`);
    return { zip, city: data.city, state: data.state, source: 'usps' };
  }

  // ---------- Tarifas ----------
  async function rates({ destinationZIP, weightOz, length = 10, width = 8, height = 4 }) {
    if (!/^\d{5}$/.test(String(destinationZIP))) throw new UspsError('ZIP de destino inválido');
    const oz = Math.max(1, Number(weightOz) || 1);
    if (!live) return mock.rates(originZIP, destinationZIP, oz);
    const pounds = Math.round((oz / 16) * 100) / 100;
    const mailingDate = new Date().toISOString().slice(0, 10);
    const results = await Promise.all(MAIL_CLASSES.map(async (mc) => {
      try {
        const data = await call('/prices/v3/base-rates/search', {
          method: 'POST',
          body: {
            originZIPCode: originZIP,
            destinationZIPCode: String(destinationZIP),
            weight: pounds,
            length, width, height,
            mailClass: mc.mailClass,
            processingCategory: 'MACHINABLE',
            rateIndicator: 'SP',
            destinationEntryFacilityType: 'NONE',
            priceType: 'RETAIL',
            mailingDate,
          },
        });
        return { ...mc, price: Number(data.totalBasePrice ?? data.rates?.[0]?.price) };
      } catch (err) {
        return { ...mc, price: null, error: err.message };
      }
    }));
    return { origin: originZIP, destination: String(destinationZIP), weightOz: oz, rates: results.filter((r) => r.price != null), source: 'usps' };
  }

  // ---------- Rastreo ----------
  async function track(trackingNumber) {
    const tn = String(trackingNumber || '').replace(/\s+/g, '').toUpperCase();
    if (!/^[A-Z0-9]{10,34}$/.test(tn)) throw new UspsError('Número de rastreo inválido');
    if (!live) return mock.track(tn);
    const data = await call(`/tracking/v3/tracking/${encodeURIComponent(tn)}?expand=DETAIL`);
    return {
      trackingNumber: tn,
      status: data.statusCategory || data.status || 'Desconocido',
      summary: data.statusSummary || '',
      expectedDelivery: data.expectedDeliveryDate || null,
      events: (data.trackingEvents || []).map((e) => ({
        date: e.eventTimestamp,
        description: e.eventType,
        location: [e.eventCity, e.eventState, e.eventZIP].filter(Boolean).join(', '),
      })),
      source: 'usps',
    };
  }

  return {
    live,
    environment,
    status: () => ({ mode: live ? 'live' : 'demo', environment: live ? environment : null, originZIP }),
    validateAddress,
    cityState,
    rates,
    track,
  };
}

function normalizeAddressInput(input = {}) {
  const a = {
    street: String(input.street || '').trim(),
    secondary: String(input.secondary || '').trim(),
    city: String(input.city || '').trim(),
    state: String(input.state || '').trim().toUpperCase(),
    zip: String(input.zip || '').trim().slice(0, 5),
  };
  if (!a.street) throw new UspsError('Falta la dirección');
  if (!US_STATES.has(a.state)) throw new UspsError('Estado inválido (usa la abreviatura de 2 letras, p. ej. FL)');
  if (!a.city && !/^\d{5}$/.test(a.zip)) throw new UspsError('Indica la ciudad o el ZIP');
  return a;
}

module.exports = { createUspsClient, UspsError, MAIL_CLASSES };
