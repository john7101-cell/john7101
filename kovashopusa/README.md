# KovaShopUSA — maqueta de tienda en línea

Maqueta funcional de **KovaShopUSA** ("Discover what's next."): un marketplace curado que vende productos de marcas latinoamericanas a consumidores de Estados Unidos y funciona como **vitrina para emprendedores**. Los envíos se hacen con **USPS** desde un centro de fulfillment en Miami, FL.

Usa el branding oficial: azul marino `#0D1B3D`, verde `#15803D`, dorado `#D4AF37`, `#F5F5F5`, `#333333` y las tipografías Poppins y Manrope.

## Qué incluye

| Página | Ruta | Qué hace |
|---|---|---|
| Inicio | `#/` | Hero, canales (Amazon, TikTok Shop, Shopify), categorías, destacados, sello *Kova Curated™*, promesa de marca |
| Tienda | `#/shop` | Filtros por categoría, precio y país de origen, búsqueda y orden |
| Producto | `#/product/:id` | Ficha, cantidad y **estimador de envío USPS por ZIP** |
| Carrito | (panel lateral) | Barra de envío gratis (más de $75) |
| Checkout | `#/checkout` | Autocompleta ciudad y estado desde el ZIP, **verifica la dirección con USPS** (ZIP+4), muestra **tarifas USPS en vivo** (Ground Advantage, Priority, Priority Express); el pago es simulado |
| Confirmación | `#/order/:id` | Número de pedido y número de rastreo USPS |
| Rastreo | `#/track` | **Rastreo USPS** por número de guía o de pedido |
| Para marcas | `#/brands` | Vitrina para emprendedores: cómo funciona, planes, marcas y formulario de postulación |
| Nuestra historia | `#/story` | Propósito, misión, visión, valores y manifiesto |

Todo el sitio está en inglés y español (botón **ES/EN**) y se adapta a celular.

## Cómo correrlo

Necesitas Node 18 o superior. No hay que instalar dependencias.

```bash
cd kovashopusa
```

```bash
npm start
```

Abre <http://localhost:3000>. Sin credenciales funciona en **modo demo**: las tarifas, direcciones y rastreos son simulados y la página lo indica con una etiqueta "demo". Si abres `public/index.html` directamente, sin servidor, también funciona en modo demo.

Pruebas:

```bash
npm test
```

## Conectar la API real de USPS

1. Crea una cuenta en <https://developers.usps.com>, crea una app y copia el **Consumer Key** y el **Consumer Secret**.
2. Copia `.env.example` como `.env` y completa los datos:

   ```
   USPS_CLIENT_ID=tu_consumer_key
   USPS_CLIENT_SECRET=tu_consumer_secret
   USPS_ENV=test          # test = apis-tem.usps.com · production = apis.usps.com
   SHIP_FROM_ZIP=33166    # ZIP desde donde salen los paquetes
   ```
3. Reinicia con `npm start`. La consola y el pie de página dirán "USPS API: connected".

Las credenciales se quedan en el servidor (`server.js`), nunca llegan al navegador.

### APIs de USPS que se usan (v3)

| Función | Endpoint de USPS | Ruta en la maqueta |
|---|---|---|
| Token OAuth 2.0 | `POST /oauth2/v3/token` | (interno, el token se guarda en caché) |
| Verificar dirección | `GET /addresses/v3/address` | `POST /api/usps/address` |
| Ciudad y estado por ZIP | `GET /addresses/v3/city-state` | `GET /api/usps/city-state?zip=` |
| Tarifas | `POST /prices/v3/base-rates/search` | `POST /api/usps/rates` |
| Rastreo | `GET /tracking/v3/tracking/{n}` | `GET /api/usps/track/:n` |

## Lo que falta para producción

- **Etiquetas de envío**: hoy el número de rastreo del pedido es simulado. Para generar etiquetas reales hace falta la API de Labels de USPS (`/labels/v3/label`), que pide una cuenta de pago (EPS o Permit), el token de pago (`/payments/v3/payment-authorization`) y la aprobación de USPS.
- **Pagos reales**: por ejemplo con Stripe o Shopify Checkout.
- **Impuesto sobre las ventas** según el estado (por ejemplo con Stripe Tax o TaxJar).
- **Base de datos** de productos, pedidos y postulaciones de marcas. Hoy se guardan en el navegador (`localStorage`).
- **Fotos reales** de producto. Hoy los productos son ilustraciones SVG.
- Los productos y las marcas del catálogo son ficticios.

## Estructura

```
kovashopusa/
├── server.js            # servidor HTTP: archivos estáticos + /api/usps/*
├── usps.js              # cliente de la API v3 de USPS (OAuth, direcciones, tarifas, rastreo)
├── public/
│   ├── index.html       # estructura de la página
│   ├── styles.css       # estilos con el branding
│   ├── app.js           # rutas, carrito, checkout, rastreo, idiomas
│   ├── products.js      # catálogo de prueba e ilustraciones SVG
│   └── usps-mock.js     # datos simulados de USPS (los usan el servidor y el navegador)
└── tests/usps.test.js
```
