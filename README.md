# superdove-pixel-purification
For PlanetScope Superdove timeseries cleaning
# Pixel purification and band-composition robustness for PlanetScope SuperDove

Code and derived data accompanying the paper:

> **Band composition governs vegetation-index robustness to orbital drift in PlanetScope SuperDove**
> Pablo Quesada-Molina et al. *Journal of Remote Sensing* (under review), 2026.
> DOI: `[añadir DOI del artículo cuando se acepte]`

This repository reproduces the analyses and figures of the paper: the orbital-drift / inter-satellite decomposition, the band-composition index-robustness comparison, the fractional-cover purity sweep, and the Retrospective Phenological Integrity Filter (RPIF).

---

## Repository structure

```
/code      Analysis notebooks and scripts (see below)
/data      Derived analysis tables (CSV) and AOI polygons (GeoJSON)
README.md
LICENSE              MIT (code)
environment.yml      Python environment
```

## Code

| File | Purpose |
|------|---------|
| `01_Image_data_inspection.py`                       | Initial inspection of the image stacks |
| `01_Visual_Validation.py`                           | Visual QC of acquisitions |
| `02_3_paper_quality_diagnostics_EXTENDED_v4.ipynb`  | Drift/inter-satellite decomposition, multi-index robustness, purity sweep, figures |
| `02_4_rpif_spectral_integrity_filter_v2.ipynb`      | RPIF design, rejection statistics and validation |
| `create_graphical_abstract.py`                      | Graphical abstract |

Run order: `01_*` → `02_3_*` → `02_4_*`. Paths are set at the top of each notebook via a `BASE` variable; edit it to point to your local `./data` folder.

## Data

**What is included** (derived, aggregated products — safe to redistribute):
- `data/tables/Table_*.csv` — the analysis-ready tables underlying every figure and statistic (see data dictionary below).
- `data/aoi/*.geojson` — the Area-of-Interest / crown-delineation polygons for the two sites.

**What is NOT included** (and why):
- **Raw PlanetScope imagery** (the harmonised Level 3B GeoTIFFs). These are proprietary; redistribution is not permitted under the Planet End-User Licence. They can be obtained from Planet (https://www.planet.com/) under licence; this repository provides the derived tables and code needed to reproduce all reported results.
- The full per-pixel surface-reflectance master is likewise not redistributed; the aggregated `Table_*.csv` products are sufficient to regenerate the figures and statistics.

### Data dictionary (CSV tables)

> Completa/ajusta esta lista con tus 23 archivos reales y añade una línea por columna clave de cada uno.

| File | Content | Used in |
|------|---------|---------|
| `Table_NDVI_Drift_Regression.csv`      | Per-entity NDVI drift regression: slope, 95% CI, p-value | Table 1 |
| `Table_NDVI_Drift_Mechanism.csv`       | Mechanistic band-bias propagation: Red/NIR biases, net NDVI bias | Table 1, Fig 5A |
| `Table_SceneGeometry_PhaseAngle.csv`   | Scattering phase angle ΔΨ by intra-day level (N1/N2/N3) | Fig 6A |
| `Table_BandBias_vs_PhaseAngle.csv`     | Pair-level per-band bias vs ΔΨ (Spearman ρ) | Fig 6B, Table S4 |
| `Table_MultiIndex_DriftRobustness.csv` | rRMSE and CCC for the eight indices | Fig 7, Table S1 |
| `Table_PuritySweep.csv`                | Per-band illumination bias across fc thresholds (0–90%) | Fig 8A, Table S5 |
| `Table_SpectralConcordance.csv`        | CCC of intra-day pairs (NDVI, PRIsat) | Fig 5B, Fig 8B |
| `Table_fcRegime_DriftContrast.csv`     | Drift contrast by fractional-cover regime | Fig 8 |
| `Table_FilterBenefit_vs_Purity.csv`    | Purification benefit as a function of purity | — |
| `Table_RPIF_RejectionStats.csv`        | RPIF rejection rates and σ-reduction per cover | Table 2 |
| `Table_RPIF_RejectionByYear.csv`       | RPIF rejection rate by hydrological year | Fig 9 |
| `Table_RPIF_RemovedClassification.csv` | Classification of removed observations (haze/substrate) | Fig 10 |
| `Table_RPIF_RemovedSpectralSignature.csv` | Spectral signature of removed vs retained | Fig 10 |
| `Table_RPIF_SensitivityAnalysis.csv`   | RPIF rejection rate vs IQR_tol parameter | Table S6 |
| `Table_RPIF_IntradayRMSE_benefit.csv`  | Intra-day NDVI RMSE before/after purification | — |
| `Table_RPIF_CloudCrossCheck.csv`       | RPIF rejections vs per-scene cloud mask | — |
| `candidate_flowering_events.csv`       | Candidate flowering events (blind detection) | — |

### AOI polygons

| File | Site | Description |
|------|------|-------------|
| `veg_AOI_1.geojson`, `veg_AOI_2.geojson` | Doñana (Cuesta Maneli) | Corema album sub-AOIs and patch delineations |
| `avocado_group.geojson`                  | Axarquía | Avocado plot (~1.07 ha) |
| `mangoe_group.geojson`                    | Axarquía | Mango plot (~1.04 ha) |

CRS: `[indicar EPSG, p.ej. EPSG:32629 / EPSG:32630]`.

---

## Licence

- **Code**: MIT (see `LICENSE`).
- **Derived data** (`Table_*.csv`, `*.geojson`): Creative Commons Attribution 4.0 (CC-BY-4.0).
- Raw PlanetScope imagery is © Planet Labs PBC and is not included; see above.

## How to cite

If you use this code or data, please cite the paper above and this repository:

> Quesada-Molina P. *Pixel purification and band-composition robustness for PlanetScope SuperDove* [software/dataset]. Zenodo; 2026. DOI: `[DOI de Zenodo]`

## Contact

Pablo Quesada-Molina — Universidad de Málaga / QSIMOV S.L. — pabquemol@uma.es
