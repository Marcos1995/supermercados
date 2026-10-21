#!/usr/bin/env python3
"""Vuelca JSON crudo de las 4 cadenas y tabla de cobertura (criterio EMPAREJADO).

Uso (desde la raíz del repo):
  python scripts/dump_cobertura.py

Salida:
  tmp-precios/<cadena>/<tipo>.json   — respuesta cruda / hits normalizados
  docs/COBERTURA.md                  — tabla producto × cadena con X
"""
from __future__ import annotations

import json
import re
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tmp-precios"
DOC = ROOT / "docs" / "COBERTURA.md"

SEMANAL = [
    "aceite de oliva", "aceite de girasol", "huevos", "leche", "pan", "mantequilla", "yogurt", "queso",
    "jamón", "pollo", "carne picada", "arroz", "pasta", "legumbres", "azúcar", "café", "agua",
    "detergente", "lavavajillas", "papel de cocina", "papel higiénico", "jabón", "champú",
    "fruta", "verdura", "patatas", "cebolla", "tomate",
]
QUERY = {
    "yogurt": "yogur natural",
    "verdura": "lechuga",
    "legumbres": "garbanzos",
    "carne picada": "picada",
    "papel higiénico": "papel higienico",
    "aceite de girasol": "aceite de girasol",
    "detergente": "detergente",
    "lavavajillas": "lavavajillas",
    "fruta": "manzana",
    "jabón": "jabon de manos",
    "champú": "champu",
    "leche": "leche semidesnatada",
    "arroz": "arroz",
}
FALLBACKS = {
    "carne picada": ["carne picada", "burger meat"],
    "lavavajillas": ["lavavajillas a mano"],
    "aceite de oliva": ["aceite oliva virgen"],
    "detergente": ["detergente ropa"],
    "pollo": ["pechuga de pollo"],
    "pasta": ["espagueti"],
    "tomate": ["tomate pera", "tomate ensalada"],
    "patatas": ["patatas freir", "patata"],
    "café": ["cafe molido", "cafe en grano"],
    "yogurt": ["yogur", "yogurt natural"],
}
LAT, LON = 40.4168, -3.7038
STOP = {"de", "del", "la", "el", "los", "las", "y", "en", "con", "para", "a", "un", "una"}
NOISE = [
    "corporal", "cabello", "facial", "bronceador", "masaje", "utensilio", "espumador", "chocolate",
    "nidos", "codorniz", "claras", "liquida", "flan", "clipsaurio", "juguete", "dinosaur",
    "silvercrest", "cebador", "cazo", "freidora", "maquina", "robot", "sarten", "croquetas",
    "perro", "gato", "helado", "tagliatelle", "bombones", "calendario", "guirnalda", "aspirador",
    "tapicer", "cafetera", "batidora", "mancuerna",
]
LIDL_HOGAR = {"detergente", "lavavajillas", "papel de cocina", "papel higiénico", "jabón", "champú"}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()


