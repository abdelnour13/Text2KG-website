"""
Visualisation utilities.

Builds interactive graph visualisations using ``neo4j-viz`` (the official
Neo4j Python visualisation library, wrapping the NVL JavaScript library)
and writes self-contained HTML files under /public/visualizations/.

neo4j-viz API summary used here:
  - Node(id, caption, size, color, properties)
  - Relationship(source, target, caption, color, width)
  - VisualizationGraph(nodes, relationships)
  - vg.render(layout, height, theme) → IPython.HTML  (.data = raw HTML string)
"""

import uuid
from collections import Counter
from datetime import datetime, timezone
from definitions import DIR
from neo4j_viz import Node, Relationship, VisualizationGraph, Layout, Renderer


# Directory where HTML files are written (must be served as static files)
VIS_DIR = DIR / "public" / "visualizations"
VIS_DIR.mkdir(parents=True, exist_ok=True)


# ── Colour palette (hex strings, one per node type) ───────────────────────────

_COLOURS: dict[str, str] = {
    "Domain":       "#534AB7",   # purple
    "SubDomain":    "#1D9E75",   # teal
    "Expertise":    "#D85A30",   # coral
    "Entity":       "#888780",   # gray
    "Article":      "#378ADD",   # blue
    "Lab":          "#378ADD",
    "Venue":        "#378ADD",
    "ExpertiseMap": "#7F77DD",
}

# Node sizes (radius in pixels) by type
_SIZES: dict[str, int] = {
    "Domain":      35,
    "SubDomain":   30,
    "Expertise":   28,
    "Entity":      20,
    "Article":     25,
    "Lab":         25,
    "Venue":       25,
    "ExpertiseMap": 40,
}

# Relationship colours by relation type
_REL_COLOURS: dict[str, str] = {
    "ISSUBDOMAINOF":  "#AFA9EC",   # light purple
    "BELONGSTO":      "#9FE1CB",   # light teal
    "HASRELATIONWITH": "#D3D1C7",  # light gray
    "APPEARSIN":      "#B5D4F4",   # light blue
}
_DEFAULT_REL_COLOUR = "#D3D1C7"
_DEFAULT_NODE_COLOUR = "#B4B2A9"


def _node_colour(node_type: str) -> str:
    return _COLOURS.get(node_type, _DEFAULT_NODE_COLOUR)


def _rel_colour(rel_type: str) -> str:
    return _REL_COLOURS.get(rel_type, _DEFAULT_REL_COLOUR)


# ── File helpers ──────────────────────────────────────────────────────────────

def _new_filename() -> str:
    """Return a timestamped unique filename for an HTML visualisation."""
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:8]
    return f"{ts}_{uid}.html"


def _render_and_save(vg: VisualizationGraph, layout: Layout = Layout.FORCE_DIRECTED) -> str:
    """
    Render *vg* to a self-contained HTML file and return the filename.

    ``vg.render()`` returns an ``IPython.display.HTML`` object whose
    ``.data`` attribute contains the complete HTML string — no Jupyter
    runtime is required to call it.
    """
    html_obj = vg.render(layout=layout, height="750px")
    filename = _new_filename()
    (VIS_DIR / filename).write_text(html_obj.data, encoding="utf-8")
    return filename

# import networkx as nx
# from ipysigma import Sigma

# def _render_and_save(vg: Sigma) -> str:
#     """
#     Render *vg* to a self-contained HTML file and return the filename.

#     ``vg.render()`` returns an ``IPython.display.HTML`` object whose
#     ``.data`` attribute contains the complete HTML string — no Jupyter
#     runtime is required to call it.
#     """
#     # html_obj = vg.render(layout=layout, height="750px")
#     filename = _new_filename()
#     vg.to_html(VIS_DIR / filename)
#     # (VIS_DIR / filename).write_text(html_obj.data, encoding="utf-8")
#     # return filename

#     return filename


# ── Public builders ───────────────────────────────────────────────────────────

