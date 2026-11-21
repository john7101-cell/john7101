// Datos simulados de USPS (modo demo). Lo usan el servidor (Node) y el navegador
// cuando no hay credenciales o no hay servidor, para que la maqueta funcione sola.
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.UspsMock = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

// Clases de envío que ofrece la tienda (nombres oficiales de la API de precios v3).
  const MAIL_CLASSES = [
    { mailClass: 'USPS_GROUND_ADVANTAGE', name: 'USPS Ground Advantage™', days: '2–5' },
    { mailClass: 'PRIORITY_MAIL', name: 'Priority Mail®', days: '1–3' },
    { mailClass: 'PRIORITY_MAIL_EXPRESS', name: 'Priority Mail Express®', days: '1–2' },
  ];
  
  const US_STATES = new Set('AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA PR RI SC SD TN TX UT VT VA WA WV WI WY'.split(' '));
  
  class UspsError extends Error {
    constructor(message, status = 400) {
      super(message);
      this.status = status;
    }
  }

  // ================= Modo demo =================
  // Pequeña tabla de prefijos ZIP para que la demo devuelva ciudades creíbles.
  const ZIP3 = {
    '100': ['NEW YORK', 'NY'], '112': ['BROOKLYN', 'NY'], '191': ['PHILADELPHIA', 'PA'], '200': ['WASHINGTON', 'DC'],
    '303': ['ATLANTA', 'GA'], '327': ['ORLANDO', 'FL'], '331': ['MIAMI', 'FL'], '332': ['MIAMI', 'FL'], '336': ['TAMPA', 'FL'],
    '606': ['CHICAGO', 'IL'], '770': ['HOUSTON', 'TX'], '752': ['DALLAS', 'TX'], '782': ['SAN ANTONIO', 'TX'],
    '850': ['PHOENIX', 'AZ'], '891': ['LAS VEGAS', 'NV'], '900': ['LOS ANGELES', 'CA'], '921': ['SAN DIEGO', 'CA'],
    '941': ['SAN FRANCISCO', 'CA'], '981': ['SEATTLE', 'WA'], '802': ['DENVER', 'CO'], '021': ['BOSTON', 'MA'],
  };
  
  function mockCityState(zip) {
    const hit = ZIP3[String(zip).slice(0, 3)];
    if (!hit) throw new UspsError('ZIP no encontrado (modo demo: prueba 33166, 10001, 90001, 77001…)', 404);
    return { zip: String(zip), city: hit[0], state: hit[1], source: 'demo' };
  }
  
  function hash(str) {
    let h = 2166136261;
    for (const c of String(str)) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
    return h >>> 0;
  }
  
  function mockValidateAddress(a) {
    let { city, state, zip } = a;
    if (/^\d{5}$/.test(zip)) {
      const hit = ZIP3[zip.slice(0, 3)];
      if (hit) { city = city || hit[0]; if (hit[1] !== state) throw new UspsError(`El ZIP ${zip} no corresponde a ${state} (corresponde a ${hit[1]})`); }
    } else {
      zip = String(10000 + (hash(city + state) % 89999)).padStart(5, '0');
    }
    if (!/\d/.test(a.street)) throw new UspsError('USPS no encontró la dirección: falta el número de la calle', 404);
    return {
      valid: true,
      address: {
        street: a.street.toUpperCase(),
        secondary: a.secondary.toUpperCase(),
        city: city.toUpperCase(),
        state,
        zip,
        zip4: String(hash(a.street) % 9999).padStart(4, '0'),
      },
      corrections: [],
      source: 'demo',
    };
  }
  
  // Aproxima la "zona" USPS con la distancia entre prefijos ZIP (1 a 8).
  function mockZone(from, to) {
    const d = Math.abs(Number(String(from).slice(0, 3)) - Number(String(to).slice(0, 3)));
    return Math.min(8, Math.max(1, Math.ceil(d / 120)));
  }
  
  function mockRates(origin, dest, oz) {
    const zone = mockZone(origin, dest);
    const lb = Math.ceil(oz / 16);
    const base = {
      USPS_GROUND_ADVANTAGE: oz <= 15.99 ? 5.4 + zone * 0.35 + oz * 0.08 : 7.9 + zone * 0.9 + lb * 1.1,
      PRIORITY_MAIL: 9.85 + zone * 0.95 + lb * 1.35,
      PRIORITY_MAIL_EXPRESS: 30.45 + zone * 2.1 + lb * 2.6,
    };
    return {
      origin, destination: String(dest), weightOz: oz, zone,
      rates: MAIL_CLASSES.map((mc) => ({ ...mc, price: Math.round(base[mc.mailClass] * 100) / 100 })),
      source: 'demo',
    };
  }
  
  function mockTrack(tn, since) {
    const h = hash(tn);
    const steps = [
      ['Shipping Label Created, USPS Awaiting Item', 'MIAMI, FL, 33166'],
      ['Accepted at USPS Origin Facility', 'MIAMI, FL, 33152'],
      ['Departed USPS Regional Facility', 'MIAMI FL DISTRIBUTION CENTER'],
      ['In Transit to Next Facility', ''],
      ['Arrived at Post Office', 'DESTINATION'],
      ['Out for Delivery', 'DESTINATION'],
      ['Delivered, In/At Mailbox', 'DESTINATION'],
    ];
    const now = Date.now();
    // Con `since` (fecha del pedido) el paquete avanza un paso cada 12 h; si no, el avance depende del número.
    const start = since ? new Date(since).getTime() : null;
    const progress = start ? Math.min(6, Math.max(0, Math.floor((now - start) / (12 * 3600_000)))) : 2 + (h % 5);
    const events = steps.slice(0, progress + 1).map(([description, location], i) => ({
      date: new Date(start ? start + i * 12 * 3600_000 : now - (progress - i) * 14 * 3600_000).toISOString(),
      description,
      location,
    })).reverse();
    const delivered = progress === 6;
    return {
      trackingNumber: tn,
      status: delivered ? 'Delivered' : progress >= 5 ? 'Out for Delivery' : progress === 0 ? 'Label Created' : 'In Transit',
      summary: events[0].description,
      expectedDelivery: delivered ? null : new Date(now + (6 - progress) * 24 * 3600_000).toISOString().slice(0, 10),
      events,
      source: 'demo',
    };
  }

  return {
    UspsError,
    MAIL_CLASSES,
    US_STATES,
    mockZone,
    mock: { validateAddress: mockValidateAddress, cityState: mockCityState, rates: mockRates, track: mockTrack },
  };
});
