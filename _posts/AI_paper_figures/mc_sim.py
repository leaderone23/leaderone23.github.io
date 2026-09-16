# -*- coding: utf-8 -*-
"""
Monte Carlo simulation for the four-layer chain model (paper Ch. 8.4).
Produces:
  - L4 total loss distributions for the three scenarios (10,000 draws each)
  - Response surface of expected L4 loss over (r_tok x r_cost) grid
All amounts in USD 100 million (亿美元), consistent with paper Tables 7-1/7-2/7-3/9-1.
Scenario parameters follow Table 3-4; L4 parameters follow Tables 7-2/7-3.
Output: mc_output.npz  (consumed by gen_figs_matplotlib.py for Fig 8-1 panels c & d)
"""
import numpy as np

rng = np.random.default_rng(20260915)
N = 10_000

# ----------------------------------------------------------------------
# Scenario parameter ranges (paper Table 3-4, quantized; Table 7-2/7-3 L4)
# All [lo, hi] inclusive-uniform draws.
# ----------------------------------------------------------------------
SCEN = {
    #            r_tok(倍/年)   r_cost(年降幅)  股权减值(亿)  EAD(亿)   PD       LGD     证券化损失(亿)
    'optimistic': ([3.0, 5.0], [0.70, 0.90], [0, 0],     [600, 1200], [0.01, 0.02], [0.60, 0.80], [0, 0]),
    'base':       ([2.0, 3.0], [0.50, 0.70], [200, 700], [1200, 2100], [0.02, 0.05], [0.60, 0.80], [50, 150]),
    'pessimistic':([1.0, 1.5], [0.30, 0.50], [800, 2000],[2000, 3000], [0.10, 0.20], [0.60, 0.80], [200, 600]),
}


def draw(rng_, lo, hi):
    return rng_.uniform(lo, hi)


def l4_total(rng_, scen):
    """One L4 total draw = equity impairment + EAD*PD*LGD + securitization losses."""
    (rt_lo, rt_hi), (rc_lo, rc_hi), (eq_lo, eq_hi), (ead_lo, ead_hi), \
        (pd_lo, pd_hi), (lgd_lo, lgd_hi), (sec_lo, sec_hi) = scen
    equity = draw(rng_, eq_lo, eq_hi)
    ead = draw(rng_, ead_lo, ead_hi)
    pd = draw(rng_, pd_lo, pd_hi)
    lgd = draw(rng_, lgd_lo, lgd_hi)
    debt = ead * pd * lgd
    sec = draw(rng_, sec_lo, sec_hi)
    return equity + debt + sec


# ----------------------------------------------------------------------
# (1) Scenario loss distributions
# ----------------------------------------------------------------------
dists = {}
for name, params in SCEN.items():
    vals = np.array([l4_total(rng, params) for _ in range(N)])
    dists[name] = vals
    print(f'{name:12s} mean={vals.mean():8.1f}  P50={np.percentile(vals,50):7.1f}  '
          f'P90={np.percentile(vals,90):7.1f}  P99={np.percentile(vals,99):7.1f}  max={vals.max():8.1f}')

# ----------------------------------------------------------------------
# (2) Response surface: expected L4 loss over (r_tok x r_cost) grid
#     Anchor interpolation on the paper's scenario midpoints:
#     extreme-optimistic params -> optimistic expectation; extreme-pessimistic -> pessimistic.
#     Optimism weight: r_tok higher and r_cost higher both push toward optimistic.
# ----------------------------------------------------------------------
opt_exp = dists['optimistic'].mean()      # ~10
pess_exp = dists['pessimistic'].mean()    # ~2100

RT_LO, RT_HI = 1.0, 5.0
RC_LO, RC_HI = 0.30, 0.90
GRID = 60

rt_grid = np.linspace(RT_LO, RT_HI, GRID)
rc_grid = np.linspace(RC_LO, RC_HI, GRID)
R = np.zeros((GRID, GRID))
# weight: r_tok (0.6) + r_cost (0.4); normalized to [0,1], 1 = most optimistic
for i, rt in enumerate(rt_grid):
    for j, rc in enumerate(rc_grid):
        w = 0.6 * (rt - RT_LO) / (RT_HI - RT_LO) + 0.4 * (rc - RC_LO) / (RC_HI - RC_LO)
        w = np.clip(w, 0.02, 0.98)
        R[i, j] = pess_exp + (opt_exp - pess_exp) * w   # linear interp in loss space

np.savez(os_path := r'E:\Projects\AI_paper_figures\mc_output.npz',
         optimistic=dists['optimistic'], base=dists['base'], pessimistic=dists['pessimistic'],
         rt_grid=rt_grid, rc_grid=rc_grid, response=R,
         opt_exp=opt_exp, pess_exp=pess_exp)
print('saved:', os_path)
print('response range: %.1f .. %.1f (opt_exp=%.1f, pess_exp=%.1f)'
      % (R.min(), R.max(), opt_exp, pess_exp))
