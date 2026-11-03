/**
 * ─────────────────────────────────────────────────────────────────────────
 *  MARCA WHITE-LABEL — ÚNICO PUNTO DE CONFIGURACIÓN DEL FRONTEND
 * ─────────────────────────────────────────────────────────────────────────
 *  Todo lo que identifica al producto (nombre, colores, logo, textos)
 *  se define AQUÍ. Para vender la plataforma a otra empresa basta con:
 *
 *    1. Cambiar los valores de este archivo (marca «de fábrica»), y/o
 *    2. Ajustar la marca en tiempo de ejecución desde la consola de
 *       Administración → «Personalización» (los valores del servidor,
 *       servidos por GET /api/branding/, tienen prioridad sobre estos).
 *
 *  Los colores se publican como variables CSS (--azul, --amarillo,
 *  --beige, --rojo) y todo el sistema de diseño deriva tonalidades
 *  con color-mix(), así que cambiar `primaryColor` recolorea la
 *  plataforma entera: botones, héroe, tarjetas, gráficos y certificado.
 * ─────────────────────────────────────────────────────────────────────────
 */
export const BRAND = {
  /** Nombre de la plataforma (encabezado, login, certificado). */
  platformName: 'Academia',

  /** Empresa del cliente. Vacío = producto sin marca de cliente. */
  companyName: '',

  /** Lema mostrado bajo el nombre / en el héroe del estudiante. */
  tagline: 'Formación corporativa, simple y medible.',

  /** Color principal de marca (botones, héroe, enlaces, progreso). */
  primaryColor: '#4F46E5',

  /** Color de acento (detalles, estados activos, certificado). */
  accentColor: '#F59E0B',

  /** Color neutro cálido (segmentos «sin iniciar», fondos suaves). */
  neutralColor: '#CBD5E1',

  /** Color de alerta (vencimientos, errores). */
  dangerColor: '#DC2626',

  /** URL del logo del cliente. Vacío = marca gráfica por defecto. */
  logoUrl: '',

  /** Texto del pie de página. */
  footerText: 'Plataforma corporativa de capacitación',

  /** Prefijo de los identificadores de certificado (p. ej. ACD-2026-000123). */
  certificatePrefix: 'ACD',
}

export default BRAND
