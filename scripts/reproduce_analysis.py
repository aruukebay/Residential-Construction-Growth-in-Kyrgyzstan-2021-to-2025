"""
Reproducible analysis for:
Residential Construction Growth in Kyrgyzstan: Regional Patterns and
Geographic Concentration, 2021 to 2025

Reads the preserved NSC JSON extract (no hard-coded values), validates it,
reproduces every statistic in the manuscript, and adds robustness checks:
normalized HHI, two-year-average comparison, contribution to national change,
dispersion, and a boundary-reform sensitivity analysis (city + surrounding region).

Usage:  python reproduce_analysis.py [path/to/raw.json] [output_dir]
"""
import json, sys, hashlib
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "kyrgyzstan_residential_construction_raw.json")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "output"); OUT.mkdir(exist_ok=True)
NAMES = {"Batken oblast": "Batken Region", "Jalal-Abat oblast": "Jalal Abad Region",
         "Yssyk-Kul oblast": "Issyk Kul Region", "Naryn oblast": "Naryn Region",
         "Osh oblast": "Osh Region", "Talas oblast": "Talas Region",
         "Chui oblast": "Chui Region", "Bishkek city": "Bishkek City", "Osh city": "Osh City"}
YEARS = [2021, 2022, 2023, 2024, 2025]

# ---- 1. Load and validate -------------------------------------------------
print("SHA-256 of source extract:", hashlib.sha256(RAW.read_bytes()).hexdigest())
raw = json.loads(RAW.read_text(encoding="utf-8"))
assert raw["units"] == "thous. sq.m.", "unexpected unit"
rows = [(NAMES[r["title_en"]], v["key"], v["value"]) for r in raw["data"] for v in r["values"]]
df = pd.DataFrame(rows, columns=["region", "year", "thousand_sqm"]).sort_values(["region", "year"])
assert len(df) == 45 and df.region.nunique() == 9 and sorted(df.year.unique()) == YEARS
assert df.thousand_sqm.notna().all() and (df.thousand_sqm > 0).all()
W = df.pivot(index="region", columns="year", values="thousand_sqm")      # 9 x 5, thousand m2
print("pandas", pd.__version__, "numpy", np.__version__)

# ---- 2. Core measures (as in manuscript) -----------------------------------
nat = W.sum()
S = W / nat                                                              # shares (decimals)
hhi = (S ** 2).sum()
N = len(W)
hhi_norm = (hhi - 1 / N) / (1 - 1 / N)
nat_tab = pd.DataFrame({"national_thousand_sqm": nat, "annual_growth_pct": nat.pct_change() * 100,
                        "hhi": hhi, "hhi_normalized": hhi_norm, "top1_share_pct": S.max() * 100})
overall = (nat[2025] / nat[2021] - 1) * 100
cagr = ((nat[2025] / nat[2021]) ** 0.25 - 1) * 100
reg = pd.DataFrame({
    "y2021": W[2021], "y2025": W[2025], "abs_change": W[2025] - W[2021],
    "pct_change": (W[2025] / W[2021] - 1) * 100,
    "cagr_pct": ((W[2025] / W[2021]) ** 0.25 - 1) * 100,
    "share_2021_pct": S[2021] * 100, "share_2025_pct": S[2025] * 100,
    "share_change_pp": (S[2025] - S[2021]) * 100,
    "contribution_to_national_change_pct": (W[2025] - W[2021]) / (nat[2025] - nat[2021]) * 100})

# ---- 3. Robustness ----------------------------------------------------------
early, late = W[[2021, 2022]].mean(axis=1), W[[2024, 2025]].mean(axis=1)
robust = pd.DataFrame({"avg_2021_22": early, "avg_2024_25": late,
                       "pct_change": (late / early - 1) * 100})
h = lambda v: float(((v / v.sum()) ** 2).sum())
two_year_hhi = (h(early), h(late))
cv = W.std(ddof=0) / W.mean()                                             # dispersion across territories
anomaly = np.log(W).diff(axis=1).stack().rename("log_change").reset_index()
anomaly["abs"] = anomaly.log_change.abs()
anomaly = anomaly.sort_values("abs", ascending=False).head(6)

# ---- 4. Boundary-reform sensitivity (city + surrounding region) -------------
M = W.copy()
M.loc["Bishkek City + Chui Region"] = W.loc["Bishkek City"] + W.loc["Chui Region"]
M.loc["Osh City + Osh Region"] = W.loc["Osh City"] + W.loc["Osh Region"]
M = M.drop(["Bishkek City", "Chui Region", "Osh City", "Osh Region"])
Sm = M / M.sum()
hhi7 = (Sm ** 2).sum(); hhi7_norm = (hhi7 - 1 / len(M)) / (1 - 1 / len(M))
sens = pd.DataFrame({"2021": M[2021], "2025": M[2025],
                     "pct_change": (M[2025] / M[2021] - 1) * 100,
                     "share_2021_pct": Sm[2021] * 100, "share_2025_pct": Sm[2025] * 100})

# ---- 5. Save tables ---------------------------------------------------------
W.to_csv(OUT / "table2_territory_year.csv"); reg.round(4).to_csv(OUT / "table3_regional.csv")
nat_tab.round(6).to_csv(OUT / "national_summary_v2.csv")
sens.round(4).to_csv(OUT / "sensitivity_city_region.csv")
pd.DataFrame({"hhi_9_units": hhi, "hhi_9_normalized": hhi_norm, "hhi_7_merged": hhi7,
              "hhi_7_normalized": hhi7_norm}).round(6).to_csv(OUT / "hhi_comparison.csv")
robust.round(3).to_csv(OUT / "robustness_two_year_avg.csv")

