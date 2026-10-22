<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/supermercados
- Vista: https://marcos1995.github.io/supermercados/ (repo público; Chrome)
- Vista local: `index.html` (con red: catálogos de las cadenas y OpenStreetMap)

## Estado
- UI tipo Maps: mapa a pantalla completa + panel/sheet plegable (mobile first).
- Lista fija **SEMANAL** (28 tipos). Criterio de ficha: `docs/EMPAREJADO.md` (código en `index.html` / scripts; no lo inventa la IA).
- Comparativa: vivas (Mercadona/Carrefour/Lidl/Aldi) + dump `data/precios-latest.json` (Consum/Dia/Eroski/Ahorramas). Mapa Overpass: más cadenas; Alcampo sin precios.
- Refresco dump: `python scripts/dump_all_precios.py` (manual `START.md`).
- GPS: alta precisión + círculo; Mi ubicación / centro del mapa. Sin GPS → Madrid centro.
- Concurrencia 8. Sin folletos ni Gemini.

## Stack
- Un `index.html` (CSS y JS dentro). Leaflet 1.9.4 y teselas de OpenStreetMap. Sin build y sin API de pago.
- Scripts Python: `scripts/dump_all_precios.py`, `scripts/dump_cobertura.py`.

## Comandos utiles
- Instalar: nada
- Local: `python -m http.server 8766` → http://127.0.0.1:8766/index.html?lat=40.4168&lon=-3.7038
- Refresco precios (todas las cadenas con fuente): `python scripts/dump_all_precios.py`
- Cobertura 4 cadenas: `python scripts/dump_cobertura.py`
- Manual: `START.md`
- Criterio: `docs/EMPAREJADO.md`

## Notas para el agente
- Emparejado = `docs/EMPAREJADO.md`. No reinventar filtros; regla nueva → doc + código.
- No inventar importes. Dump en `data/` solo con lo que devolvió la red. Lean kit (ver AGENTS.md).
