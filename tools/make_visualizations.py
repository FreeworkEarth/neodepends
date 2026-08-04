#!/usr/bin/env python3
"""make_visualizations.py -- self-contained HTML views of NeoDepends output.

Generates two offline-capable HTML files from a dependency JSON:
  dsm_view.html   -- DV8-style dependency structure matrix
  graph_view.html -- D3 force-directed dependency graph (2D/3D)

Input: dv8-dsm-v3.json (variables + cells with value-type dicts).
All CSS/JS is inlined -- no CDN, works offline via file://.

v0.3.10 development -- NeoDepends (FreeworkEarth fork)

When used via the pipeline (neodepends_python_export.py --viz), default
level is 'file'.  Standalone CLI supports --level file|entity|both.

Optional --clustering <json> for DV8-style nested group boxes.
The clustering JSON should be either:
  - DV8 drh-clustering format ({"name":..., "children":[...]})
  - A simple nested tree  {"name": "root", "children": [...]}
Leaf names must match variable names in the DSM.  When given, the DSM
row/col order follows the clustering leaf order and nested group boxes
are drawn.  Without it, package grouping is used.

The arch-agent DRH json (from dv8-console dr-hier:dr-hier) is the
intended producer of clustering input.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------

KIND_COLORS = {
    "Import": "#3b82f6",
    "ImportLazy": "#f59e0b",
    "ImportType": "#8b5cf6",
    "Call": "#10b981",
    "Use": "#6b7280",
    "Create": "#ef4444",
    "Extend": "#14b8a6",
    "Override": "#ec4899",
    "Contain": "#a3a3a3",
}

PKG_PALETTE = [
    "#4e9df3", "#3ecf8e", "#f2a33c", "#e5484d",
    "#9a7bff", "#2dd4bf", "#ff7854", "#e06bd0",
    "#06b6d4", "#84cc16",
]


# ---------------------------------------------------------------------------
# Variable name normalization
# ---------------------------------------------------------------------------

_ENTITY_SUFFIX_RE = re.compile(r"/[^/]+\s+\([^)]+\)$")


def _normalize_var(name: str) -> str:
    """Strip entity suffixes like '/self (File)', '/foo (Method)' etc.

    >>> _normalize_var("tts/booking_service.py/self (File)")
    'tts/booking_service.py'
    >>> _normalize_var("tts/booking_service.py/BookingService (Class)")
    'tts/booking_service.py/BookingService'
    >>> _normalize_var("main.py")
    'main.py'
    """
    # Strip '/self (File)' -- the most common case
    if name.endswith("/self (File)"):
        return name[:-len("/self (File)")]
    # Strip any '/<entity> (<Kind>)' suffix
    m = _ENTITY_SUFFIX_RE.search(name)
    if m:
        return name[:m.start()]
    return name


def _pkg_of(path: str) -> str:
    """Extract package (parent directory) from a file path."""
    parts = Path(path).parts
    return "/".join(parts[:-1]) + "/" if len(parts) > 1 else "(root)"


def _short_name(path: str) -> str:
    """Extract short display name (filename) from a path."""
    return Path(path).name


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dep_json(path: Path) -> Tuple[List[str], List[Dict]]:
    """Load variables + cells from a dv8-dsm-v3 / dv8-dependency JSON."""
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, dict) and "variables" in data and "cells" in data:
        return data["variables"], data["cells"]
    raise ValueError(f"Need {{variables, cells}} in {path}")


def load_clustering(path: Path) -> Optional[Dict]:
    """Load a clustering JSON (DV8 DRH format or simple tree)."""
    with open(path) as f:
        data = json.load(f)
    return data


def _clustering_leaf_order(tree: Dict) -> List[str]:
    """Extract leaf names in tree traversal order."""
    leaves: List[str] = []

    def _walk(node):
        children = node.get("children", [])
        if not children:
            leaves.append(node.get("name", ""))
        else:
            for child in children:
                _walk(child)

    _walk(tree)
    return leaves


def _clustering_groups(tree: Dict, depth: int = 0) -> List[Dict]:
    """Extract nested groups with their leaf ranges for box drawing.

    Returns list of {name, start, count, depth} where start/count
    refer to leaf-order positions.
    """
    groups: List[Dict] = []
    _pos = [0]  # mutable counter

    def _walk(node, d):
        children = node.get("children", [])
        if not children:
            _pos[0] += 1
            return
        start = _pos[0]
        for child in children:
            _walk(child, d + 1)
        count = _pos[0] - start
        if count > 0:
            groups.append({
                "name": node.get("name", ""),
                "start": start,
                "count": count,
                "depth": d,
            })

    _walk(tree, 0)
    return groups


# ---------------------------------------------------------------------------
# D3 library loader
# ---------------------------------------------------------------------------

def _load_d3_lib() -> str:
    """Load the inlined D3 v7 + d3-force-3d library."""
    lib_path = Path(__file__).resolve().parent / "viz_libs" / "d3.min.js"
    if lib_path.exists():
        return lib_path.read_text(encoding="utf-8")
    return ""


# ---------------------------------------------------------------------------
# DSM view
# ---------------------------------------------------------------------------

def generate_dsm_html(variables: List[str], cells: List[Dict],
                      output_path: Path, title: str = "DSM View",
                      clustering: Optional[Dict] = None,
                      is_entity_level: bool = False) -> None:
    n = len(variables)

    # Normalize variable names
    norm_names = [_normalize_var(v) for v in variables]

    # Determine row/col order
    if clustering:
        # Use clustering leaf order
        leaf_order = _clustering_leaf_order(clustering)
        # Map leaf names to indices (try both raw and normalized)
        name_to_idx = {}
        for i, v in enumerate(variables):
            name_to_idx[v] = i
            name_to_idx[norm_names[i]] = i
        order = []
        for leaf in leaf_order:
            if leaf in name_to_idx:
                order.append(name_to_idx[leaf])
        # Add any variables not in the clustering
        in_order = set(order)
        for i in range(n):
            if i not in in_order:
                order.append(i)
        # Build clustering groups for box drawing
        cluster_groups = _clustering_groups(clustering)
    else:
        # Sort by normalized name (groups by package)
        order = sorted(range(n), key=lambda i: norm_names[i])
        cluster_groups = None

    # Build package groups (when no clustering)
    pkg_groups_list = []
    if not clustering:
        pkgs_seen: Dict[str, List[int]] = {}
        for pos, idx in enumerate(order):
            if is_entity_level:
                # For entity level, group by parent file
                parts = norm_names[idx].split("/")
                # Find the .py file part
                pkg = "(root)"
                for j, part in enumerate(parts):
                    if part.endswith(".py"):
                        pkg = "/".join(parts[:j + 1])
                        break
                else:
                    pkg = _pkg_of(norm_names[idx])
            else:
                pkg = _pkg_of(norm_names[idx])
            pkgs_seen.setdefault(pkg, []).append(pos)
        for pkg, positions in pkgs_seen.items():
            pkg_groups_list.append({"name": pkg, "start": positions[0],
                                    "count": len(positions)})

    # Build matrix as sparse dict "row,col" -> {kind: count}
    idx_to_pos = {idx: pos for pos, idx in enumerate(order)}
    matrix: Dict[str, Dict[str, float]] = {}
    for cell in cells:
        s, d = cell.get("src", -1), cell.get("dest", -1)
        if s < 0 or s >= n or d < 0 or d >= n:
            continue
        values = cell.get("values", {})
        if not values:
            continue
        sp, dp = idx_to_pos.get(s), idx_to_pos.get(d)
        if sp is None or dp is None:
            continue
        key = f"{sp},{dp}"
        if key not in matrix:
            matrix[key] = {}
        for k, v in values.items():
            matrix[key][k] = matrix[key].get(k, 0) + v

    # Ordered display names
    ordered_names = [norm_names[i] for i in order]

    data_json = json.dumps({
        "title": title,
        "variables": ordered_names,
        "pkgGroups": pkg_groups_list,
        "clusterGroups": cluster_groups,
        "matrix": matrix,
        "kindColors": KIND_COLORS,
        "isEntity": is_entity_level,
    })

    html = _DSM_TEMPLATE.replace("__DATA_JSON__", data_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


_DSM_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>DSM View</title>
<style>
:root {
  --bg: #12151c; --panel: #1b202b; --panel2: #232a38;
  --ink: #e8ecf3; --dim: #8b94a7; --accent: #5aa9e6;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
       background: var(--bg); color: var(--ink); overflow: auto; }
#header { padding: 12px 20px; display: flex; align-items: center; gap: 24px;
          background: var(--panel); border-bottom: 1px solid #2c3442; flex-wrap: wrap; }
#header h2 { font-size: 16px; font-weight: 600; white-space: nowrap; }
#legend { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
.legend-item { display: flex; align-items: center; gap: 4px; font-size: 11px; }
.legend-swatch { width: 14px; height: 14px; border-radius: 2px; }
#pkg-list { display: flex; gap: 8px; flex-wrap: wrap; font-size: 11px; }
.pkg-btn { cursor: pointer; padding: 2px 8px; border: 1px solid #3a4557;
           border-radius: 3px; background: var(--panel2); user-select: none;
           color: var(--ink); }
.pkg-btn:hover { background: #39445a; }
.pkg-btn.collapsed { opacity: 0.4; text-decoration: line-through; }
#dsm-controls { display: flex; gap: 16px; flex-wrap: wrap; align-items: center; font-size: 11px; }
.sl { display: flex; align-items: center; gap: 6px; }
.sl span { color: var(--dim); white-space: nowrap; }
.sl input[type=range] { width: 80px; accent-color: var(--accent); height: 14px; }
.sl b { width: 28px; text-align: right; color: var(--ink); font-weight: 500; }
label.ck { display: flex; align-items: center; gap: 5px; font-size: 11px;
           cursor: pointer; color: var(--dim); }
label.ck input { accent-color: var(--accent); }
#container { padding: 10px; overflow: auto; }
#tooltip { position: fixed; pointer-events: none; background: #0c1016ee;
           border: 1px solid #3a4557; border-radius: 6px; padding: 8px 12px;
           font-size: 12px; max-width: 420px; display: none; z-index: 999;
           line-height: 1.5; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
canvas { image-rendering: pixelated; }
</style>
</head>
<body>
<div id="header">
  <h2 id="title"></h2>
  <div id="legend"></div>
  <div id="pkg-list"></div>
  <div id="dsm-controls">
    <div class="sl"><span>Cell</span><input type="range" id="sl-cell" min="8" max="40" step="1"><b id="v-cell"></b></div>
    <div class="sl"><span>Labels</span><input type="range" id="sl-lw" min="100" max="300" step="5"><b id="v-lw"></b></div>
    <label class="ck"><input type="checkbox" id="ck-counts" checked> counts in cells</label>
  </div>
</div>
<div id="container"><canvas id="dsm"></canvas></div>
<div id="tooltip"></div>
<script>
(function(){
const D = __DATA_JSON__;
const vars = D.variables;
const N = vars.length;
const mat = D.matrix;
const KC = D.kindColors;
const pkgs = D.pkgGroups || [];
const clusterGroups = D.clusterGroups || null;

document.getElementById("title").textContent = D.title || "DSM View";

// Legend
const leg = document.getElementById("legend");
const usedKinds = new Set();
for (const v of Object.values(mat)) {
  for (const k of Object.keys(v)) usedKinds.add(k);
}
for (const [k, c] of Object.entries(KC)) {
  if (!usedKinds.has(k)) continue;
  const d = document.createElement("span");
  d.className = "legend-item";
  d.innerHTML = '<span class="legend-swatch" style="background:'+c+'"></span>'+k;
  leg.appendChild(d);
}

// Short name helper
function shortName(p) {
  const i = p.lastIndexOf("/");
  return i >= 0 ? p.substring(i + 1) : p;
}
function pkgOf(p) {
  if (D.isEntity) {
    // For entity: find the .py file, use it as grouping key
    const parts = p.split("/");
    for (let j = 0; j < parts.length; j++) {
      if (parts[j].endsWith(".py")) return parts.slice(0, j + 1).join("/");
    }
  }
  const i = p.lastIndexOf("/");
  return i > 0 ? p.substring(0, i + 1) : "(root)";
}

// Package toggle buttons
const collapsed = new Set();
const pkgList = document.getElementById("pkg-list");
if (!clusterGroups) {
  pkgs.forEach(p => {
    const btn = document.createElement("span");
    btn.className = "pkg-btn";
    btn.textContent = p.name + " (" + p.count + ")";
    btn.onclick = () => {
      if (collapsed.has(p.name)) { collapsed.delete(p.name); btn.classList.remove("collapsed"); }
      else { collapsed.add(p.name); btn.classList.add("collapsed"); }
      draw();
    };
    pkgList.appendChild(btn);
  });
}

const canvas = document.getElementById("dsm");
const ctx = canvas.getContext("2d");
const tooltip = document.getElementById("tooltip");

let CELL = N > 80 ? 14 : N > 40 ? 20 : 28;
let LABEL_W = N > 80 ? 120 : 180;
let LABEL_H = N > 80 ? 100 : 140;
let showCounts = true;
let visibleIdx = [];

// DSM control sliders
const slCell = document.getElementById("sl-cell");
const slLW = document.getElementById("sl-lw");
const ckCounts = document.getElementById("ck-counts");
slCell.value = CELL; document.getElementById("v-cell").textContent = CELL;
slLW.value = LABEL_W; document.getElementById("v-lw").textContent = LABEL_W;
slCell.addEventListener("input", () => {
  CELL = +slCell.value; document.getElementById("v-cell").textContent = CELL;
  LABEL_H = Math.max(CELL * 4, 80); draw();
});
slLW.addEventListener("input", () => {
  LABEL_W = +slLW.value; document.getElementById("v-lw").textContent = LABEL_W; draw();
});
ckCounts.addEventListener("change", () => { showCounts = ckCounts.checked; draw(); });

function draw() {
  // Determine visible indices
  visibleIdx = [];
  for (let i = 0; i < N; i++) {
    if (!collapsed.has(pkgOf(vars[i]))) visibleIdx.push(i);
  }
  const VN = visibleIdx.length;
  const W = LABEL_W + VN * CELL;
  const H = LABEL_H + VN * CELL;
  const dpr = window.devicePixelRatio || 1;
  canvas.width = W * dpr;
  canvas.height = H * dpr;
  canvas.style.width = W + "px";
  canvas.style.height = H + "px";
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

  // Background
  ctx.fillStyle = "#12151c";
  ctx.fillRect(0, 0, W, H);

  const ox = LABEL_W;
  const oy = LABEL_H;

  // Draw cells
  for (let ri = 0; ri < VN; ri++) {
    for (let ci = 0; ci < VN; ci++) {
      const r = visibleIdx[ri];
      const c = visibleIdx[ci];
      const key = r + "," + c;
      const x = ox + ci * CELL;
      const y = oy + ri * CELL;

      if (r === c) {
        ctx.fillStyle = "#1e293b";
        ctx.fillRect(x, y, CELL, CELL);
      } else {
        const vals = mat[key];
        if (vals) {
          let maxK = "", maxV = 0;
          for (const [k, v] of Object.entries(vals)) {
            if (v > maxV) { maxV = v; maxK = k; }
          }
          const color = KC[maxK] || "#555";
          const alpha = Math.min(1, 0.3 + 0.7 * Math.min(maxV, 10) / 10);
          ctx.globalAlpha = alpha;
          ctx.fillStyle = color;
          ctx.fillRect(x + 1, y + 1, CELL - 2, CELL - 2);
          ctx.globalAlpha = 1;
          if (showCounts && CELL >= 16) {
            const total = Object.values(vals).reduce((a, b) => a + b, 0);
            if (total > 0) {
              ctx.fillStyle = "#fff";
              const fs = Math.max(7, Math.min(11, CELL * 0.38));
              ctx.font = fs + "px monospace";
              ctx.textAlign = "center";
              ctx.textBaseline = "middle";
              ctx.fillText(total > 99 ? "99+" : String(Math.round(total)),
                           x + CELL/2, y + CELL/2);
            }
          }
        }
      }
    }
  }

  // Grid lines
  ctx.strokeStyle = "#2c3442";
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= VN; i++) {
    ctx.beginPath();
    ctx.moveTo(ox + i * CELL, oy);
    ctx.lineTo(ox + i * CELL, oy + VN * CELL);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(ox, oy + i * CELL);
    ctx.lineTo(ox + VN * CELL, oy + i * CELL);
    ctx.stroke();
  }

  // Clustering boxes (DV8-style nested groups)
  if (clusterGroups) {
    const maxDepth = Math.max(...clusterGroups.map(g => g.depth));
    const groupColors = ["#5aa9e6", "#f59e0b", "#8b5cf6", "#10b981", "#ef4444"];
    clusterGroups.forEach(g => {
      // Map cluster positions to visible positions
      const vs = [], ve = [];
      for (let i = 0; i < VN; i++) {
        const vi = visibleIdx[i];
        if (vi >= g.start && vi < g.start + g.count) {
          if (vs.length === 0) vs.push(i);
          ve.push(i);
        }
      }
      if (vs.length === 0) return;
      const startPos = vs[0];
      const endPos = ve[ve.length - 1] + 1;
      const color = groupColors[g.depth % groupColors.length];
      const pad = (maxDepth - g.depth) * 2;

      ctx.strokeStyle = color;
      ctx.lineWidth = Math.max(1, 2 - g.depth * 0.5);
      ctx.globalAlpha = 0.7;
      // Row box
      ctx.strokeRect(ox + startPos * CELL - pad, oy + startPos * CELL - pad,
                     (endPos - startPos) * CELL + pad * 2,
                     (endPos - startPos) * CELL + pad * 2);
      ctx.globalAlpha = 1;

      // Group label in margin
      if (g.name && g.depth <= 1) {
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.8;
        ctx.font = (g.depth === 0 ? "bold " : "") + "10px monospace";
        ctx.textAlign = "right";
        ctx.textBaseline = "top";
        const label = g.name.length > 20 ? g.name.substring(0, 18) + ".." : g.name;
        ctx.fillText(label, ox - 4 - pad, oy + startPos * CELL);
        ctx.globalAlpha = 1;
      }
    });
  } else {
    // Package separator lines
    let prevPkg = "";
    ctx.strokeStyle = "#f59e0b";
    ctx.lineWidth = 2;
    for (let i = 0; i < VN; i++) {
      const pkg = pkgOf(vars[visibleIdx[i]]);
      if (pkg !== prevPkg && i > 0) {
        ctx.beginPath();
        ctx.moveTo(ox, oy + i * CELL);
        ctx.lineTo(ox + VN * CELL, oy + i * CELL);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(ox + i * CELL, oy);
        ctx.lineTo(ox + i * CELL, oy + VN * CELL);
        ctx.stroke();
      }
      prevPkg = pkg;
    }
  }

  // Diagonal line
  ctx.strokeStyle = "rgba(255,255,255,0.12)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(ox, oy);
  ctx.lineTo(ox + VN * CELL, oy + VN * CELL);
  ctx.stroke();

  // Row labels
  ctx.fillStyle = "#ccc";
  ctx.font = "11px monospace";
  ctx.textAlign = "right";
  ctx.textBaseline = "middle";
  for (let i = 0; i < VN; i++) {
    const name = D.isEntity ? vars[visibleIdx[i]] : shortName(vars[visibleIdx[i]]);
    const maxLen = Math.floor((LABEL_W - 12) / 6.6);
    const label = name.length > maxLen ? name.substring(0, maxLen - 2) + ".." : name;
    ctx.fillText(label, ox - 6, oy + i * CELL + CELL / 2);
  }

  // Column labels (rotated)
  ctx.save();
  ctx.fillStyle = "#ccc";
  ctx.font = "11px monospace";
  ctx.textAlign = "left";
  ctx.textBaseline = "middle";
  for (let i = 0; i < VN; i++) {
    const name = D.isEntity ? vars[visibleIdx[i]] : shortName(vars[visibleIdx[i]]);
    const label = name.length > 18 ? name.substring(0, 16) + ".." : name;
    const x = ox + i * CELL + CELL / 2;
    const y = oy - 6;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(-Math.PI / 4);
    ctx.fillText(label, 0, 0);
    ctx.restore();
  }
  ctx.restore();
}

// Hover tooltip
canvas.addEventListener("mousemove", function(e) {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const VN2 = visibleIdx.length;
  const col = Math.floor((mx - LABEL_W) / CELL);
  const row = Math.floor((my - LABEL_H) / CELL);

  if (col >= 0 && col < VN2 && row >= 0 && row < VN2) {
    const ri = visibleIdx[row];
    const ci = visibleIdx[col];
    const key = ri + "," + ci;
    const vals = mat[key];
    let html = "<b>" + vars[ri] + "</b><br>&rarr; <b>" + vars[ci] + "</b>";
    if (vals) {
      html += "<br><br>";
      for (const [k, v] of Object.entries(vals)) {
        const c = KC[k] || "#888";
        html += '<span style="color:'+c+'">&#9632;</span> ' + k + ": " + Math.round(v) + "<br>";
      }
    } else if (ri === ci) {
      html += "<br><i>(self)</i>";
    } else {
      html += "<br><i>(no dependency)</i>";
    }
    tooltip.innerHTML = html;
    tooltip.style.display = "block";
    tooltip.style.left = (e.clientX + 16) + "px";
    tooltip.style.top = (e.clientY + 16) + "px";
  } else {
    tooltip.style.display = "none";
  }
});
canvas.addEventListener("mouseleave", () => { tooltip.style.display = "none"; });

draw();
window.addEventListener("resize", draw);
})();
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Graph view (D3 force-directed, arch-agent visual language)
# ---------------------------------------------------------------------------

def generate_graph_html(variables: List[str], cells: List[Dict],
                        output_path: Path, title: str = "Graph View",
                        is_entity_level: bool = False) -> None:
    n = len(variables)

    # Normalize variable names
    norm_names = [_normalize_var(v) for v in variables]

    # Build nodes
    in_deg = [0] * n
    out_deg = [0] * n
    links: List[Dict] = []
    all_kinds: set = set()

    for cell in cells:
        s, d = cell.get("src", -1), cell.get("dest", -1)
        if s < 0 or s >= n or d < 0 or d >= n or s == d:
            continue
        values = cell.get("values", {})
        for k, v in values.items():
            if v > 0:
                links.append({"src": s, "dst": d, "kind": k, "weight": v})
                out_deg[s] += v
                in_deg[d] += v
                all_kinds.add(k)

    # Package assignment
    def _pkg_for_graph(name: str) -> str:
        if is_entity_level:
            parts = name.split("/")
            for j, part in enumerate(parts):
                if part.endswith(".py"):
                    return "/".join(parts[:j + 1])
            return _pkg_of(name)
        return _pkg_of(name)

    pkg_set = sorted({_pkg_for_graph(v) for v in norm_names})
    pkg_color_map = {p: PKG_PALETTE[i % len(PKG_PALETTE)]
                     for i, p in enumerate(pkg_set)}

    nodes = []
    for i, v in enumerate(norm_names):
        pkg = _pkg_for_graph(v)
        nodes.append({
            "id": i,
            "name": v,
            "short": _short_name(v) if not is_entity_level else v,
            "pkg": pkg,
            "color": pkg_color_map[pkg],
            "degree": in_deg[i] + out_deg[i],
            "inDeg": in_deg[i],
            "outDeg": out_deg[i],
        })

    # Deduplicate links (combine same src,dst with different kinds)
    link_map: Dict[str, Dict] = {}
    for l in links:
        key = f"{l['src']},{l['dst']}"
        if key not in link_map:
            link_map[key] = {"src": l["src"], "dst": l["dst"],
                             "weight": 0, "kinds": {}}
        link_map[key]["weight"] += l["weight"]
        link_map[key]["kinds"][l["kind"]] = (
            link_map[key]["kinds"].get(l["kind"], 0) + l["weight"])
    deduped_links = list(link_map.values())

    d3_lib = _load_d3_lib()

    data_json = json.dumps({
        "title": title,
        "nodes": nodes,
        "links": deduped_links,
        "kindColors": KIND_COLORS,
        "pkgColors": pkg_color_map,
        "allKinds": sorted(all_kinds),
        "isEntity": is_entity_level,
    })

    html = _GRAPH_TEMPLATE.replace("__DATA_JSON__", data_json)
    html = html.replace("/*__D3LIB__*/", d3_lib)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")


_GRAPH_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Graph View</title>
<script>/*__D3LIB__*/</script>
<style>
:root {
  --bg: #12151c; --panel: #1b202b; --panel2: #232a38;
  --ink: #e8ecf3; --dim: #8b94a7; --accent: #5aa9e6;
  --red: #e5484d; --green: #46c98e;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
       background: var(--bg); color: var(--ink); overflow: hidden; }
#header { padding: 10px 20px; display: flex; align-items: center; gap: 16px;
          background: var(--panel); border-bottom: 1px solid #2c3442; flex-wrap: wrap;
          z-index: 10; position: relative; }
#header h2 { font-size: 16px; font-weight: 600; white-space: nowrap; }
#controls { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
button { background: var(--panel2); color: var(--ink); border: 1px solid #3a4557;
         border-radius: 6px; padding: 5px 9px; font-size: 12px; cursor: pointer; }
button:hover { background: #39445a; }
button.on { background: var(--accent); border-color: var(--accent); color: #0c1016;
            font-weight: 600; }
button.warn { }
button.warn.on { background: var(--red); border-color: var(--red); color: #fff; }
.toggle { display: flex; align-items: center; gap: 4px; font-size: 11px; cursor: pointer;
          padding: 3px 8px; border: 1px solid #3a4557; border-radius: 3px;
          background: var(--panel2); user-select: none; color: var(--ink); }
.toggle:hover { background: #39445a; }
.toggle.off { opacity: 0.3; text-decoration: line-through; }
.toggle-swatch { display: inline-block; width: 12px; height: 12px; border-radius: 2px; }
#search { background: #12151c; border: 1px solid #3a4557; color: var(--ink);
          padding: 4px 10px; border-radius: 6px; font-size: 12px; width: 180px; }
#search:focus { outline: none; border-color: var(--accent); }
#pkg-legend { display: flex; gap: 10px; flex-wrap: wrap; font-size: 11px; }
.pkg-legend-item { display: flex; align-items: center; gap: 4px; }
.pkg-swatch { width: 10px; height: 10px; border-radius: 50%; }
canvas { position: absolute; inset: 0; }
#main { flex: 1; position: relative; width: 100%; height: calc(100vh - 52px); display: flex; }
#graph-area { flex: 1; position: relative; }
#side { width: 220px; min-width: 220px; background: var(--panel); padding: 12px;
        overflow-y: auto; border-left: 1px solid #2c3442; transition: width 0.15s;
        font-size: 11.5px; }
#side.collapsed { width: 0; min-width: 0; padding: 0; overflow: hidden; }
#side h3 { font-size: 11px; text-transform: uppercase; letter-spacing: .8px;
           color: var(--dim); margin: 10px 0 6px; }
#side h3:first-child { margin-top: 0; }
.sl { display: flex; align-items: center; gap: 6px; padding: 2px 0; }
.sl span { width: 80px; color: var(--dim); white-space: nowrap; }
.sl input[type=range] { flex: 1; accent-color: var(--accent); height: 14px; }
.sl b { width: 32px; text-align: right; color: var(--ink); font-weight: 500; font-size: 11px; }
label.ck { display: flex; align-items: center; gap: 6px; padding: 3px 0;
           cursor: pointer; color: var(--dim); }
label.ck input { accent-color: var(--accent); }
#btn-panel { position: absolute; top: 60px; right: 8px; z-index: 6; }
#btn-panel.shifted { right: 228px; }
#btn-reset { margin-top: 8px; width: 100%; }
#tooltip { position: fixed; pointer-events: none; background: #0c1016ee;
           border: 1px solid #3a4557; border-radius: 8px; padding: 8px 12px;
           font-size: 12px; max-width: 340px; display: none; z-index: 999;
           line-height: 1.55; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }
#tooltip .t { font-weight: 600; color: #fff; }
#tooltip .d { color: var(--dim); }
#modebar { position: absolute; top: 12px; left: 50%; transform: translateX(-50%);
           display: flex; gap: 14px; z-index: 5; }
.bargroup { display: flex; gap: 6px; background: #1b202bcc; padding: 6px;
            border-radius: 10px; border: 1px solid #2c3442; }
#hint { position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%);
        font-size: 11px; color: var(--dim); background: #1b202bcc; padding: 4px 12px;
        border-radius: 8px; z-index: 5; }
.pill { display: inline-block; padding: 1px 7px; border-radius: 99px; font-size: 10.5px;
        margin-left: 4px; }
.pill.scc { background: #e5484d33; color: #ff8f92; border: 1px solid #e5484d66; }
</style>
</head>
<body>
<div id="header">
  <h2 id="title"></h2>
  <input id="search" type="text" placeholder="Search...">
  <div id="controls"></div>
  <div id="pkg-legend"></div>
</div>
<div id="main">
  <div id="graph-area">
    <canvas id="cv"></canvas>
    <div id="modebar">
      <div class="bargroup">
        <button data-r="2d" class="on">2D</button>
        <button data-r="3d">3D orbit</button>
      </div>
      <div class="bargroup">
        <button id="btn-fit">Fit</button>
        <button id="btn-scc" class="warn">Cycles (SCC)</button>
      </div>
    </div>
    <button id="btn-panel">Controls</button>
    <div id="hint">scroll = zoom | drag background = pan | drag node = move | click = isolate | double-click = reset</div>
  </div>
  <div id="side">
    <h3>Visual</h3>
    <div class="sl"><span>Node size</span><input type="range" id="sl-node" min="0.3" max="3" step="0.05" value="1"><b id="v-node">1.0</b></div>
    <div class="sl"><span>Edge opacity</span><input type="range" id="sl-eo" min="0.02" max="1" step="0.01" value="0.16"><b id="v-eo">0.16</b></div>
    <div class="sl"><span>Edge width</span><input type="range" id="sl-ew" min="0.3" max="4" step="0.05" value="1"><b id="v-ew">1.0</b></div>
    <div class="sl"><span>Label threshold</span><input type="range" id="sl-lt" min="0" max="100" step="1" value="0"><b id="v-lt">0</b></div>
    <label class="ck"><input type="checkbox" id="ck-alllabels"> all labels</label>
    <h3>Physics</h3>
    <div class="sl"><span>Link distance</span><input type="range" id="sl-ld" min="10" max="200" step="1" value="38"><b id="v-ld">38</b></div>
    <div class="sl"><span>Charge</span><input type="range" id="sl-ch" min="-300" max="-10" step="1" value="-42"><b id="v-ch">-42</b></div>
    <div class="sl"><span>Collide</span><input type="range" id="sl-co" min="0" max="3" step="0.05" value="1"><b id="v-co">1.0</b></div>
    <button id="btn-reset">Reset controls</button>
  </div>
  <div id="tooltip"></div>
</div>
<script>
(function(){
const D = __DATA_JSON__;
const nodes = D.nodes;
const links = D.links;
const KC = D.kindColors;
const N = nodes.length;

document.getElementById("title").textContent = D.title || "Graph View";

// ---------- Tarjan SCC ----------
function tarjanSCC(n, edges) {
  let index = 0;
  const stack = [], onStack = new Array(n).fill(false);
  const idx = new Array(n).fill(-1), low = new Array(n).fill(-1);
  const sccs = [];
  const adj = Array.from({length: n}, () => []);
  edges.forEach(e => adj[e.src].push(e.dst));

  function strongconnect(v) {
    idx[v] = low[v] = index++;
    stack.push(v); onStack[v] = true;
    for (const w of adj[v]) {
      if (idx[w] < 0) { strongconnect(w); low[v] = Math.min(low[v], low[w]); }
      else if (onStack[w]) { low[v] = Math.min(low[v], idx[w]); }
    }
    if (low[v] === idx[v]) {
      const scc = [];
      let w;
      do { w = stack.pop(); onStack[w] = false; scc.push(w); } while (w !== v);
      if (scc.length > 1) sccs.push(scc);
    }
  }
  for (let v = 0; v < n; v++) { if (idx[v] < 0) strongconnect(v); }
  return sccs;
}

const sccs = tarjanSCC(N, links);
const sccOf = new Array(N).fill(-1);
sccs.forEach((scc, i) => scc.forEach(v => sccOf[v] = i));
const inSCC = new Set();
sccs.forEach(scc => scc.forEach(v => inSCC.add(v)));

// ---------- edge kind toggles ----------
const hiddenKinds = new Set();
const ctrlDiv = document.getElementById("controls");
D.allKinds.forEach(k => {
  const btn = document.createElement("span");
  btn.className = "toggle";
  const c = KC[k] || "#888";
  btn.innerHTML = '<span class="toggle-swatch" style="background:'+c+'"></span> ' + k;
  btn.onclick = () => {
    if (hiddenKinds.has(k)) { hiddenKinds.delete(k); btn.classList.remove("off"); }
    else { hiddenKinds.add(k); btn.classList.add("off"); }
    draw();
  };
  ctrlDiv.appendChild(btn);
});

// Package legend
const pkgLeg = document.getElementById("pkg-legend");
for (const [p, c] of Object.entries(D.pkgColors)) {
  const d = document.createElement("span");
  d.className = "pkg-legend-item";
  d.innerHTML = '<span class="pkg-swatch" style="background:'+c+'"></span>' + p;
  pkgLeg.appendChild(d);
}

// ---------- slider state ----------
const S = {node: 1, eo: 0.16, ew: 1, lt: 0, allLabels: false,
           ld: 38, ch: -42, co: 1};
const S_DEFAULTS = {...S};

// ---------- canvas ----------
const cv = document.getElementById("cv");
const ctx = cv.getContext("2d");
const tip = document.getElementById("tooltip");
const graphArea = document.getElementById("graph-area");
let W = 0, H = 0, DPR = window.devicePixelRatio || 1;

function resize() {
  const r = graphArea.getBoundingClientRect();
  W = r.width; H = r.height;
  cv.width = W * DPR; cv.height = H * DPR;
  cv.style.width = W + "px"; cv.style.height = H + "px";
  draw();
}
window.addEventListener("resize", resize);

// ---------- state ----------
let renderer = "2d";
let showSCC = false;
let selected = -1, hovered = -1;
let searchHits = new Set();
let transform = typeof d3 !== "undefined" ? d3.zoomIdentity : {x:0, y:0, k:1,
  applyX(v){return v*this.k+this.x}, applyY(v){return v*this.k+this.y}};

// 3D camera
const cam = {yaw: 0.55, pitch: 0.32, zoom: 1, panx: 0, pany: 0, fov: 1200, off: 520};

// ---------- derived ----------
const maxDeg = Math.max(1, ...nodes.map(n => n.degree));
const nbrs = Array.from({length: N}, () => new Set());
links.forEach(l => { nbrs[l.src].add(l.dst); nbrs[l.dst].add(l.src); });

function radiusOf(n) { return (2 + Math.pow(Math.sqrt(n.degree) * 0.85, 1) * 1.2) * S.node; }

nodes.forEach(n => { n.z = Math.sin(n.id * 13.7) * 120; });

// ---------- simulation ----------
let sim = null;

function layout(reseed) {
  if (sim) sim.stop();
  const is3 = renderer === "3d";

  if (typeof d3 === "undefined") {
    // Fallback: circular layout without D3
    nodes.forEach((n, i) => {
      const angle = (i / N) * 2 * Math.PI;
      const r = Math.min(W, H) * 0.35;
      n.x = W/2 + r * Math.cos(angle);
      n.y = H/2 + r * Math.sin(angle);
    });
    draw();
    return;
  }

  sim = d3.forceSimulation(nodes, is3 ? 3 : 2)
    .force("link", d3.forceLink(links.map(l => ({source: l.src, target: l.dst, w: l.weight})))
      .id(d => d.id))
    .force("charge", d3.forceManyBody().theta(0.95))
    .force("collide", d3.forceCollide().radius(d => radiusOf(d) * S.co + 1.4).iterations(1))
    .on("tick", draw);

  const link = sim.force("link"), charge = sim.force("charge");

  if (is3) {
    charge.strength(S.ch);
    link.distance(S.ld).strength(e => 0.10);
    sim.force("center", d3.forceCenter(0, 0, 0));
    if (reseed) nodes.forEach(n => {
      n.x = Math.sin(n.id * 7.1) * 300;
      n.y = Math.cos(n.id * 3.3) * 300;
      n.z = Math.sin(n.id * 13.7) * 300;
      n.vx = n.vy = n.vz = 0; n.fx = n.fy = n.fz = null;
    });
  } else {
    charge.strength(S.ch);
    link.distance(S.ld).strength(e => 0.12);
    sim.force("center", d3.forceCenter(W/2, H/2));
    if (reseed) nodes.forEach(n => { n.fx = n.fy = null; });
  }
  sim.alpha(0.9).restart();
}

// ---------- zoom to fit ----------
function zoomToFit() {
  if (renderer === "3d" || typeof d3 === "undefined") return;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  nodes.forEach(n => {
    const r = radiusOf(n);
    if (n.x - r < minX) minX = n.x - r;
    if (n.x + r > maxX) maxX = n.x + r;
    if (n.y - r < minY) minY = n.y - r;
    if (n.y + r > maxY) maxY = n.y + r;
  });
  const pad = 40;
  const dw = maxX - minX + pad * 2;
  const dh = maxY - minY + pad * 2;
  const scale = Math.min(W / dw, H / dh, 3);
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;
  transform = d3.zoomIdentity
    .translate(W/2 - cx * scale, H/2 - cy * scale)
    .scale(scale);
  d3.select(cv).call(zoom.transform, transform);
  draw();
}

// ---------- 3D projection ----------
function projSetup() {
  const ca = Math.cos(cam.yaw), sa = Math.sin(cam.yaw);
  const cb = Math.cos(cam.pitch), sb = Math.sin(cam.pitch);
  return function(x, y, z) {
    const x1 = x*ca + z*sa, z1 = -x*sa + z*ca;
    const y1 = y*cb - z1*sb, z2 = y*sb + z1*cb;
    const f = cam.fov / (cam.fov + z2 + cam.off);
    return [W/2 + cam.panx + x1*f*cam.zoom, H/2 + cam.pany - y1*f*cam.zoom, z2, f];
  };
}

// ---------- drawing ----------
function draw() {
  ctx.save();
  ctx.clearRect(0, 0, cv.width, cv.height);
  ctx.scale(DPR, DPR);
  ctx.fillStyle = "#12151c";
  ctx.fillRect(0, 0, W, H);

  const focus = selected >= 0 ? selected : (hovered >= 0 ? hovered : -1);
  const focusSet = focus >= 0 ? nbrs[focus] : null;
  const k2 = renderer === "2d" ? transform.k : 1;

  if (renderer === "2d") {
    ctx.translate(transform.x, transform.y);
    ctx.scale(transform.k, transform.k);
    nodes.forEach(n => { n.sx = n.x; n.sy = n.y; n.sr = radiusOf(n); n.sf = 1; });
  } else {
    const P = projSetup();
    nodes.forEach(n => {
      const [sx, sy, z2, f] = P(n.x, n.y, n.z || 0);
      n.sx = sx; n.sy = sy; n.sz = z2; n.sf = f * cam.zoom; n.sr = radiusOf(n) * n.sf;
    });
  }

  // SCC hulls (2D only)
  if (renderer === "2d" && showSCC && sccs.length > 0 && typeof d3 !== "undefined") {
    sccs.forEach(scc => {
      if (scc.length < 2) return;
      const pts = scc.map(v => [nodes[v].sx, nodes[v].sy]);
      const hull = d3.polygonHull(pts);
      if (!hull) return;
      const cx = d3.mean(hull, p => p[0]), cy = d3.mean(hull, p => p[1]);
      const exp = hull.map(([x, y]) => {
        const dx = x - cx, dy = y - cy, l = Math.hypot(dx, dy) || 1;
        return [x + dx/l * 16, y + dy/l * 16];
      });
      ctx.beginPath();
      exp.forEach((p, i) => i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]));
      ctx.closePath();
      ctx.globalAlpha = 0.09; ctx.fillStyle = "#e5484d"; ctx.fill();
      ctx.globalAlpha = 0.5; ctx.strokeStyle = "#e5484d"; ctx.lineWidth = 1.2 / k2;
      ctx.setLineDash([6/k2, 4/k2]); ctx.stroke(); ctx.setLineDash([]);
      ctx.globalAlpha = 1;
    });
  }

  // edges
  const lw = Math.max(0.3, 0.7 / k2) * S.ew;
  links.forEach(l => {
    // Find dominant visible kind
    let bestK = "", bestV = 0;
    for (const [k, v] of Object.entries(l.kinds)) {
      if (!hiddenKinds.has(k) && v > bestV) { bestV = v; bestK = k; }
    }
    if (!bestK) return;

    let alpha = S.eo, width = lw * (0.7 + Math.min(l.weight, 8) * 0.12);
    let color = KC[bestK] || "#666";

    if (focus >= 0) {
      if (l.src === focus || l.dst === focus) { alpha = 0.95; width = Math.max(width, lw * 1.8); }
      else alpha *= 0.05;
    } else if (searchHits.size && !(searchHits.has(l.src) || searchHits.has(l.dst))) {
      alpha *= 0.25;
    }

    const sn = nodes[l.src], tn = nodes[l.dst];
    ctx.strokeStyle = color;
    ctx.globalAlpha = Math.min(1, alpha);
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(sn.sx, sn.sy);
    ctx.lineTo(tn.sx, tn.sy);
    ctx.stroke();
  });
  ctx.globalAlpha = 1;

  // nodes
  const drawOrder = renderer === "3d" ? nodes.slice().sort((a, b) => b.sz - a.sz) : nodes;
  drawOrder.forEach(n => {
    let a = 1;
    if (focus >= 0) a = (n.id === focus || focusSet.has(n.id)) ? 1 : 0.12;
    else if (searchHits.size) a = searchHits.has(n.id) ? 1 : 0.18;
    ctx.globalAlpha = a;
    ctx.beginPath();
    ctx.arc(n.sx, n.sy, Math.max(n.sr, 0.4), 0, 2 * Math.PI);
    ctx.fillStyle = n.color;
    ctx.fill();

    // SCC ring
    if (showSCC && inSCC.has(n.id)) {
      ctx.lineWidth = Math.max(0.5, 1.1 / k2) * (renderer === "3d" ? n.sf : 1);
      ctx.strokeStyle = "#ff8f92";
      ctx.stroke();
    }
  });

  // labels
  ctx.globalAlpha = 1;
  const showAll = S.allLabels || (renderer === "2d" && transform.k > 2.4);
  const hubs = new Set(nodes.slice().sort((a, b) => b.degree - a.degree).slice(0, 26).map(n => n.id));
  nodes.forEach(n => {
    const isFocus = n.id === focus || (focusSet && focusSet.has(n.id) && (renderer === "3d" || transform.k > 1.2));
    const isSearch = searchHits.has(n.id) && searchHits.size <= 25;
    const aboveThreshold = n.degree >= S.lt;
    const lab = showAll || isFocus || isSearch || (aboveThreshold && (N <= 30 || hubs.has(n.id) || (N <= 50 || transform.k > 0.6)));
    if (!lab) return;
    const a = focus >= 0 ? ((n.id === focus || focusSet.has(n.id)) ? 1 : 0.12) :
              searchHits.size ? (searchHits.has(n.id) ? 1 : 0.18) : 1;
    ctx.globalAlpha = a;
    const fs = renderer === "3d" ? Math.min(26, Math.max(5, 11 * n.sf)) : 11 / k2;
    ctx.font = (n.id === focus ? "600 " : "") + fs + "px sans-serif";
    ctx.fillStyle = "#e8ecf3";
    ctx.strokeStyle = "#12151c"; ctx.lineWidth = 3 / k2;
    ctx.strokeText(n.short, n.sx + n.sr + 2.5 / k2, n.sy + 3 / k2);
    ctx.fillText(n.short, n.sx + n.sr + 2.5 / k2, n.sy + 3 / k2);
  });

  ctx.restore();
}

// ---------- picking ----------
function findNode(ev) {
  const r = cv.getBoundingClientRect();
  const mx = (ev.touches ? ev.touches[0].clientX : ev.clientX) - r.left;
  const my = (ev.touches ? ev.touches[0].clientY : ev.clientY) - r.top;
  let best = null, bd = 1e9;
  const k2 = renderer === "2d" ? transform.k : 1;
  nodes.forEach(n => {
    let sx = n.sx, sy = n.sy;
    if (renderer === "2d") { sx = transform.applyX(n.sx); sy = transform.applyY(n.sy); }
    const d = (sx - mx) ** 2 + (sy - my) ** 2;
    const rr = (n.sr * k2 + 5) ** 2;
    if (d < rr && d < bd) { bd = d; best = n; }
  });
  return best;
}

// ---------- 2D zoom/drag ----------
let zoom;
if (typeof d3 !== "undefined") {
  zoom = d3.zoom().scaleExtent([0.04, 60])
    .filter(ev => {
      if (renderer !== "2d") return false;
      if (ev.type === "mousedown" || ev.type === "touchstart") return !findNode(ev);
      return true;
    })
    .on("zoom", ev => { transform = ev.transform; draw(); });

  const drag = d3.drag()
    .subject(ev => renderer === "2d" ? findNode(ev.sourceEvent) : null)
    .on("start", ev => {
      if (!ev.subject) return;
      if (!ev.active) sim.alphaTarget(0.25).restart();
      ev.subject.fx = ev.subject.x; ev.subject.fy = ev.subject.y;
    })
    .on("drag", ev => {
      if (!ev.subject) return;
      const r = cv.getBoundingClientRect();
      const mx = ev.sourceEvent.clientX - r.left;
      const my = ev.sourceEvent.clientY - r.top;
      ev.subject.fx = (mx - transform.x) / transform.k;
      ev.subject.fy = (my - transform.y) / transform.k;
    })
    .on("end", ev => {
      if (!ev.subject) return;
      if (!ev.active) sim.alphaTarget(0);
      ev.subject.fx = null; ev.subject.fy = null;
    });
  d3.select(cv).call(drag).call(zoom).on("dblclick.zoom", null);
}

// ---------- 3D orbit ----------
let m3 = {down: false, x: 0, y: 0, moved: 0, pan: false};
cv.addEventListener("mousedown", ev => {
  if (renderer !== "3d") return;
  m3.down = true; m3.moved = 0; m3.x = ev.clientX; m3.y = ev.clientY;
  m3.pan = ev.shiftKey || ev.button === 2;
});
window.addEventListener("mousemove", ev => {
  if (renderer !== "3d" || !m3.down) return;
  const dx = ev.clientX - m3.x, dy = ev.clientY - m3.y;
  m3.x = ev.clientX; m3.y = ev.clientY; m3.moved += Math.abs(dx) + Math.abs(dy);
  if (m3.pan) { cam.panx += dx; cam.pany += dy; }
  else { cam.yaw += dx * 0.005; cam.pitch = Math.max(-1.35, Math.min(1.35, cam.pitch + dy * 0.005)); }
  draw();
});
window.addEventListener("mouseup", () => { m3.down = false; });
cv.addEventListener("wheel", ev => {
  if (renderer !== "3d") return;
  ev.preventDefault();
  cam.zoom *= Math.pow(1.0016, -ev.deltaY);
  cam.zoom = Math.max(0.08, Math.min(40, cam.zoom));
  draw();
}, {passive: false});
cv.addEventListener("contextmenu", ev => { if (renderer === "3d") ev.preventDefault(); });

// hover + click
cv.addEventListener("mousemove", ev => {
  if (renderer === "3d" && m3.down) return;
  const n = findNode(ev);
  if (n) {
    hovered = n.id;
    tip.style.display = "block";
    const r = cv.parentNode.getBoundingClientRect();
    tip.style.left = Math.min(ev.clientX - r.left + 16, W - 360) + "px";
    tip.style.top = (ev.clientY - r.top + 14) + "px";
    let html = '<div class="t">' + n.name;
    if (inSCC.has(n.id)) html += '<span class="pill scc">in cycle</span>';
    html += '</div>';
    html += '<div class="d">package: <b style="color:' + n.color + '">' + n.pkg + '</b>';
    html += ' | in: ' + Math.round(n.inDeg) + ' | out: ' + Math.round(n.outDeg) + '</div>';
    tip.innerHTML = html;
  } else { hovered = -1; tip.style.display = "none"; }
  draw();
});
cv.addEventListener("click", ev => {
  if (renderer === "3d" && m3.moved > 6) return;
  const n = findNode(ev);
  selected = n ? n.id : -1;
  draw();
});
cv.addEventListener("dblclick", () => {
  selected = -1; searchHits.clear();
  document.getElementById("search").value = "";
  if (typeof d3 !== "undefined") {
    transform = d3.zoomIdentity;
    d3.select(cv).call(zoom.transform, d3.zoomIdentity);
  }
  cam.yaw = 0.55; cam.pitch = 0.32; cam.zoom = 1; cam.panx = cam.pany = 0;
  draw();
});

// ---------- UI ----------
// Mode buttons
document.querySelectorAll("#modebar button[data-r]").forEach(b => {
  b.addEventListener("click", () => {
    document.querySelectorAll("#modebar button[data-r]").forEach(x => x.classList.remove("on"));
    b.classList.add("on");
    renderer = b.dataset.r;
    const hint = document.getElementById("hint");
    hint.textContent = renderer === "2d"
      ? "scroll = zoom | drag background = pan | drag node = move | click = isolate | double-click = reset"
      : "drag = rotate 3D | scroll = zoom | shift-drag = pan | click = isolate | double-click = reset";
    layout(true);
  });
});

// Fit button
document.getElementById("btn-fit").addEventListener("click", () => {
  if (renderer === "3d") { cam.yaw = 0.55; cam.pitch = 0.32; cam.zoom = 1; cam.panx = cam.pany = 0; draw(); }
  else zoomToFit();
});

// SCC toggle
const sccBtn = document.getElementById("btn-scc");
sccBtn.textContent = "Cycles (" + sccs.length + " SCC" + (sccs.length !== 1 ? "s" : "") + ", " + inSCC.size + " nodes)";
sccBtn.addEventListener("click", () => {
  showSCC = !showSCC;
  sccBtn.classList.toggle("on", showSCC);
  draw();
});

// Search
const searchInput = document.getElementById("search");
searchInput.addEventListener("input", () => {
  const q = searchInput.value.toLowerCase().trim();
  searchHits.clear();
  if (q.length >= 2) {
    nodes.forEach(n => { if (n.name.toLowerCase().includes(q)) searchHits.add(n.id); });
  }
  draw();
});

// ---------- Controls panel ----------
const sidePanel = document.getElementById("side");
const panelBtn = document.getElementById("btn-panel");
panelBtn.addEventListener("click", () => {
  sidePanel.classList.toggle("collapsed");
  panelBtn.classList.toggle("shifted", !sidePanel.classList.contains("collapsed"));
  setTimeout(resize, 160);
});

// Visual sliders (redraw only, no sim restart)
function wireVisual(id, key, fmt) {
  const el = document.getElementById("sl-" + id);
  const lab = document.getElementById("v-" + id);
  el.addEventListener("input", () => {
    S[key] = +el.value; lab.textContent = fmt ? fmt(+el.value) : (+el.value).toFixed(1);
    draw();
  });
}
wireVisual("node", "node");
wireVisual("eo", "eo", v => v.toFixed(2));
wireVisual("ew", "ew");
wireVisual("lt", "lt", v => String(Math.round(v)));
document.getElementById("ck-alllabels").addEventListener("change", ev => {
  S.allLabels = ev.target.checked; draw();
});

// Physics sliders (update forces + reheat sim)
function wirePhysics(id, key, fmt) {
  const el = document.getElementById("sl-" + id);
  const lab = document.getElementById("v-" + id);
  el.addEventListener("input", () => {
    S[key] = +el.value; lab.textContent = fmt ? fmt(+el.value) : String(Math.round(+el.value));
    if (sim && typeof d3 !== "undefined") {
      sim.force("link").distance(S.ld);
      sim.force("charge").strength(S.ch);
      sim.force("collide").radius(d => radiusOf(d) * S.co + 1.4);
      sim.alpha(0.4).restart();
    }
  });
}
wirePhysics("ld", "ld");
wirePhysics("ch", "ch");
wirePhysics("co", "co", v => v.toFixed(1));

// Reset button
document.getElementById("btn-reset").addEventListener("click", () => {
  Object.assign(S, S_DEFAULTS);
  document.getElementById("sl-node").value = S.node;
  document.getElementById("v-node").textContent = S.node.toFixed(1);
  document.getElementById("sl-eo").value = S.eo;
  document.getElementById("v-eo").textContent = S.eo.toFixed(2);
  document.getElementById("sl-ew").value = S.ew;
  document.getElementById("v-ew").textContent = S.ew.toFixed(1);
  document.getElementById("sl-lt").value = S.lt;
  document.getElementById("v-lt").textContent = String(S.lt);
  document.getElementById("ck-alllabels").checked = S.allLabels;
  document.getElementById("sl-ld").value = S.ld;
  document.getElementById("v-ld").textContent = String(S.ld);
  document.getElementById("sl-ch").value = S.ch;
  document.getElementById("v-ch").textContent = String(S.ch);
  document.getElementById("sl-co").value = S.co;
  document.getElementById("v-co").textContent = S.co.toFixed(1);
  if (sim && typeof d3 !== "undefined") {
    sim.force("link").distance(S.ld);
    sim.force("charge").strength(S.ch);
    sim.force("collide").radius(d => radiusOf(d) * S.co + 1.4);
    sim.alpha(0.4).restart();
  }
  draw();
});

// ---------- init ----------
resize();
layout(true);

// Auto zoom-to-fit after simulation settles
if (typeof d3 !== "undefined" && sim) {
  sim.on("end", () => { zoomToFit(); });
  // Also schedule a fit after initial stabilization
  setTimeout(() => { if (renderer === "2d") zoomToFit(); }, 2500);
}
})();
</script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate self-contained DSM + graph HTML views "
                    "from NeoDepends dependency JSON"
    )
    parser.add_argument("input", type=Path,
                        help="dv8-dsm-v3.json or dv8-dependency.json")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Output directory (default: same as input)")
    parser.add_argument("--title", type=str, default=None,
                        help="Title for the views")
    parser.add_argument("--dsm-only", action="store_true",
                        help="Generate only DSM view")
    parser.add_argument("--graph-only", action="store_true",
                        help="Generate only graph view")
    parser.add_argument("--level", choices=["file", "entity", "both"],
                        default="file",
                        help="Visualization level (default: file)")
    parser.add_argument("--clustering", type=Path, default=None,
                        help="Clustering JSON for DV8-style nested group "
                             "boxes (DRH format or simple tree)")
    args = parser.parse_args()

    variables, cells = load_dep_json(args.input)
    out_dir = args.output_dir or args.input.parent
    title = args.title or args.input.stem

    clustering = None
    if args.clustering:
        clustering = load_clustering(args.clustering)

    is_entity = args.level == "entity"

    if not args.graph_only:
        dsm_path = out_dir / "dsm_view.html"
        generate_dsm_html(variables, cells, dsm_path,
                          title=f"DSM: {title}",
                          clustering=clustering,
                          is_entity_level=is_entity)
        print(f"[OK] DSM view: {dsm_path}")

    if not args.dsm_only:
        graph_path = out_dir / "graph_view.html"
        generate_graph_html(variables, cells, graph_path,
                            title=f"Graph: {title}",
                            is_entity_level=is_entity)
        print(f"[OK] Graph view: {graph_path}")


if __name__ == "__main__":
    main()
