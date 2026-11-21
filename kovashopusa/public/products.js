// Catálogo de prueba: marcas latinoamericanas ficticias.
// weightOz = peso de envío (con empaque) que se usa para cotizar con USPS.
window.CATEGORIES = [
  { id: 'skincare', en: 'Skincare & Cosmetics', es: 'Skincare & Cosméticos', icon: 'drop' },
  { id: 'supplements', en: 'Supplements', es: 'Suplementos', icon: 'leaf' },
  { id: 'food', en: 'Snacks & Food', es: 'Snacks & Alimentos', icon: 'cup' },
  { id: 'pet', en: 'Pet Care', es: 'Pet Care', icon: 'paw' },
  { id: 'apparel', en: 'Apparel & Accessories', es: 'Ropa & Accesorios', icon: 'shirt' },
];

window.PRODUCTS = [
  { id: 'cafe-huila', name: 'Huila Highlands Coffee', brand: 'Café Altamira', country: 'Colombia', flag: '🇨🇴', category: 'food', price: 18.99, weightOz: 14, rating: 4.9, reviews: 412, badge: 'bestseller', shape: 'bag', color: '#C9A77C', label: 'COLOMBIAN\nCOFFEE',
    en: 'Single-origin washed arabica from small farms in Huila. Notes of panela, orange and cocoa. Whole bean, 12 oz.',
    es: 'Arábica lavado de origen único, de pequeñas fincas del Huila. Notas de panela, naranja y cacao. Grano entero, 12 oz.' },
  { id: 'serum-sacha', name: 'Botanical Skin Serum', brand: 'Selva Botánica', country: 'Peru', flag: '🇵🇪', category: 'skincare', price: 32.0, weightOz: 6, rating: 4.8, reviews: 236, badge: 'curated', shape: 'dropper', color: '#7A4A2A', label: 'BOTANICAL\nSERUM',
    en: 'Lightweight facial serum with Amazonian sacha inchi oil and camu camu vitamin C. 1 fl oz.',
    es: 'Sérum facial ligero con aceite amazónico de sacha inchi y vitamina C de camu camu. 1 fl oz.' },
  { id: 'crema-cacao', name: 'Natural Moisturizer', brand: 'Tierra Maya', country: 'Mexico', flag: '🇲🇽', category: 'skincare', price: 24.0, weightOz: 9, rating: 4.7, reviews: 158, badge: null, shape: 'jar', color: '#F1E7D6', label: 'NATURAL\nMOISTURIZER',
    en: 'Whipped body and face cream with aloe vera and raw cacao butter. Fragrance-free. 2 oz.',
    es: 'Crema batida para cuerpo y rostro con aloe vera y manteca de cacao. Sin fragancia. 2 oz.' },
  { id: 'jabon-romero', name: 'Rosemary Shampoo Bar', brand: 'Raíz Pura', country: 'Colombia', flag: '🇨🇴', category: 'skincare', price: 13.5, weightOz: 5, rating: 4.6, reviews: 97, badge: 'new', shape: 'box', color: '#4E7D5B', label: 'SHAMPOO\nBAR',
    en: 'Zero-waste solid shampoo with rosemary and coffee extract. About 60 washes.',
    es: 'Shampoo sólido cero residuos con romero y extracto de café. Unos 60 lavados.' },
  { id: 'maca', name: 'Andean Maca Powder', brand: 'Inti Wasi', country: 'Peru', flag: '🇵🇪', category: 'supplements', price: 26.0, weightOz: 18, rating: 4.8, reviews: 301, badge: 'bestseller', shape: 'tub', color: '#E9DFC9', label: 'MACA\nANDINA',
    en: 'Gelatinized organic maca grown above 13,000 ft in Junín. 8.8 oz, 50 servings.',
    es: 'Maca orgánica gelatinizada cultivada a más de 4.000 m en Junín. 250 g, 50 porciones.' },
  { id: 'moringa', name: 'Moringa Leaf Capsules', brand: 'Verde Vivo', country: 'Honduras', flag: '🇭🇳', category: 'supplements', price: 22.0, weightOz: 7, rating: 4.5, reviews: 88, badge: null, shape: 'bottle', color: '#FFFFFF', label: 'MORINGA',
    en: 'Shade-dried moringa leaf, 500 mg per capsule. 90 vegan capsules.',
    es: 'Hoja de moringa secada a la sombra, 500 mg por cápsula. 90 cápsulas veganas.' },
  { id: 'yerba', name: 'Organic Yerba Mate', brand: 'Campo Guaraní', country: 'Argentina', flag: '🇦🇷', category: 'food', price: 12.0, weightOz: 19, rating: 4.7, reviews: 143, badge: null, shape: 'bag', color: '#5E8C4A', label: 'YERBA\nMATE',
    en: 'Traditional cut, aged 24 months. Smooth, earthy and energizing. 1.1 lb.',
    es: 'Corte tradicional, estacionada 24 meses. Suave, terrosa y energizante. 500 g.' },
  { id: 'chifles', name: 'Plantain Chips — Sea Salt', brand: 'Costa Dorada', country: 'Ecuador', flag: '🇪🇨', category: 'food', price: 5.99, weightOz: 6, rating: 4.6, reviews: 520, badge: null, shape: 'pouch', color: '#E3B23C', label: 'CHIFLES',
    en: 'Thin-sliced green plantain chips cooked in coconut oil. 5 oz.',
    es: 'Chifles de plátano verde en láminas finas, fritos en aceite de coco. 140 g.' },
  { id: 'chocolate', name: '70% Arriba Cacao Bar', brand: 'Nacional', country: 'Ecuador', flag: '🇪🇨', category: 'food', price: 7.5, weightOz: 4, rating: 4.9, reviews: 211, badge: 'curated', shape: 'bar', color: '#5A3220', label: 'CACAO 70%',
    en: 'Bean-to-bar dark chocolate from fine-flavor Arriba Nacional cacao. 2.5 oz.',
    es: 'Chocolate oscuro bean-to-bar de cacao fino de aroma Arriba Nacional. 70 g.' },
  { id: 'dulce-leche', name: 'Artisan Dulce de Leche', brand: 'La Estancia', country: 'Argentina', flag: '🇦🇷', category: 'food', price: 11.5, weightOz: 20, rating: 4.8, reviews: 176, badge: null, shape: 'jar', color: '#B5793B', label: 'DULCE\nDE LECHE',
    en: 'Slow-cooked in copper pots with whole milk and vanilla. 15.8 oz glass jar.',
    es: 'Cocido lentamente en pailas de cobre con leche entera y vainilla. Frasco de 450 g.' },
  { id: 'dog-treats', name: 'Sweet Potato Dog Treats', brand: 'Patitas', country: 'Chile', flag: '🇨🇱', category: 'pet', price: 14.0, weightOz: 10, rating: 4.7, reviews: 129, badge: 'new', shape: 'pouch', color: '#D9774B', label: 'DOG\nTREATS',
    en: 'Single-ingredient dehydrated sweet potato chews. Grain-free. 6 oz.',
    es: 'Snacks de camote deshidratado de un solo ingrediente. Sin granos. 170 g.' },
  { id: 'pet-hammock', name: 'Hand-woven Cat Hammock', brand: 'Telar Vivo', country: 'Guatemala', flag: '🇬🇹', category: 'pet', price: 29.0, weightOz: 22, rating: 4.6, reviews: 64, badge: null, shape: 'box', color: '#C0392B', label: 'CAT\nHAMMOCK',
    en: 'Cotton hammock woven on backstrap looms by artisans in Sololá. Fits most radiators and chairs.',
    es: 'Hamaca de algodón tejida en telar de cintura por artesanas de Sololá. Para sillas y radiadores.' },
  { id: 'alpaca-beanie', name: 'Baby Alpaca Beanie', brand: 'Andes Knit', country: 'Peru', flag: '🇵🇪', category: 'apparel', price: 45.0, weightOz: 6, rating: 4.9, reviews: 92, badge: 'curated', shape: 'beanie', color: '#8A8F98', label: '',
    en: 'Ultra-soft baby alpaca knit, hand-finished in Cusco. One size.',
    es: 'Tejido de baby alpaca ultrasuave, terminado a mano en Cusco. Talla única.' },
  { id: 'guayabera', name: 'Linen Guayabera Shirt', brand: 'Mérida Linen Co.', country: 'Mexico', flag: '🇲🇽', category: 'apparel', price: 68.0, weightOz: 12, rating: 4.7, reviews: 77, badge: null, shape: 'shirt', color: '#F5F0E6', label: '',
    en: 'Classic four-pocket guayabera in breathable 100% linen. Sizes S–XXL.',
    es: 'Guayabera clásica de cuatro bolsillos en 100% lino transpirable. Tallas S–XXL.' },
  { id: 'tote', name: 'Wayuu Mochila Bag', brand: 'Kanas', country: 'Colombia', flag: '🇨🇴', category: 'apparel', price: 59.0, weightOz: 16, rating: 4.8, reviews: 58, badge: 'new', shape: 'mochila', color: '#1F7A8C', label: '',
    en: 'Crocheted by Wayuu artisans in La Guajira. Each pattern is unique; takes up to 20 days to make.',
    es: 'Tejida a crochet por artesanas wayuu de La Guajira. Cada diseño es único; toma hasta 20 días.' },
];

