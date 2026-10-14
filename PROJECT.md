<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/supermercados
- Vista: https://marcos1995.github.io/supermercados/ (repo público; Chrome)
- Vista local: `index.html` (con red: catálogos de las cadenas y OpenStreetMap)

## Estado
- Mapa con filtros: escribes un producto, eliges cualquier marca o solo marca blanca, y ves los supermercados a 8 km. El más barato va arriba.
- Precios del catálogo online de hoy de Mercadona, Carrefour, Lidl y Aldi (el mismo en todas las tiendas de esa cadena). Se ordena por precio de unidad (€/L, €/kg o docena) cuando existe. Dia, Alcampo y el resto salen en el mapa sin precio.
- Sin GPS usa Madrid centro. El precio no es el del lineal de esa tienda.

## Stack
- Un `index.html` (CSS y JS dentro). Leaflet 1.9.4 y teselas de OpenStreetMap. Sin build y sin API de pago.

## Comandos utiles
- Instalar: nada
- Test: abrir `index.html?lat=40.4168&lon=-3.7038&lista=aceite` y comprobar un importe real
- Dev: abrir el archivo en Chrome

## Notas para el agente
- Supuesto: España. Tiendas = Overpass (espejo que responda). Precios = búsqueda JSON de las cuatro cadenas, no HTML. No inventar un importe.
- No cachear precios en el repo. Open Prices no se usa: en España casi no hay precios de artículos.
- Lean kit (ver AGENTS.md)
