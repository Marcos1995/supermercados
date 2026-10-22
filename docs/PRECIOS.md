# Precios: fuentes y límites

Detalle del **criterio de ficha** (qué producto vale): `docs/EMPAREJADO.md` — implementado en código (`lineBan` / `pick` / `QUERY`), no lo elige la IA al vuelo.  
Refresco manual de todos los precios: `START.md` → `python scripts/dump_all_precios.py`.

## Cómo se obtienen

No hay scraping de HTML ni folletos. El navegador pide JSON público:

| Cadena | Fuente | Notas |
|--------|--------|--------|
| Mercadona | Algolia `products_prod_*_es` | Estable; CORS OK |
| Carrefour | Empathy `api.empathy.co` …/carrefour/search | Estable; CORS OK desde github.io |
| Lidl | `lidl.es/q/api/search` | 200 OK, pero indexa mal lácteos/huevos/azúcar; hogar solo en tipos limpieza |
| Aldi | Algolia `an_prd_es_es_*_products2` | Estable; **sin huevos frescos** ni **aceite de girasol** embotellado en el índice |

Dia, Alcampo, Eroski, Consum, Hipercor, BM, etc. **solo mapa** (Overpass/OSM). Sin conector de precios en `index.html`.

### Dump terminal 2026-10-22 (sin CORS)

Script: `python scripts/dump_all_precios.py` → [`data/precios-2026-10-22.json`](../data/precios-2026-10-22.json) (lista SEMANAL × cadenas; solo `price > 0`).

| Cadena | Productos | Plan usado |
|--------|----------:|------------|
| Mercadona | 1031 | A: Algolia |
| Carrefour | 1443 | A: Empathy |
| Lidl | 376 | A: lidl.es/q/api |
| Aldi | 671 | A: Algolia |
| Consum | 2306 | A: REST `tienda.consum.es` (sin CORS en browser) |
| Eroski | 737 | B: HTML `supermercado.eroski.es` |
| Dia | 1619 | B: `search-back/search` en **páginas pequeñas** + cookies (el endpoint `standard_search` 404; requests grandes → 403) |
| Ahorramas | 774 | B: HTML Demandware `Search-UpdateGrid` |
| **Alcampo** | **0** | A search 202 vacío; B home con `retailerProductId` (también `73514-FILETES`); C API `bop` 202 vacío — **sin precios tras agotar** |
| Resto mapa (Hipercor, BM, Gadis…) | 0 | Sin fuente JSON/HTML usable conocida |

**Browser (`index.html`)**: Mercadona/Carrefour/Lidl/Aldi en vivo (CORS) + el resto con datos desde `data/precios-latest.json` (mismo criterio `EMPAREJADO` / `pick`). Sin datos en dump → solo mapa.

## Caché en el navegador

Los catálogos de las **4** cadenas de la web se guardan en IndexedDB con clave `día + almacén Mercadona/Aldi`. Misma visita o recarga el mismo día → no se vuelven a pedir.

El dump offline (`data/precios-*.json`) sí vive en el repo: lo genera el script Python, no la IA. Incluye Consum/Dia/Eroski/Ahorramas cuando la red responde.

## Causas (resuelto / aceptado)

1. Carrefour/Lidl no fallaban por CORS: fallaba el emparejado flojo → criterio en `EMPAREJADO.md`.
2. Lidl: no inventar precio con gadgets; Food/F+V (+ hogar en limpieza).
3. Aldi: huevos/girasol ausentes en Algolia = hueco real.
4. `QUERY` / `FALLBACKS` / cola de 8 peticiones en paralelo.

## Conteos de referencia (Madrid, 28 tipos)

| Cadena | Tipos con precio | Notas |
|--------|------------------|--------|
| Mercadona | **28 / 28** | |
| Carrefour | **28 / 28** | |
| Aldi | **~24–26 / 28** | Sin huevos ni girasol; a veces azúcar |
| Lidl | **~6 / 28** | Límite del buscador online |

## Qué no se promete

- Catálogo completo de Lidl/Aldi si su API no lo indexa.
- Precio del lineal de una tienda concreta.
- Precio de **Alcampo** en el dump hasta que deje de devolver HTTP 202 vacío (búsqueda y `bop`).
- Conectores CORS en el navegador para Consum/Dia/Eroski (hoy solo dump terminal).
