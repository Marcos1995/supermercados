<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/supermercados
- Vista: https://marcos1995.github.io/supermercados/ (repo público; Chrome)
- Vista local: `index.html` (con red: catálogos de las cadenas y OpenStreetMap)

## Estado
- Lista fija **SEMANAL** (28 tipos). Una ficha por tipo y cadena = más barata por unidad.
- Criterio de emparejado **fijo y documentado**: `docs/EMPAREJADO.md` (código = ese doc). Cómo lanzarlo a mano: `START.md`.
- JSON en vivo (no HTML). Fuentes/huecos: `docs/PRECIOS.md`.
- Mercadona/Carrefour ~28/28; Aldi sin huevos ni girasol en Algolia; Lidl indexa pocos básicos. Dia/Alcampo/Eroski: solo mapa.
- Concurrencia 8. Sin GPS → Madrid centro. Sin folletos ni Gemini.

## Stack
- Un `index.html` (CSS y JS dentro). Leaflet 1.9.4 y teselas de OpenStreetMap. Sin build y sin API de pago.

## Comandos utiles
- Instalar: nada
- Local: `python -m http.server 8766` → http://127.0.0.1:8766/index.html?lat=40.4168&lon=-3.7038
- Manual: `START.md`
- Criterio: `docs/EMPAREJADO.md`

## Notas para el agente
- Emparejado = `docs/EMPAREJADO.md`. No reinventar filtros en cada sesión; si hace falta una regla, se añade al doc y a `lineBan`/`QUERY` en el mismo cambio.
- No inventar importes. No cachear precios en el repo. Lean kit (ver AGENTS.md).
