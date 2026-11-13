// Plantilla de interior para libro impreso (KDP tapa blanda). La rellena ugc_agency/ebooks/maquetacion.py.
#let titulo-libro = [{{titulo}}]
#let subtitulo-libro = [{{subtitulo}}]
#let autor-libro = [{{autor}}]
#let tinta = rgb("{{color_tinta}}")
#let gris = rgb("#6b6b6b")
#let acento = rgb("{{color_acento}}")
#let sans = ("Lato", "Inter")

#set document(title: "{{titulo}}", author: "{{autor}}")
#set text(font: "{{fuente}}", size: {{cuerpo}}, lang: "{{idioma}}", fill: tinta, hyphenate: true,
          number-type: "old-style")
#set par(justify: true, leading: 0.68em, first-line-indent: (amount: 1.2em, all: false), spacing: 0.68em)
#set page(
  width: {{ancho}}, height: {{alto}},
  margin: {{margen}},
  binding: left,
)

#show heading: set text(hyphenate: false)
#show heading: set par(justify: false)
// ---------- elementos que emite Pandoc
#let horizontalrule = align(center, block(above: 1.2em, below: 1.2em, text(fill: gris)[#sym.ast.op #h(0.8em) #sym.ast.op #h(0.8em) #sym.ast.op]))
#let blockquote(cuerpo) = block(
  width: 100%, inset: (left: 1em, right: 0.8em, y: 0.7em), above: 1.1em, below: 1.1em,
  stroke: (left: 2pt + acento), fill: rgb("{{color_recuadro}}"),
  { set par(first-line-indent: 0em); set text(size: 0.95em); cuerpo },
)
#show heading.where(level: 2): it => block(above: 1.6em, below: 0.8em, sticky: true,
  text(font: sans, weight: "bold", size: 1.05em, fill: tinta, it.body))
#show heading.where(level: 3): it => block(above: 1.2em, below: 0.6em, sticky: true,
  text(font: sans, weight: "bold", size: 0.92em, fill: gris, it.body))
#show heading.where(level: 4): it => block(above: 1em, below: 0.5em, sticky: true, emph(it.body))
#show list: set block(above: 0.9em, below: 0.9em)
#show list: set par(justify: false)
#show enum: set par(justify: false)
#show enum: set block(above: 0.9em, below: 0.9em)
#set list(indent: 0.6em, marker: text(fill: acento)[•])
#set enum(indent: 0.6em)
#show table: set text(size: 0.88em)
#set table(stroke: 0.5pt + gris, inset: 6pt)
#show link: it => it.body
#set footnote.entry(separator: line(length: 25%, stroke: 0.4pt))

// ---------- páginas preliminares (sin cabecera ni folio)
#set page(header: none, footer: none)
{{portada}}
#align(center + horizon)[
  #text(size: 2.2em, weight: "bold")[#titulo-libro]
  #v(0.6em)
  #text(size: 1.1em, style: "italic", fill: gris)[#subtitulo-libro]
  #v(3em)
  #text(font: sans, size: 0.9em, tracking: 0.12em)[#upper(autor-libro)]
]
#pagebreak()
#align(bottom)[
  #set text(size: 0.78em, fill: gris)
  #set par(first-line-indent: 0em, justify: false)
  {{creditos}}
]
#pagebreak(to: {{abrir}})
#text(font: sans, weight: "bold", size: 1.3em)[Índice]
#v(1em)
#outline(title: none, depth: 1, indent: 0em)
#show outline.entry: set text(size: 0.95em)
#metadata(none) <fin-bloque>

// ---------- cuerpo: cabeceras vivas y folios; nada en páginas que abren capítulo
#let abre-capitulo() = {
  let aqui = here().page()
  query(heading.where(level: 1)).any(h => h.location().page() == aqui)
}
// Página en blanco que deja un capítulo para abrir en impar: el bloque anterior acabó en la página previa
// y el siguiente capítulo abre en la próxima.
#let pagina-blanca() = {
  let aqui = here().page()
  query(<fin-bloque>).any(m => m.location().page() == aqui - 1) and query(heading.where(level: 1)).any(h => h.location().page() == aqui + 1)
}
#set page(
  header: context {
    if abre-capitulo() or pagina-blanca() { return }
    let pag = here().page()
    set text(font: sans, size: 0.7em, fill: gris, tracking: 0.08em)
    if calc.even(pag) {
      upper(titulo-libro)
    } else {
      let previos = query(heading.where(level: 1)).filter(h => h.location().page() <= pag)
      if previos.len() > 0 { align(right, upper(previos.last().body)) }
    }
  },
  footer: context {
    if pagina-blanca() { return }
    let pag = here().page()
    set text(size: 0.85em, fill: gris)
    if calc.even(pag) { counter(page).display() } else { align(right, counter(page).display()) }
  },
)
#counter(page).update({{inicio_folio}})

#let capitulo(numero: none, titulo: none) = {
  [#metadata(none) <fin-bloque>]
  pagebreak(to: {{abrir}}, weak: true)
  v(1.4in)
  if numero != none {
    text(font: sans, size: 0.8em, tracking: 0.25em, fill: acento)[CAPÍTULO #numero]
    v(0.4em)
  }
  heading(level: 1, outlined: true, titulo)
  v(0.3in)
  line(length: 2.5em, stroke: 1.2pt + acento)
  v(0.35in)
}
#show heading.where(level: 1): it => block(below: 0em, text(size: 1.9em, weight: "regular", hyphenate: false, it.body))