# ---- 6. Figures (axes include context; titles belong in captions) -----------
plt.rcParams.update({"font.family": "serif", "font.size": 10})
fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.plot(YEARS, nat / 1000, marker="o", color="#1f4e79"); ax.set_ylim(0, 2.0)
ax.set_ylabel("Million square meters"); ax.set_xlabel("Year"); ax.set_xticks(YEARS); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(OUT / "figure1_national_total.png", dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 3.8))
ax.plot(YEARS, hhi, marker="o", color="#1f4e79", label="Nine territories")
ax.plot(YEARS, hhi7, marker="s", ls="--", color="#c55a11", label="Seven units (city + surrounding region)")
ax.axhline(1 / 9, color="grey", lw=.8, ls=":"); ax.text(2021, 1 / 9 + .004, "Minimum for 9 units (1/9)", fontsize=8, color="grey")
ax.set_ylim(0, 0.35); ax.set_ylabel("Herfindahl–Hirschman index"); ax.set_xlabel("Year")
ax.set_xticks(YEARS); ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 0.01), ncol=2, fontsize=8); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(OUT / "figure5_hhi.png", dpi=300); plt.close(fig)

idx = W.div(W[2021], axis=0) * 100
fig, axes = plt.subplots(3, 3, figsize=(7, 6), sharex=True, sharey=True)
for a, r in zip(axes.ravel(), idx.index):
    for o in idx.index: a.plot(YEARS, idx.loc[o], color="#cccccc", lw=.8)
    a.plot(YEARS, idx.loc[r], color="#1f4e79", lw=1.8, marker="o", ms=3); a.axhline(100, color="k", lw=.5)
    a.set_title(r, fontsize=9); a.set_xticks([2021, 2023, 2025])
fig.supylabel("Index (2021 = 100)"); fig.tight_layout(); fig.savefig(OUT / "figure3_index_small_multiples.png", dpi=300); plt.close(fig)

# ---- 6b. Remaining manuscript figures (2, 4, 6) ----------------------------
PAL = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#8c564b", "#e377c2", "#ff7f0e", "#17becf", "#7f7f7f"]
order = W[2025].sort_values().index
fig, ax = plt.subplots(figsize=(6.5, 4.2)); yy = np.arange(len(order))
ax.barh(yy - .2, W.loc[order, 2021], .4, label="2021", color="#9ecae1")
ax.barh(yy + .2, W.loc[order, 2025], .4, label="2025", color="#1f4e79")
ax.set_yticks(yy); ax.set_yticklabels(order); ax.set_xlabel("Thousand square meters")
ax.legend(frameon=False, loc="lower right"); ax.grid(axis="x", alpha=.3)
fig.tight_layout(); fig.savefig(OUT / "figure2_territory_2021_vs_2025.png", dpi=300); plt.close(fig)

def line_labels(data, ylabel, fname, ref_year=None, ylim=None):
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ends = data[2025].sort_values()
    for i, r in enumerate(data.index):
        ax.plot(YEARS, data.loc[r], marker="o", ms=3, lw=1.5, color=PAL[i], ls="-" if i < 5 else "--")
    # end labels, nudged apart to avoid overlap
    ys = list(ends.values); lab = list(ends.index); gap = (max(ys) - min(ys)) * 0.045; pos = []
    for y in ys: pos.append(y if not pos else max(y, pos[-1] + gap))
    for l, y0, y1 in zip(lab, ys, pos):
        ax.text(2025.08, y1, l, fontsize=7.5, va="center", color=PAL[list(data.index).index(l)])
    if ref_year: ax.axvline(ref_year, color="k", lw=.7, ls=":"); ax.text(ref_year + .03, ax.get_ylim()[1] * .98, "2024 reform", fontsize=7, va="top")
    ax.set_xlim(2020.8, 2026.4); ax.set_xticks(YEARS); ax.set_ylabel(ylabel); ax.set_xlabel("Year"); ax.grid(alpha=.3)
    if ylim: ax.set_ylim(*ylim)
    fig.tight_layout(); fig.savefig(OUT / fname, dpi=300); plt.close(fig)

line_labels(S * 100, "Percent of national total", "figure4_regional_shares.png", ylim=(0, 38))
POP = Path(sys.argv[3] if len(sys.argv) > 3 else "kyrgyzstan_residential_construction_clean.csv")
if POP.exists():
    pc = pd.read_csv(POP)
    P = pc.pivot(index="region", columns="year", values="population_thousand")
    pc_int = (W * 1000) / P                       # m2 per 1,000 residents (W in thousand m2, P in thousand persons)
    P.to_csv(OUT / "tableA1_population_thousand.csv"); pc_int.round(1).to_csv(OUT / "exploratory_sqm_per_1000.csv")
    line_labels(pc_int, "Square meters per 1,000 residents", "figure6_per_1000_residents.png", ref_year=2024, ylim=(60, 520))

# ---- 7. Report --------------------------------------------------------------
pd.set_option("display.width", 200, "display.float_format", "{:.4f}".format)
print("\nNational:\n", nat_tab); print(f"Overall growth {overall:.2f}%  CAGR {cagr:.2f}%")
print("\nRegional:\n", reg.round(2)); print("\nTwo-year-average comparison:\n", robust.round(1))
print("two-year HHI:", [round(x, 4) for x in two_year_hhi]); print("CV across territories:\n", cv.round(3).to_dict())
print("\nLargest year-to-year log changes (check against source):\n", anomaly.round(3).to_string(index=False))
print("\nSensitivity (merged):\n", sens.round(2)); print("HHI 7 units:", hhi7.round(4).to_dict()); print("Normalized:", hhi7_norm.round(4).to_dict())