// Ilustración SVG por tipo de empaque (estilo minimalista de la marca).
window.productArt = function productArt(p) {
  const c = p.color;
  const lines = (p.label || '').split('\n');
  const text = (x, y, size, fill) => lines.map((l, i) =>
    `<text x="${x}" y="${y + i * (size + 3)}" font-family="Poppins,sans-serif" font-size="${size}" font-weight="600" fill="${fill}" text-anchor="middle" letter-spacing="1">${l}</text>`).join('');
  const dark = isDark(c);
  const ink = dark ? '#F5F5F5' : '#0D1B3D';
  const shapes = {
    bag: `<path d="M62 52 L138 52 L146 182 Q100 190 54 182 Z" fill="${c}"/><path d="M62 52 L70 40 L130 40 L138 52 Z" fill="${shade(c, -18)}"/><rect x="68" y="98" width="64" height="48" rx="4" fill="#fff" opacity=".9"/>${text(100, 116, 8, '#0D1B3D')}<circle cx="100" cy="74" r="7" fill="none" stroke="${ink}" stroke-width="1.5"/>`,
    dropper: `<rect x="86" y="30" width="28" height="30" rx="5" fill="#1b1b1b"/><rect x="92" y="18" width="16" height="16" rx="7" fill="#2a2a2a"/><rect x="70" y="58" width="60" height="122" rx="14" fill="${c}"/><rect x="76" y="96" width="48" height="52" rx="3" fill="#F3EBDD"/>${text(100, 116, 7, '#0D1B3D')}`,
    jar: `<rect x="58" y="64" width="84" height="20" rx="5" fill="${shade(c, -25)}"/><rect x="54" y="82" width="92" height="96" rx="14" fill="${c}" stroke="${shade(c, -12)}"/><rect x="62" y="108" width="76" height="44" rx="3" fill="#fff" opacity=".92"/>${text(100, 126, 7.5, '#0D1B3D')}`,
    box: `<path d="M52 78 L100 58 L148 78 L148 160 L100 182 L52 160 Z" fill="${c}"/><path d="M100 98 L148 78 L148 160 L100 182 Z" fill="${shade(c, -16)}"/><path d="M52 78 L100 58 L148 78 L100 98 Z" fill="${shade(c, 14)}"/>${text(76, 126, 7, ink)}`,
    tub: `<rect x="60" y="56" width="80" height="18" rx="4" fill="#0D1B3D"/><path d="M62 74 L138 74 L134 180 L66 180 Z" fill="${c}"/><rect x="66" y="104" width="68" height="46" fill="#15803D"/>${text(100, 124, 8, '#fff')}`,
    bottle: `<rect x="80" y="40" width="40" height="22" rx="4" fill="#15803D"/><path d="M72 66 Q72 60 80 60 L120 60 Q128 60 128 66 L128 178 Q128 184 120 184 L80 184 Q72 184 72 178 Z" fill="${c}" stroke="#ddd"/><rect x="72" y="100" width="56" height="50" fill="#15803D"/>${text(100, 129, 8, '#fff')}`,
    pouch: `<path d="M60 48 L140 48 L144 70 L148 176 Q100 186 52 176 L56 70 Z" fill="${c}"/><rect x="60" y="48" width="80" height="10" fill="${shade(c, -20)}"/><circle cx="100" cy="104" r="26" fill="#fff" opacity=".9"/>${text(100, 102, 7, '#0D1B3D')}`,
    bar: `<rect x="40" y="76" width="120" height="70" rx="4" fill="${c}" transform="rotate(-8 100 110)"/><rect x="84" y="76" width="40" height="70" fill="#D4AF37" transform="rotate(-8 100 110)"/><text x="104" y="114" font-family="Poppins,sans-serif" font-size="8" font-weight="700" fill="#0D1B3D" text-anchor="middle" transform="rotate(-98 104 112)">${lines[0]}</text>`,
    beanie: `<path d="M50 150 Q50 70 100 66 Q150 70 150 150 Z" fill="${c}"/><rect x="46" y="144" width="108" height="28" rx="8" fill="${shade(c, -14)}"/>${[0, 1, 2, 3, 4, 5, 6].map((i) => `<line x1="${58 + i * 14}" y1="146" x2="${58 + i * 14}" y2="170" stroke="${shade(c, -26)}" stroke-width="2"/>`).join('')}<circle cx="100" cy="60" r="12" fill="${shade(c, 10)}"/>`,
    shirt: `<path d="M70 50 L100 60 L130 50 L160 72 L148 96 L134 88 L134 180 L66 180 L66 88 L52 96 L40 72 Z" fill="${c}" stroke="#d9d2c3"/><path d="M90 54 L100 72 L110 54" fill="none" stroke="#cfc6b3" stroke-width="2"/>${[86, 104, 122, 140, 158].map((y) => `<circle cx="100" cy="${y}" r="2" fill="#bfb49c"/>`).join('')}<line x1="80" y1="96" x2="80" y2="176" stroke="#e1d9c8" stroke-width="2"/><line x1="120" y1="96" x2="120" y2="176" stroke="#e1d9c8" stroke-width="2"/>`,
    mochila: `<path d="M74 70 Q100 20 126 70" fill="none" stroke="${shade(c, -20)}" stroke-width="6"/><path d="M60 76 L140 76 L146 176 Q100 186 54 176 Z" fill="${c}"/>${[96, 120, 144].map((y, i) => `<path d="M58 ${y} ${Array.from({ length: 6 }, (_, k) => `L${66 + k * 14} ${y + (k % 2 ? -8 : 8)}`).join(' ')} L142 ${y}" fill="none" stroke="${['#D4AF37', '#fff', '#C0392B'][i]}" stroke-width="3"/>`).join('')}`,
  };
  return `<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${p.name}"><ellipse cx="100" cy="186" rx="58" ry="6" fill="#000" opacity=".08"/>${shapes[p.shape] || shapes.box}</svg>`;
};

function shade(hex, pct) {
  const n = parseInt(hex.slice(1), 16);
  const f = (v) => Math.max(0, Math.min(255, Math.round(v + (pct / 100) * 255)));
  return '#' + [f(n >> 16), f((n >> 8) & 255), f(n & 255)].map((v) => v.toString(16).padStart(2, '0')).join('');
}
function isDark(hex) {
  const n = parseInt(hex.slice(1), 16);
  return ((n >> 16) * 0.299 + ((n >> 8) & 255) * 0.587 + (n & 255) * 0.114) < 140;
}
