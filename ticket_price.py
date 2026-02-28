# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

import numpy as np
import matplotlib.pyplot as plt
from typing import cast
from collections.abc import Iterable

from matplotlib.lines import Line2D

DARK_MODE_CSS = """\
<style>
@media (prefers-color-scheme: dark) {
  g[id^="text_"] { fill: #c9d1d9 !important; }
  use[style*="stroke: #000000"] { stroke: #c9d1d9 !important; }
  path[style*="stroke: #000000"] { stroke: #c9d1d9 !important; }
  g[id^="legend_"] > g:first-child path { fill: #21262d !important; stroke: #444c56 !important; }
}
</style>"""


def inject_dark_mode(svg_path: str) -> None:
    with open(svg_path) as f:
        content = f.read()
    content = content.replace("<defs>", f"{DARK_MODE_CSS}\n<defs>", 1)
    with open(svg_path, "w") as f:
        f.write(content)


# X range (guaranteed amount) from $10 to $10M
X = np.logspace(1, 7, 500)

# Wealth levels of potential buyers
wealth_levels = {
    "$10K": 1e4,
    "$100K": 1e5,
    "$1M": 1e6,
    "$10M": 1e7,
    "$100M": 1e8,
}


def certainty_equivalent_log(W, X):
    """CE for option B with u(w) = ln(w), i.e. CRRA γ=1"""
    ce_b = np.sqrt(W * (W + 100 * X)) - W
    return np.maximum(ce_b, X)


def market_price(X, W_median=1e5, k=1.5):
    """Approximate market price with diverse buyers"""
    ev = 50 * X
    price = ev / (1 + k * X / W_median)
    return np.maximum(price, X)


# =========== PLOT 1: Line charts ===========
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

colors = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0"]
for (label, W), color in zip(wealth_levels.items(), colors):
    price = certainty_equivalent_log(W, X)
    ax1.loglog(X, price, label=f"Buyer Wealth={label}", color=color, linewidth=2)

ax1.loglog(X, 50 * X, "--", color="gray", alpha=0.7, linewidth=1.5, label="𝔼 = 50X")
ax1.loglog(
    X, X, ":", color="black", alpha=0.5, linewidth=1.5, label="Floor = X (green button)"
)
ax1.loglog(
    X,
    market_price(X),
    color="red",
    linewidth=3,
    alpha=0.8,
    label="Market price (approx.)",
)

ax1.set_xlabel("X (guaranteed amount)", fontsize=13)
ax1.set_ylabel("Ticket price", fontsize=13)
ax1.set_title("Ticket Price vs X (absolute)", fontsize=14)
ax1.legend(fontsize=10, loc="upper left")
ax1.grid(True, alpha=0.3, which="both")
ax1.set_xlim(X[0], X[-1])

for (label, W), color in zip(wealth_levels.items(), colors):
    price = certainty_equivalent_log(W, X)
    ratio = price / (50 * X)
    ax2.semilogx(X, ratio * 100, label=f"Wealth={label}", color=color, linewidth=2)

ax2.semilogx(
    X,
    market_price(X) / (50 * X) * 100,
    color="red",
    linewidth=3,
    alpha=0.8,
    label="Market price",
)
ax2.axhline(y=100, color="gray", linestyle="--", alpha=0.5, label="100% 𝔼")
ax2.axhline(y=2, color="black", linestyle=":", alpha=0.5, label="Floor = X/50X = 2%")

ax2.set_xlabel("X (guaranteed amount)", fontsize=13)
ax2.set_ylabel("Ticket price as % of 𝔼 (50X)", fontsize=13)
ax2.set_title("Discount to 𝔼 vs X", fontsize=14)
ax2.legend(fontsize=10, loc="upper right")
ax2.grid(True, alpha=0.3, which="both")
ax2.set_xlim(X[0], X[-1])
ax2.set_ylim(0, 105)

plt.tight_layout()
plt.savefig("img/ticket_price_plot.svg", bbox_inches="tight", transparent=True)
inject_dark_mode("img/ticket_price_plot.svg")
print("Saved line charts")


# =========== PLOT 2: Violin plot ===========
# For each X value, simulate ticket prices across a realistic population
# Population wealth follows a log-normal distribution (Pareto-like tail)

np.random.seed(42)
n_people = 50_000

# Log-normal wealth: median ~$60K, heavy right tail
log_wealth = np.random.normal(loc=11.0, scale=1.2, size=n_people)  # ln($60K) ≈ 11.0
pop_wealth = np.exp(log_wealth)

x_values = [100, 1_000, 10_000, 100_000, 1_000_000]
x_labels = ["$100", "$1K", "$10K", "$100K", "$1M"]

# For each X, compute ticket price (as % of EV) for each person in population
violin_data = []
for x_val in x_values:
    ce = np.sqrt(pop_wealth * (pop_wealth + 100 * x_val)) - pop_wealth
    ticket = np.maximum(ce, x_val)
    ev = 50 * x_val
    pct_of_ev = (ticket / ev) * 100
    # Clip to [0, 100] for display
    pct_of_ev = np.clip(pct_of_ev, 0, 100)
    violin_data.append(pct_of_ev)

fig2, ax3 = plt.subplots(figsize=(10, 5.5))

parts = ax3.violinplot(
    violin_data,
    positions=list(range(len(x_values))),
    showmeans=True,
    showmedians=True,
    showextrema=False,
)

# Style the violins
gradient_colors = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63", "#9C27B0"]
for i, pc in enumerate(cast(Iterable, parts["bodies"])):
    pc.set_facecolor(gradient_colors[i])
    pc.set_alpha(0.7)
    pc.set_edgecolor(gradient_colors[i])

parts["cmeans"].set_color("#333333")
parts["cmeans"].set_linewidth(2)
parts["cmedians"].set_color("#c62828")
parts["cmedians"].set_linewidth(2)

# Add market price markers
for i, x_val in enumerate(x_values):
    mp = market_price(np.array([x_val]))[0]
    mp_pct = (mp / (50 * x_val)) * 100
    ax3.plot(
        i,
        mp_pct,
        "D",
        color="red",
        markersize=10,
        zorder=5,
        markeredgecolor="white",
        markeredgewidth=1.5,
    )

# Annotations
ax3.axhline(y=100, color="gray", linestyle="--", alpha=0.4, linewidth=1)
ax3.text(-0.4, 101.5, "100% of 𝔼", color="gray", fontsize=10, alpha=0.7)

ax3.set_xticks(range(len(x_values)))
ax3.set_xticklabels(x_labels, fontsize=13)
ax3.set_xlabel("Guaranteed amount (X)", fontsize=14)
ax3.set_ylabel("Ticket price as % of expected value", fontsize=14)
ax3.set_ylim(-2, 108)
ax3.grid(True, alpha=0.2, axis="y")

# Legend
legend_elements = [
    Line2D([0], [0], color="#333333", linewidth=2, label="Mean"),
    Line2D([0], [0], color="#c62828", linewidth=2, label="Median"),
    Line2D(
        [0],
        [0],
        marker="D",
        color="red",
        markersize=8,
        linestyle="None",
        markeredgecolor="white",
        markeredgewidth=1.5,
        label="Market price",
    ),
]
ax3.legend(handles=legend_elements, fontsize=11, loc="upper right")

plt.tight_layout()
plt.savefig("img/violin_plot.svg", bbox_inches="tight", transparent=True)
inject_dark_mode("img/violin_plot.svg")
print("Saved violin plot")
