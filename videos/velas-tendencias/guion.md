# TENDENCIAS en velas que tienes que usar — "La #3 casi nadie la usa"

Reel vertical 9:16 · ~40-45 s · 6 tomas de ≤ 8 s · avatar IA hablando a cámara · español latino.
Revisión automática (`guion-revisar --sin-llm`): ✔ sin hallazgos.

## Guion por tomas

| # | Intención | Energía | ~s | Voz |
|---|---|---|---|---|
| 1 | Gancho: promete 5 y deja abierta la #3 | Media-alta, intriga | 6 | Cinco tendencias en velas que tienes que usar... y la tres, casi nadie la usa. |
| 2 | #1 Velas con forma | Alta, ritmo rápido | 6.5 | Número uno: velas con forma. Burbujas, espirales, nudos... Hay quien ni las prende: son pura decoración. |
| 3 | #2 Mecha de madera (sensorial) | Baja, cálida | 7 | Número dos: mecha de madera. Cuando la enciendes, chisporrotea suavecito... como una chimenea chiquita en tu mesa. |
| 4 | #3 La secreta: mezclar aromas (punto íntimo) | Íntima → sube al final | 6.5 | Y la tres, la secreta: mezclar aromas. Vainilla con café... y tu casa huele a ti. |
| 5 | #4 Envases reutilizables | Media, práctica | 7.5 | Número cuatro: envases que se reutilizan. Se acaba la vela... y te queda un vaso o una maceta. |
| 6 | #5 Colores tierra + CTA (callback a la #3) | Alta, sonriendo | 7 | Y la cinco: colores tierra. Terracota, arena, verde oliva. Guárdalo... y dime, ¿la tres ya la usabas? |

## Voz con emociones (ElevenLabs v3) — listo para pegar

```
[intrigante, voz baja y cercana] Cinco tendencias en velas que tienes que usar... [pausa corta] [cómplice, sonriendo] y la tres, casi nadie la usa.

[enérgica, ritmo rápido] Número uno: velas con forma. Burbujas, espirales, nudos... [divertida] Hay quien ni las prende: son pura decoración.

[cálida, más lento] Número dos: mecha de madera. Cuando la enciendes, chisporrotea suavecito... [suave, soñadora] como una chimenea chiquita en tu mesa.

[voz baja, como contando un secreto] Y la tres, la secreta: mezclar aromas. [pausa corta] Vainilla con café... [cálida, la energía sube] y tu casa huele a ti.

[práctica, segura] Número cuatro: envases que se reutilizan. Se acaba la vela... [sonriendo] y te queda un vaso o una maceta.

[animada] Y la cinco: colores tierra. Terracota, arena, verde oliva. [pausa corta] [sonriendo, invitante] Guárdalo... y dime, ¿la tres ya la usabas?
```

## Voz sin etiquetas

```
Cinco tendencias en velas que tienes que usar... y la tres, casi nadie la usa.
Número uno: velas con forma. Burbujas, espirales, nudos... Hay quien ni las prende: son pura decoración.
Número dos: mecha de madera. Cuando la enciendes, chisporrotea suavecito... como una chimenea chiquita en tu mesa.
Y la tres, la secreta: mezclar aromas. Vainilla con café... y tu casa huele a ti.
Número cuatro: envases que se reutilizan. Se acaba la vela... y te queda un vaso o una maceta.
Y la cinco: colores tierra. Terracota, arena, verde oliva. Guárdalo... y dime, ¿la tres ya la usabas?
```

**Por qué funciona el arco:** el gancho abre un bucle (la #3) que mantiene a la gente mirando hasta la mitad; la #3 es el punto íntimo (voz de secreto) y la #5 cierra con energía alta y vuelve a la #3 para provocar comentarios ("yo sí / yo no") y guardados.

## Avatar IA

**Prompt de referencia del personaje** (genera una imagen y úsala en las 6 tomas para mantener cara y ropa):

> Mujer latina de 30 años, cabello castaño ondulado suelto, maquillaje natural, suéter tejido color crema, sentada en una sala acogedora de tonos tierra; detrás, una repisa de madera con velas encendidas de formas esculturales (burbuja, espiral) en terracota y arena; luz cálida de atardecer, desenfoque suave de fondo; plano medio vertical 9:16, mirando a cámara, estética de celular, realista.

**Negative prompt (todas las tomas):** texto en pantalla, logos, manos deformes, dedos extra, llamas exageradas, humo negro, cortes bruscos, labios desincronizados, mirada perdida.

## Plan de producción por toma

| # | Plano del avatar (prompt de video) | Texto en pantalla | B-roll / inserto (2-3 s sobre la voz) |
|---|---|---|---|
| 1 | Plano medio, se inclina un poco hacia cámara y sonríe con complicidad al decir "casi nadie la usa". | **TENDENCIAS EN VELAS** · abajo: "la #3 casi nadie la usa 👀" | Barrido rápido por la repisa con velas encendidas. |
| 2 | Plano medio, gesticula enumerando con la mano, energía alta. | **#1 Velas con forma** | Velas burbuja, espiral y de nudo sobre una mesa clara, giro de 180°. |
| 3 | Punch-in (plano más cerrado), voz suave, mira de reojo a la vela. | **#2 Mecha de madera** | Macro de una mecha de madera encendiéndose (con sonido de chisporroteo). |
| 4 | Plano cerrado, se acerca a cámara como contando un secreto; al final sonríe. | **#3 Mezclar aromas 🤫** · "vainilla + café" | Dos velas encendiéndose a la vez, una junto a la otra, humo suave cruzándose. |
| 5 | Vuelve al plano medio, tono práctico, levanta un vaso de vidrio vacío. | **#4 Envases reutilizables** | Transición: vela consumida → mismo frasco con una suculenta / como vaso. |
| 6 | Plano medio, sonríe y señala hacia abajo (comentarios). | **#5 Colores tierra** · luego "¿La #3 ya la usabas? 👇" | Paleta: velas terracota, arena y verde oliva en fila. |

**Edición:** cortes secos con punch-in entre tomas (no fundidos), subtítulos TikTok de 2-3 palabras, música lo-fi cálida baja (-20 dB bajo la voz), sonido de cerillo al inicio de la toma 1 y chisporroteo en la toma 3.

Para armarlo con el compositor del repo:

```bash
python -m ugc_agency compose toma1.mp4 toma2.mp4 toma3.mp4 toma4.mp4 toma5.mp4 toma6.mp4 --graphics videos/velas-tendencias/graficos.json --out reel_velas.mp4
```

## Publicación

**Caption:**
Guarda esto para tu próxima compra de velas 🕯️ La #3 cambió cómo huele mi casa… ¿tú ya la usabas? Cuéntame tu combinación de aromas 👇

**Hashtags:** #velas #velasaromaticas #decoracion #decoracionhogar #tendenciasdeco #homedecor #velasartesanales #hogarcalido

**Comentario fijado:** ¿Qué combo de aromas pruebo en el próximo video? Vainilla + café ya lo tengo 😏

**Cumplimiento:** el avatar es generado con IA → activa la etiqueta de contenido IA de TikTok/Instagram/YouTube al publicar. Si el video promociona velas propias o de una marca, agrega la divulgación correspondiente (#ad / colaboración pagada).

## Pendientes

- ¿El video promociona una marca o tienda de velas? Si sí, dime el nombre/CTA (p. ej. "link en mi perfil") y ajusto la toma 6.
- Imágenes/clips de B-roll: generarlos con IA o usar fotos de tus productos.
- Voz del avatar: elegir voz (ElevenLabs) o la que trae tu herramienta de avatar.
