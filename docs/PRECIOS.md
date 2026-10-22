# Precios: fuentes y límites

Detalle del **criterio de ficha** (qué producto vale): `docs/EMPAREJADO.md`.  
Cómo reejecutar a mano: `START.md`.

## Cómo se obtienen

No hay scraping de HTML ni folletos. El navegador pide JSON público:

| Cadena | Fuente | Notas |
|--------|--------|--------|
| Mercadona | Algolia `products_prod_*_es` | Estable; CORS OK |
| Carrefour | Empathy `api.empathy.co` …/carrefour/search | Estable; CORS OK desde github.io |
| Lidl | `lidl.es/q/api/search` | 200 OK, pero indexa mal lácteos/huevos/azúcar; hogar solo en tipos limpieza |
| Aldi | Algolia `an_prd_es_es_*_products2` | Estable; **sin huevos frescos** ni **aceite de girasol** embotellado en el índice |

Dia, Alcampo, Eroski, Consum, Hipercor, BM, etc. **solo mapa** (Overpass/OSM). Sin conector de precios en `index.html`.

### Investigación 2026-10-22 (precios de cadenas extra)

La app es solo navegador + CORS. Hace falta JSON público con `Access-Control-Allow-Origin` usable desde `github.io` (como Mercadona/Carrefour/Lidl/Aldi). Resultado de pruebas reales:

| Cadena | Qué hay | ¿Usable en la web? | Notas |
|--------|---------|-------------------|--------|
| **Consum** | REST JSON `tienda.consum.es/api/rest/V1.0/catalog/product?q=` | **No** | 200 + precios reales (p.ej. leche 0,83 €); **sin header CORS** → el navegador bloquea desde github.io |
| **Dia** | Endpoints `/api/v1/...` | **No** | **403** desde este entorno; scrapers de terceros / Playwright; no API pública CORS |
| **Alcampo** | HTML SSR `compraonline.alcampo.es`; API producto con `regionId` | **No** | Búsqueda = HTML (~1,5 MB); API búsqueda 404/403; hace falta tienda/CP |
| **Eroski** | HTML `supermercado.eroski.es` | **No** | Sin JSON de búsqueda; scrapers HTML |
| **Ahorramas** | Suggest HTML Demandware | **No** | No catálogo JSON CORS |
| **Gadis / Caprabo / Bonpreu** | — | **No** | Sin endpoint JSON CORS verificado |
| **Hipercor / BM / resto mapa** | Solo OSM | **No** | Sin conector de catálogo |

Mapa (Madrid, radio 8 km, Overpass): ~72 Dia, ~13 Mercadona/Carrefour/Lidl, ~10 Alcampo, etc. Esas tiendas **sí** salen en el mapa; el panel las marca «solo mapa · sin catálogo online». No es un fallo de Overpass: **nunca se implementó la fase de precios** para ellas.

## Caché en el navegador

Los catálogos de las **4** cadenas con precios se guardan en IndexedDB con clave `día + almacén Mercadona/Aldi`. Misma visita o recarga el mismo día → no se vuelven a pedir. Al cambiar el día calendario local se recalcula una vez. No hay JSON de precios en el repo. La caché **no** incluye Consum/Dia/etc. (no hay conector).

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
- Dia/Alcampo/Eroski hasta tener JSON usable.
