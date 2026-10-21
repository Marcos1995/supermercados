<!-- managed-by-telegram-cursor-bot:agent-kit -->
# supermercados

Compra semanal fija: marcas tipos; cada súper aporta la ficha más barata por unidad.

- **Cómo ejecutarlo a mano:** [`START.md`](START.md)
- **Criterio de emparejado (no reinventar):** [`docs/EMPAREJADO.md`](docs/EMPAREJADO.md)
- Vista: https://marcos1995.github.io/supermercados/

## Setup

```bash
python -m http.server 8766
# abrir http://127.0.0.1:8766/index.html?lat=40.4168&lon=-3.7038
# Todo → Ver precios
```

Nada que instalar.

## Docs

- `PROJECT.md` — memoria del repo para agentes
- `AGENTS.md` — reglas (Karpathy) + flujo
- `START.md` — lanzar y comprobar a mano
- `docs/EMPAREJADO.md` — criterio unificado de fichas
- `docs/PRECIOS.md` — fuentes JSON y huecos de API
- `docs/DECISIONES.md` — decisiones (skill `laya`)
- `graphify-out/` — mapa del código (se regenera en cada commit)
