#!/usr/bin/env python3
"""Recoge precios SEMANAL de todas las cadenas con fuente usable (terminal, sin CORS).

Plan A = API JSON. Plan B = otro endpoint / HTML. Sin inventar precios.

Uso: python scripts/dump_all_precios.py
Salida: data/precios-YYYY-MM-DD.json (+ .summary.json)
"""
from __future__ import annotations

import http.cookiejar
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
LAT, LON = 40.4168, -3.7038

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
    "fruta": "manzana",
    "jabón": "jabon de manos",
    "champú": "champu",
    "leche": "leche semidesnatada",
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
LIDL_HOGAR = {"detergente", "lavavajillas", "papel de cocina", "papel higiénico", "jabón", "champú"}

# Consultas Dia cortas (evitar bloqueos por request grande)
DIA_QUERIES = {
    "aceite de oliva": ["aceite oliva"],
    "aceite de girasol": ["aceite girasol"],
    "huevos": ["huevos"],
    "leche": ["leche"],
    "pan": ["pan"],
    "mantequilla": ["mantequilla"],
    "yogurt": ["yogur"],
    "queso": ["queso"],
    "jamón": ["jamon"],
    "pollo": ["pollo"],
    "carne picada": ["carne picada"],
    "arroz": ["arroz"],
    "pasta": ["pasta"],
    "legumbres": ["garbanzos"],
    "azúcar": ["azucar"],
    "café": ["cafe"],
    "agua": ["agua"],
    "detergente": ["detergente"],
    "lavavajillas": ["lavavajillas"],
    "papel de cocina": ["papel cocina"],
    "papel higiénico": ["papel higienico"],
    "jabón": ["jabon"],
    "champú": ["champu"],
    "fruta": ["manzana"],
    "verdura": ["lechuga"],
    "patatas": ["patatas"],
    "cebolla": ["cebolla"],
    "tomate": ["tomate"],
}

CHAINS_TRY = [
    "mercadona", "carrefour", "lidl", "aldi", "consum", "eroski", "dia", "alcampo", "ahorramas",
]
CHAINS_MAP_ONLY = [
    "hipercor", "supercor", "elcorteingles", "bm", "familycash", "gadis", "mas",
    "froiz", "hiperusera", "alimerka", "lupa", "simply", "supeco", "spar", "eurospar",
    "bonpreu", "caprabo", "condis", "coviran",
]


def fold(s: str) -> str:
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower()


def queries_for(line: str) -> list[str]:
    main = QUERY.get(line, line)
    return list(dict.fromkeys([main, line, *(FALLBACKS.get(line) or [])]))


def http_json(url: str, method: str = "GET", body: dict | None = None, headers: dict | None = None, opener=None):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    open_fn = opener.open if opener else urllib.request.urlopen
    with open_fn(req, timeout=35) as r:
        raw = r.read().decode("utf-8", "replace")
        return r.status, json.loads(raw) if raw.strip() else None


def http_text(url: str, headers: dict | None = None, opener=None) -> tuple[int, str]:
    h = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*", "Accept-Language": "es-ES,es;q=0.9"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    open_fn = opener.open if opener else urllib.request.urlopen
    try:
        with open_fn(req, timeout=40) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace") if e.fp else ""
        return e.code, body


def search_mercadona(q: str) -> list[dict]:
    url = (
        "https://7uzjkl1dj0-dsn.algolia.net/1/indexes/products_prod_mad3_es/query"
        "?x-algolia-application-id=7UZJKL1DJ0&x-algolia-api-key=9d8f2e39e90df472b4f2e559a116fe17"
    )
    _, raw = http_json(url, "POST", {"params": f"query={urllib.parse.quote(q)}&hitsPerPage=40&page=0"})
    hits = []
    for h in (raw or {}).get("hits") or []:
        pi = h.get("price_instructions") or {}
        price = float(pi.get("unit_price") or 0)
        if price <= 0:
            continue
        ref = float(pi.get("reference_price") or 0)
        hits.append({
            "name": h.get("display_name") or "", "brand": h.get("brand") or "",
            "price": price, "unit": ref if ref > 0 else price, "source": "algolia",
        })
    return hits


