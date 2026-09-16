# -*- coding: utf-8 -*-
"""
Regenerate all five paper figures with matplotlib (English labels).
Output: SVG (vector, overwrite original files) + PNG previews.
v3: larger minimum font size, darker text colors, tighter non-overlapping layout.
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = r'E:\Projects\AI_paper_figures'
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.edgecolor': '#333333',
    'text.color': '#111111',
    'axes.labelcolor': '#111111',
    'xtick.color': '#222222',
    'ytick.color': '#222222',
})

# --- color palette (darker text, medium-tone fills) ---
GRAY = '#f0f0f0'
BLUE = '#dce9f8'
YELLOW = '#fdf0d5'
GREEN = '#dff0df'
RED = '#fbebeb'
PURPLE = '#eee3f7'
EDGE = '#3a3a3a'
INK = '#111111'
INK2 = '#333333'
INK3 = '#555555'   # only for very minor captions; otherwise INK/INK2


def box(ax, x, y, w, h, fc, ec=EDGE, lw=1.0, ls='-', zorder=2, r=1.0):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.02,rounding_size={r}',
                       fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=zorder, mutation_aspect=1)
    ax.add_patch(p)


def txt(ax, x, y, s, ha='left', va='center', fs=9, c=INK, weight='normal', zorder=3, style='normal'):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=c, fontweight=weight,
            zorder=zorder, fontstyle=style, linespacing=1.45)


def arrow(ax, x1, y1, x2, y2, color='#333333', lw=1.4, ls='-', zorder=1, style='-|>', ms=11):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                        color=color, lw=lw, linestyle=ls, zorder=zorder, shrinkA=0, shrinkB=0)
    ax.add_patch(a)


def newax(figw, figh):
    fig, ax = plt.subplots(figsize=(figw, figh))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    return fig, ax


# =====================================================================
# Fig 1-1  Four-layer valuation transmission chain (architecture)
# =====================================================================
fig, ax = newax(12.5, 8.6)
txt(ax, 50, 97.8, 'Fig 1-1  Four-Layer Valuation Transmission Chain Framework', ha='center', fs=14, weight='bold')
txt(ax, 50, 94.8, 'Source: author. Data and parameter definitions: Tables 3-2, 3-4 of the paper.', ha='center', fs=9, c=INK2)

# Parameter band (top)
params = [('r_tok', 'Token consumption\ngrowth rate'),
          ('r_cost', 'Unit compute cost\nannual decline'),
          ('S_capex', 'Compute supply\nincrement'),
          ('F', 'Financing\navailability'),
          ('Reg', 'Regulation')]
pw = 17.5
x0 = 3
for i, (sym, desc) in enumerate(params):
    x = x0 + i * (pw + 1.2)
    box(ax, x, 85.5, pw, 8.0, PURPLE, ec='#6d4c8f')
    txt(ax, x + pw / 2, 90.0, sym, ha='center', fs=11, weight='bold', c='#4a3370')
    txt(ax, x + pw / 2, 87.0, desc, ha='center', fs=8.2, c=INK)
txt(ax, 50, 83.9, 'Key uncertainty parameters (Table 3-2); dotted arrows mark which layer each parameter enters',
    ha='center', fs=8.5, c=INK2)

# Layers (compressed to leave room for K boxes at bottom)
layers = [
    ('L1  Model Company Valuation', 65.5, 13.5,
     ['Revenue = Inference tokens \u00d7 tiered price + subscribers \u00d7 ARPU',
      'Cost = training \u00d7 frequency + inference + R&D',
      'Valuation = P/S \u00d7 ARR or simplified DCF'],
     BLUE),
    ('L2  Compute Lease Fees', 47.5, 13.5,
     ['Lease fees = training cost \u00d7 outsourced share + inference cost \u00d7 outsourced share',
      'Anchors: Anthropic\u2013AWS $100B / 10 yr;  OpenAI 2 GW Trainium'],
     YELLOW),
    ('L3  Data Center ROI & Valuation', 29.5, 13.5,
     ['ROI = (lease income \u2212 electricity \u2212 depreciation \u2212 O&M \u2212 interest) / capex',
      'Valuation = NOI / cap rate;  securitization: REITs / ABS / private credit'],
     GREEN),
    ('L4  Exposure Mapping Layer', 11.5, 13.5,
     ['Equity path: holdings \u00d7 write-down rate \u2192 impairment',
      'Debt path: EAD \u00d7 PD \u00d7 LGD \u2192 credit losses'],
     RED),
]
for title, y, h, lines, c in layers:
    box(ax, 4, y, 92, h, c)
    txt(ax, 6.5, y + h - 2.6, title, fs=10.5, weight='bold')
    for j, ln in enumerate(lines):
        txt(ax, 8, y + h - 5.8 - j * 2.9, ln, fs=9.0)

# arrows between layers
arrow(ax, 50, 65.5, 50, 61.3, lw=1.7)
arrow(ax, 50, 47.5, 50, 43.3, lw=1.7)
arrow(ax, 50, 29.5, 50, 25.3, lw=1.7)

# parameter dotted arrows into layers
for px, ty in [(6, 70.0), (25, 63.0), (45, 57.0), (68, 70.0), (90, 63.0)]:
    arrow(ax, px, 85.5, px + 0.5, ty, color='#6d4c8f', lw=1.0, ls=':', style='-|>', ms=8)

# K failure conditions (below L4, boxed title integrated)
txt(ax, 50, 9.6, 'Three structural failure conditions (trigger \u21d2 stop using model; see Table 8-3)',
    ha='center', fs=9.5, weight='bold')
kconds = [('K1  Self-built compute', 'Self-built share breaches threshold;\nL2 fees decouple from capex \u2192\nrebuild L2\u2013L3 interface'),
          ('K2  Vertical integration', 'Cloud + model companies merge;\nrelated-party pricing internalizes,\nL1\u2013L4 independence breaks \u2192\nmodel terminated'),
          ('K3  Open-source diversion', 'Open-source models erode\ncommercial API revenue \u2192\nrebuild L1 revenue structure')]
kw = 29.5
for i, (t, d) in enumerate(kconds):
    x = 4 + i * (kw + 1.8)
    box(ax, x, 0.8, kw, 8.2, '#ffffff', ec='#b32424', ls='--')
    txt(ax, x + kw / 2, 7.6, t, ha='center', fs=9.0, weight='bold', c='#8f1f1f')
    txt(ax, x + kw / 2, 4.6, d, ha='center', fs=7.4, c=INK)

txt(ax, 50, 0.4, 'Note: dotted arrows mark where failure conditions enter the chain. Equity and debt paths keep separate inputs, formulas and outputs (Ch. 7).',
    ha='center', fs=8.2, c=INK2)
fig.savefig(os.path.join(OUT, 'fig1-1_four_layer_valuation_chain.svg'), format='svg', bbox_inches='tight')
fig.savefig(os.path.join(OUT, '_preview1.png'), dpi=120, bbox_inches='tight')
plt.close(fig)
print('fig 1-1 done')

# =====================================================================
# Fig 3-1  Four-layer data flow diagram
# =====================================================================
fig, ax = newax(13.8, 11.0)
txt(ax, 50, 98.2, 'Fig 3-1  Four-Layer Transmission-Chain Data Flow', ha='center', fs=14, weight='bold')
txt(ax, 50, 95.6, 'Source: author. Data definitions: Tables 3-1, 3-2; source-level colors per legend below.',
    ha='center', fs=9, c=INK2)

# legend chips (top row)
lg = [('Primary disclosure', '#c62828'), ('Database / institutional estimate', '#1565c0'),
      ('Industry estimate / derived', '#2e7d32'), ('Analyst assumption (threshold)', '#f9a825')]
x = 14
for name, c in lg:
    ax.add_patch(Rectangle((x, 91.6), 2.0, 1.6, fc=c, ec='none'))
    txt(ax, x + 2.7, 92.4, name, fs=8.5, c=INK)
    x += 4.6 + len(name) * 0.40

COLW = 24.2
cols = [('Input', 2), ('Core computation', 26.5), ('Output', 51), ('Data sources', 75.5)]
rows = [
    ('L1', 66,
     ['ARR (Anthropic $65B)', 'Market share (API / consumer)', 'Training / inference cost'],
     ['Revenue = tokens \u00d7 price + subs \u00d7 ARPU', 'Cost = training \u00d7 freq. + inference + R&D',
      'Valuation = P/S \u00d7 ARR or DCF', 'cost items (train + infer) \u00d7 outsourced share'],
     ['Valuation ranges (3 scenarios)', 'Sensitivity: g_rev > cost share > multiple', '\u2192 cost items to L2'],
     ['Training: GPT-4 class ~$100M/gen [unverified]', 'DeepSeek $5.576M [report]',
      'Inference: CICC ~$2/M tokens [unverified\u00b7report]', 'ARR / valuation: disclosures + database (T4-1)'],
     '#c62828'),
    ('L2', 42.5,
     ['L1 cost items', 'Outsourcing / self-build ratio', 'Disclosed compute commitments'],
     ['Lease = train\u00d7out + infer\u00d7out', 'Anchors: Anthropic\u2013AWS $100B / 10 yr',
      'OpenAI 2 GW Trainium', 'demand side (lease fees)'],
     ['Global / NA annual lease fees (3 scenarios)', 'Optimistic $110\u2013160B;  Base $65\u2013110B', 'Pessimistic $30\u201360B'],
     ['Disclosed commitments: cited [8] (primary / DB)', 'Global inference cost total: $68.16B/yr [derived]',
      'Outsourced share, NA share: [assumption]', ''],
     '#1565c0'),
    ('L3', 19,
     ['L2 lease fees (demand)', 'NA stock / under-construction MW', 'Electricity / capex / rent'],
     ['Supply\u2013price model \u2192 utilization / rent', 'ROI = (income \u2212 elec \u2212 dep \u2212 O&M \u2212 int) / capex',
      'Val = NOI / cap rate; 3 sec. channels', 'P&L (valuation shock + cash-flow shock)'],
     ['ROI: Opt 15%\u201325% / Base \u22125% to +10%', 'Pess \u221215% to \u22125% (T6-2)', 'Valuation direction; securitization size'],
     ['Stock: JLL 50 GW / CBRE 10,903 MW (T3-5)', 'Rent: N. Virginia $190\u2013235/kW\u00b7mo (CBRE Q1 2026)',
      'Debt: securitized $61B outstanding; $200B/yr issuance', ''],
     '#2e7d32'),
    ('L4', -4.5,
     ['L1 valuation shock (equity)', 'L2\u2013L3 cash-flow shock (debt)', 'Holdings; EAD / PD / LGD'],
     ['Equity: holdings \u00d7 w/d rate \u2192 impairment', 'Debt: EAD \u00d7 PD \u00d7 LGD \u2192 credit losses',
      'two paths never merged (Ch. 7)', ''],
     ['Entity \u00d7 exposure \u00d7 scenario matrix', 'Pessimistic total: $112\u2013308B', '(Tables 7-3, 9-1)'],
     ['Holdings: [unverified\u00b7media] (T7-1)', 'EAD: securitized $61B + annual issuance',
      'PD / LGD: [assumption] (T7-2)', ''],
     '#f9a825'),
]

for rname, ry, inp, comp, outp, srcs, scol in rows:
    y0 = ry
    h = 21.5
    # column headers
    for cname, cx in cols:
        ax.add_patch(Rectangle((cx, y0 + h + 0.5), COLW, 2.6, fc='#dcdcdc', ec=EDGE, lw=0.9))
        txt(ax, cx + 1, y0 + h + 1.8, cname, fs=9, weight='bold', c=INK)
    # cells
    ax.add_patch(Rectangle((2, y0), COLW, h, fc='#f5f9ff', ec=EDGE, lw=0.9))
    ax.add_patch(Rectangle((26.5, y0), COLW, h, fc='#fffcf2', ec=EDGE, lw=0.9))
    ax.add_patch(Rectangle((51, y0), COLW, h, fc='#f4fbf4', ec=EDGE, lw=0.9))
    ax.add_patch(Rectangle((75.5, y0), COLW, h, fc='#fafafa', ec=EDGE, lw=0.9))
    txt(ax, 3.2, y0 + h - 1.6, rname, fs=11, weight='bold', c=INK)
    # inputs
    for j, ln in enumerate(inp):
        txt(ax, 3.2, y0 + h - 4.6 - j * 3.2, ln, fs=8.6)
    # computation
    for j, ln in enumerate(comp):
        txt(ax, 27.7, y0 + h - 4.6 - j * 3.2, ln, fs=8.6)
    # output
    for j, ln in enumerate(outp):
        txt(ax, 52.2, y0 + h - 4.6 - j * 3.2, ln, fs=8.6)
    # sources (colored bullets)
    for j, ln in enumerate(srcs):
        if not ln:
            continue
        ax.add_patch(Rectangle((77.0, y0 + h - 4.6 - j * 3.2), 1.3, 1.3, fc=scol, ec='none'))
        txt(ax, 79.0, y0 + h - 4.6 - j * 3.2, ln, fs=8.6)

# vertical flow arrows between layers (right side of input column)
arrow(ax, 14, 66, 14, 64.2, lw=1.5)
arrow(ax, 14, 42.5, 14, 40.7, lw=1.5)
arrow(ax, 14, 19, 14, 17.2, lw=1.5)

txt(ax, 50, 3.6, 'Note: arrows show data flow direction; colors of the source-level bullets match the legend. Assumption-type parameters state their rationale and are not presented as empirical estimates.',
    ha='center', fs=8.2, c=INK2)
fig.savefig(os.path.join(OUT, 'fig3-1_four_layer_data_flow.svg'), format='svg', bbox_inches='tight')
fig.savefig(os.path.join(OUT, '_preview3.png'), dpi=115, bbox_inches='tight')
plt.close(fig)
print('fig 3-1 done')

# =====================================================================
# Fig 7-1  Exposure mapping layer structure
# =====================================================================
fig, ax = newax(12.5, 8.2)
txt(ax, 50, 97.8, 'Fig 7-1  Exposure Mapping Layer Structure', ha='center', fs=14, weight='bold')
txt(ax, 50, 94.6, 'Source: author. Parameters: Tables 7-1, 7-2, 7-3 of the paper.', ha='center', fs=9, c=INK2)

# left: L1-L3 outputs
box(ax, 2, 77, 21, 11, BLUE)
txt(ax, 4, 85.5, 'L1\u2013L3 outputs', fs=10, weight='bold')
txt(ax, 4, 82.2, 'Valuation shock: L1 markdown,', fs=8.2)
txt(ax, 4, 79.6, 'L3 cap-rate up', fs=8.2)
txt(ax, 4, 76.9, 'Cash-flow shock: L2 lease', fs=8.2)
txt(ax, 4, 74.3, 'contraction, L3 ROI < 0', fs=8.2)

box(ax, 2, 62, 21, 10, PURPLE)
txt(ax, 4, 70.0, 'Securitization channels', fs=10, weight='bold')
txt(ax, 4, 66.8, 'REITs (NOI / cap-rate pricing)', fs=8.2)
txt(ax, 4, 64.0, 'ABS / CMBS (junior 5%\u201315% first loss)', fs=8.2)

box(ax, 2, 44, 21, 11, PURPLE)
txt(ax, 4, 53.0, 'Securitization (cont.)', fs=9.5, weight='bold')
txt(ax, 4, 50.0, 'Private credit: maturity mismatch,', fs=8.2)
txt(ax, 4, 47.2, 'no public pricing', fs=8.2)

# equity path
box(ax, 28, 70, 30, 15.5, YELLOW)
txt(ax, 30, 83.0, 'Equity path', fs=11, weight='bold')
txt(ax, 30, 80.0, 'Impairment = holdings \u00d7 write-down amount', fs=8.6)
txt(ax, 30, 77.2, 'Write-down: Opt 0% / Base 10%\u201330% / Pess 50%\u201380%', fs=8.2)
txt(ax, 30, 74.4, 'Entities: Microsoft\u2013OpenAI,', fs=8.2)
txt(ax, 30, 71.6, 'AWS\u2013Anthropic, Amazon\u2013OpenAI', fs=8.2)

# debt path
box(ax, 28, 49, 30, 15.5, RED)
txt(ax, 30, 62.0, 'Debt path', fs=11, weight='bold')
txt(ax, 30, 59.0, 'Credit losses = EAD \u00d7 PD \u00d7 LGD', fs=8.6)
txt(ax, 30, 56.2, 'PD from DSCR: Base 2%\u20135% / Pess 10%\u201320%', fs=8.2)
txt(ax, 30, 53.4, 'LGD 60%\u201380%', fs=8.2)
txt(ax, 30, 50.6, 'Entities: private credit, ABS junior, banks', fs=8.2)

# arrows from left to paths
arrow(ax, 23, 81, 28, 79, lw=1.4)
arrow(ax, 23, 62, 28, 58, lw=1.4)

# right: matrix table
mxx = 63
my0 = 72
mxw = 34
tbl = [('Entity', 'Exposure type', 'Pessimistic ($B)'),
       ('Microsoft', 'Equity (OpenAI)', '50\u201390'),
       ('AWS / Amazon', 'Equity', '30\u2013110'),
       ('NA financial institutions', 'Debt (DC debt)', '12\u201348'),
       ('Securitization investors', 'Junior / REITs', '20\u201360'),
       ('Total', '\u2014', '112\u2013308')]
ax.add_patch(Rectangle((mxx, my0 + 3.4), mxw, 4.6, fc='#e6e6e6', ec=EDGE, lw=0.9))
txt(ax, mxx + 1, my0 + 5.7, 'Output: entity \u00d7 exposure type \u00d7 scenario matrix', fs=9, weight='bold')
colx = [mxx, mxx + 15, mxx + 24.5]
for cx, hd in zip(colx, tbl[0]):
    ax.add_patch(Rectangle((cx, my0), 15 if hd == 'Entity' else 9.5, 3.4, fc='#d9d9d9', ec=EDGE, lw=0.9))
    txt(ax, cx + 0.8, my0 + 1.7, hd, fs=8.4, weight='bold')
for ri, row in enumerate(tbl[1:]):
    ry = my0 - 3.4 - ri * 5.0
    fc = '#fdecec' if ri == 4 else '#ffffff'
    ax.add_patch(Rectangle((mxx, ry), 15, 3.4, fc=fc, ec=EDGE, lw=0.7))
    ax.add_patch(Rectangle((mxx + 15, ry), 9.5, 3.4, fc=fc, ec=EDGE, lw=0.7))
    ax.add_patch(Rectangle((mxx + 24.5, ry), 9.5, 3.4, fc=fc, ec=EDGE, lw=0.7))
    txt(ax, mxx + 0.8, ry + 1.7, row[0], fs=8.4)
    txt(ax, mxx + 15.8, ry + 1.7, row[1], fs=8.2)
    txt(ax, mxx + 25.3, ry + 1.7, row[2], fs=8.6, weight='bold' if ri == 4 else 'normal')

txt(ax, mxx, 44.5, 'Optimistic total $0.4\u20131.9B;  Base $26.4\u201393.4B (Table 9-1)', fs=8.4, c=INK)
txt(ax, mxx, 41.4, 'Total = sum of each entity\u2019s interval endpoints [derived]', fs=8.0, c=INK2)
txt(ax, mxx, 38.3, 'Pessimistic magnitudes are not point forecasts', fs=8.0, c=INK2)

txt(ax, 50, 1.8, 'Note: equity and debt paths keep separate inputs, formulas and outputs; never merged into one number (paper 2.6).',
    ha='center', fs=8.2, c=INK2)
txt(ax, 50, 1.0, 'Holdings are reported magnitudes [unverified\u00b7media]; PD / LGD are analyst assumptions, stated in the text.',
    ha='center', fs=8.0, c=INK2)
fig.savefig(os.path.join(OUT, 'fig7-1_exposure_mapping_structure.svg'), format='svg', bbox_inches='tight')
fig.savefig(os.path.join(OUT, '_preview7.png'), dpi=120, bbox_inches='tight')
plt.close(fig)
print('fig 7-1 done')

# =====================================================================
# Fig 8-1  Model robustness test panels
# =====================================================================
_mc = np.load(r'E:\Projects\AI_paper_figures\mc_output.npz')

fig = plt.figure(figsize=(14.5, 11))
gs = fig.add_gridspec(3, 2, hspace=0.62, wspace=0.22,
                      left=0.07, right=0.97, top=0.93, bottom=0.08)

fig.text(0.5, 0.965, 'Fig 8-1  Model Robustness Test Panels', ha='center', fontsize=15, fontweight='bold')
fig.text(0.5, 0.944, 'Monte Carlo (10,000 draws per scenario) and response surface use actual simulation output (paper 8.4).',
         ha='center', fontsize=8.5, color=INK2)

# (a) Tornado
axa = fig.add_subplot(gs[0, 0])
axa.set_title('(a) Tornado: parameter sensitivity of L4 losses', fontsize=10.5)
items = [('r_tok (token growth)', 8.0, '#b71c1c'),
         ('r_cost (cost decline)', 6.2, '#e65100'),
         ('Financing availability F', 4.4, '#f9a825'),
         ('Valuation multiple compression', 2.6, '#757575')]
for i, (lab, v, c) in enumerate(items):
    axa.barh(3 - i, v, height=0.58, color=c, alpha=0.9)
    axa.text(0.25, 3 - i, lab, va='center', fontsize=8.6, color=INK)
    axa.text(v + 0.15, 3 - i, f'{v:.1f}', va='center', fontsize=8.6, color=INK)
axa.set_xlim(0, 10)
axa.set_yticks([])
axa.set_xlabel('Relative impact on L4 total losses (qualitative ranking)', fontsize=8.6)
axa.text(0.01, -0.24, 'Source: sensitivity ranking of paper 9.3 [derived]', transform=axa.transAxes, fontsize=7.8, color=INK2)

# (b) Sensitivity curve: token growth vs L2 lease fees
axb = fig.add_subplot(gs[0, 1])
axb.set_title('(b) Sensitivity: token growth \u00d7 L2 lease fees', fontsize=10.5)
xg = np.linspace(0, 1, 100)
axb.fill_between(xg, 30, 60, color='#e57373', alpha=0.55, label='Pessimistic $30\u201360B')
axb.fill_between(xg, 65, 110, color='#ffcc80', alpha=0.65, label='Base $65\u2013110B')
axb.fill_between(xg, 110, 160, color='#81c784', alpha=0.6, label='Optimistic $110\u2013160B')
axb.set_xlabel('Token consumption growth rate r_tok', fontsize=8.6)
axb.set_ylabel('L2 lease fees ($B / yr)', fontsize=8.6)
axb.set_ylim(0, 190)
axb.legend(fontsize=8, loc='upper left', framealpha=0.95)
axb.text(0.01, -0.24, 'Data: three-scenario lease intervals of Table 5-2 [derived\u00b7base]', transform=axb.transAxes, fontsize=7.8, color=INK2)

# (c) Monte Carlo histogram (actual simulation output)
axc = fig.add_subplot(gs[1, 0])
axc.set_title('(c) Monte Carlo L4 loss distribution (10,000 draws)', fontsize=10.5)
for name, col, lab in [('pessimistic', '#e57373', 'Pessimistic'),
                       ('base', '#ffcc80', 'Base'),
                       ('optimistic', '#81c784', 'Optimistic')]:
    v = _mc[name]
    axc.hist(v, bins=70, color=col, alpha=0.7, edgecolor='white', lw=0.3, label=lab)
for pct, col in [(90, '#8f1f1f'), (99, '#4a0000')]:
    vp = np.percentile(_mc['pessimistic'], pct)
    axc.axvline(vp, color=col, lw=1.3, ls='--')
    axc.text(vp + 12, axc.get_ylim()[1] * 0.9, f'Pess. P{pct}: ${vp:.0f}B', fontsize=8, color=col, weight='bold')
axc.set_xlabel('L4 total losses ($B)', fontsize=8.6)
axc.set_ylabel('Frequency', fontsize=8.6)
axc.set_xlim(0, 3200)
axc.legend(fontsize=8, loc='upper right', framealpha=0.95)
axc.text(0.01, -0.26, 'Data: mc_sim.py, 10,000 uniform draws per scenario; L4 = equity + EAD\u00d7PD\u00d7LGD + securitization [derived\u00b7simulation]',
         transform=axc.transAxes, fontsize=7.6, color=INK2)

# (d) Response surface (actual simulation output)
axd = fig.add_subplot(gs[1, 1])
axd.set_title('(d) Response surface: expected L4 loss over r_tok \u00d7 r_cost', fontsize=10.5)
R = _mc['response']
rt_grid = _mc['rt_grid']
rc_grid = _mc['rc_grid']
im = axd.imshow(R, origin='lower', aspect='auto', cmap='YlOrRd',
                extent=[rt_grid[0], rt_grid[-1], rc_grid[0], rc_grid[-1]])
cs = axd.contour(R, levels=8, colors='#4a2a1a', linewidths=0.8,
                 extent=[rt_grid[0], rt_grid[-1], rc_grid[0], rc_grid[-1]])
axd.clabel(cs, inline=True, fontsize=7, fmt='%.0f')
cb = fig.colorbar(im, ax=axd, fraction=0.046, pad=0.04)
cb.set_label('Expected L4 loss ($B)', fontsize=8.5)
cb.ax.tick_params(labelsize=8)
axd.set_xlabel('r_tok: token consumption growth (x/yr, low \u2192 high)', fontsize=8.6)
axd.set_ylabel('r_cost: unit compute cost decline (small \u2192 large)', fontsize=8.6)
axd.axhline(0.50, color='#7f0000', lw=1.4, ls=':')
axd.axvline(1.5, color='#7f0000', lw=1.4, ls=':')
axd.text(1.14, 0.36, 'Pessimistic region\n(r_tok<1.5x, r_cost<50%)', fontsize=8, color='#7f0000', weight='bold',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#7f0000', alpha=0.85))
axd.text(0.01, -0.26, 'Data: mc_sim.py grid interpolation on scenario midpoints; contours in $B expected loss [derived\u00b7simulation]',
         transform=axd.transAxes, fontsize=7.6, color=INK2)

# (e) Fan chart
axe = fig.add_subplot(gs[2, :])
axe.set_title('(e) Three-scenario L4 total exposure fan chart (illustrative expansion)', fontsize=10.5)
xs = np.array([0, 1, 2, 3, 4])
lab = ['2026', '2027', '2028', '2029', '2030']
pe_lo = np.array([112, 130, 150, 170, 200])
pe_hi = np.array([308, 360, 420, 500, 600])
ba_lo = np.array([26.4, 32, 40, 50, 60])
ba_hi = np.array([93.4, 110, 130, 150, 180])
op_lo = np.array([0.4, 0.5, 0.6, 0.7, 0])
op_hi = np.array([1.9, 3, 4, 5, 6])
axe.fill_between(xs, pe_lo, pe_hi, color='#e57373', alpha=0.55, label='Pessimistic $112\u2013308B \u2192 200\u2013600B')
axe.fill_between(xs, ba_lo, ba_hi, color='#ffcc80', alpha=0.6, label='Base $26.4\u201393.4B \u2192 60\u2013180B')
axe.fill_between(xs, op_lo, op_hi, color='#81c784', alpha=0.6, label='Optimistic $0.4\u20131.9B \u2192 0\u20136B')
axe.plot(xs, (pe_lo + pe_hi) / 2, color='#8f1f1f', lw=1.4, ls='--')
axe.plot(xs, (ba_lo + ba_hi) / 2, color='#bf360c', lw=1.4, ls='--')
axe.plot(xs, (op_lo + op_hi) / 2, color='#1b5e20', lw=1.4, ls='--')
axe.axhspan(200, 300, color='#9e9e9e', alpha=0.25)
axe.text(4.03, 250, 'Global DC annual capex\n~$200\u2013300B (reference)', fontsize=8, color=INK, va='center')
axe.set_xticks(xs)
axe.set_xticklabels(lab, fontsize=9.5)
for xv, nm in zip(xs[1:], ['P1 window (2027\u20132028)', 'P2 (2027\u20132028)', 'P3 (2027\u20132029)']):
    axe.axvline(xv, color='#888888', lw=1.0, ls=':')
    axe.text(xv, 470, nm, fontsize=8, ha='center', color=INK)
axe.set_ylabel('L4 total exposure ($B)', fontsize=8.6)
axe.set_ylim(0, 620)
axe.legend(fontsize=8.5, loc='upper left', framealpha=0.95, ncol=2)
axe.text(0.01, -0.22, 'Data: Table 9-1 totals are 2026 present values; 2027\u20132030 are illustrative expansion paths, not dynamic simulation output. K1\u2013K4 trigger terminates the model.',
         transform=axe.transAxes, fontsize=7.8, color=INK2)

fig.savefig(os.path.join(OUT, 'fig8-1_model_robustness_panels.svg'), format='svg', bbox_inches='tight')
fig.savefig(os.path.join(OUT, '_preview8.png'), dpi=115, bbox_inches='tight')
plt.close(fig)
print('fig 8-1 done')

# =====================================================================
# Fig 9-1  Fan chart (standalone)
# =====================================================================
fig, ax = plt.subplots(figsize=(10.5, 7.0))
xs = np.array([0, 1, 2, 3, 4])
lab = ['2026', '2027', '2028', '2029', '2030']
pe_lo = np.array([112, 130, 150, 170, 200])
pe_hi = np.array([308, 360, 420, 500, 600])
ba_lo = np.array([26.4, 32, 40, 50, 60])
ba_hi = np.array([93.4, 110, 130, 150, 180])
op_lo = np.array([0.4, 0.5, 0.6, 0.7, 0])
op_hi = np.array([1.9, 3, 4, 5, 6])

ax.fill_between(xs, pe_lo, pe_hi, color='#e57373', alpha=0.6, label='Pessimistic: 2026 $112\u2013308B \u2192 2030 illus. $200\u2013600B')
ax.fill_between(xs, ba_lo, ba_hi, color='#ffcc80', alpha=0.65, label='Base: 2026 $26.4\u201393.4B \u2192 2030 illus. $60\u2013180B')
ax.fill_between(xs, op_lo, op_hi, color='#81c784', alpha=0.65, label='Optimistic: 2026 $0.4\u20131.9B \u2192 2030 illus. $0\u20136B')
ax.plot(xs, (pe_lo + pe_hi) / 2, color='#8f1f1f', lw=1.5, ls='--', label='Scenario midpoints')
ax.plot(xs, (ba_lo + ba_hi) / 2, color='#bf360c', lw=1.5, ls='--')
ax.plot(xs, (op_lo + op_hi) / 2, color='#1b5e20', lw=1.5, ls='--')
ax.axhspan(200, 300, color='#9e9e9e', alpha=0.25)
ax.text(4.04, 250, 'Global DC annual capex ~$200\u2013300B (reference line)', fontsize=8.5, color=INK, va='center')
ax.set_xticks(xs)
ax.set_xticklabels(lab, fontsize=10.5)
for xv, nm in zip(xs[1:], ['P1 window\n(2027\u20132028)', 'P2\n(2027\u20132028)', 'P3\n(2027\u20132029)']):
    ax.axvline(xv, color='#888888', lw=1.0, ls=':')
    ax.text(xv, 460, nm, fontsize=8.5, ha='center', color=INK)
ax.text(4.04, 90, 'K1\u2013K4 trigger \u21d2\nmodel terminated', fontsize=8.5, color='#8f1f1f', va='center', weight='bold')
ax.set_xlabel('Year', fontsize=10)
ax.set_ylabel('L4 total exposure ($B)', fontsize=10)
ax.set_ylim(0, 620)
ax.set_xlim(-0.35, 4.65)
ax.set_title('Fig 9-1  Three-Scenario L4 Total Exposure Fan Chart', fontsize=13, weight='bold', pad=12)
ax.legend(fontsize=8.5, loc='upper left', framealpha=0.95)
ax.text(0.0, -0.17, 'Data: Table 9-1 totals are 2026 present values; 2027\u20132030 are illustrative expansion paths, not dynamic simulation output [derived\u00b7formula]. P1\u2013P3 are out-of-sample check points.',
        transform=ax.transAxes, fontsize=8, color=INK2)
fig.tight_layout(rect=[0, 0.03, 1, 1])
fig.savefig(os.path.join(OUT, 'fig9-1_three_scenario_fan_chart.svg'), format='svg', bbox_inches='tight')
fig.savefig(os.path.join(OUT, '_preview9.png'), dpi=120, bbox_inches='tight')
plt.close(fig)
print('fig 9-1 done')

print('ALL DONE')
