# Graph Report - supermercados  (2026-10-21)

## Corpus Check
- 19 files · ~10,742 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: .mdc 2, (none) 1)

## Summary
- 79 nodes · 65 edges · 18 communities (13 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `08fe2e7e`
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
- EMPAREJADO.md
- tablas/SKILL.md
- DESIGN.md
- DECISIONES.md
- Criterio unificado de emparejado
- Precios: fuentes y límites
- Arrancar a mano

## God Nodes (most connected - your core abstractions)
1. `Debug` - 6 edges
2. `Contexto del proyecto` - 6 edges
3. `Criterio unificado de emparejado` - 6 edges
4. `Dashboard brief (for the Stitch prompt)` - 5 edges
5. `Arrancar a mano` - 5 edges
6. `Precios: fuentes y límites` - 5 edges
7. `Verify (UI)` - 4 edges
8. `Web design` - 4 edges
9. `Build judgments with Laya` - 3 edges
10. `Laya` - 3 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (18 total, 5 thin omitted)

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

### Community 9 - "EMPAREJADO.md"
Cohesion: 0.32
Nodes (4): Ejecutar a mano, Docs, Setup, supermercados

### Community 15 - "Criterio unificado de emparejado"
Cohesion: 0.33
Nodes (6): APIs (no scrape), Conteos esperados (Madrid, 28 tipos), Criterio unificado de emparejado, Objetivo, Pipeline (orden fijo), Qué cuenta como “producto base”

### Community 16 - "Precios: fuentes y límites"
Cohesion: 0.33
Nodes (5): Causas (resuelto / aceptado), Conteos de referencia (Madrid, 28 tipos), Cómo se obtienen, Precios: fuentes y límites, Qué no se promete

### Community 17 - "Arrancar a mano"
Cohesion: 0.40
Nodes (5): Arrancar a mano, Comprobar conteos (DevTools), Criterio de fichas (no reinventar), Local, Producción

## Knowledge Gaps
- **47 isolated node(s):** `1. Root cause`, `2. Compare`, `3. Hypothesis`, `4. Fix`, `Red flags → back to step 1` (+42 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 62 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Criterio unificado de emparejado` connect `Criterio unificado de emparejado` to `EMPAREJADO.md`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Arrancar a mano` connect `Arrancar a mano` to `EMPAREJADO.md`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `1. Root cause`, `2. Compare`, `3. Hypothesis` to the rest of the system?**
  _47 weakly-connected nodes found - possible documentation gaps or missing edges._