def search_carrefour(q: str) -> list[dict]:
    url = (
        "https://api.empathy.co/search/v1/query/carrefour/search?query="
        + urllib.parse.quote(q.lower()) + "&lang=es&catalog=food&rows=40&start=0"
    )
    _, raw = http_json(url)
    hits = []
    for c in ((raw or {}).get("catalog") or {}).get("content") or []:
        price = float(c.get("active_price") or 0)
        if price <= 0:
            continue
        factor = float(c.get("unit_conversion_factor") or 1) or 1
        hits.append({
            "name": c.get("display_name") or "", "brand": c.get("brand") or "",
            "price": price, "unit": price / factor, "source": "empathy",
        })
    return hits


def lidl_cat_ok(cat: str, line: str) -> bool:
    c = fold(cat or "")
    if c in ("food", "f+v") or c.startswith("food") or c.startswith("f+v"):
        return True
    return line in LIDL_HOGAR


def search_lidl(q: str, line: str) -> list[dict]:
    url = (
        "https://www.lidl.es/q/api/search?assortment=ES&locale=es_ES&version=2.1.0&q="
        + urllib.parse.quote(q) + "&fetchsize=40&offset=0"
    )
    _, raw = http_json(url, headers={"Accept": "application/mindshift.search+json;version=2"})
    hits = []
    for it in (raw or {}).get("items") or []:
        data = ((it.get("gridbox") or {}).get("data")) or {}
        if not data.get("fullTitle") or not data.get("price"):
            continue
        if not lidl_cat_ok(data.get("category") or "", line):
            continue
        price = float((data.get("price") or {}).get("price") or 0)
        if price <= 0:
            continue
        hits.append({"name": data["fullTitle"], "brand": "", "price": price, "unit": price, "source": "lidl-api"})
    return hits


def search_aldi(q: str) -> list[dict]:
    url = (
        "https://l9knu74io7-dsn.algolia.net/1/indexes/an_prd_es_es_pen_products2/query"
        "?x-algolia-application-id=L9KNU74IO7&x-algolia-api-key=83df5acd172c42ab174afa4583232b5d"
    )
    _, raw = http_json(url, "POST", {"params": f"query={urllib.parse.quote(q)}&hitsPerPage=40&page=0"})
    hits = []
    for h in (raw or {}).get("hits") or []:
        cur = h.get("currentPrice") or {}
        base = (cur.get("basePrice") or [None])[0]
        price = float(cur.get("priceValue") or 0)
        if price <= 0:
            continue
        unit = float(base.get("basePriceValue")) if base and base.get("basePriceValue") is not None else price
        hits.append({
            "name": h.get("name") or "", "brand": h.get("brandName") or "",
            "price": price, "unit": unit, "source": "algolia",
        })
    return hits


def search_consum(q: str) -> list[dict]:
    hits = []
    offset = 0
    limit = 40
    while offset < 120:
        url = (
            "https://tienda.consum.es/api/rest/V1.0/catalog/product?q="
            + urllib.parse.quote(q) + f"&limit={limit}&offset={offset}"
        )
        _, raw = http_json(url)
        products = (raw or {}).get("products") or []
        for p in products:
            pd = p.get("productData") or {}
            prices = ((p.get("priceData") or {}).get("prices")) or []
            price = 0.0
            for pr in prices:
                if pr.get("id") == "PRICE":
                    price = float((pr.get("value") or {}).get("centAmount") or 0)
                    break
            if price <= 0 and prices:
                price = float((prices[0].get("value") or {}).get("centAmount") or 0)
            if price <= 0:
                continue
            brand = ((pd.get("brand") or {}).get("name")) or ""
            unit = float((prices[0].get("value") or {}).get("centUnitAmount") or 0) if prices else price
            hits.append({
                "name": pd.get("name") or pd.get("description") or "",
                "brand": brand, "price": price, "unit": unit or price,
                "source": "consum-api", "url": pd.get("url") or "",
            })
        if not (raw or {}).get("hasMore") or not products:
            break
        offset += limit
        time.sleep(0.08)
    return hits


