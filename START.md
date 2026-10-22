# Arrancar a mano

Sin install. Hace falta red (APIs de las cadenas + mapa).

## Criterio unificado (código, no la IA)

Qué ficha vale y qué se descarta está **implementado** en el repo, no lo decide un agente al vuelo:

| Qué | Dónde |
|-----|--------|
| Lista de tipos | `SEMANAL` en `index.html` y en `scripts/dump_*.py` |
| Consultas / fallbacks | `QUERY`, `FALLBACKS` |
| Filtros de emparejado | `docs/EMPAREJADO.md` → `lineBan` / `primaryOk` / `NOISE` en `index.html` y `dump_cobertura.py` |
| Fuentes por cadena | `docs/PRECIOS.md` + funciones `search_*` en los scripts |

Si hace falta una regla nueva: se añade al doc **y** al código en el mismo cambio. No inventar precios.

## Refresco manual de TODOS los precios (dump)

Desde la raíz del repo:

```bash
python scripts/dump_all_precios.py
```

- Recorre la lista **SEMANAL** × cada cadena con fuente (Mercadona, Carrefour, Lidl, Aldi, Consum, Dia, Eroski, Ahorramas; intenta Alcampo).
- Solo guarda hits con `price > 0`. Si una cadena no responde, queda a 0 con errores en el JSON (no se rellenan datos falsos).
- Escribe:
  - `data/precios-YYYY-MM-DD.json` — productos
  - `data/precios-YYYY-MM-DD.summary.json` — conteos por cadena
- Último dump de referencia: [`data/precios-2026-10-22.json`](data/precios-2026-10-22.json).

Detalle de fuentes / huecos (p. ej. **Alcampo = 0** tras agotar API y HTML): [`docs/PRECIOS.md`](docs/PRECIOS.md).

### Cobertura de emparejado (las 4 del navegador)

```bash
python scripts/dump_cobertura.py
```

Salida local: `tmp-precios/` (gitignored) + actualiza `docs/COBERTURA.md`.

## Producción (web)

https://marcos1995.github.io/supermercados/?lat=40.4168&lon=-3.7038

La web compara **todas las cadenas con precios**:
- En vivo (CORS): Mercadona, Carrefour, Lidl, Aldi.
- Desde `data/precios-latest.json` (dump): Consum, Dia, Eroski, Ahorramas (y las que el script haya rellenado).
- Solo mapa: Alcampo y otras sin fuente.

Al abrir: carga sola; **IndexedDB** guarda las vivas un día. El dump se lee del fichero en cada carga (y queda en la misma entrada de caché). Tras `dump_all_precios.py`, el script actualiza `precios-latest.json`.

## Local

```bash
python -m http.server 8766
```

http://127.0.0.1:8766/index.html?lat=40.4168&lon=-3.7038

Preferible el servidor frente a `file://`.

## UI

Mapa a pantalla completa. Panel/sheet plegable. Mi ubicación / Usar centro del mapa.

## Comprobar conteos (DevTools, tras carga web)

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

Esperado (Madrid, 28 tipos): Mercadona/Carrefour 28; Aldi ~24–26; Lidl ~6. Detalle: `docs/EMPAREJADO.md`.