def build_vis(data : list[dict], layout : Layout = Layout.FORCE_DIRECTED) -> str:

    nodes: dict[str, Node] = {}
    relationships: dict[str, Node] = {}

    def _node_id(node : dict) -> str:
        return f"{node['labels'][0]}_{node['id']}"

    degrees = Counter(
        [_node_id(row['src']) for row in data] + [_node_id(row['dst']) for row in data]
    )

    def _node_size(node: dict) -> int:

        size = _SIZES.get(node['labels'][0], 16)

        if 'Entity' in node['labels']:
            size = size + 10 * (degrees.get(_node_id(node)) / degrees.most_common(1)[0][1])

    def _caption(node : dict) -> str:

        if 'llm_label' in node and node['llm_label'] is not None and 'Expertise' in node['labels']:
            return node['llm_label']

        if 'personalized_pagerank_name' in node and node['personalized_pagerank_name'] is not None:
            return node['personalized_pagerank_name']
        
        if 'name' in node and node['name'] is not None:
            return node['name']
        
        return node['labels'][0]

    def _rel_caption(row : dict) -> str:

        props = row['props']

        if props.get('predicate') is not None:
            return props.get('predicate')
        
        if props.get('score') is not None:
            return f'{row["relation"]} : {100 * props.get("score"):.2f}%'
        
        return row['relation']
    
    def _node_props(d : dict) -> dict:

        r = {
            'name' : d.get('name'),
            'llm_label': d.get('llm_label'),
        } 

        return {
            key : value
            for key, value in r.items() 
            if value is not None
        }
    
    def _rel_props(d : dict) -> dict:

        r = {
            'predicate' : d.get('predicate'),
            'score': d.get('score'),
        } 

        return {
            key : value
            for key, value in r.items() 
            if value is not None
        }

    for row in data:
        
        src = row['src']
        dst = row['dst']
        relation = row['relation']

        src_id = _node_id(src)
        dst_id = _node_id(dst)
        rel_id = f"{src_id}_{relation}_{dst_id}"

        nodes[src_id] = Node(
            id=src_id,
            caption=_caption(src),
            size=_node_size(src),
            color=_node_colour(src['labels'][0]),
            properties=_node_props(src)
        )

        nodes[dst_id] = Node(
            id=dst_id,
            caption=_caption(dst),
            size=_node_size(dst),
            color=_node_colour(dst['labels'][0]),
            properties=_node_props(dst)
        )

        relationships[rel_id] = Relationship(
            source=src_id,
            target=dst_id,
            caption=_rel_caption(row),
            color=_rel_colour(relation),
            properties=_rel_props(row['props'])
        )

    nodes = list(nodes.values())
    relationships = list(relationships.values())

    vg = VisualizationGraph(nodes=nodes, relationships=relationships)
    return _render_and_save(vg, layout=layout)


# def build_vis(data: list[dict]):

#     G = nx.DiGraph()  # or nx.Graph() if undirected

#     def _caption(node: dict) -> str:
#         if 'name' in node and node['name'] is not None:
#             return node['name']
#         return node['labels'][0]

#     for row in data:
#         src = row['src']
#         dst = row['dst']
#         relation = row['relation']

#         src_id = f"{src['labels'][0]}_{src['id']}"
#         dst_id = f"{dst['labels'][0]}_{dst['id']}"

#         # Add source node
#         if src_id not in G:
#             G.add_node(
#                 src_id,
#                 label=_caption(src),
#                 size=_node_size(src['labels'][0]),
#                 color=_node_colour(src['labels'][0]),
#                 **src
#             )

#         # Add destination node
#         if dst_id not in G:
#             G.add_node(
#                 dst_id,
#                 label=_caption(dst),
#                 size=_node_size(dst['labels'][0]),
#                 color=_node_colour(dst['labels'][0]),
#                 **dst
#             )

#         # Add edge
#         G.add_edge(
#             src_id,
#             dst_id,
#             label=relation,
#             color=_rel_colour(relation),
#             **row['props']
#         )

