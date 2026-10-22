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

Dia, Alcampo, Eroski, Consum, Hipercor, BM, etc. solo mapa (OpenStreetMap). Sin conector de precios (fase posterior si hay JSON+CORS).

## Caché en el navegador

Los catálogos de las 4 cadenas se guardan en IndexedDB con clave `día + almacén Mercadona/Aldi`. Misma visita o recarga el mismo día → no se vuelven a pedir. Al cambiar el día calendario local se recalcula una vez. No hay JSON de precios en el repo.

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