def tokens(q: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", fold(q)) if len(t) > 2 and t not in STOP]


def match_toks(line: str) -> list[str]:
    if line == "yogurt":
        return ["yogur"]
    if line == "verdura":
        return ["lechuga"]
    if line == "legumbres":
        return ["garbanzos"]
    if line == "fruta":
        return ["manzana"]
    if line == "carne picada":
        return ["picada"]
    return tokens(line)


def words_of(name: str) -> list[str]:
    return [w for w in re.split(r"[^a-z0-9]+", fold(name)) if w]


def hit_word(w: str, t: str) -> bool:
    return w == t or (len(t) > 3 and w.startswith(t)) or (len(w) > 3 and t.startswith(w))


def matches(name: str, toks: list[str]) -> bool:
    n = fold(name)
    if not toks:
        return False
    for t in toks:
        if t in n:
            continue
        stem = t[:-2] if t.endswith("es") else (t[:-1] if t.endswith("s") else t)
        if len(stem) > 3 and stem in n:
            continue
        return False
    return True


def primary_ok(name: str, toks: list[str]) -> bool:
    if not toks:
        return False
    words = words_of(name)
    idx = next((i for i, w in enumerate(words) if hit_word(w, toks[0])), -1)
    if idx < 0 or idx > 3:
        return False
    return all(any(hit_word(w, t) for w in words) for t in toks)


def noisy(name: str, toks: list[str]) -> bool:
    n = fold(name)
    return any(w in n and not any(t in w or w in t for t in toks) for w in NOISE)


def line_ban(name: str, line: str) -> bool:
    n = fold(name)
    if line == "leche":
        if re.search(r"(leche|bebida) de (coco|almendra|soja|avena|arroz|avellana)", n):
            return True
        if re.search(r"(solar|corporal|crema|limpiador|friegasuelos|fermentada|condensada|evaporada)", n):
            return True
    if line == "arroz" and re.search(r"(arroz con|croqueta|perro|gato)", n):
        return True
    if line == "huevos" and re.search(r"(chocolate|flan|pasta|tagliatelle)", n):
        return True
    if line == "aceite de oliva":
        if not re.search(r"aceite de oliva", n):
            return True
        if re.search(r"(atun|sardina|sardinillas|pota|bonito|ventresca)", n):
            return True
    if line == "aceite de girasol":
        if not re.search(r"aceite de girasol", n):
            return True
        if re.search(r"(atun|sardina|sardinillas|pota|bonito|ventresca)", n):
            return True
    if line == "carne picada":
        if re.search(r"(cebolla|chocolate|avellana|girasoli)", n):
            return True
        if not re.search(r"(vacuno|cerdo|pollo|pavo|ternera|burger meat|carne|mixto)", n):
            return True
    if line == "jamón" and re.search(r"(jamoncitos|croqueta|pavo|york|cocido de pavo)", n):
        return True
    if line == "pan" and re.search(r"(panettone|empanado)", n):
        return True
    if line == "pollo" and re.search(r"(croqueta|nugget|crispies|perro|gato|caldo|sopa|stock|curry|empanado|relleno|pate|paté)", n):
        return True
    if line == "lavavajillas" and re.search(r"(sal para|abrillantador)", n):
        return True
    if line == "jabón" and re.search(r"(dispensador|vaso|organizador|jabonera)", n):
        return True
    if line == "azúcar" and not re.search(r"^azucar\b", n):
        return True
    if line == "fruta" and re.search(r"(friegasuelos|limpiador|ambientador|gel|jabon|champu|zumo|smoothie)", n):
        return True
    if line == "patatas" and re.search(r"(fritas|chips|snack|congelad|bacon|gajo|especiad|queso|american|cocidas)", n):
        return True
    if line == "tomate" and re.search(r"(frito|salsa|ketchup|concentrado|triturado|fideos|troceado|pelado|siciliana)", n):
        return True
    if line == "café" and re.search(r"(cappuccino|capuccino|helado|bombon|con leche|puleva|latte)", n):
        return True
    if line == "papel de cocina" and re.search(r"(vegetal|horno|aluminio)", n):
        return True
    return False


def visible(hits: list[dict], line: str) -> list[dict]:
    toks = match_toks(line)
    out = []
    for p in hits:
        if not (p.get("price") and p["price"] > 0):
            continue
        if not matches(p["name"], toks):
            continue
        if not primary_ok(p["name"], toks):
            continue
        if noisy(p["name"], toks):
            continue
        if line_ban(p["name"], line):
            continue
        out.append(p)
    return out


def pick(hits: list[dict], line: str) -> dict | None:
    toks = match_toks(line)
    pool = visible(hits, line)
    if not pool:
        return None
    lead = [p for p in pool if any(fold(p["name"]).startswith(t) for t in toks)]
    if lead:
        pool = lead
    pool = sorted(pool, key=lambda p: (p.get("unit") or p["price"], p["price"]))
    return pool[0]


def http_get(url: str, headers: dict | None = None) -> dict | list:
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "supermercados-dump/1.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def http_post(url: str, body: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json", "User-Agent": "supermercados-dump/1.0"}
    )
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def merca_wh(lat: float, lon: float) -> str:
    if lat > 41 and lon > 0.3:
        return "bcn1"
    if 38.2 < lat < 40.3 and -1.3 < lon < 0.7:
        return "vlc1"
    if lat < 38.6 and lon < -3:
        return "svq1"
    return "mad3"


