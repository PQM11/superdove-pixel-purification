# Estructura esperada (relativa a la raíz del repo):
#   ./01_data/<proyecto>/AOI/                -> polígonos AOI (incluidos)
#   ./01_data/<proyecto>/images/             -> imágenes Planet (NO incluidas; bajo licencia Planet)
#   ./03_figures_&_results/<proyecto>/        -> tablas derivadas y figuras (salidas)

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.patches as patches

# -----------------------------------------------------------------------------
# 0. CONFIGURACIÓN ESTÉTICA Q1 (Remote Sensing of Environment / ISPRS)
# -----------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "lines.linewidth": 2,
    "lines.markersize": 5
})

# Paleta segura para daltonismo (Okabe-Ito) + colores funcionales
COLORS = {
    "blue": "#0072B2", "orange": "#D55E00", "green": "#009E73", 
    "light_blue": "#56B4E9", "yellow": "#F0E442", "purple": "#CC79A7",
    "soil": "#8C564B", "haze": "#AEC7E8", "raw": "#BDBDBD", "clean": "#2CA02C"
}

fig = plt.figure(figsize=(18, 9), constrained_layout=True)
gs = gridspec.GridSpec(2, 4, figure=fig, width_ratios=[1, 1, 1, 1.2])

# -----------------------------------------------------------------------------
# PANEL 1: THE PHYSICAL FORCING (Izquierda, 2 subplots)
# -----------------------------------------------------------------------------
# 1A: Deriva Orbital (Scatter temporal)
ax1a = fig.add_subplot(gs[0, 0])
years = np.linspace(2020, 2025, 150)
# Simulación de la deriva: tendencia ascendente de +75 mins con ruido y estacionalidad
drift_lst = 10.0 + (years - 2020) * 0.25 + np.sin((years - 2020) * np.pi * 2) * 0.1 + np.random.normal(0, 0.08, 150)
scatter = ax1a.scatter(years, drift_lst, c=drift_lst, cmap="viridis", alpha=0.7, s=20)
ax1a.plot(years, 10.0 + (years - 2020) * 0.25, color="black", linestyle="--", alpha=0.8)
ax1a.set_title("A. Constellation Orbital Drift")
ax1a.set_ylabel("Local Solar Time (h)")
ax1a.set_xticks([2020, 2021, 2022, 2023, 2024, 2025])

# 1B: Dependencia Espectral del Ángulo de Fase (Gráfico de barras)
ax1b = fig.add_subplot(gs[1, 0])
bands = ['NIR\n(Resilient)', 'Red\n(Resilient)', 'Yellow', 'Green I', 'Coastal Blue\n(Geometry-driven)']
spearman_rho = [0.22, 0.07, 0.61, 0.59, 0.62] # Datos físicos del manuscrito
y_pos = np.arange(len(bands))
colors_1b = [COLORS["green"], COLORS["green"], COLORS["orange"], COLORS["orange"], COLORS["orange"]]

ax1b.barh(y_pos, spearman_rho, color=colors_1b, alpha=0.8)
ax1b.set_yticks(y_pos)
ax1b.set_yticklabels(bands)
ax1b.set_xlabel(r"Sensitivity to Scattering Geometry ($Spearman\ \rho\ vs\ \Delta\Psi$)")
ax1b.set_title("B. Band-Specific Geometry Sensitivity")

# -----------------------------------------------------------------------------
# PANEL 2: SAFEGUARD 1 - INDEX ROBUSTNESS (Centro Superior)
# -----------------------------------------------------------------------------
ax2 = fig.add_subplot(gs[0, 1:3])
ax2.set_title("C. Safeguard 1: Index Robustness via Band Cancellation")
ax2.axis('off') # Usamos el espacio para dibujar vectores matemáticos

# NDVI Sub-panel
ax2.text(0.25, 0.9, "NDVI: Co-directional Bands\n(Intrinsic Cancellation)", ha='center', va='center', fontweight='bold')
ax2.annotate("", xy=(0.15, 0.4), xytext=(0.35, 0.7), arrowprops=dict(arrowstyle="<-", color="darkred", lw=3))
ax2.text(0.27, 0.6, r"$\Delta\rho_{Red}$", color="darkred", fontsize=12)
ax2.annotate("", xy=(0.20, 0.4), xytext=(0.40, 0.7), arrowprops=dict(arrowstyle="<-", color="darkgray", lw=3))
ax2.text(0.35, 0.5, r"$\Delta\rho_{NIR}$", color="darkgray", fontsize=12)
ax2.text(0.25, 0.25, r"$\approx 0\%$ Net Bias", color=COLORS["green"], fontsize=14, fontweight='bold', ha='center')

# Línea divisoria
ax2.plot([0.5, 0.5], [0.1, 0.9], color="black", linestyle=":", lw=1)

