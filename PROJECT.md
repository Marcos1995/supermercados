<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/supermercados
- Vista: https://marcos1995.github.io/supermercados/ (repo público; Chrome)
- Vista local: `index.html` (con red: catálogos de las cadenas y OpenStreetMap)

## Estado
- UI tipo Maps: mapa a pantalla completa + panel/sheet plegable (mobile first).
- Lista fija **SEMANAL** (28 tipos). Al abrir carga sola; catálogos se guardan en **IndexedDB** con clave de día local (una descarga de precios por día y zona de almacén).
- Criterio: `docs/EMPAREJADO.md`. Manual: `START.md`. Cobertura: `python scripts/dump_cobertura.py` → `docs/COBERTURA.md` + `tmp-precios/`.
- Precios: Mercadona/Carrefour/Lidl/Aldi. Mapa Overpass: muchas más cadenas (Dia, Alcampo, Consum…); sin catálogo = solo mapa.
- GPS: alta precisión + círculo de accuracy; botones Mi ubicación / centro del mapa. Sin GPS → Madrid centro.
- Concurrencia 8. Sin folletos ni Gemini. No hay precios en el repo (solo caché del navegador).

## Stack
- Un `index.html` (CSS y JS dentro). Leaflet 1.9.4 y teselas de OpenStreetMap. Sin build y sin API de pago.

## Comandos utiles
- Instalar: nada
- Local: `python -m http.server 8766` → http://127.0.0.1:8766/index.html?lat=40.4168&lon=-3.7038
- Manual: `START.md`
- Criterio: `docs/EMPAREJADO.md`

## Notas para el agente
- Emparejado = `docs/EMPAREJADO.md`. No reinventar filtros en cada sesión; si hace falta una regla, se añade al doc y a `lineBan`/`QUERY` en el mismo cambio.
- No inventar importes. No cachear precios en el repo (sí IndexedDB en el cliente, un día). Lean kit (ver AGENTS.md).