def search_eroski(q: str) -> list[dict]:
    url = "https://supermercado.eroski.es/es/search/results/?q=" + urllib.parse.quote(q) + "&searchSource=search"
    status, html = http_text(url)
    if status != 200 or len(html) < 5000:
        raise RuntimeError(f"eroski HTTP {status} len={len(html)}")
    hits, seen = [], set()
    for c in re.split(r'class="[^"]*product-item[^"]*"', html)[1:]:
        if "product-title" not in c[:2000] and "productdetail" not in c[:2000]:
            continue
        name_m = re.search(r'class="[^"]*product-title[^"]*"[^>]*>(.*?)</', c, re.I | re.S)
        if name_m:
            name = re.sub(r"<[^>]+>", "", name_m.group(1)).strip()
        else:
            tm = re.search(r'title="([^"]{8,120})"', c)
            name = tm.group(1) if tm else ""
        price_m = re.search(r'class="[^"]*price[^"]*"[^>]*>\s*([0-9]+,[0-9]{2})\s*<', c, re.I)
        href_m = re.search(r'href="([^"]*productdetail/\d+[^"]*)"', c)
        if not name or not price_m:
            continue
        price = float(price_m.group(1).replace(",", "."))
        key = fold(name) + "|" + str(price)
        if key in seen:
            continue
        seen.add(key)
        hits.append({
            "name": name, "brand": "", "price": price, "unit": price,
            "source": "eroski-html", "url": href_m.group(1) if href_m else "",
        })
    return hits


_dia_opener = None


def dia_session():
    global _dia_opener
    if _dia_opener is None:
        cj = http.cookiejar.CookieJar()
        _dia_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        # warm cookies
        http_text("https://www.dia.es/", opener=_dia_opener)
        time.sleep(0.2)
    return _dia_opener


def search_dia_page(q: str, page: int) -> list[dict]:
    """Plan A: API search-back en páginas pequeñas (≈30 ítems)."""
    op = dia_session()
    url = (
        "https://www.dia.es/api/v1/search-back/search?q="
        + urllib.parse.quote(q)
        + f"&page={page}"
    )
    try:
        _, raw = http_json(
            url,
            headers={
                "Accept": "application/json",
                "Referer": "https://www.dia.es/search?q=" + urllib.parse.quote(q),
                "Origin": "https://www.dia.es",
            },
            opener=op,
        )
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"dia page={page} HTTP {e.code}") from e
    hits = []
    for it in (raw or {}).get("search_items") or []:
        prices = it.get("prices") or {}
        price = float(prices.get("price") or 0)
        unit = float(prices.get("price_per_unit") or 0) or price
        name = it.get("display_name") or ""
        if not name or price <= 0:
            continue
        hits.append({
            "name": name,
            "brand": it.get("brand") or "",
            "price": price,
            "unit": unit,
            "source": "dia-api-search-back",
            "sku": it.get("sku_id") or "",
            "url": ("https://www.dia.es" + it["url"]) if it.get("url") else "",
        })
    return hits


def search_dia(q: str) -> list[dict]:
    """Páginas cortas 1..3; si falla, plan B: HTML search (sin inventar)."""
    hits, errors = [], []
    for page in (1, 2, 3):
        try:
            batch = search_dia_page(q, page)
            hits.extend(batch)
            if len(batch) < 5:
                break
            time.sleep(0.25)
        except Exception as e:
            errors.append(str(e))
            time.sleep(0.6)
            # re-warm session once
            global _dia_opener
            _dia_opener = None
            try:
                batch = search_dia_page(q, page)
                hits.extend(batch)
            except Exception as e2:
                errors.append(str(e2))
                break
    if hits:
        return hits
    # Plan B: página HTML (a veces trae JSON embebido)
    op = dia_session()
    status, html = http_text(
        "https://www.dia.es/search?q=" + urllib.parse.quote(q),
        headers={"Referer": "https://www.dia.es/"},
        opener=op,
    )
    if status == 200:
        # precios en JSON-LD u objetos
        for m in re.finditer(
            r'"display_name"\s*:\s*"([^"]+)".{0,400}?"price"\s*:\s*([0-9]+(?:\.[0-9]+)?)',
            html,
        ):
            hits.append({
                "name": m.group(1), "brand": "", "price": float(m.group(2)),
                "unit": float(m.group(2)), "source": "dia-html-embed",
            })
        if hits:
            return hits
    raise RuntimeError("dia sin datos: " + "; ".join(errors[:4]) or f"HTML {status}")