def search_mercadona(q: str) -> tuple[list[dict], dict]:
    wh = merca_wh(LAT, LON)
    # Mismas claves públicas que index.html (web Mercadona)
    url = (
        "https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_"
        + wh
        + "_es/query?x-algolia-application-id=7UZJKL1DJ0&x-algolia-api-key=9d8f2e39e90df472b4f2e559a116fe17"
    )
    raw = http_post(url, {"params": f"query={urllib.parse.quote(q)}&hitsPerPage=40&page=0"})
    hits = []
    for h in raw.get("hits") or []:
        pi = (h.get("price_instructions") or {})
        price = float(pi.get("unit_price") or 0)
        ref = float(pi.get("reference_price") or 0)
        hits.append({
            "name": h.get("display_name") or "",
            "brand": h.get("brand") or "",
            "price": price,
            "unit": ref if ref > 0 else price,
        })
    return hits, raw


def search_carrefour(q: str) -> tuple[list[dict], dict]:
    url = (
        "https://api.empathy.co/search/v1/query/carrefour/search?query="
        + urllib.parse.quote(q.lower())
        + "&lang=es&catalog=food&rows=40&start=0"
    )
    raw = http_get(url)
    hits = []
    for c in ((raw.get("catalog") or {}).get("content") or []):
        price = float(c.get("active_price") or 0)
        factor = float(c.get("unit_conversion_factor") or 1) or 1
        hits.append({
            "name": c.get("display_name") or "",
            "brand": c.get("brand") or "",
            "price": price,
            "unit": price / factor,
        })
    return hits, raw


def lidl_cat_ok(cat: str, line: str) -> bool:
    c = fold(cat or "")
    if c in ("food", "f+v") or c.startswith("food") or c.startswith("f+v"):
        return True
    return line in LIDL_HOGAR


def search_lidl(q: str, line: str) -> tuple[list[dict], dict]:
    url = (
        "https://www.lidl.es/q/api/search?assortment=ES&locale=es_ES&version=2.1.0&q="
        + urllib.parse.quote(q)
        + "&fetchsize=40&offset=0"
    )
    raw = http_get(url, {"Accept": "application/mindshift.search+json;version=2", "User-Agent": "supermercados-dump/1.0"})
    hits = []
    for it in raw.get("items") or []:
        data = ((it.get("gridbox") or {}).get("data")) or {}
        if not data.get("fullTitle") or not data.get("price"):
            continue
        if not lidl_cat_ok(data.get("category") or "", line):
            continue
        price = float((data.get("price") or {}).get("price") or 0)
        if price <= 0:
            continue
        hits.append({"name": data["fullTitle"], "brand": "", "price": price, "unit": price})
    return hits, raw


def search_aldi(q: str) -> tuple[list[dict], dict]:
    url = (
        "https://l9knu74io7-dsn.algolia.net/1/indexes/an_prd_es_es_pen_products2/query"
        "?x-algolia-application-id=L9KNU74IO7&x-algolia-api-key=83df5acd172c42ab174afa4583232b5d"
    )
    raw = http_post(url, {"params": f"query={urllib.parse.quote(q)}&hitsPerPage=40&page=0"})
    hits = []
    for h in raw.get("hits") or []:
        cur = h.get("currentPrice") or {}
        base = (cur.get("basePrice") or [None])[0]
        price = float(cur.get("priceValue") or 0)
        unit = float(base.get("basePriceValue")) if base and base.get("basePriceValue") is not None else price
        hits.append({
            "name": h.get("name") or "",
            "brand": h.get("brandName") or "",
            "price": price,
            "unit": unit,
        })
    return hits, raw


