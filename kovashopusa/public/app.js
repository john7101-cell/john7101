/* KovaShopUSA — maqueta de tienda en línea (sin frameworks). */
(function () {
  'use strict';

  const FREE_SHIP_MIN = 75;
  const PACKAGING_OZ = 8;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const main = $('#main');

  // ---------------- Almacenamiento local (tolerante a fallos) ----------------
  const store = {
    get(k, d) { try { const v = localStorage.getItem('kova.' + k); return v ? JSON.parse(v) : d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem('kova.' + k, JSON.stringify(v)); } catch { /* sin almacenamiento */ } },
  };

  // ---------------- Idioma ----------------
  const I18N = {
    en: {
      skip: 'Skip to content',
      announce: 'Free USPS Ground Advantage™ shipping on orders over $75 · Ships from Miami, FL',
      'nav.shop': 'Shop', 'nav.categories': 'Categories', 'nav.brands': 'For Brands', 'nav.story': 'Our Story', 'nav.track': 'Track Order',
      search: 'Search brands & products',
      'hero.title1': 'Discover extraordinary', 'hero.title2': 'brands from', 'hero.title3': 'Latin America.',
      'hero.lead': 'A curated marketplace connecting U.S. shoppers with the best brands from Latin America. Curated quality. Trusted shopping.',
      'hero.shop': 'Shop now', 'hero.brands': 'Sell with us',
      'trust.curated': 'Kova Curated™', 'trust.usps': 'Ships with USPS', 'trust.compliant': 'U.S. compliant',
      'channels.also': 'Also available on',
      'cats.eyebrow': 'Main categories', 'cats.title': 'Shop by category', 'cats.items': 'products',
      'feat.eyebrow': 'Curated for you', 'feat.title': 'Featured this week', 'feat.all': 'View all products',
      'why.title': 'Why KovaShopUSA?',
      why: ['Carefully selected brands', 'High-quality, innovative products', 'Compliant with U.S. regulations', 'Safe, sustainable ingredients', 'Authentic founder stories', 'Secure, trusted checkout', 'Fast USPS shipping nationwide', 'Backed by WeComex Intl'],
      'seal.copy': 'Our selection. Your trust. Brands that inspire.',
      'promise.title': 'Brand promise',
      'promise.text': 'If a product is on <b>KovaShopUSA</b>, you can trust it was carefully selected.',
      'clients.title': 'For our customers', 'clients.text': 'Discover incredible brands, quality products and experiences that keep you coming back.',
      'brands.title': 'For brands', 'brands.text': 'We help you grow in the United States with logistics, strategy and high-impact digital channels.',
      'brands.cta': 'Apply as a brand',
      'quote.text': '“I found an incredible brand.”', 'quote.who': '— Verified customer, Houston TX',
      'shop.title': 'All products', 'shop.cat': 'Category', 'shop.all': 'All', 'shop.country': 'Origin', 'shop.price': 'Price',
      'shop.under25': 'Under $25', 'shop.25to50': '$25 – $50', 'shop.over50': 'Over $50', 'shop.results': 'results', 'shop.none': 'No products match your filters.',
      'sort.featured': 'Featured', 'sort.low': 'Price: low to high', 'sort.high': 'Price: high to low', 'sort.rating': 'Top rated',
      'badge.bestseller': 'Best seller', 'badge.curated': 'Kova Curated', 'badge.new': 'New',
      add: 'Add', 'add.long': 'Add to cart', 'buy.now': 'Buy now', added: 'Added to cart',
      'pdp.origin': 'Made in', 'pdp.seal': '<b>Kova Curated™</b> — reviewed for quality, authenticity and U.S. compliance.',
      'pdp.ship': 'Shipping estimate', 'pdp.zip': 'ZIP code', 'pdp.calc': 'Calculate', 'pdp.weight': 'Shipping weight',
      'pdp.free': 'Free with orders over $75', 'pdp.related': 'You may also like',
      'cart.title': 'Your cart', 'cart.empty': 'Your cart is empty.', 'cart.keep': 'Continue shopping', 'cart.remove': 'Remove',
      'cart.subtotal': 'Subtotal', 'cart.checkout': 'Checkout', 'cart.shipnote': 'Shipping calculated at checkout with live USPS rates.',
      'cart.freeLeft': 'You are {x} away from free shipping', 'cart.freeOk': 'You unlocked free USPS Ground Advantage™ shipping!',
      'co.title': 'Checkout', 'co.contact': 'Contact', 'co.email': 'Email', 'co.phone': 'Phone (for USPS delivery updates)',
      'co.address': 'Shipping address', 'co.name': 'Full name', 'co.street': 'Street address', 'co.apt': 'Apt, suite, unit (optional)',
      'co.zip': 'ZIP code', 'co.city': 'City', 'co.state': 'State', 'co.verify': 'Verify address with USPS',
      'co.verified': 'Address verified by USPS', 'co.edit': 'Edit',
      'co.method': 'Shipping method', 'co.methodHint': 'Verify your address to see live USPS rates.',
      'co.days': 'business days', 'co.free': 'FREE',
      'co.payment': 'Payment', 'co.payDemo': 'Prototype: payments are simulated. Do not enter real card data.',
      'co.card': 'Card number', 'co.exp': 'Expiry', 'co.cvc': 'CVC',
      'co.place': 'Place order', 'co.summary': 'Order summary', 'co.shipping': 'Shipping', 'co.tax': 'Estimated tax', 'co.total': 'Total',
      'co.pending': 'Calculated next', 'co.needAddress': 'Please verify your shipping address first.', 'co.needRate': 'Choose a shipping method.',
      'co.needContact': 'Please enter a valid email.', 'co.emptyCart': 'Your cart is empty.',
      'ord.thanks': 'Thank you!', 'ord.sub': 'You just discovered something amazing.', 'ord.num': 'Order', 'ord.track': 'USPS tracking number',
      'ord.trackBtn': 'Track package', 'ord.shipTo': 'Ships to', 'ord.service': 'Service', 'ord.notFound': 'Order not found.',
      'ord.labelNote': 'In this prototype the shipping label is simulated. In production it is created with the USPS Labels API once payment is captured.',
      'tr.title': 'Track your order', 'tr.lead': 'Enter your USPS tracking number or KovaShopUSA order number.',
      'tr.ph': 'e.g. 9400 1112 0000 0000 0000 00 or KS-123456', 'tr.btn': 'Track', 'tr.expected': 'Expected delivery', 'tr.history': 'Tracking history',
      'tr.recent': 'Your recent orders',
      'story.eyebrow': 'Our essence', 'story.title': 'The trusted place to discover exceptional Latin American brands.',
      'story.purpose': 'Purpose', 'story.purposeText': 'Create opportunities for the best Latin American brands to reach the U.S. market, building trust in every purchase and growth for every company.',
      'story.mission': 'Mission', 'story.missionText': 'We carefully select Latin American brands that meet high standards of quality, innovation and regulatory compliance, and connect them with U.S. consumers through a trusted shopping experience.',
      'story.vision': 'Vision', 'story.visionText': 'To be the leading marketplace in the United States to discover and buy high-quality Latin American brands, driving their international expansion.',
      'story.values': 'Our values',
      values: ['Trust', 'Quality', 'Transparency', 'Innovation', 'Fair Trade', 'Growth', 'Authenticity', 'Excellence', 'Responsibility'],
      'story.manifesto': 'Manifesto',
      manifesto: ['We believe Latin America is full of extraordinary brands that deserve to be known around the world.', 'We believe quality doesn’t depend on the size of a company, but on its passion, its innovation and its commitment.', 'We believe discovering a new brand can become an unforgettable experience.', 'That’s why we carefully select every product that reaches KovaShopUSA.'],
      'manifesto.strong': 'We don’t want to sell more. We want to discover better.',
      'manifesto.end': 'Because behind every brand there is a story. And behind every story there is an opportunity.',
      'b.eyebrow': 'Showcase for entrepreneurs', 'b.title1': 'Bring your brand to', 'b.title2': 'the United States.',
      'b.lead': 'KovaShopUSA is a storefront for Latin American entrepreneurs: we curate, list, store and ship your products to U.S. customers with USPS — you focus on making great products.',
      'b.apply': 'Apply now', 'b.how': 'How it works',
      steps: [['Apply', 'Tell us about your brand, products and certifications.'], ['Curation', 'Our team reviews quality, labeling and FDA/FTC compliance.'], ['Showcase', 'We create your brand page and list your products on KovaShopUSA, Amazon, TikTok Shop and Shopify.'], ['We ship', 'Inventory lives in our Miami hub; every order ships with USPS with tracking.']],
      'b.plans': 'Plans for brands', 'b.month': '/month', 'b.commission': 'commission per sale', 'b.choose': 'Choose plan', 'b.popular': 'Most popular',
      plans: [['Vitrina', '0', '18%', ['Brand page + up to 5 products', 'USPS fulfillment from Miami', 'Monthly sales report']], ['Crecimiento', '149', '12%', ['Up to 30 products', 'Amazon + TikTok Shop listings', 'UGC content pack', 'Compliance review']], ['Expansión', '399', '8%', ['Unlimited products', 'All channels + paid ads', 'Dedicated account manager', 'Wholesale & retail intros']]],
      'b.showcase': 'Brands in our showcase',
      'b.form': 'Brand application', 'b.formLead': 'We review every application within 5 business days.',
      'f.brand': 'Brand name', 'f.contact': 'Contact name', 'f.email': 'Email', 'f.country': 'Country', 'f.category': 'Category',
      'f.site': 'Website or Instagram', 'f.products': 'Tell us about your products', 'f.fda': 'My products are already registered / labeled for the U.S. (FDA, English labels)',
      'f.send': 'Send application', 'f.sent': 'Application received! We’ll contact you within 5 business days. (Prototype: saved only in this browser.)',
      'footer.about': 'A curated marketplace connecting U.S. shoppers with the best brands from Latin America.',
      'footer.shop': 'Shop', 'footer.company': 'Company', 'footer.sell': 'Sell with us', 'footer.ship': 'Shipping',
      'footer.shipText': 'All orders ship with USPS from our Miami, FL fulfillment center. Real-time rates, address verification and tracking.',
      'footer.backed': 'Backed by WeComex Intl', 'footer.mock': 'Prototype for testing — no real payments are processed.',
      'usps.live': 'USPS API: connected', 'usps.demo': 'USPS: demo mode (simulated data)', 'usps.demoShort': 'demo',
      loading: 'Loading…',
    },
    es: {
      skip: 'Ir al contenido',
      announce: 'Envío gratis USPS Ground Advantage™ en pedidos de más de $75 · Enviamos desde Miami, FL',
      'nav.shop': 'Tienda', 'nav.categories': 'Categorías', 'nav.brands': 'Para marcas', 'nav.story': 'Nuestra historia', 'nav.track': 'Rastrear pedido',
      search: 'Buscar marcas y productos',
      'hero.title1': 'Descubre marcas', 'hero.title2': 'extraordinarias de', 'hero.title3': 'Latinoamérica.',
      'hero.lead': 'Un marketplace curado que conecta a los consumidores de Estados Unidos con las mejores marcas de Latinoamérica. Calidad curada. Compra confiable.',
      'hero.shop': 'Comprar ahora', 'hero.brands': 'Vende con nosotros',
      'trust.curated': 'Kova Curated™', 'trust.usps': 'Envíos con USPS', 'trust.compliant': 'Cumple normas de EE. UU.',
      'channels.also': 'También disponible en',
      'cats.eyebrow': 'Categorías principales', 'cats.title': 'Compra por categoría', 'cats.items': 'productos',
      'feat.eyebrow': 'Curado para ti', 'feat.title': 'Destacados de la semana', 'feat.all': 'Ver todos los productos',
      'why.title': '¿Por qué KovaShopUSA?',
      why: ['Marcas cuidadosamente seleccionadas', 'Productos de alta calidad e innovación', 'Cumplimiento de normas de EE. UU.', 'Ingredientes seguros y sostenibles', 'Historias auténticas y emprendedoras', 'Experiencia de compra segura y confiable', 'Envíos rápidos con USPS en todo EE. UU.', 'Respaldo de WeComex Intl'],
      'seal.copy': 'Nuestra selección. Tu confianza. Marcas que inspiran.',
      'promise.title': 'Promesa de marca',
      'promise.text': 'Si un producto está en <b>KovaShopUSA</b>, puedes confiar en que fue cuidadosamente seleccionado.',
      'clients.title': 'Para nuestros clientes', 'clients.text': 'Descubre marcas increíbles, productos de calidad y experiencias que te hacen volver.',
      'brands.title': 'Para las marcas', 'brands.text': 'Te ayudamos a crecer en Estados Unidos con logística, estrategia y canales digitales de alto impacto.',
      'brands.cta': 'Postula tu marca',
      'quote.text': '“Encontré una marca increíble.”', 'quote.who': '— Cliente verificada, Houston TX',
      'shop.title': 'Todos los productos', 'shop.cat': 'Categoría', 'shop.all': 'Todas', 'shop.country': 'Origen', 'shop.price': 'Precio',
      'shop.under25': 'Menos de $25', 'shop.25to50': '$25 – $50', 'shop.over50': 'Más de $50', 'shop.results': 'resultados', 'shop.none': 'Ningún producto coincide con los filtros.',
      'sort.featured': 'Destacados', 'sort.low': 'Precio: menor a mayor', 'sort.high': 'Precio: mayor a menor', 'sort.rating': 'Mejor calificados',
      'badge.bestseller': 'Más vendido', 'badge.curated': 'Kova Curated', 'badge.new': 'Nuevo',
      add: 'Agregar', 'add.long': 'Agregar al carrito', 'buy.now': 'Comprar ahora', added: 'Agregado al carrito',
      'pdp.origin': 'Hecho en', 'pdp.seal': '<b>Kova Curated™</b> — revisado en calidad, autenticidad y cumplimiento en EE. UU.',
      'pdp.ship': 'Estimar envío', 'pdp.zip': 'Código ZIP', 'pdp.calc': 'Calcular', 'pdp.weight': 'Peso de envío',
      'pdp.free': 'Gratis en pedidos de más de $75', 'pdp.related': 'También te puede gustar',
      'cart.title': 'Tu carrito', 'cart.empty': 'Tu carrito está vacío.', 'cart.keep': 'Seguir comprando', 'cart.remove': 'Quitar',
      'cart.subtotal': 'Subtotal', 'cart.checkout': 'Pagar', 'cart.shipnote': 'El envío se calcula en el checkout con tarifas de USPS en tiempo real.',
      'cart.freeLeft': 'Te faltan {x} para el envío gratis', 'cart.freeOk': '¡Desbloqueaste envío gratis USPS Ground Advantage™!',
      'co.title': 'Checkout', 'co.contact': 'Contacto', 'co.email': 'Correo electrónico', 'co.phone': 'Teléfono (avisos de entrega USPS)',
      'co.address': 'Dirección de envío', 'co.name': 'Nombre completo', 'co.street': 'Dirección', 'co.apt': 'Apto, suite, unidad (opcional)',
      'co.zip': 'Código ZIP', 'co.city': 'Ciudad', 'co.state': 'Estado', 'co.verify': 'Verificar dirección con USPS',
      'co.verified': 'Dirección verificada por USPS', 'co.edit': 'Editar',
      'co.method': 'Método de envío', 'co.methodHint': 'Verifica tu dirección para ver tarifas de USPS en tiempo real.',
      'co.days': 'días hábiles', 'co.free': 'GRATIS',
      'co.payment': 'Pago', 'co.payDemo': 'Maqueta: los pagos son simulados. No ingreses datos reales de tarjeta.',
      'co.card': 'Número de tarjeta', 'co.exp': 'Vencimiento', 'co.cvc': 'CVC',
      'co.place': 'Realizar pedido', 'co.summary': 'Resumen del pedido', 'co.shipping': 'Envío', 'co.tax': 'Impuesto estimado', 'co.total': 'Total',
      'co.pending': 'Se calcula después', 'co.needAddress': 'Primero verifica tu dirección de envío.', 'co.needRate': 'Elige un método de envío.',
      'co.needContact': 'Ingresa un correo válido.', 'co.emptyCart': 'Tu carrito está vacío.',
      'ord.thanks': '¡Gracias!', 'ord.sub': 'Acabas de descubrir algo increíble.', 'ord.num': 'Pedido', 'ord.track': 'Número de rastreo USPS',
      'ord.trackBtn': 'Rastrear paquete', 'ord.shipTo': 'Se envía a', 'ord.service': 'Servicio', 'ord.notFound': 'Pedido no encontrado.',
      'ord.labelNote': 'En esta maqueta la etiqueta de envío es simulada. En producción se crea con la API de Labels de USPS cuando se captura el pago.',
      'tr.title': 'Rastrea tu pedido', 'tr.lead': 'Ingresa tu número de rastreo USPS o tu número de pedido KovaShopUSA.',
      'tr.ph': 'p. ej. 9400 1112 0000 0000 0000 00 o KS-123456', 'tr.btn': 'Rastrear', 'tr.expected': 'Entrega estimada', 'tr.history': 'Historial de rastreo',
      'tr.recent': 'Tus pedidos recientes',
      'story.eyebrow': 'Nuestra esencia', 'story.title': 'El lugar de confianza para descubrir marcas latinoamericanas excepcionales.',
      'story.purpose': 'Propósito', 'story.purposeText': 'Generar oportunidades para que las mejores marcas latinoamericanas lleguen al mercado estadounidense, creando confianza en cada compra y crecimiento para cada empresa.',
      'story.mission': 'Misión', 'story.missionText': 'Seleccionamos cuidadosamente marcas latinoamericanas que cumplen altos estándares de calidad, innovación y cumplimiento normativo, para conectarlas con consumidores en Estados Unidos a través de una experiencia de compra confiable.',
      'story.vision': 'Visión', 'story.visionText': 'Ser el marketplace referente en Estados Unidos para descubrir y comprar marcas latinoamericanas de alta calidad, impulsando su expansión internacional.',
      'story.values': 'Nuestros valores',
      values: ['Confianza', 'Calidad', 'Transparencia', 'Innovación', 'Comercio justo', 'Crecimiento', 'Autenticidad', 'Excelencia', 'Responsabilidad'],
      'story.manifesto': 'Manifiesto',
      manifesto: ['Creemos que Latinoamérica está llena de marcas extraordinarias que merecen ser conocidas en el mundo.', 'Creemos que la calidad no depende del tamaño de una empresa, sino de su pasión, su innovación y su compromiso.', 'Creemos que descubrir una nueva marca puede convertirse en una experiencia inolvidable.', 'Por eso seleccionamos cuidadosamente cada producto que llega a KovaShopUSA.'],
      'manifesto.strong': 'No buscamos vender más. Buscamos descubrir mejor.',
      'manifesto.end': 'Porque detrás de cada marca hay una historia. Y detrás de cada historia hay una oportunidad.',
      'b.eyebrow': 'Vitrina para emprendedores', 'b.title1': 'Lleva tu marca a', 'b.title2': 'Estados Unidos.',
      'b.lead': 'KovaShopUSA es una vitrina para emprendedores latinoamericanos: curamos, publicamos, almacenamos y enviamos tus productos a clientes en EE. UU. con USPS — tú te enfocas en crear grandes productos.',
      'b.apply': 'Postular ahora', 'b.how': 'Cómo funciona',
      steps: [['Postula', 'Cuéntanos sobre tu marca, productos y certificaciones.'], ['Curaduría', 'Nuestro equipo revisa calidad, etiquetado y cumplimiento FDA/FTC.'], ['Vitrina', 'Creamos tu página de marca y publicamos tus productos en KovaShopUSA, Amazon, TikTok Shop y Shopify.'], ['Enviamos', 'El inventario está en nuestro centro de Miami; cada pedido sale por USPS con rastreo.']],
      'b.plans': 'Planes para marcas', 'b.month': '/mes', 'b.commission': 'de comisión por venta', 'b.choose': 'Elegir plan', 'b.popular': 'Más popular',
      plans: [['Vitrina', '0', '18%', ['Página de marca + hasta 5 productos', 'Fulfillment USPS desde Miami', 'Reporte mensual de ventas']], ['Crecimiento', '149', '12%', ['Hasta 30 productos', 'Publicación en Amazon + TikTok Shop', 'Paquete de contenido UGC', 'Revisión de cumplimiento']], ['Expansión', '399', '8%', ['Productos ilimitados', 'Todos los canales + pauta', 'Gerente de cuenta dedicado', 'Contactos mayoristas y retail']]],
      'b.showcase': 'Marcas en nuestra vitrina',
      'b.form': 'Postulación de marca', 'b.formLead': 'Revisamos cada postulación en un máximo de 5 días hábiles.',
      'f.brand': 'Nombre de la marca', 'f.contact': 'Nombre de contacto', 'f.email': 'Correo', 'f.country': 'País', 'f.category': 'Categoría',
      'f.site': 'Sitio web o Instagram', 'f.products': 'Cuéntanos sobre tus productos', 'f.fda': 'Mis productos ya están registrados / etiquetados para EE. UU. (FDA, etiqueta en inglés)',
      'f.send': 'Enviar postulación', 'f.sent': '¡Postulación recibida! Te contactaremos en 5 días hábiles. (Maqueta: se guarda solo en este navegador.)',
      'footer.about': 'Un marketplace curado que conecta a los consumidores de Estados Unidos con las mejores marcas de Latinoamérica.',
      'footer.shop': 'Tienda', 'footer.company': 'Empresa', 'footer.sell': 'Vende con nosotros', 'footer.ship': 'Envíos',
      'footer.shipText': 'Todos los pedidos se envían con USPS desde nuestro centro en Miami, FL. Tarifas en tiempo real, verificación de dirección y rastreo.',
      'footer.backed': 'Respaldo de WeComex Intl', 'footer.mock': 'Maqueta de prueba — no se procesan pagos reales.',
      'usps.live': 'API de USPS: conectada', 'usps.demo': 'USPS: modo demo (datos simulados)', 'usps.demoShort': 'demo',
      loading: 'Cargando…',
    },
  };
  let lang = store.get('lang', (navigator.language || 'en').startsWith('es') ? 'es' : 'en');
  const t = (k, vars) => {
    let s = I18N[lang][k] ?? I18N.en[k] ?? k;
    if (vars && typeof s === 'string') for (const [a, b] of Object.entries(vars)) s = s.replace(`{${a}}`, b);
    return s;
  };
  const money = (n) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const catName = (id) => { const c = CATEGORIES.find((x) => x.id === id); return c ? c[lang] : id; };
  const product = (id) => PRODUCTS.find((p) => p.id === id);
  const desc = (p) => p[lang] || p.en;

  // ---------------- Iconos ----------------
  const I = {
    check: '<svg viewBox="0 0 24 24" width="18" height="18"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="m7.5 12.5 3 3 6-6.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    shield: '<svg viewBox="0 0 24 24" width="18" height="18"><path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m8.5 12 2.5 2.5 4.5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    truck: '<svg viewBox="0 0 24 24" width="18" height="18"><path d="M2 6h12v10H2zM14 10h4l3 3v3h-7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="6" cy="18" r="2" fill="#fff" stroke="currentColor" stroke-width="2"/><circle cx="17" cy="18" r="2" fill="#fff" stroke="currentColor" stroke-width="2"/></svg>',
    flag: '<svg viewBox="0 0 24 24" width="18" height="18"><path d="M5 21V4M5 4h11l-2 4 2 4H5" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    drop: '<svg viewBox="0 0 32 32" width="30" height="30"><path d="M16 4c5 7 8 11 8 15a8 8 0 0 1-16 0c0-4 3-8 8-15z" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    leaf: '<svg viewBox="0 0 32 32" width="30" height="30"><path d="M6 26C6 12 14 6 27 5c0 13-6 21-20 21zM6 26 18 14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    cup: '<svg viewBox="0 0 32 32" width="30" height="30"><path d="M5 12h18v6a8 8 0 0 1-8 8h-2a8 8 0 0 1-8-8zM23 14h2a3 3 0 0 1 0 6h-2.5M11 4c-1 2 1 3 0 5M16 4c-1 2 1 3 0 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    paw: '<svg viewBox="0 0 32 32" width="30" height="30"><ellipse cx="16" cy="21" rx="6" ry="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="8" cy="13" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="13" cy="8" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="19" cy="8" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="24" cy="13" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
    shirt: '<svg viewBox="0 0 32 32" width="30" height="30"><path d="M11 5 5 8l2 6 3-1v14h12V13l3 1 2-6-6-3c0 2-2 3.5-5 3.5S11 7 11 5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
    target: '<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="18" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="24" cy="24" r="11" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="24" cy="24" r="4" fill="currentColor"/><path d="m24 24 16-16M34 8h6v6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
    mountain: '<svg viewBox="0 0 48 48"><path d="M4 40 18 18l7 10 5-6 14 18z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/><path d="M24 26V6l9 3-9 3" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/></svg>',
    eye: '<svg viewBox="0 0 48 48"><path d="M3 24s8-13 21-13 21 13 21 13-8 13-21 13S3 24 3 24z" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="24" cy="24" r="7" fill="none" stroke="currentColor" stroke-width="2.5"/></svg>',
    leafBig: '<svg viewBox="0 0 100 100" class="leaf" aria-hidden="true"><path d="M20 85C15 45 40 15 90 10c0 45-25 75-70 75zM20 85 70 32" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><path d="M38 66l-2-18M52 52l-2-18M38 66l18 2M52 52l18 2" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
  };
  const seal = `<svg viewBox="0 0 200 200" class="seal" role="img" aria-label="Kova Curated — Selected for quality">
    <defs><path id="sealTop" d="M30 100a70 70 0 0 1 140 0"/><path id="sealBot" d="M24 100a76 76 0 0 0 152 0"/></defs>
    <circle cx="100" cy="100" r="94" fill="none" stroke="currentColor" stroke-width="3"/>
    <circle cx="100" cy="100" r="54" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text font-family="Poppins,sans-serif" font-size="19" font-weight="600" letter-spacing="5" fill="currentColor"><textPath href="#sealTop" startOffset="50%" text-anchor="middle">KOVA CURATED™</textPath></text>
    <text font-family="Poppins,sans-serif" font-size="13" font-weight="600" letter-spacing="3" fill="currentColor"><textPath href="#sealBot" startOffset="50%" text-anchor="middle">SELECTED FOR QUALITY</textPath></text>
    <text x="100" y="118" font-family="Poppins,sans-serif" font-size="52" font-weight="500" fill="currentColor" text-anchor="middle">K</text>
  </svg>`;
  const stars = (r, n) => `<span class="stars" aria-label="${r} / 5">${'★'.repeat(Math.round(r))}${'☆'.repeat(5 - Math.round(r))} <small>${r} (${n})</small></span>`;

  // ---------------- USPS: servidor o modo demo en el navegador ----------------
  const usps = {
    mode: 'unknown',
    ready: null,
    init() { this.ready = this._init(); return this.ready; },
    async _init() {
      try {
        const r = await fetch('api/usps/status', { cache: 'no-store' });
        if (!r.ok) throw new Error();
        const s = await r.json();
        this.mode = s.mode === 'live' ? 'live' : 'server-demo';
      } catch { this.mode = 'browser-demo'; }
      renderUspsMode();
    },
    get isDemo() { return this.mode !== 'live'; },
    async req(path, opts, fallback) {
      await this.ready;
      if (this.mode === 'browser-demo') {
        try { return await fallback(); } catch (e) { throw new Error(e.message); }
      }
      const r = await fetch('api/usps/' + path, opts);
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || 'USPS error');
      return data;
    },
    validateAddress(a) {
      return this.req('address', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(a) }, () => {
        if (!UspsMock.US_STATES.has(a.state)) throw new Error('Estado inválido / Invalid state');
        return UspsMock.mock.validateAddress({ street: a.street.trim(), secondary: (a.secondary || '').trim(), city: a.city.trim(), state: a.state, zip: a.zip.trim() });
      });
    },
    cityState(zip) { return this.req('city-state?zip=' + encodeURIComponent(zip), {}, () => UspsMock.mock.cityState(zip)); },
    rates(destinationZIP, weightOz) {
      return this.req('rates', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ destinationZIP, weightOz }) },
        () => UspsMock.mock.rates('33166', destinationZIP, weightOz));
    },
    track(n, demoSince) {
      if (demoSince) return Promise.resolve(UspsMock.mock.track(n.replace(/\s+/g, ''), demoSince));
      return this.req('track/' + encodeURIComponent(n.replace(/\s+/g, '')), {}, () => UspsMock.mock.track(n.replace(/\s+/g, '').toUpperCase()));
    },
  };
  function renderUspsMode() {
    const el = $('#uspsMode');
    el.innerHTML = usps.mode === 'live' ? `<span class="usps-tag">USPS</span> ${t('usps.live')}` : `<span class="usps-tag">USPS</span> <span class="demo-tag">${t('usps.demoShort')}</span> ${t('usps.demo')}`;
  }

  // ---------------- Carrito ----------------
  let cart = store.get('cart', []).filter((i) => product(i.id));
  const saveCart = () => { store.set('cart', cart); renderCartCount(); renderCart(); };
  const cartQty = () => cart.reduce((s, i) => s + i.qty, 0);
  const subtotal = () => cart.reduce((s, i) => s + product(i.id).price * i.qty, 0);
  const cartWeight = () => cart.reduce((s, i) => s + product(i.id).weightOz * i.qty, 0) + PACKAGING_OZ;
  function addToCart(id, qty = 1) {
    const it = cart.find((i) => i.id === id);
    if (it) it.qty = Math.min(20, it.qty + qty); else cart.push({ id, qty });
    saveCart();
    toast(`${t('added')} · ${product(id).name}`);
  }
  function setQty(id, qty) {
    if (qty <= 0) cart = cart.filter((i) => i.id !== id);
    else { const it = cart.find((i) => i.id === id); if (it) it.qty = Math.min(20, qty); }
    saveCart();
  }
  function renderCartCount() { $('#cartCount').textContent = cartQty(); }
  function freeBar() {
    const s = subtotal();
    const pct = Math.min(100, (s / FREE_SHIP_MIN) * 100);
    const msg = s >= FREE_SHIP_MIN ? t('cart.freeOk') : t('cart.freeLeft', { x: money(FREE_SHIP_MIN - s) });
    return `<div class="free-bar">${msg}<div class="progress"><div style="width:${pct}%"></div></div></div>`;
  }
  function renderCart() {
    const body = $('#cartItems');
    const foot = $('#cartFoot');
    if (!cart.length) {
      body.innerHTML = `<div class="empty"><p>${t('cart.empty')}</p><a href="#/shop" class="btn btn-outline" data-close-cart>${t('cart.keep')}</a></div>`;
      foot.innerHTML = '';
      return;
    }
    body.innerHTML = freeBar() + cart.map(({ id, qty }) => {
      const p = product(id);
      return `<div class="cart-item"><div class="th">${productArt(p)}</div><div class="grow">
        <div class="name">${esc(p.name)}</div><div class="note">${esc(p.brand)} · ${p.flag} ${esc(p.country)}</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px">
          <div class="qty"><button data-dec="${id}" aria-label="-">−</button><input value="${qty}" readonly aria-label="qty"><button data-inc="${id}" aria-label="+">+</button></div>
          <b>${money(p.price * qty)}</b></div>
        <button class="link-btn" data-rm="${id}">${t('cart.remove')}</button></div></div>`;
    }).join('');
    foot.innerHTML = `<div class="line"><span>${t('cart.subtotal')}</span><b>${money(subtotal())}</b></div>
      <p class="note">${t('cart.shipnote')}</p>
      <a href="#/checkout" class="btn btn-primary btn-block" data-close-cart>${t('cart.checkout')}</a>`;
  }
  function openCart(open) {
    $('#cartDrawer').classList.toggle('open', open);
    $('#cartDrawer').setAttribute('aria-hidden', String(!open));
    $('#scrim').hidden = !open;
    if (open) renderCart();
  }

  // ---------------- Componentes ----------------
  function card(p) {
    return `<article class="card">
      <a class="media" href="#/product/${p.id}" aria-label="${esc(p.name)}">${p.badge ? `<span class="badge ${p.badge}">${t('badge.' + p.badge)}</span>` : ''}${productArt(p)}</a>
      <div class="body"><span class="brand">${esc(p.brand)} · ${p.flag}</span>
        <h3><a href="#/product/${p.id}">${esc(p.name)}</a></h3>${stars(p.rating, p.reviews)}
        <div class="foot"><span class="price">${money(p.price)}</span><button class="add-btn" data-add="${p.id}">+ ${t('add')}</button></div>
      </div></article>`;
  }
  const catCards = () => CATEGORIES.map((c) => `<a class="cat-card" href="#/shop?cat=${c.id}"><div class="ico">${I[c.icon]}</div><h3>${c[lang]}</h3><small>${PRODUCTS.filter((p) => p.category === c.id).length} ${t('cats.items')}</small></a>`).join('');

  // ---------------- Vistas ----------------
  function viewHome() {
    const featured = ['cafe-huila', 'serum-sacha', 'maca', 'alpaca-beanie', 'chocolate', 'dog-treats', 'crema-cacao', 'tote'].map(product);
    const hp = ['cafe-huila', 'serum-sacha', 'crema-cacao', 'chocolate'].map(product);
    return `
    <section class="hero"><div class="wrap hero-grid">
      <div>
        <div class="eyebrow">Discover what's next.</div>
        <h1>${t('hero.title1')} ${t('hero.title2')} <em>${t('hero.title3')}</em></h1>
        <p class="lead">${t('hero.lead')}</p>
        <div class="hero-cta"><a href="#/shop" class="btn btn-primary">${t('hero.shop')}</a><a href="#/brands" class="btn btn-outline">${t('hero.brands')}</a></div>
        <div class="hero-trust"><span>${I.shield} ${t('trust.curated')}</span><span>${I.truck} ${t('trust.usps')}</span><span>${I.flag} ${t('trust.compliant')}</span></div>
      </div>
      <div class="hero-art" aria-hidden="true"><div class="blob"></div>${I.leafBig}
        ${hp.map((p, i) => `<div class="p p${i + 1}">${productArt(p)}</div>`).join('')}
      </div>
    </div></section>
    <div class="channels"><div class="wrap"><span>${t('channels.also')}</span><b>amazon</b><b>TikTok Shop</b><b>shopify</b></div></div>
    <section><div class="wrap">
      <div class="section-title"><div class="eyebrow">${t('cats.eyebrow')}</div><h2>${t('cats.title')}</h2></div>
      <div class="cat-grid">${catCards()}</div>
    </div></section>
    <section style="padding-top:0"><div class="wrap">
      <div class="section-title"><div class="eyebrow">${t('feat.eyebrow')}</div><h2>${t('feat.title')}</h2></div>
      <div class="grid">${featured.map(card).join('')}</div>
      <p style="text-align:center;margin-top:28px"><a href="#/shop" class="btn btn-navy">${t('feat.all')}</a></p>
    </div></section>
    <section style="padding-top:0"><div class="wrap"><div class="why">
      <div><h2>${t('why.title')}</h2><ul>${t('why').map((w) => `<li>${I.check}${w}</li>`).join('')}</ul></div>
      <div>${seal}<p class="seal-copy">${t('seal.copy')}</p></div>
    </div></div></section>
    <div class="promise wrap"><div class="eyebrow">${t('promise.title')}</div><blockquote>${t('promise.text')}</blockquote></div>
    <section style="padding-top:0"><div class="wrap"><div class="split">
      <div class="a"><h3>${t('clients.title')}</h3><p>${t('clients.text')}</p><div class="quote" style="text-align:left"><p style="color:#fff">${t('quote.text')}</p><span style="color:var(--gold);letter-spacing:2px">★★★★★</span> <small>${t('quote.who')}</small></div></div>
      <div class="b"><h3>${t('brands.title')}</h3><p>${t('brands.text')}</p><a href="#/brands" class="btn btn-primary">${t('brands.cta')}</a></div>
    </div></div></section>`;
  }

  function viewShop(params) {
    const cat = params.get('cat') || 'all';
    const q = (params.get('q') || '').toLowerCase();
    const price = params.get('price') || 'all';
    const sort = params.get('sort') || 'featured';
    const countries = [...new Set(PRODUCTS.map((p) => p.country))].sort();
    const country = params.get('country') || 'all';
    let list = PRODUCTS.filter((p) =>
      (cat === 'all' || p.category === cat) &&
      (country === 'all' || p.country === country) &&
      (price === 'all' || (price === 'u25' && p.price < 25) || (price === '25-50' && p.price >= 25 && p.price <= 50) || (price === 'o50' && p.price > 50)) &&
      (!q || `${p.name} ${p.brand} ${p.country} ${catName(p.category)}`.toLowerCase().includes(q)));
    if (sort === 'low') list.sort((a, b) => a.price - b.price);
    if (sort === 'high') list.sort((a, b) => b.price - a.price);
    if (sort === 'rating') list.sort((a, b) => b.rating - a.rating);
    const radio = (name, val, label, cur) => `<label><input type="radio" name="${name}" value="${val}" ${cur === val ? 'checked' : ''}> ${label}</label>`;
    const title = q ? `“${esc(q)}”` : cat === 'all' ? t('shop.title') : catName(cat);
    return `<div class="wrap shop-layout">
      <aside class="filters" id="filters">
        <h4>${t('shop.cat')}</h4>${radio('cat', 'all', t('shop.all'), cat)}${CATEGORIES.map((c) => radio('cat', c.id, c[lang], cat)).join('')}
        <h4>${t('shop.price')}</h4>${radio('price', 'all', t('shop.all'), price)}${radio('price', 'u25', t('shop.under25'), price)}${radio('price', '25-50', t('shop.25to50'), price)}${radio('price', 'o50', t('shop.over50'), price)}
        <h4>${t('shop.country')}</h4>${radio('country', 'all', t('shop.all'), country)}${countries.map((c) => radio('country', c, `${PRODUCTS.find((p) => p.country === c).flag} ${c}`, country)).join('')}
      </aside>
      <div>
        <div class="chips">${[['all', t('shop.all')], ...CATEGORIES.map((c) => [c.id, c[lang]])].map(([id, n]) => `<button class="chip ${cat === id ? 'on' : ''}" data-chip="${id}">${n}</button>`).join('')}</div>
        <div class="shop-top"><div><h1 style="font-size:26px;margin:0">${title}</h1><span class="note">${list.length} ${t('shop.results')}</span></div>
          <select id="sortSel" aria-label="Sort">${['featured', 'low', 'high', 'rating'].map((s) => `<option value="${s}" ${sort === s ? 'selected' : ''}>${t('sort.' + s)}</option>`).join('')}</select></div>
        ${list.length ? `<div class="grid">${list.map(card).join('')}</div>` : `<p class="empty">${t('shop.none')}</p>`}
      </div></div>`;
  }

  function viewProduct(id) {
    const p = product(id);
    if (!p) return `<div class="wrap empty">404</div>`;
    const related = PRODUCTS.filter((x) => x.category === p.category && x.id !== p.id).slice(0, 4);
    return `<div class="wrap"><div class="crumbs"><a href="#/shop">${t('nav.shop')}</a> / <a href="#/shop?cat=${p.category}">${catName(p.category)}</a> / ${esc(p.name)}</div>
      <div class="pdp">
        <div class="media">${p.badge ? `<span class="badge ${p.badge}">${t('badge.' + p.badge)}</span>` : ''}${productArt(p)}</div>
        <div>
          <div class="eyebrow">${esc(p.brand)}</div>
          <h1>${esc(p.name)}</h1>
          ${stars(p.rating, p.reviews)}
          <div class="price">${money(p.price)}</div>
          <p>${esc(desc(p))}</p>
          <p class="note">${t('pdp.origin')} ${p.flag} <b>${esc(p.country)}</b> · ${t('pdp.weight')}: ${p.weightOz} oz</p>
          <div class="buy-row">
            <div class="qty"><button id="qDec" aria-label="-">−</button><input id="qVal" value="1" inputmode="numeric" aria-label="qty"><button id="qInc" aria-label="+">+</button></div>
            <button class="btn btn-primary" id="pdpAdd">${t('add.long')}</button>
          </div>
          <button class="btn btn-navy btn-block" id="pdpBuy">${t('buy.now')}</button>
          <div class="seal-line" style="margin-top:16px"><span style="color:var(--gold)">${I.shield}</span><span>${t('pdp.seal')}</span></div>
          <div class="ship-box">
            <h4><span class="usps-tag">USPS</span> ${t('pdp.ship')} ${usps.isDemo ? `<span class="demo-tag">${t('usps.demoShort')}</span>` : ''}</h4>
            <form class="inline-form" id="estForm"><input id="estZip" inputmode="numeric" maxlength="5" placeholder="${t('pdp.zip')} (e.g. 10001)" value="${esc(store.get('zip', ''))}" aria-label="${t('pdp.zip')}"><button class="btn btn-outline" style="padding:10px 16px">${t('pdp.calc')}</button></form>
            <div id="estOut"></div>
            <p class="note" style="margin:10px 0 0">${t('pdp.free')}</p>
          </div>
        </div>
      </div>
      ${related.length ? `<h2 style="font-size:24px">${t('pdp.related')}</h2><div class="grid" style="margin-bottom:64px">${related.map(card).join('')}</div>` : ''}
    </div>`;
  }

  function ratesList(r, name, freeEligible, selected) {
    return `<ul class="rates">${r.rates.map((x, i) => {
      const free = freeEligible && x.mailClass === 'USPS_GROUND_ADVANTAGE';
      const inner = `<span class="grow"><b>${x.name}</b><small>${x.days} ${t('co.days')}</small></span><b>${free ? `<span style="color:var(--green)">${t('co.free')}</span> <s class="note">${money(x.price)}</s>` : money(x.price)}</b>`;
      return name ? `<li><label class="rate"><input type="radio" name="${name}" value="${x.mailClass}" ${(selected ? selected === x.mailClass : i === 0) ? 'checked' : ''}>${inner}</label></li>` : `<li class="rate" style="cursor:default">${inner}</li>`;
    }).join('')}</ul>`;
  }

  // ---- Checkout ----
  const co = { address: null, rates: null, mailClass: null };
  const STATES = 'AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA PR RI SC SD TN TX UT VT VA WA WV WI WY'.split(' ');
  function shippingCost() {
    if (!co.rates || !co.mailClass) return null;
    const r = co.rates.rates.find((x) => x.mailClass === co.mailClass);
    if (!r) return null;
    return subtotal() >= FREE_SHIP_MIN && r.mailClass === 'USPS_GROUND_ADVANTAGE' ? 0 : r.price;
  }
  function viewCheckout() {
    if (!cart.length) return `<div class="wrap empty"><h2>${t('co.emptyCart')}</h2><a class="btn btn-primary" href="#/shop">${t('cart.keep')}</a></div>`;
    const d = store.get('draft', {});
    const f = (id, label, attrs = '') => `<div class="field"><label for="${id}">${label}</label><input id="${id}" name="${id}" value="${esc(d[id] || '')}" ${attrs}></div>`;
    return `<div class="wrap"><h1 style="padding-top:28px;font-size:30px;margin:0">${t('co.title')}</h1>
      <div class="checkout">
        <form id="coForm" novalidate>
          <div class="panel"><h3><span class="n">1</span>${t('co.contact')}</h3>
            <div class="row">${f('email', t('co.email'), 'type="email" autocomplete="email" required')}${f('phone', t('co.phone'), 'type="tel" autocomplete="tel"')}</div>
          </div>
          <div class="panel"><h3><span class="n">2</span>${t('co.address')} <span class="usps-tag" style="margin-left:auto">USPS</span></h3>
            <div id="addrFields">
              ${f('name', t('co.name'), 'autocomplete="name" required')}
              ${f('street', t('co.street'), 'autocomplete="address-line1" required placeholder="1200 Brickell Ave"')}
              ${f('secondary', t('co.apt'), 'autocomplete="address-line2"')}
              <div class="row-3">
                ${f('city', t('co.city'), 'autocomplete="address-level2"')}
                <div class="field"><label for="state">${t('co.state')}</label><select id="state" name="state" autocomplete="address-level1"><option value=""></option>${STATES.map((s) => `<option ${d.state === s ? 'selected' : ''}>${s}</option>`).join('')}</select></div>
                ${f('zip', t('co.zip'), 'inputmode="numeric" maxlength="5" autocomplete="postal-code" required')}
              </div>
              <div class="error" id="addrErr" hidden></div>
              <button type="button" class="btn btn-navy" id="verifyBtn">${t('co.verify')}</button>
            </div>
            <div id="addrOk" hidden></div>
          </div>
          <div class="panel"><h3><span class="n">3</span>${t('co.method')}</h3><div id="rateBox"><p class="note">${t('co.methodHint')}</p></div></div>
          <div class="panel"><h3><span class="n">4</span>${t('co.payment')}</h3>
            <p class="note" style="background:#FFF4CC;color:#7A5B00;padding:10px 12px;border-radius:10px">${t('co.payDemo')}</p>
            <div class="field"><label for="card">${t('co.card')}</label><input id="card" value="4242 4242 4242 4242" readonly></div>
            <div class="row"><div class="field"><label for="exp">${t('co.exp')}</label><input id="exp" value="12 / 29" readonly></div><div class="field"><label for="cvc">${t('co.cvc')}</label><input id="cvc" value="123" readonly></div></div>
          </div>
          <div class="error" id="coErr" hidden></div>
          <button class="btn btn-primary btn-block" id="placeBtn" style="padding:16px">${t('co.place')}</button>
        </form>
        <aside class="panel summary" id="summary"></aside>
      </div></div>`;
  }
  function renderSummary() {
    const el = $('#summary');
    if (!el) return;
    const ship = shippingCost();
    const sub = subtotal();
    el.innerHTML = `<h3>${t('co.summary')}</h3>
      ${cart.map(({ id, qty }) => { const p = product(id); return `<div class="mini"><div class="th">${productArt(p)}<span class="q">${qty}</span></div><div class="grow"><b>${esc(p.name)}</b><div class="note">${esc(p.brand)}</div></div><span>${money(p.price * qty)}</span></div>`; }).join('')}
      <div style="margin-top:10px">${freeBar()}</div>
      <div class="line"><span>${t('cart.subtotal')}</span><span>${money(sub)}</span></div>
      <div class="line"><span>${t('co.shipping')}${co.mailClass ? ` <small class="note">(${co.rates.rates.find((r) => r.mailClass === co.mailClass)?.name || ''})</small>` : ''}</span><span>${ship == null ? `<span class="note">${t('co.pending')}</span>` : ship === 0 ? t('co.free') : money(ship)}</span></div>
      <div class="line"><span>${t('co.tax')}</span><span>${money(0)}</span></div>
      <div class="line total"><span>${t('co.total')}</span><span>${money(sub + (ship || 0))}</span></div>
      <p class="note">${usps.isDemo ? `<span class="demo-tag">${t('usps.demoShort')}</span> ` : ''}${t('cart.shipnote')}</p>`;
  }
  function bindCheckout() {
    if (!$('#coForm')) return;
    co.address = null; co.rates = null; co.mailClass = null;
    renderSummary();
    const form = $('#coForm');
    form.addEventListener('input', () => {
      const d = Object.fromEntries(['email', 'phone', 'name', 'street', 'secondary', 'city', 'state', 'zip'].map((k) => [k, form.elements[k].value]));
      store.set('draft', d);
    });
    // Autocompletar ciudad/estado desde el ZIP (USPS City/State API)
    form.elements.zip.addEventListener('input', async (e) => {
      const z = e.target.value.replace(/\D/g, '');
      e.target.value = z;
      if (z.length !== 5) return;
      try {
        const r = await usps.cityState(z);
        if (!form.elements.city.value) form.elements.city.value = titleCase(r.city);
        form.elements.state.value = r.state;
      } catch { /* el usuario puede escribirlo a mano */ }
    });
    $('#verifyBtn').addEventListener('click', verifyAddress);
    form.addEventListener('change', (e) => {
      if (e.target.name === 'rate') { co.mailClass = e.target.value; renderSummary(); }
    });
    form.addEventListener('submit', placeOrder);
  }
  const titleCase = (s) => String(s).toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase());
  async function verifyAddress() {
    const form = $('#coForm');
    const err = $('#addrErr');
    const btn = $('#verifyBtn');
    err.hidden = true;
    const a = { street: form.elements.street.value, secondary: form.elements.secondary.value, city: form.elements.city.value, state: form.elements.state.value, zip: form.elements.zip.value };
    if (!form.elements.name.value.trim() || !a.street.trim() || !a.state || (!a.city.trim() && a.zip.length !== 5)) {
      err.textContent = lang === 'es' ? 'Completa nombre, dirección, estado y ciudad o ZIP.' : 'Please fill in name, street, state and city or ZIP.';
      err.hidden = false; return;
    }
    btn.disabled = true; btn.innerHTML = `<span class="spinner"></span> ${t('loading')}`;
    try {
      const res = await usps.validateAddress(a);
      co.address = { name: form.elements.name.value.trim(), ...res.address };
      store.set('zip', co.address.zip);
      $('#addrFields').hidden = true;
      const ok = $('#addrOk');
      ok.hidden = false;
      ok.innerHTML = `<div class="verified">${I.check}<div><b>${t('co.verified')}</b> ${res.source === 'demo' ? `<span class="demo-tag">${t('usps.demoShort')}</span>` : ''}<br>${esc(co.address.name)}<br>${esc(co.address.street)}${co.address.secondary ? ' ' + esc(co.address.secondary) : ''}<br>${esc(co.address.city)}, ${esc(co.address.state)} ${esc(co.address.zip)}${co.address.zip4 ? '-' + esc(co.address.zip4) : ''}</div></div>
        <button type="button" class="link-btn" id="editAddr">${t('co.edit')}</button>`;
      $('#editAddr').addEventListener('click', () => {
        co.address = null; co.rates = null; co.mailClass = null;
        $('#addrFields').hidden = false; ok.hidden = true;
        $('#rateBox').innerHTML = `<p class="note">${t('co.methodHint')}</p>`;
        renderSummary();
      });
      await loadRates();
    } catch (e) {
      err.textContent = e.message; err.hidden = false;
    } finally {
      btn.disabled = false; btn.textContent = t('co.verify');
    }
  }
  async function loadRates() {
    const box = $('#rateBox');
    box.innerHTML = `<p class="note"><span class="spinner"></span> ${t('loading')}</p>`;
    try {
      co.rates = await usps.rates(co.address.zip, cartWeight());
      if (!co.rates.rates.length) throw new Error('USPS no devolvió tarifas');
      co.mailClass = co.rates.rates[0].mailClass;
      box.innerHTML = `<p class="note">${t('pdp.weight')}: ${Math.round(co.rates.weightOz)} oz · Miami, FL ${co.rates.origin} → ${esc(co.rates.destination)}${co.rates.zone ? ` · Zone ${co.rates.zone}` : ''}</p>` + ratesList(co.rates, 'rate', subtotal() >= FREE_SHIP_MIN, co.mailClass);
    } catch (e) {
      box.innerHTML = `<p class="error">${esc(e.message)}</p>`;
    }
    renderSummary();
  }
  function placeOrder(e) {
    e.preventDefault();
    const form = $('#coForm');
    const err = $('#coErr');
    const fail = (m) => { err.textContent = m; err.hidden = false; };
    err.hidden = true;
    if (!/^\S+@\S+\.\S+$/.test(form.elements.email.value)) return fail(t('co.needContact'));
    if (!co.address) return fail(t('co.needAddress'));
    if (shippingCost() == null) return fail(t('co.needRate'));
    const id = 'KS-' + String(Math.floor(100000 + Math.random() * 900000));
    // Número de rastreo con formato USPS (simulado). En producción viene de la API de Labels.
    const tracking = '9400111' + Array.from({ length: 15 }, () => Math.floor(Math.random() * 10)).join('');
    const rate = co.rates.rates.find((r) => r.mailClass === co.mailClass);
    const order = {
      id, tracking, demoLabel: true, date: new Date().toISOString(), email: form.elements.email.value,
      items: cart.map((i) => ({ ...i, price: product(i.id).price })), subtotal: subtotal(), shipping: shippingCost(),
      service: rate.name, days: rate.days, address: co.address,
    };
    const orders = store.get('orders', []);
    orders.unshift(order);
    store.set('orders', orders.slice(0, 20));
    cart = []; saveCart();
    store.set('draft', {});
    location.hash = '#/order/' + id;
  }

  function viewOrder(id) {
    const o = store.get('orders', []).find((x) => x.id === id);
    if (!o) return `<div class="wrap empty">${t('ord.notFound')}</div>`;
    const a = o.address;
    return `<div class="wrap confirm">
      <div class="check"><svg viewBox="0 0 24 24" width="36" height="36"><path d="m5 12.5 4.5 4.5L19 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
      <h1>${t('ord.thanks')}</h1><p class="muted">${t('ord.sub')}</p>
      <div class="thanks-card">
        <div><div style="opacity:.75;font-size:13px">${t('ord.num')} <b>${o.id}</b> · ${o.service}</div>
          <div style="margin:10px 0 6px;font-size:13px;opacity:.75">${t('ord.track')}</div><code>${o.tracking.replace(/(\d{4})(?=\d)/g, '$1 ')}</code></div>
        <a class="btn btn-gold" href="#/track?n=${o.tracking}">${t('ord.trackBtn')}</a>
      </div>
      <div class="panel" style="text-align:left">
        <div class="row"><div><b>${t('ord.shipTo')}</b><p class="note" style="margin:6px 0">${esc(a.name)}<br>${esc(a.street)} ${esc(a.secondary || '')}<br>${esc(a.city)}, ${a.state} ${a.zip}${a.zip4 ? '-' + a.zip4 : ''}</p></div>
        <div><b>${t('ord.service')}</b><p class="note" style="margin:6px 0">${o.service} · ${o.days} ${t('co.days')}<br>${o.shipping === 0 ? t('co.free') : money(o.shipping)}</p></div></div>
        ${o.items.map((i) => { const p = product(i.id); return `<div class="mini"><div class="th">${productArt(p)}<span class="q">${i.qty}</span></div><div class="grow"><b>${esc(p.name)}</b></div><span>${money(i.price * i.qty)}</span></div>`; }).join('')}
        <div class="line total"><span>${t('co.total')}</span><span>${money(o.subtotal + o.shipping)}</span></div>
      </div>
      <p class="note">${t('ord.labelNote')}</p>
      <a class="btn btn-outline" href="#/shop">${t('cart.keep')}</a>
    </div>`;
  }

  function viewTrack(params) {
    const orders = store.get('orders', []);
    return `<div class="wrap" style="max-width:760px;padding-top:44px;padding-bottom:64px">
      <div class="eyebrow"><span class="usps-tag">USPS</span></div>
      <h1>${t('tr.title')}</h1><p class="muted">${t('tr.lead')}</p>
      <form class="inline-form" id="trackForm"><input id="trackInput" placeholder="${t('tr.ph')}" value="${esc(params.get('n') || '')}" aria-label="${t('tr.title')}"><button class="btn btn-primary">${t('tr.btn')}</button></form>
      <div id="trackOut"></div>
      ${orders.length ? `<h3 style="margin-top:36px;font-size:16px">${t('tr.recent')}</h3>${orders.slice(0, 5).map((o) => `<div class="mini" style="border-bottom:1px solid var(--line)"><div class="grow"><b>${o.id}</b> · <span class="note">${new Date(o.date).toLocaleDateString(lang)} · ${o.service}</span></div><a class="link-btn" href="#/track?n=${o.tracking}">${t('tr.btn')}</a></div>`).join('')}` : ''}
    </div>`;
  }
  async function runTrack(raw) {
    const out = $('#trackOut');
    if (!out || !raw.trim()) return;
    const orders = store.get('orders', []);
    let n = raw.trim().toUpperCase();
    const byOrder = orders.find((o) => o.id === n);
    if (byOrder) n = byOrder.tracking;
    const own = orders.find((o) => o.tracking === n.replace(/\s+/g, ''));
    out.innerHTML = `<p class="note" style="margin-top:20px"><span class="spinner"></span> ${t('loading')}</p>`;
    try {
      const r = await usps.track(n, own?.demoLabel ? own.date : null);
      const steps = 7;
      const done = r.status === 'Delivered' ? steps : Math.min(steps - 1, r.events.length);
      out.innerHTML = `<div class="panel" style="margin-top:24px">
        <div class="track-status"><div><div class="note">${r.trackingNumber.replace(/(\d{4})(?=\d)/g, '$1 ')}</div><h3 style="margin:4px 0 0">${esc(r.summary || r.status)}</h3></div><span class="status-pill">${esc(r.status)}</span></div>
        <div class="progress"><div style="width:${(done / steps) * 100}%"></div></div>
        ${r.expectedDelivery ? `<p class="note">${t('tr.expected')}: <b>${new Date(r.expectedDelivery + 'T12:00:00').toLocaleDateString(lang, { weekday: 'long', month: 'long', day: 'numeric' })}</b></p>` : ''}
        ${r.source === 'demo' ? `<span class="demo-tag">${t('usps.demoShort')}</span>` : ''}
        <h4 style="margin-top:18px">${t('tr.history')}</h4>
        <ol class="timeline">${r.events.map((e) => `<li><b>${esc(e.description)}</b><small>${new Date(e.date).toLocaleString(lang, { dateStyle: 'medium', timeStyle: 'short' })}${e.location ? ' · ' + esc(e.location) : ''}</small></li>`).join('')}</ol>
      </div>`;
    } catch (e) {
      out.innerHTML = `<p class="error" style="margin-top:16px">${esc(e.message)}</p>`;
    }
  }

  function viewStory() {
    return `<section class="hero" style="padding:64px 0"><div class="wrap" style="max-width:860px;text-align:center">
        <div class="eyebrow">${t('story.eyebrow')}</div><h1 style="font-size:clamp(28px,4vw,44px)">${t('story.title')}</h1></div></section>
      <section><div class="wrap"><div class="mvv">
        <div><div class="ico">${I.target}</div><h3>${t('story.purpose')}</h3><p class="muted">${t('story.purposeText')}</p></div>
        <div><div class="ico">${I.mountain}</div><h3>${t('story.mission')}</h3><p class="muted">${t('story.missionText')}</p></div>
        <div><div class="ico">${I.eye}</div><h3>${t('story.vision')}</h3><p class="muted">${t('story.visionText')}</p></div>
      </div></div></section>
      <section style="padding-top:0"><div class="wrap"><div class="section-title"><h2>${t('story.values')}</h2></div>
        <div class="values">${t('values').map((v) => `<div>${v}</div>`).join('')}</div></div></section>
      <section style="padding-top:0"><div class="wrap"><div class="manifesto">
        <div class="eyebrow">${t('story.manifesto')}</div>
        ${t('manifesto').map((m) => `<p>${m}</p>`).join('')}
        <p class="strong">${t('manifesto.strong')}</p><p class="strong" style="font-size:16px">${t('manifesto.end')}</p>
      </div></div></section>`;
  }

  function viewBrands() {
    const makers = [...new Map(PRODUCTS.map((p) => [p.brand, p])).values()].slice(0, 9);
    return `<div class="brand-hero"><div class="wrap" style="max-width:860px">
        <div class="eyebrow" style="color:#4ADE80">${t('b.eyebrow')}</div>
        <h1>${t('b.title1')} <em>${t('b.title2')}</em></h1>
        <p style="font-size:18px">${t('b.lead')}</p>
        <div class="hero-cta"><a href="#apply" class="btn btn-primary" data-scroll="apply">${t('b.apply')}</a><a href="#how" class="btn btn-outline" style="color:#fff" data-scroll="how">${t('b.how')}</a></div>
      </div></div>
      <section id="how"><div class="wrap"><div class="section-title"><h2>${t('b.how')}</h2></div>
        <div class="steps">${t('steps').map(([h, p]) => `<div><h3 style="font-size:17px">${h}</h3><p class="muted" style="margin:0">${p}</p></div>`).join('')}</div></div></section>
      <section style="padding-top:0"><div class="wrap"><div class="section-title"><h2>${t('b.plans')}</h2></div>
        <div class="plans">${t('plans').map(([n, price, com, feats], i) => `<div class="plan ${i === 1 ? 'featured' : ''}">${i === 1 ? `<span class="badge new" style="position:static;align-self:flex-start">${t('b.popular')}</span>` : ''}<h3 style="margin:0">${n}</h3>
          <div><span class="amount">$${price}</span><span class="note">${t('b.month')}</span></div><div class="note"><b>${com}</b> ${t('b.commission')}</div>
          <ul>${feats.map((f) => `<li>${f}</li>`).join('')}</ul><a href="#apply" data-scroll="apply" data-plan="${n}" class="btn ${i === 1 ? 'btn-primary' : 'btn-outline'}">${t('b.choose')}</a></div>`).join('')}</div></div></section>
      <section style="padding-top:0"><div class="wrap"><div class="section-title"><h2>${t('b.showcase')}</h2></div>
        <div class="showcase">${makers.map((p) => `<a class="maker" href="#/shop?q=${encodeURIComponent(p.brand)}" style="text-decoration:none"><div class="av">${p.flag}</div><div><b>${esc(p.brand)}</b><span class="note">${esc(p.country)} · ${catName(p.category)}</span></div></a>`).join('')}</div></div></section>
      <section id="apply" style="padding-top:0"><div class="wrap"><div class="form-card">
        <h2>${t('b.form')}</h2><p class="muted">${t('b.formLead')}</p>
        <form id="brandForm">
          <div class="row"><div class="field"><label for="bf-brand">${t('f.brand')}</label><input id="bf-brand" required></div><div class="field"><label for="bf-contact">${t('f.contact')}</label><input id="bf-contact" required></div></div>
          <div class="row"><div class="field"><label for="bf-email">${t('f.email')}</label><input id="bf-email" type="email" required></div><div class="field"><label for="bf-country">${t('f.country')}</label><select id="bf-country">${['Argentina', 'Bolivia', 'Brasil', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'El Salvador', 'Guatemala', 'Honduras', 'México', 'Nicaragua', 'Panamá', 'Paraguay', 'Perú', 'Puerto Rico', 'Rep. Dominicana', 'Uruguay', 'Venezuela'].map((c) => `<option>${c}</option>`).join('')}</select></div></div>
          <div class="row"><div class="field"><label for="bf-cat">${t('f.category')}</label><select id="bf-cat">${CATEGORIES.map((c) => `<option>${c[lang]}</option>`).join('')}</select></div><div class="field"><label for="bf-plan">Plan</label><select id="bf-plan">${t('plans').map(([n]) => `<option>${n}</option>`).join('')}</select></div></div>
          <div class="field"><label for="bf-site">${t('f.site')}</label><input id="bf-site" placeholder="https:// · @"></div>
          <div class="field"><label for="bf-products">${t('f.products')}</label><textarea id="bf-products" rows="4"></textarea></div>
          <label style="display:flex;gap:10px;align-items:flex-start;font-size:14px;margin-bottom:18px"><input type="checkbox" id="bf-fda" style="margin-top:4px;accent-color:var(--green)"> ${t('f.fda')}</label>
          <button class="btn btn-primary btn-block">${t('f.send')}</button>
          <p class="verified" id="bfOk" hidden>${I.check}<span>${t('f.sent')}</span></p>
        </form>
      </div></div></section>`;
  }

  // ---------------- Router ----------------
  function route() {
    const hash = location.hash.replace(/^#/, '') || '/';
    if (!hash.startsWith('/')) return; // anclas internas
    const [path, qs] = hash.split('?');
    const params = new URLSearchParams(qs || '');
    const parts = path.split('/').filter(Boolean);
    let html;
    switch (parts[0]) {
      case undefined: html = viewHome(); break;
      case 'shop': html = viewShop(params); break;
      case 'product': html = viewProduct(parts[1]); break;
      case 'checkout': html = viewCheckout(); break;
      case 'order': html = viewOrder(parts[1]); break;
      case 'track': html = viewTrack(params); break;
      case 'story': html = viewStory(); break;
      case 'brands': html = viewBrands(); break;
      default: html = `<div class="wrap empty"><h2>404</h2><a class="btn btn-primary" href="#/">KovaShopUSA</a></div>`;
    }
    main.innerHTML = html;
    $$('.main-nav a').forEach((a) => a.classList.toggle('active', a.getAttribute('href') === '#/' + (parts[0] || '') && !a.id));
    $('#mainNav').classList.remove('open');
    $('#menuBtn').setAttribute('aria-expanded', 'false');
    window.scrollTo(0, 0);
    if (parts[0] === 'checkout') bindCheckout();
    if (parts[0] === 'track' && params.get('n')) runTrack(params.get('n'));
    if (parts[0] === 'product') bindProduct(parts[1]);
    $('#searchInput').value = params.get('q') || '';
  }
  function setParam(k, v) {
    const [path, qs] = (location.hash.replace(/^#/, '') || '/shop').split('?');
    const p = new URLSearchParams(qs || '');
    if (v === 'all' || !v) p.delete(k); else p.set(k, v);
    location.hash = '#' + (path.startsWith('/shop') ? path : '/shop') + (p.toString() ? '?' + p : '');
  }
  function bindProduct(id) {
    const p = product(id);
    if (!p) return;
    const q = $('#qVal');
    const getQ = () => Math.max(1, Math.min(20, parseInt(q.value, 10) || 1));
    $('#qDec').onclick = () => { q.value = Math.max(1, getQ() - 1); };
    $('#qInc').onclick = () => { q.value = Math.min(20, getQ() + 1); };
    $('#pdpAdd').onclick = () => addToCart(id, getQ());
    $('#pdpBuy').onclick = () => { addToCart(id, getQ()); location.hash = '#/checkout'; };
    $('#estForm').onsubmit = async (e) => {
      e.preventDefault();
      const zip = $('#estZip').value.trim();
      const out = $('#estOut');
      if (!/^\d{5}$/.test(zip)) { out.innerHTML = `<p class="error">${lang === 'es' ? 'Ingresa un ZIP de 5 dígitos.' : 'Enter a 5-digit ZIP code.'}</p>`; return; }
      store.set('zip', zip);
      out.innerHTML = `<p class="note"><span class="spinner"></span> ${t('loading')}</p>`;
      try {
        const r = await usps.rates(zip, p.weightOz * getQ() + PACKAGING_OZ);
        out.innerHTML = ratesList(r, null, p.price * getQ() >= FREE_SHIP_MIN);
      } catch (err) { out.innerHTML = `<p class="error">${esc(err.message)}</p>`; }
    };
  }

  // ---------------- Eventos globales ----------------
  document.addEventListener('click', (e) => {
    const add = e.target.closest('[data-add]');
    if (add) { addToCart(add.dataset.add); return; }
    const inc = e.target.closest('[data-inc]');
    if (inc) { const it = cart.find((i) => i.id === inc.dataset.inc); setQty(inc.dataset.inc, it.qty + 1); return; }
    const dec = e.target.closest('[data-dec]');
    if (dec) { const it = cart.find((i) => i.id === dec.dataset.dec); setQty(dec.dataset.dec, it.qty - 1); return; }
    const rm = e.target.closest('[data-rm]');
    if (rm) { setQty(rm.dataset.rm, 0); return; }
    if (e.target.closest('[data-close-cart]')) openCart(false);
    const chip = e.target.closest('[data-chip]');
    if (chip) setParam('cat', chip.dataset.chip);
    const sc = e.target.closest('[data-scroll]');
    if (sc) {
      e.preventDefault();
      if (sc.dataset.plan && $('#bf-plan')) $('#bf-plan').value = sc.dataset.plan;
      document.getElementById(sc.dataset.scroll)?.scrollIntoView({ behavior: 'smooth' });
    }
  });
  document.addEventListener('change', (e) => {
    if (e.target.closest('#filters') && e.target.type === 'radio') setParam(e.target.name, e.target.value);
    if (e.target.id === 'sortSel') setParam('sort', e.target.value);
  });
  document.addEventListener('submit', (e) => {
    if (e.target.id === 'trackForm') { e.preventDefault(); const v = $('#trackInput').value; history.replaceState(null, '', '#/track?n=' + encodeURIComponent(v.trim())); runTrack(v); }
    if (e.target.id === 'brandForm') {
      e.preventDefault();
      const apps = store.get('brandApps', []);
      apps.push({ brand: $('#bf-brand').value, email: $('#bf-email').value, plan: $('#bf-plan').value, date: new Date().toISOString() });
      store.set('brandApps', apps);
      e.target.reset();
      $('#bfOk').hidden = false;
    }
  });
  $('#searchForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const q = $('#searchInput').value.trim();
    location.hash = '#/shop' + (q ? '?q=' + encodeURIComponent(q) : '');
  });
  $('#cartBtn').addEventListener('click', () => openCart(true));
  $('#closeCart').addEventListener('click', () => openCart(false));
  $('#scrim').addEventListener('click', () => openCart(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') openCart(false); });
  $('#menuBtn').addEventListener('click', () => {
    const open = $('#mainNav').classList.toggle('open');
    $('#menuBtn').setAttribute('aria-expanded', String(open));
  });
  $('#langBtn').addEventListener('click', () => { lang = lang === 'en' ? 'es' : 'en'; store.set('lang', lang); applyStatic(); route(); renderCart(); renderUspsMode(); });
  window.addEventListener('hashchange', route);

  function applyStatic() {
    document.documentElement.lang = lang;
    $('#langBtn').textContent = lang === 'en' ? 'ES' : 'EN';
    $$('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
    $$('[data-i18n-ph]').forEach((el) => { el.placeholder = t(el.dataset.i18nPh); });
    $('#footerCats').innerHTML = CATEGORIES.map((c) => `<li><a href="#/shop?cat=${c.id}">${c[lang]}</a></li>`).join('');
  }

  let toastTimer;
  function toast(msg) {
    const el = $('#toast');
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('show'), 2200);
  }

  // ---------------- Inicio ----------------
  applyStatic();
  renderCartCount();
  const initDone = usps.init();
  route();
  initDone.then(() => { if (/^#\/product\//.test(location.hash)) route(); });
})();