def extract_alcampo_ids(html: str) -> list[str]:
    """IDs en JSON escapado: retailerProductId\":\"13367\" o \"73514-FILETES\"."""
    ids = re.findall(r'retailerProductId\\":\\"([^\\"]+)', html)
    ids += re.findall(r'"retailerProductId"\s*:\s*"([^"]+)"', html)
    seen, out = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            out.append(i)
    return out


def search_alcampo(q: str) -> list[dict]:
    """
    Plan A: HTML de búsqueda (suele bloquearse con 202).
    Plan B: home + bop por retailerProductId (IDs escapados).
    Plan C: extraer amount del HTML embebido si aparece.
    """
    errors = []
    # Plan A
    status, html = http_text("https://www.compraonline.alcampo.es/search?q=" + urllib.parse.quote(q))
    if status == 200 and len(html) > 20000:
        hits = []
        for m in re.finditer(
            r'"name"\s*:\s*"([^"]{5,120})"[^{}]{0,500}?"amount"\s*:\s*"([0-9]+(?:\.[0-9]+)?)"',
            html,
        ):
            price = float(m.group(2))
            if price > 0:
                hits.append({
                    "name": m.group(1), "brand": "", "price": price, "unit": price,
                    "source": "alcampo-search-html",
                })
        if hits:
            return hits
        errors.append(f"search HTML {status} len={len(html)} sin precios")
    else:
        errors.append(f"search HTTP {status} len={len(html)}")

    # Plan B: home embebido + detalle bop
    status, home = http_text("https://www.compraonline.alcampo.es/")
    if status != 200 or len(home) < 10000:
        raise RuntimeError("alcampo: " + "; ".join(errors) + f"; home {status}")
    ids = extract_alcampo_ids(home)
    # amounts near products in escaped JSON
    hits = []
    for m in re.finditer(
        r'retailerProductId\\*":\\*"(\d+)\\*".{0,1200}?amount\\*":\\*"([0-9]+(?:\.[0-9]+)?)\\*"',
        home,
    ):
        hits.append({
            "name": f"Alcampo product {m.group(1)}",
            "brand": "",
            "price": float(m.group(2)),
            "unit": float(m.group(2)),
            "source": "alcampo-home-embed",
            "sku": m.group(1),
        })
    # Prefer named products if present
    named = []
    for m in re.finditer(
        r'name\\*":\\*"([^\\"]{5,100})\\*".{0,800}?retailerProductId\\*":\\*"(\d+)\\*"',
        home,
    ):
        named.append((m.group(1), m.group(2)))
    # fetch bop for first N ids (small batches)
    region_candidates = re.findall(r'regionId\\*":\\*"([^\\"]+)"', home)
    region_candidates += re.findall(r'"regionId"\s*:\s*"([^"]+)"', home)
    regions = list(dict.fromkeys(region_candidates))[:3] or ["5245"]  # fallback común Auchan ES
    detail_hits = []
    for pid in ids[:25]:
        got = False
        for region in regions:
            url = (
                "https://www.compraonline.alcampo.es/api/webproductpagews/v5/products/bop"
                f"?retailerProductId={pid}&regionId={urllib.parse.quote(region)}"
            )
            try:
                st, raw = http_json(url, headers={"Accept": "application/json", "Referer": "https://www.compraonline.alcampo.es/"})
            except Exception as e:
                errors.append(f"bop {pid}/{region}: {e}")
                continue
            if not raw:
                continue
            # walk common shapes
            name = (
                (raw.get("product") or {}).get("name")
                or raw.get("name")
                or (raw.get("data") or {}).get("name")
                or ""
            )
            price = 0.0
            for path in [
                lambda r: float((((r.get("price") or {}).get("current") or {}).get("amount") or 0) or 0),
                lambda r: float((r.get("price") or {}).get("amount") or 0),
                lambda r: float((((r.get("product") or {}).get("price") or {}).get("amount") or 0) or 0),
            ]:
                try:
                    price = path(raw)
                except Exception:
                    price = 0.0
                if price > 0:
                    break
            # recursive amount
            if price <= 0:
                blob = json.dumps(raw)
                am = re.search(r'"amount"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?', blob)
                if am:
                    price = float(am.group(1))
                nm = re.search(r'"name"\s*:\s*"([^"]{5,120})"', blob)
                if nm and not name:
                    name = nm.group(1)
            if name and price > 0:
                detail_hits.append({
                    "name": name, "brand": "", "price": price, "unit": price,
                    "source": "alcampo-bop", "sku": pid,
                })
                got = True
                break
            time.sleep(0.05)
        if not got:
            time.sleep(0.05)
        if len(detail_hits) >= 40:
            break

    # filter by query token if we have details
    toks = [t for t in fold(q).split() if len(t) > 2]
    if detail_hits and toks:
        filtered = [h for h in detail_hits if any(t in fold(h["name"]) for t in toks)]
        if filtered:
            return filtered
    if detail_hits:
        return detail_hits
    if hits:
        return hits
    # named without price doesn't count
    raise RuntimeError("alcampo sin precios: " + "; ".join(errors[:6]) + f"; ids={len(ids)}")