#     s = Sigma(
#         G,
#         node_label="label",
#         node_size="size",
#         node_color="color",
#         edge_label="label",
#         edge_color="color"
#     )

#     print(list(G.nodes(data=True))[:5])

#     return _render_and_save(s)

def build_taxonomy_vis(data: list[dict]) -> str:
    return build_vis(data)

def build_expertises_vis(data: list[dict]) -> str:
    return build_vis(data)

def build_expertise_detail_vis(data: list[dict]) -> str:
    return build_vis(data)


# ── Summary statistics visualisation (Plotly) ────────────────────────────────
 
def build_summary_vis(data: dict) -> str:
    """
    Build a self-contained HTML page containing 10 interactive Plotly charts
    for the summary statistics of one expertise map.
 
    Layout (scrollable HTML page, plotly.js embedded once):
      Row 1 — Articles by Lab | Articles by Domain | Articles by SubDomain
      Row 2 — Articles by Domain & Lab (stacked bar)
      Row 3 — Articles by SubDomain & Lab (stacked bar)
      Row 4 — Expertises by Lab | Expertises by Domain | Expertises by SubDomain
      Row 5 — Expertises by Domain & Lab (stacked bar)
      Row 6 — Expertises by SubDomain & Lab (stacked bar)
 
    plotly.js is embedded once in the first chart div and reused for all
    subsequent divs, keeping the file fully self-contained.
 
    Returns the saved HTML filename.
    """
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
 
    # ── Colour palette ────────────────────────────────────────────────────────

 
    STACK_PALETTE = [
        "#534AB7", "#1D9E75", "#D85A30", "#378ADD",
        "#BA7517", "#0F6E56", "#993C1D", "#185FA5",
        "#3B6D11", "#712B13", "#085041", "#3C3489",
    ]
 
    PLOTLY_CONFIG = {
        "displaylogo": False,
        "modeBarButtonsToRemove": ["select2d", "lasso2d"],
        "responsive": True,
    }
 
    # ── Chart builders ────────────────────────────────────────────────────────
 
    def _pie_fig(
        labels: list[str],
        values: list[int],
        title: str,
    ) -> go.Figure:
        """Donut pie chart."""
        if not labels:
            fig = go.Figure()
            fig.add_annotation(
                text="No data", x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font={"size": 14, "color": "#aaa"},
            )
            fig.update_layout(title=title, height=320, paper_bgcolor="#ffffff")
            return fig
 
        # colours = (STACK_PALETTE * ((len(labels) // len(STACK_PALETTE)) + 1))[:len(labels)]
        n_colors = len(labels)
        colours = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
 
        fig = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.38,
            marker_colors=colours,
            textinfo="percent",
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
            sort=True,
        ))
        fig.update_layout(
            title={"text": title, "font": {"size": 13, "color": "#1c1917"}, "x": 0},
            height=320,
            margin={"l": 10, "r": 10, "t": 44, "b": 10},
            paper_bgcolor="#ffffff",
            font={"family": "system-ui, sans-serif", "color": "#1c1917"},
            legend={"font": {"size": 9}, "orientation": "v"},
            showlegend=True,
        )
        return fig
 
    def _grid_pie_fig(
        rows: list[dict],
        group_key: str,
        stack_key: str,
        value_key: str,
        title: str,
    ) -> go.Figure:
        """
        One donut pie per unique *stack_key* value (i.e. one pie per Lab),
        showing how *group_key* values (Domain or SubDomain) are distributed
        within that lab.  Pies are laid out in a responsive row.
        """
        from plotly.subplots import make_subplots
 
        if not rows:
            fig = go.Figure()
            fig.add_annotation(
                text="No data", x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False, font={"size": 14, "color": "#aaa"},
            )
            fig.update_layout(title=title, height=320, paper_bgcolor="#ffffff")
            return fig
 
        df = pd.DataFrame(rows)
        labs = sorted(df[stack_key].unique().tolist())
        groups_all = sorted(df[group_key].unique().tolist())
 
        # Consistent colour per group across all pies
        n_colors = len(groups_all)
        colours = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
        group_colours = {
            g: colours[i]
            for i, g in enumerate(groups_all)
        }
 
        n_cols = min(len(labs), 4)          # max 4 pies per row
        n_rows = -(-len(labs) // n_cols)    # ceiling division
 
        specs = [[{"type": "domain"} for _ in range(n_cols)] for _ in range(n_rows)]
        subplot_titles = labs + [""] * (n_rows * n_cols - len(labs))
 
        fig = make_subplots(
            rows=n_rows, cols=n_cols,
            specs=specs,
            subplot_titles=subplot_titles,
        )
 
        for idx, lab in enumerate(labs):
            r = idx // n_cols + 1
            c = idx %  n_cols + 1
            lab_df  = df[df[stack_key] == lab]
            glabels = lab_df[group_key].tolist()
            gvalues = lab_df[value_key].tolist()
            colours = [group_colours[g] for g in glabels]
 
            fig.add_trace(
                go.Pie(
                    labels=glabels,
                    values=gvalues,
                    hole=0.38,
                    marker_colors=colours,
                    textinfo="percent",
                    hovertemplate=f"{lab}<br>%{{label}}: %{{value}} (%{{percent}})<extra></extra>",
                    showlegend=True,   # legend entries from first pie only
                    sort=True,
                    name=lab,
                ),
                row=r, col=c,
            )
 
        # Annotation font size for subplot titles
        for ann in fig.layout.annotations:
            ann.font.size = 10
 
        fig.update_layout(
            title={"text": title, "font": {"size": 13, "color": "#1c1917"}, "x": 0},
            height=max(280, n_rows * 280),
            margin={"l": 10, "r": 10, "t": 56, "b": 10},
            paper_bgcolor="#ffffff",
            font={"family": "system-ui, sans-serif", "color": "#1c1917"},
            legend={"font": {"size": 9}, "orientation": "v", "title": {"text": group_key.replace("_", " ").title(), "font": {"size": 9}}},
        )
        return fig
 
    # ── Build all 10 figures ──────────────────────────────────────────────────
 
    figs: list[tuple[str, go.Figure, bool]] = []  # (section, fig, is_wide)
 
    # — Articles —
    figs.append(("articles", _pie_fig(
        [r["lab"] for r in data["articles_by_lab"]],
        [r["numArticles"] for r in data["articles_by_lab"]],
        "Articles by Lab",
    ), False))
 
    figs.append(("articles", _pie_fig(
        [r["domain"] for r in data["articles_by_domain"]],
        [r["numArticles"] for r in data["articles_by_domain"]],
        "Articles by Domain",
    ), False))
 
    figs.append(("articles", _pie_fig(
        [r["sub_domain"] for r in data["articles_by_subdomain"]],
        [r["numArticles"] for r in data["articles_by_subdomain"]],
        "Articles by SubDomain",
    ), False))
 
    figs.append(("articles", _grid_pie_fig(
        data["articles_by_domain_lab"],
        group_key="domain", stack_key="lab", value_key="numArticles",
        title="Articles by Domain & Lab",
    ), True))
 
    figs.append(("articles", _grid_pie_fig(
        data["articles_by_subdomain_lab"],
        group_key="sub_domain", stack_key="lab", value_key="numArticles",
        title="Articles by SubDomain & Lab",
    ), True))
 
    # — Expertises —
    figs.append(("expertises", _pie_fig(
        [r["lab"] for r in data["expertises_by_lab"]],
        [r["numExpertises"] for r in data["expertises_by_lab"]],
        "Expertises by Lab",
    ), False))
 
    figs.append(("expertises", _pie_fig(
        [r["domain"] for r in data["expertises_by_domain"]],
        [r["numExpertises"] for r in data["expertises_by_domain"]],
        "Expertises by Domain",
    ), False))
 
    figs.append(("expertises", _pie_fig(
        [r["sub_domain"] for r in data["expertises_by_subdomain"]],
        [r["numExpertises"] for r in data["expertises_by_subdomain"]],
        "Expertises by SubDomain",
    ), False))
 
    figs.append(("expertises", _grid_pie_fig(
        data["expertises_by_domain_lab"],
        group_key="domain", stack_key="lab", value_key="numExpertises",
        title="Expertises by Domain & Lab",
    ), True))
 
    figs.append(("expertises", _grid_pie_fig(
        data["expertises_by_subdomain_lab"],
        group_key="sub_domain", stack_key="lab", value_key="numExpertises",
        title="Expertises by SubDomain & Lab",
    ), True))
 
    # ── Render to HTML divs ───────────────────────────────────────────────────
    # plotly.js is embedded once in the first div; all subsequent divs reuse it.
 
    chart_divs: list[str] = []
    for i, (_, fig, wide) in enumerate(figs):
        include_js = (i == 0)  # embed plotly.js exactly once
        div_html = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs=include_js,
            config=PLOTLY_CONFIG,
            div_id=f"chart-{i}",
        )
        css_class = "card wide" if wide else "card"
        chart_divs.append(f'<div class="{css_class}">{div_html}</div>')
 
    # Group divs into sections
    # chart_divs indices:
    #   0  Articles by Lab          | simple
    #   1  Articles by Domain       | simple
    #   2  Articles by SubDomain    | simple
    #   3  Articles by Domain & Lab | stacked  ──┐ side by side
    #   4  Articles by SubDomain & Lab | stacked  |
    #   5  Expertises by Lab          | simple   |
    #   6  Expertises by Domain       | simple   |
    #   7  Expertises by SubDomain    | simple   |
    #   8  Expertises by Domain & Lab | stacked  ──┘ side by side with [3]
    #   9  Expertises by SubDomain & Lab | stacked
 
    art_narrow       = "\n".join(chart_divs[0:3])  # 3 simple
    domain_lab_row   = "\n".join([chart_divs[3], chart_divs[8]])  # side by side
    art_sd_lab       = chart_divs[4]                # full-width stacked
    exp_narrow       = "\n".join(chart_divs[5:8])  # 3 simple
    exp_sd_lab       = chart_divs[9]                # full-width stacked
 
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Summary Statistics</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: system-ui, sans-serif;
    background: #fafaf9;
    color: #1c1917;
    padding: 24px 20px 48px;
  }}
  h1 {{
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 4px;
    color: #1c1917;
  }}
  .subtitle {{
    font-size: 0.75rem;
    color: #78716c;
    margin-bottom: 28px;
  }}
  .section-label {{
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #a8a29e;
    margin: 32px 0 14px;
  }}
  .grid-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }}
  .grid-2 {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin-top: 14px;
  }}
  .card {{
    background: #fff;
    border: 1px solid #e7e5e4;
    border-radius: 8px;
    padding: 4px 8px 8px;
    overflow: hidden;
  }}
  .full-width {{
    margin-top: 14px;
  }}
  @media (max-width: 780px) {{
    .grid-3, .grid-2 {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
 
<h1>Summary Statistics</h1>
<p class="subtitle">Distribution of articles and expertises across labs, domains, and subdomains.</p>
 
<p class="section-label">Articles</p>
<div class="grid-3">
{art_narrow}
</div>
 
<p class="section-label">By Domain &amp; Lab</p>
<div class="grid-2">
{domain_lab_row}
</div>
 
<p class="section-label">Articles by SubDomain &amp; Lab</p>
<div class="full-width">
{art_sd_lab}
</div>
 
<p class="section-label">Expertises</p>
<div class="grid-3">
{exp_narrow}
</div>
 
<p class="section-label">Expertises by SubDomain &amp; Lab</p>
<div class="full-width">
{exp_sd_lab}
</div>
 
</body>
</html>"""
 
    filename = _new_filename()
    (VIS_DIR / filename).write_text(html, encoding="utf-8")
    print(VIS_DIR)
    return filename