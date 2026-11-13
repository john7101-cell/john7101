/**
 * Guarda los registros de la landing "Apegos Emocionales" en una Hoja de cálculo de Google.
 *
 * CÓMO CONFIGURARLO (5 minutos, gratis):
 * 1. Crea una Hoja de cálculo nueva en Google Drive (por ejemplo "Asistentes Apegos Emocionales").
 * 2. En la hoja: menú Extensiones → Apps Script.
 * 3. Borra el código que aparece, pega TODO este archivo y guarda (icono de disquete).
 * 4. Botón "Implementar" → "Nueva implementación" → tipo "Aplicación web".
 *      - Ejecutar como: Yo
 *      - Quién tiene acceso: Cualquier usuario
 *    Pulsa "Implementar" y autoriza los permisos con tu cuenta de Google.
 * 5. Copia la "URL de la aplicación web" (termina en /exec) y pégala en index.html,
 *    en CONFIG.SCRIPT_URL.
 *
 * Cada registro aparecerá como una fila nueva en la pestaña "Registros".
 * Si cambias este código, vuelve a "Implementar" → "Gestionar implementaciones" → editar → "Nueva versión".
 */

const SHEET_NAME = "Registros";
const FIELDS = ["fecha_registro", "nombre", "correo", "telefono", "ciudad", "origen", "expectativa", "consentimiento", "pagina"];
const HEADERS = ["Fecha de registro", "Nombre", "Correo", "Teléfono", "Ciudad", "¿Cómo se enteró?", "Qué quiere trabajar", "Consentimiento", "Página"];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
    }
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold").setBackground("#F6EFEC");
      sheet.setFrozenRows(1);
    }
    const p = (e && e.parameter) || {};
    // Evita que un texto que empiece por =, +, - o @ se ejecute como fórmula.
    const clean = v => {
      const s = String(v == null ? "" : v).slice(0, 1000);
      return /^[=+\-@]/.test(s) ? "'" + s : s;
    };
    sheet.appendRow(FIELDS.map(f => clean(p[f])));
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

function doGet() {
  return ContentService.createTextOutput("El formulario de Apegos Emocionales está activo.");
}