def search_ahorramas(q: str) -> list[dict]:
    url = (
        "https://www.ahorramas.com/on/demandware.store/Sites-Ahorramas-Site/es_ES/"
        "Search-UpdateGrid?q=" + urllib.parse.quote(q) + "&start=0&sz=24"
    )
    status, html = http_text(url, headers={"Referer": "https://www.ahorramas.com/"})
    if status != 200:
        # plan B suggest (sin precio → error)
        st2, html2 = http_text(
            "https://www.ahorramas.com/on/demandware.store/Sites-Ahorramas-Site/es_ES/"
            "SearchServices-GetSuggestions?q=" + urllib.parse.quote(q)
        )
        raise RuntimeError(f"ahorramas grid HTTP {status}; suggest {st2} sin precios")
    hits = []
    # Demandware product tiles
    for block in re.split(r'class="[^"]*product-tile[^"]*"', html)[1:]:
        name_m = re.search(r'class="[^"]*pdp-link[^"]*"[^>]*>\s*<a[^>]*>([^<]+)</a>', block, re.I) or \
            re.search(r'class="[^"]*product-name[^"]*"[^>]*>([^<]+)<', block, re.I)
        price_m = re.search(r'class="[^"]*sales[^"]*"[^>]*>.*?([0-9]+,[0-9]{2})', block, re.I | re.S) or \
            re.search(r'data-price[^>]*=\"([0-9]+(?:\.[0-9]+)?)\"', block) or \
            re.search(r'([0-9]+,[0-9]{2})\s*€', block)
        if not name_m or not price_m:
            continue
        name = name_m.group(1).strip()
        raw_p = price_m.group(1).replace(",", ".")
        price = float(raw_p)
        if price <= 0:
            continue
        hits.append({"name": name, "brand": "", "price": price, "unit": price, "source": "ahorramas-html"})
    if not hits:
        raise RuntimeError("ahorramas HTML sin precios parseables")
    return hits


SEARCHERS = {
    "mercadona": lambda q, line: search_mercadona(q),
    "carrefour": lambda q, line: search_carrefour(q),
    "lidl": lambda q, line: search_lidl(q, line),
    "aldi": lambda q, line: search_aldi(q),
    "consum": lambda q, line: search_consum(q),
    "eroski": lambda q, line: search_eroski(q),
    "dia": lambda q, line: search_dia(q),
    "alcampo": lambda q, line: search_alcampo(q),
    "ahorramas": lambda q, line: search_ahorramas(q),
}


