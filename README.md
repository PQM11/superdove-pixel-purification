# superdove-pixel-purification

Code and derived data accompanying the paper:

> **Band composition governs vegetation-index robustness to orbital drift in PlanetScope SuperDove**
> Quesada-Molina P. et al. *Journal of Remote Sensing* (sent/under review), 2026.
> Article DOI: `[once it has been accepted by the journal]`

The repository reproduces the analyses and figures of the paper: the orbital-drift / inter-satellite decomposition, the band-composition index-robustness comparison, the fractional-cover purity sweep, and the Retrospective Phenological Integrity Filter (RPIF).

**Derived data are archived on Zenodo:** https://doi.org/10.5281/zenodo.21052352 (CC-BY-4.0).

---

## Code

| File | Purpose |
|------|---------|
| `01_Image_data_inspection.py`            | Initial inspection of the image stacks |
| `02_Visual_Validation.py`                | Visual QC of acquisitions |
| `02_3_paper_quality_diagnostics.ipynb`   | Drift/inter-satellite decomposition, multi-index robustness, purity sweep, figures |
| `02_4_rpif_spectral_integrity_filter.ipynb` | RPIF design, rejection statistics and validation |
| `create_graphical_abstract.py`           | Graphical abstract |

Paths are set at the top of each notebook via a `BASE` variable pointing to a local results/data folder. Raw PlanetScope imagery and the per-pixel reflectance master are **not** redistributed (see below); the derived tables reproduce all reported results.

## Data (archived on Zenodo, DOI above)

### Area-of-Interest polygons (zipped shapefiles)

| File | Site | Description |
|------|------|-------------|
| `veg_AOI_1.zip`      | Doñana (Cuesta Maneli) | Corema album Sub-AOI 1 and patch delineations |
| `veg_AOI_2.zip`      | Doñana (Cuesta Maneli) | Corema album Sub-AOI 2 and patch delineations |
| `avocado_group.zip`  | Axarquía (Vélez-Málaga) | Avocado plot (~1.07 ha) |
| `mangoe_group.zip`   | Axarquía (Vélez-Málaga) | Mango plot (~1.04 ha) |

Each archive contains the full shapefile set (`.shp`, `.shx`, `.dbf`, `.prj`). CRS: `[indicar EPSG]`.

### Derived analysis tables (CSV)

*Drift and cancellation mechanism*
| File | Content | Figure/Table |
|------|---------|--------------|
| `Table_NDVI_Drift_Regression.csv`      | Per-entity NDVI drift regression (slope, 95% CI, p) | Table 1 |
| `Table_NDVI_Drift_Mechanism.csv`       | Mechanistic band-bias propagation (Red/NIR → net NDVI bias) | Table 1, Fig 5A |
| `Table_InterSatellite_vs_Drift.csv`    | Inter-satellite vs orbital-drift decomposition (N1/N2/N3) | Fig 6 |
| `Table_SceneGeometry_PhaseAngle.csv`   | Scene-level scattering phase angle ΔΨ by intra-day level | Fig 6A |
| `Table_BandBias_vs_PhaseAngle.csv`     | Pair-level per-band bias vs ΔΨ (Spearman ρ) | Fig 6B, Table S4 |

*Index robustness and purity*
| File | Content | Figure/Table |
|------|---------|--------------|
| `Table_MultiIndex_DriftRobustness.csv` | rRMSE and CCC for the eight indices | Fig 7, Table S1 |
| `Table_SpectralConcordance.csv`        | CCC of intra-day pairs (NDVI, PRIsat) | Fig 5B, Fig 8B |
| `Table_PuritySweep.csv`                | Per-band illumination bias across fc thresholds (0–90%) | Fig 8A, Table S5 |
| `Table_fcRegime_DriftContrast.csv`     | Drift contrast by fractional-cover regime | Fig 8 |
| `Table_FilterBenefit_vs_Purity.csv`    | Purification benefit as a function of purity | — |
| `Table_CrossEntity_Statistics.csv`     | Cross-entity summary statistics | — |

*RPIF (filter design, yield and validation)*
| File | Content | Figure/Table |
|------|---------|--------------|
| `Table_RPIF_RejectionStats.csv`          | RPIF rejection rates and σ-reduction per cover | Table 2 |
| `Table_RPIF_RejectionByYear.csv`         | Rejection rate by hydrological year | Fig 9 |
| `Table_RPIF_RemovedClassification.csv`   | Classification of removed observations (haze/substrate) | Fig 10 |
| `Table_RPIF_RemovedSpectralSignature.csv`| Spectral signature of removed vs retained | Fig 10 |
| `Table_RPIF_SensitivityAnalysis.csv`     | Rejection rate vs IQR_tol tolerance parameter | Table S6 |
| `Table_RPIF_IntradayRMSE_benefit.csv`    | Intra-day NDVI RMSE before/after purification | — |
| `Table_RPIF_CloudCrossCheck.csv`         | RPIF rejections vs per-scene cloud mask | — |
| `Table_RPIF_Thresholds_Avocado.csv`      | RPIF phenological-envelope thresholds — avocado | — |
| `Table_RPIF_Thresholds_Mango.csv`        | RPIF phenological-envelope thresholds — mango | — |
| `Table_RPIF_Thresholds_Corema_album.csv` | RPIF phenological-envelope thresholds — Corema album | — |

*Data quality and supplementary*
| File | Content | Figure/Table |
|------|---------|--------------|
| `Table2_DataQuality_Summary.csv`                     | Per-site data-quality summary (cloud / unusable %) | Table S2 |
| `Supplementary_SatelliteConsistency_OrbitalDrift.csv`| Satellite-consistency / orbital-drift supplementary table | SI |

---

## Not included (and why)

- **Raw PlanetScope imagery** (harmonised Level 3B GeoTIFFs): © Planet Labs PBC; redistribution is not permitted under the Planet End-User Licence. Available from Planet (https://www.planet.com/) under licence.
- **Per-pixel surface-reflectance master** (`Pixel_Spectral_Master_v2.parquet`) and the RPIF-filtered master: not redistributed; the aggregated `Table_*.csv` products reproduce all reported results.

## Licence

- **Code**: MIT (see `LICENSE`).
- **Derived data** (`Table_*.csv`, AOI archives): Creative Commons Attribution 4.0 (CC-BY-4.0), as archived on Zenodo.
- Raw imagery is © Planet Labs PBC and is not included.

## How to cite

> Quesada-Molina P. *superdove-pixel-purification* [dataset]. Zenodo; 2026. https://doi.org/10.5281/zenodo.21052352

## Contact

Pablo Quesada-Molina — Universidad de Málaga / QSIMOV S.L. — pabquemol@uma.es
