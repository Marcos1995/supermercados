# Arrancar a mano

Sin install. Hace falta red (APIs de las cadenas + mapa).

## Criterio de fichas (no reinventar)

[`docs/EMPAREJADO.md`](docs/EMPAREJADO.md) — qué producto vale, pipeline de filtros, huecos Lidl/Aldi.

## Producción

https://marcos1995.github.io/supermercados/?lat=40.4168&lon=-3.7038

1. **Todo** (o marca tipos).
2. Marca: **Cualquier marca** o **Solo marca blanca**.
3. **Ver precios**.
4. Mira ranking + mapa.

## Local

```bash
python -m http.server 8766
```

Abre: http://127.0.0.1:8766/index.html?lat=40.4168&lon=-3.7038

(En Windows también: `start index.html` — algunas APIs pueden fallar con `file://`; preferible el servidor.)

## Comprobar conteos (DevTools)

Tras **Ver precios**, en la consola:

```js
Object.fromEntries(
  ["mercadona","carrefour","lidl","aldi"].map((chain) => {
    let n = 0;
    const missing = [];
    const got = {};
    for (const line of SEMANAL) {
      const p = pick((catalogs[chain] && catalogs[chain][line]) || [], line, false, chain);
      if (p) { n++; got[line] = p.name; } else missing.push(line);
    }
    return [chain, { picked: n, of: SEMANAL.length, missing, got }];
  })
);
```

Esperado (Madrid, 28 tipos): Mercadona/Carrefour 28; Aldi ~24–26 (sin huevos ni girasol); Lidl ~6 (límite del buscador). Detalle: `docs/EMPAREJADO.md`.