def merge_hits(chain: str, line: str) -> tuple[list[dict], list[str], str]:
    fetcher = SEARCHERS[chain]
    merged, seen, errors = [], set(), []
    method = ""
    qs = DIA_QUERIES.get(line) if chain == "dia" else queries_for(line)
    # Dia: solo queries cortas (1 término) para no bloquear
    if chain == "dia":
        qs = DIA_QUERIES.get(line) or [line.split()[0]]
    for q in qs:
        try:
            hits = fetcher(q, line)
            if hits and not method:
                method = hits[0].get("source") or "ok"
            for h in hits:
                if not h.get("name") or not (h.get("price") and h["price"] > 0):
                    continue
                k = fold(h["name"]) + "|" + str(h["price"])
                if k in seen:
                    continue
                seen.add(k)
                h = dict(h)
                h["query"] = q
                h["line"] = line
                merged.append(h)
        except Exception as e:
            errors.append(f"{q}: {e}")
        time.sleep(0.15 if chain != "dia" else 0.35)
    return merged, errors, method


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    day = date.today().isoformat()
    out_path = DATA / f"precios-{day}.json"
    summary_path = DATA / f"precios-{day}.summary.json"

    payload = {
        "date": day,
        "lat": LAT,
        "lon": LON,
        "note": "Dump terminal. Solo price>0. Plan A/B por cadena en source/methods.",
        "lines": SEMANAL,
        "chains": {},
        "map_only_no_source": CHAINS_MAP_ONLY,
    }

    for chain in CHAINS_TRY:
        print(f"=== {chain} ===", flush=True)
        all_hits, chain_errors, methods = [], [], set()
        for line in SEMANAL:
            print(f"  {line}", flush=True)
            hits, errs, method = merge_hits(chain, line)
            all_hits.extend(hits)
            chain_errors.extend([f"{line}/{e}" for e in errs])
            if method:
                methods.add(method)
            by_count = len(hits)
            print(f"    -> {by_count}", flush=True)

        seen, unique = set(), []
        for h in all_hits:
            k = fold(h["name"]) + "|" + str(h["price"])
            if k in seen:
                continue
            seen.add(k)
            unique.append(h)

        by_line_counts = {}
        for line in SEMANAL:
            by_line_counts[line] = sum(1 for h in unique if h.get("line") == line)

        payload["chains"][chain] = {
            "ok": len(unique) > 0,
            "product_count": len(unique),
            "methods": sorted(methods),
            "products": unique,
            "by_line_counts": by_line_counts,
            "errors": chain_errors[:50],
            "error_count": len(chain_errors),
        }
        print(f"  → {len(unique)} productos | methods={sorted(methods)}", flush=True)

    for chain in CHAINS_MAP_ONLY:
        payload["chains"][chain] = {
            "ok": False,
            "product_count": 0,
            "methods": [],
            "products": [],
            "by_line_counts": {},
            "errors": ["sin fuente JSON/HTML usable conocida tras revisión (solo mapa OSM)"],
            "error_count": 1,
        }

    summary = {
        "date": day,
        "file": str(out_path.relative_to(ROOT)).replace("\\", "/"),
        "per_chain": {
            c: {
                "product_count": payload["chains"][c]["product_count"],
                "ok": payload["chains"][c]["ok"],
                "methods": payload["chains"][c].get("methods") or [],
                "error_count": payload["chains"][c]["error_count"],
            }
            for c in list(CHAINS_TRY) + CHAINS_MAP_ONLY
        },
        "with_data": [c for c in CHAINS_TRY if payload["chains"][c]["ok"]],
        "no_data": [c for c in list(CHAINS_TRY) + CHAINS_MAP_ONLY if not payload["chains"][c]["ok"]],
        "total_products": sum(payload["chains"][c]["product_count"] for c in CHAINS_TRY),
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    # Puntero fijo que lee la web (index.html)
    latest = DATA / "precios-latest.json"
    latest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {out_path}")
    print(f"Wrote {latest}")


if __name__ == "__main__":
    main()
