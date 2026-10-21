# Criterio unificado de emparejado

Fuente de verdad. El código en `index.html` (`pick`, `visibleHits`, `lineBan`, `QUERY`, `FALLBACKS`) implementa esto. Si cambias una regla, cambia este doc en el mismo commit.

## Objetivo

Por cada tipo de la lista semanal (`SEMANAL`) y cada cadena con precios (Mercadona, Carrefour, Lidl, Aldi): **una sola ficha** = producto base del tipo, la más barata por unidad (€/L, €/kg o €/docena). **No se mezclan SKUs entre cadenas.**

Si la API no devuelve un producto base válido → ese tipo queda sin precio en esa cadena. **No se inventa.**

## Pipeline (orden fijo)

1. **Buscar** con `QUERY[tipo]` y, si hay, `FALLBACKS[tipo]` (misma cadena, se fusionan resultados).
2. **Filtrar** candidato (`visibleHits`), todos obligatorios:
   - `price > 0`
   - el nombre contiene los tokens del tipo (`matchToks`)
   - `primaryOk`: el token principal aparece en las **4 primeras** palabras (permite marca delante: `OLI SONE Aceite…`)
   - no es `NOISE` (gadgets, flan, mascotas, etc.)
   - no cae en `lineBan` del tipo (producto base vs elaborado/accesorio)
   - si “solo marca blanca”: `isOwn`
3. **Elegir** (`pick`):
   - preferir nombres que **empiezan** por el token
   - familia de unidad según `EXPECT` (si no hay, la más frecuente entre L/kg/docena/pack)
   - menor €/unidad; empate → menor precio de pack

## Qué cuenta como “producto base”

| Tipo | Vale | No vale |
|------|------|---------|
| Aceites | Botella “aceite de oliva/girasol” | Atún/sardinas en aceite |
| Leche | Leche de vaca | Vegetal, solar, evaporada, fermentada |
| Huevos | Huevos de gallina | Chocolate, flan, pasta |
| Azúcar | Nombre que empieza por “azúcar” | Gofres/yogur “con azúcar” |
| Café | Molido, grano, soluble “de café” | Cappuccino, latte, café con leche bebida |
| Carne picada | Picada / burger meat de carne | Cebolla picada, chocolate |
| Pollo | Pieza/trozo de pollo | Caldo, nugget, paté, empanado, relleno |
| Jamón | Jamón loncheado/pieza | Jamoncitos de pollo |
| Fruta | Fruta fresca (proxy manzana) | Zumo, smoothie, friegasuelos |
| Patatas | Patata fresca | Fritas, gajo, cocidas, snack |
| Tomate | Tomate fresco | Frito, troceado, salsa |
| Lavavajillas | Líquido/gel/pastillas | Sal, abrillantador |
| Jabón | Jabón de manos | Dispensador / organizador |
| Papel cocina | Papel de cocina | Papel vegetal / horno |

Lidl hogar (detergente, lavavajillas, papeles, jabón, champú): se admiten categorías no-Food; el resto Lidl solo Food/F+V.

## APIs (no scrape)

| Cadena | Endpoint | Notas fijas |
|--------|----------|-------------|
| Mercadona | Algolia `products_prod_*_es` | Estable |
| Carrefour | Empathy `api.empathy.co` …/carrefour/search | Estable; CORS OK |
| Lidl | `lidl.es/q/api/search` (mindshift) | Indexa mal lácteos/huevos/azúcar; muchos básicos no salen |
| Aldi | Algolia `an_prd_es_es_*_products2` | Sin huevos frescos ni aceite de girasol embotellado en el índice |

Dia / Alcampo / Eroski: solo mapa (Overpass), sin conector de precios.

## Conteos esperados (Madrid, 28 tipos)

No son un objetivo a forzar inventando fichas:

| Cadena | Esperado | Huecos conocidos |
|--------|----------|------------------|
| Mercadona | 28/28 | — |
| Carrefour | 28/28 | — |
| Aldi | ~24–26/28 | Huevos; aceite de girasol; a veces azúcar si el índice no trae “Azúcar …” |
| Lidl | ~6/28 | El buscador online no indexa la mayoría de básicos |

Verificación paso a paso: `START.md`.
