# Graph Report - supermercados  (2026-10-21)

## Corpus Check
- 21 files · ~13,640 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: .mdc 2, (none) 2)

## Summary
- 143 nodes · 164 edges · 19 communities (14 shown, 5 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `feff402c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Debug
- Contexto del proyecto
- Dashboard brief (for the Stitch prompt)
- Verify (UI)
- Web design
- Agent rules
- Build judgments with Laya
- Laya
- Review
- Arrancar a mano
- tablas/SKILL.md
- DESIGN.md
- DECISIONES.md
- Criterio unificado de emparejado
- Precios: fuentes y límites
- Ficha elegida (si hay X)
- dump_cobertura.py

## God Nodes (most connected - your core abstractions)
1. `Ficha elegida (si hay X)` - 29 edges
2. `fold()` - 10 edges
3. `visible()` - 8 edges
4. `fetch_line()` - 8 edges
5. `pick()` - 7 edges
6. `Criterio unificado de emparejado` - 7 edges
7. `main()` - 6 edges
8. `Debug` - 6 edges
9. `Contexto del proyecto` - 6 edges
10. `Arrancar a mano` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Pipeline (orden fijo)` --references--> `pick()`  [INFERRED]
  docs/EMPAREJADO.md → scripts/dump_cobertura.py
- `Criterio unificado de emparejado` --references--> `pick()`  [INFERRED]
  docs/EMPAREJADO.md → scripts/dump_cobertura.py

## Import Cycles
- None detected.

## Communities (19 total, 5 thin omitted)

### Community 0 - "Debug"
Cohesion: 0.29
Nodes (6): 1. Root cause, 2. Compare, 3. Hypothesis, 4. Fix, Debug, Red flags → back to step 1

### Community 1 - "Contexto del proyecto"
Cohesion: 0.29
Nodes (6): Comandos utiles, Contexto del proyecto, Estado, Notas para el agente, Produccion, Stack

### Community 2 - "Dashboard brief (for the Stitch prompt)"
Cohesion: 0.33
Nodes (5): Anatomy (always), Charts without libraries (inline SVG, no CDN), CSS, Dashboard brief (for the Stitch prompt), Data honesty (non-negotiable)

### Community 3 - "Verify (UI)"
Cohesion: 0.40
Nodes (4): 1. Screenshots, 2. Look, 3. Fix and repeat, Verify (UI)

### Community 4 - "Web design"
Cohesion: 0.40
Nodes (4): Before HECHO, Steps, Style = `DESIGN.md`, Web design

### Community 5 - "Agent rules"
Cohesion: 0.50
Nodes (3): Agent rules, Flujo, Think → Simple → Surgical → Verify (Karpathy)

### Community 6 - "Build judgments with Laya"
Cohesion: 0.50
Nodes (3): Build judgments with Laya, Call, Design

### Community 7 - "Laya"
Cohesion: 0.50
Nodes (3): Laya, Reply (decision-only requests), Steps

### Community 8 - "Review"
Cohesion: 0.50
Nodes (3): Check, Do, Review

### Community 9 - "Arrancar a mano"
Cohesion: 0.16
Nodes (10): Ejecutar a mano, Docs, Setup, supermercados, Arrancar a mano, Comprobar conteos (DevTools), Criterio de fichas (no reinventar), Local (+2 more)

### Community 15 - "Criterio unificado de emparejado"
Cohesion: 0.33
Nodes (7): APIs (no scrape), Conteos esperados (Madrid, 28 tipos), Criterio unificado de emparejado, Objetivo, Pipeline (orden fijo), Qué cuenta como “producto base”, pick()

### Community 16 - "Precios: fuentes y límites"
Cohesion: 0.33
Nodes (5): Causas (resuelto / aceptado), Conteos de referencia (Madrid, 28 tipos), Cómo se obtienen, Precios: fuentes y límites, Qué no se promete

### Community 17 - "Ficha elegida (si hay X)"
Cohesion: 0.06
Nodes (30): aceite de girasol, aceite de oliva, agua, arroz, azúcar, café, carne picada, cebolla (+22 more)

### Community 18 - "dump_cobertura.py"
Cohesion: 0.13
Nodes (30): json, pathlib, re, fetch_line(), fold(), hit_word(), http_get(), http_post() (+22 more)

## Knowledge Gaps
- **75 isolated node(s):** `1. Root cause`, `2. Compare`, `3. Hypothesis`, `4. Fix`, `Red flags → back to step 1` (+70 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 99 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Criterio unificado de emparejado` connect `Criterio unificado de emparejado` to `Arrancar a mano`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `pick()` connect `Criterio unificado de emparejado` to `dump_cobertura.py`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `pick()` (e.g. with `Criterio unificado de emparejado` and `Pipeline (orden fijo)`) actually correct?**
  _`pick()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `1. Root cause`, `2. Compare`, `3. Hypothesis` to the rest of the system?**
  _75 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Ficha elegida (si hay X)` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._
- **Should `dump_cobertura.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13118279569892474 - nodes in this community are weakly interconnected._