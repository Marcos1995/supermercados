<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/supermercados
- Vista: https://marcos1995.github.io/supermercados/ (repo público; Chrome)
- Vista local: `index.html` (con red: catálogos de las cadenas y OpenStreetMap)

## Estado
- Lista fija de **compra semanal** (`SEMANAL` en `index.html`): tipos unificados (aceite de oliva, aceite de girasol, huevos, leche, papel de cocina, papel higiénico, etc.). Casillas para marcar qué entra. Filtro cualquier marca / solo marca blanca. Botón Ver precios.
- Al buscar, el navegador pide el JSON de la propia web solo de los tipos marcados (hasta ~100 fichas por cadena y palabra). Por cada tipo y cadena se elige **sola** la ficha más barata por litro, kilo o docena. No se mezclan SKUs entre súpers. Debajo, “qué eligió” en solo lectura.
  - Mercadona: Algolia `products_prod_*_es` (almacén mad3, bcn1, vlc1 o svq1).
  - Carrefour: Empathy, catálogo food.
  - Lidl: `lidl.es/q/api/search`, surtido ES.
  - Aldi: Algolia `an_prd_es_es_*_products2`.
- El mapa (8 km) ordena por el total de esos packs. Sin GPS, Madrid centro. Dia y Alcampo sin precio. Sin folletos ni Gemini. No se archiva el catálogo.

## Stack
- Un `index.html` (CSS y JS dentro). Leaflet 1.9.4 y teselas de OpenStreetMap. Sin build y sin API de pago.

## Comandos utiles
- Instalar: nada
- Test: abrir `index.html?lat=40.4168&lon=-3.7038`, dejar aceite de oliva / huevos / leche, Ver precios, comprobar un total
- Dev: abrir el archivo en Chrome

## Notas para el agente
- Supuesto: España. Tiendas = Overpass. Precios = búsquedas JSON; criterio = menor €/unidad por tipo y cadena. No inventar importes.
- No cachear precios en el repo. Lean kit (ver AGENTS.md)
