<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/supermercados
- Vista: https://marcos1995.github.io/supermercados/ (repo público; Chrome)
- Vista local: `index.html` (con red: Open Prices y OpenStreetMap)

## Estado
- Lista de la compra (uno o varios productos). En 8 km, supermercados de OpenStreetMap y precios con prueba de Open Prices. La cesta es un envase de cada producto, el más barato cuyo nombre contiene lo escrito. «Solo marca blanca» filtra marcas de cadena. Si no hay precio, sin dato.
- El total más barato va arriba. El mapa lleva a ese punto; Ruta abre Google Maps con la tienda como destino.
- Sin GPS usa Madrid centro. El precio es el del ticket subido, no el lineal de esta hora.

## Stack
- Un `index.html` (CSS y JS dentro). Leaflet 1.9.4 y teselas de OpenStreetMap. Sin build y sin API de pago.

## Comandos utiles
- Instalar: nada
- Test: abrir la página y comprobar que el hallazgo deja de ser el texto inicial
- Dev: `python -m http.server` en la raíz y abrir la URL local

## Notas para el agente
- Supuesto: España. Precios = Open Prices (Laya). Tiendas = Overpass. No inventar un importe.
- No cachear precios en el repo. No usar el catálogo online de las cadenas.
- Lean kit (ver AGENTS.md)
