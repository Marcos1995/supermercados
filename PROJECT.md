<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/supermercados
- Vista: https://marcos1995.github.io/supermercados/ (repo público; Chrome)
- Vista local: `index.html` (con red: catálogos de las cadenas y OpenStreetMap)

## Estado
- Al buscar, el navegador pide el JSON de búsqueda de la propia web (hasta ~100 fichas por cadena y palabra, 3 páginas). No descarga el catálogo entero, no lo guarda y no lee folletos.
  - Mercadona: Algolia `products_prod_*_es` (almacén mad3, bcn1, vlc1 o svq1 según la zona).
  - Carrefour: Empathy, catálogo food.
  - Lidl: `lidl.es/q/api/search`, surtido ES.
  - Aldi: Algolia `an_prd_es_es_*_products2` (península, Canarias o Baleares).
- Lista separada por comas, hasta 8 palabras. Cada una abre un bloque con todas las fichas de las cuatro cadenas (tipo y formato en el nombre: oliva, girasol, 6 ud, 12 ud). Casilla por ficha; el total suma solo lo marcado. Sin marcar, el total no se inventa. Si una cadena no trae esa palabra, se dice. Arriba, la tienda cercana de la cadena más barata con algo marcado. Filtro de marca blanca. Sin GPS, Madrid centro.
- Dia y Alcampo salen en el mapa sin precio. El precio no es el del lineal. Gemini queda fuera.

## Stack
- Un `index.html` (CSS y JS dentro). Leaflet 1.9.4 y teselas de OpenStreetMap. Sin build y sin API de pago.

## Comandos utiles
- Instalar: nada
- Test: abrir `index.html?lat=40.4168&lon=-3.7038&lista=aceite,huevos,leche`, marcar una ficha por cadena y comprobar el total
- Dev: abrir el archivo en Chrome

## Notas para el agente
- Supuesto: España. Tiendas = Overpass (espejo que responda). Precios = las cuatro búsquedas JSON de Estado, desde el navegador. El total solo cuenta fichas marcadas; no se inventa un importe.
- No cachear precios en el repo. Sin folletos y sin Gemini. Open Prices no se usa: en España casi no hay precios de artículos.
- Lean kit (ver AGENTS.md)