# PRI Sub-panel
ax2.text(0.75, 0.9, "PRI: Asymmetric Bands\n(Bias Amplification)", ha='center', va='center', fontweight='bold')
ax2.annotate("", xy=(0.85, 0.7), xytext=(0.65, 0.4), arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=3))
ax2.text(0.70, 0.6, r"$\Delta\rho_{Green I}$", color=COLORS["green"], fontsize=12)
ax2.annotate("", xy=(0.75, 0.4), xytext=(0.85, 0.6), arrowprops=dict(arrowstyle="<-", color="olive", lw=3))
ax2.text(0.85, 0.45, r"$\Delta\rho_{Green}$", color="olive", fontsize=12)
ax2.text(0.75, 0.25, "Amplified Error\n(rRMSE > 100%)", color=COLORS["orange"], fontsize=14, fontweight='bold', ha='center')

# -----------------------------------------------------------------------------
# PANEL 3: SAFEGUARD 2 - PIXEL PURIFICATION (Centro Inferior)
# -----------------------------------------------------------------------------
ax3 = fig.add_subplot(gs[1, 1:3])
ax3.set_title("D. Safeguard 2: Phenological Integrity Filtering (RPIF)")
np.random.seed(42)
t_rpif = np.linspace(1, 52, 200)
# Base signal
ndvi_base = 0.5 + 0.2 * np.sin(t_rpif * 2 * np.pi / 52)
ndvi_valid = ndvi_base + np.random.normal(0, 0.05, 200)

# Envelope
envelope = ndvi_base - 0.15
ax3.plot(t_rpif, envelope, color="black", linestyle="--", label="Adaptive RPIF Lower Bound")

# Valid points
ax3.scatter(t_rpif, ndvi_valid, color=COLORS["clean"], s=15, alpha=0.6, label="Valid Observations")

# Contamination spikes
haze_idx = np.random.choice(200, 8, replace=False)
soil_idx = np.random.choice(200, 10, replace=False)

ax3.scatter(t_rpif[haze_idx], ndvi_base[haze_idx] - 0.35, color=COLORS["haze"], s=40, marker="X", edgecolor="black", label=r"Haze ($Elevated\ Coastal\ Blue$)")
ax3.scatter(t_rpif[soil_idx], ndvi_base[soil_idx] - 0.25, color=COLORS["soil"], s=40, marker="v", edgecolor="black", label=r"Substrate ($Bare\ Sand/Soil$)")

ax3.set_xlabel("Hydrological Week")
ax3.set_ylabel("NDVI")
ax3.legend(loc="lower right", fontsize=8, frameon=False)

# -----------------------------------------------------------------------------
# PANEL 4: PHENOLOGICAL RECOVERY (Derecha, 2 subplots)
# -----------------------------------------------------------------------------
# 4A: Closed Canopy
ax4a = fig.add_subplot(gs[0, 3])
t = np.linspace(1, 52, 100)
clean_avocado = 0.65 + 0.1 * np.sin(t * 2 * np.pi / 52)
raw_avocado = clean_avocado.copy()
raw_avocado[np.random.choice(100, 15, replace=False)] -= np.random.uniform(0.15, 0.35, 15) # Ruido asimétrico

ax4a.plot(t, raw_avocado, color=COLORS["raw"], linestyle="--", alpha=0.8, label="Raw Satellite Signal")
ax4a.plot(t, clean_avocado, color=COLORS["clean"], linewidth=2.5, label="Purified Signal")
ax4a.set_title("E. Closed Canopy (Avocado)")
ax4a.set_ylabel("NDVI")
ax4a.set_ylim(0.2, 0.9)
ax4a.legend(loc="lower left", fontsize=8, frameon=False)

# 4B: Open Canopy
ax4b = fig.add_subplot(gs[1, 3])
clean_mango = 0.35 + 0.15 * np.sin(t * 2 * np.pi / 52 - 0.5)
raw_mango = clean_mango.copy()
raw_mango[np.random.choice(100, 20, replace=False)] -= np.random.uniform(0.1, 0.25, 20) # Ruido de sustrato

ax4b.plot(t, raw_mango, color=COLORS["raw"], linestyle="--", alpha=0.8)
ax4b.plot(t, clean_mango, color=COLORS["orange"], linewidth=2.5) # Color distinto para mostrar la diferencia de arquitectura
ax4b.set_title("F. Open Canopy (Mango/Corema)")
ax4b.set_xlabel("Hydrological Week")
ax4b.set_ylabel("NDVI")
ax4b.set_ylim(0.05, 0.65)

# -----------------------------------------------------------------------------
# EXPORTACIÓN
# -----------------------------------------------------------------------------
plt.savefig("graphical_abstract_base.svg", format="svg", bbox_inches="tight", transparent=True)
plt.close()