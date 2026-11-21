'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { createUspsClient } = require('../usps');
const { createServer } = require('../server');

test('modo demo cuando no hay credenciales', async () => {
  const usps = createUspsClient({});
  assert.equal(usps.status().mode, 'demo');
  const r = await usps.rates({ destinationZIP: '90001', weightOz: 20 });
  assert.equal(r.rates.length, 3);
  assert.ok(r.rates.every((x) => x.price > 0));
  const a = await usps.validateAddress({ street: '1200 Brickell Ave', city: 'Miami', state: 'fl', zip: '33131' });
  assert.equal(a.address.state, 'FL');
  assert.match(a.address.zip4, /^\d{4}$/);
  await assert.rejects(usps.validateAddress({ street: 'Brickell Ave', city: 'Miami', state: 'FL', zip: '33131' }));
  await assert.rejects(usps.validateAddress({ street: '1 Main St', city: 'Miami', state: 'XX' }));
  const t = await usps.track('9400111200000000000000');
  assert.ok(t.events.length >= 3);
});

test('modo real: OAuth + llamadas a la API v3 con el token', async () => {
  const calls = [];
  const fakeFetch = async (url, opts = {}) => {
    calls.push({ url, opts });
    const json = (body, status = 200) => ({ ok: status < 400, status, json: async () => body });
    if (url.endsWith('/oauth2/v3/token')) return json({ access_token: 'tok123', expires_in: 3600 });
    if (url.includes('/addresses/v3/address')) return json({ address: { streetAddress: '1200 BRICKELL AVE', city: 'MIAMI', state: 'FL', ZIPCode: '33131', ZIPPlus4: '3214' } });
    if (url.includes('/prices/v3/base-rates/search')) {
      const b = JSON.parse(opts.body);
      return json({ totalBasePrice: { USPS_GROUND_ADVANTAGE: 8.1, PRIORITY_MAIL: 11.2, PRIORITY_MAIL_EXPRESS: 40.5 }[b.mailClass] });
    }
    if (url.includes('/tracking/v3/tracking/')) return json({ statusCategory: 'In Transit', trackingEvents: [{ eventType: 'Accepted', eventTimestamp: '2026-11-20T10:00:00Z', eventCity: 'MIAMI', eventState: 'FL' }] });
    return json({}, 404);
  };
  const usps = createUspsClient({ USPS_CLIENT_ID: 'id', USPS_CLIENT_SECRET: 'secret' }, fakeFetch);
  assert.equal(usps.status().mode, 'live');
  const a = await usps.validateAddress({ street: '1200 Brickell Ave', city: 'Miami', state: 'FL' });
  assert.equal(a.address.zip4, '3214');
  const r = await usps.rates({ destinationZIP: '33131', weightOz: 32 });
  assert.deepEqual(r.rates.map((x) => x.price), [8.1, 11.2, 40.5]);
  const rateBody = JSON.parse(calls.find((c) => c.url.includes('base-rates')).opts.body);
  assert.equal(rateBody.weight, 2);
  assert.equal(rateBody.originZIPCode, '33166');
  const t = await usps.track('9400111200000000000000');
  assert.equal(t.events[0].location, 'MIAMI, FL');
  // el token se pide una sola vez y se reutiliza
  assert.equal(calls.filter((c) => c.url.endsWith('/oauth2/v3/token')).length, 1);
  assert.ok(calls.filter((c) => !c.url.endsWith('/token')).every((c) => c.opts.headers.Authorization === 'Bearer tok123'));
  assert.ok(calls[0].url.startsWith('https://apis-tem.usps.com'));
});

test('servidor HTTP: rutas /api/usps y archivos estáticos', async () => {
  const server = createServer(createUspsClient({})).listen(0);
  const base = `http://127.0.0.1:${server.address().port}`;
  try {
    assert.equal((await (await fetch(`${base}/api/usps/status`)).json()).mode, 'demo');
    const rates = await (await fetch(`${base}/api/usps/rates`, { method: 'POST', body: JSON.stringify({ destinationZIP: '10001', weightOz: 12 }) })).json();
    assert.equal(rates.rates.length, 3);
    const bad = await fetch(`${base}/api/usps/rates`, { method: 'POST', body: JSON.stringify({ destinationZIP: 'abc' }) });
    assert.equal(bad.status, 400);
    assert.equal((await fetch(`${base}/api/usps/city-state?zip=33166`)).status, 200);
    assert.equal((await fetch(`${base}/`)).status, 200);
    assert.equal((await fetch(`${base}/../server.js`)).status, 404);
  } finally {
    server.close();
  }
});