def queries_for(line: str) -> list[str]:
    main = QUERY.get(line, line)
    return list(dict.fromkeys([main, line, *(FALLBACKS.get(line) or [])]))


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(s)).strip("-")


def fetch_line(chain: str, line: str) -> tuple[list[dict], list]:
    merged: list[dict] = []
    seen = set()
    raws = []
    for q in queries_for(line):
        try:
            if chain == "mercadona":
                hits, raw = search_mercadona(q)
            elif chain == "carrefour":
                hits, raw = search_carrefour(q)
            elif chain == "lidl":
                hits, raw = search_lidl(q, line)
            else:
                hits, raw = search_aldi(q)
        except Exception as e:
            raws.append({"query": q, "error": str(e)})
            continue
        raws.append({"query": q, "raw": raw, "normalized_count": len(hits)})
        for h in hits:
            k = fold(h["name"]) + "|" + str(h["price"])
            if k in seen:
                continue
            seen.add(k)
            merged.append(h)
        time.sleep(0.15)
    return merged, raws


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chains = ["mercadona", "carrefour", "lidl", "aldi"]
    table: dict[str, dict[str, str]] = {line: {} for line in SEMANAL}
    picks: dict[str, dict[str, str]] = {line: {} for line in SEMANAL}

    for chain in chains:
        cdir = OUT / chain
        cdir.mkdir(parents=True, exist_ok=True)
        for line in SEMANAL:
            print(f"{chain} · {line}", flush=True)
            hits, raws = fetch_line(chain, line)
            chosen = pick(hits, line)
            ok = chosen is not None
            table[line][chain] = "X" if ok else ""
            picks[line][chain] = chosen["name"] if chosen else ""
            payload = {
                "chain": chain,
                "line": line,
                "queries": queries_for(line),
                "hits_normalized": hits[:80],
                "visible": [p["name"] for p in visible(hits, line)[:20]],
                "pick": chosen,
                "ok": ok,
                "responses": raws,
            }
            (cdir / f"{slug(line)}.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    # yogurt spotlight
    spotlight = OUT / "_yogurt_spotlight.json"
    spot = {}
    for chain in chains:
        p = OUT / chain / "yogurt.json"
        if p.exists():
            spot[chain] = json.loads(p.read_text(encoding="utf-8"))
    spotlight.write_text(json.dumps(spot, ensure_ascii=False, indent=2), encoding="utf-8")

    lines_md = [
        "# Cobertura de emparejado (Madrid)",
        "",
        "Generado por `python scripts/dump_cobertura.py`.",
        "Criterio: `docs/EMPAREJADO.md`. JSON crudos: carpeta `tmp-precios/` (local, no subir).",
        "",
        "| Producto | Mercadona | Carrefour | Lidl | Aldi |",
        "|----------|:---------:|:---------:|:----:|:----:|",
    ]
    for line in SEMANAL:
        row = table[line]
        lines_md.append(
            f"| {line} | {row.get('mercadona','')} | {row.get('carrefour','')} | {row.get('lidl','')} | {row.get('aldi','')} |"
        )
    lines_md += ["", "## Ficha elegida (si hay X)", ""]
    for line in SEMANAL:
        lines_md.append(f"### {line}")
        for chain in chains:
            name = picks[line].get(chain) or "—"
            mark = "X" if table[line].get(chain) == "X" else "·"
            lines_md.append(f"- {mark} **{chain}**: {name}")
        lines_md.append("")
    DOC.write_text("\n".join(lines_md), encoding="utf-8")
    print(f"Tabla → {DOC}")
    print(f"JSON  → {OUT}")


if __name__ == "__main__":
    main()
