# Estructura esperada (relativa a la raíz del repo):
#   ./01_data/<proyecto>/AOI/                -> polígonos AOI (incluidos)
#   ./01_data/<proyecto>/images/             -> imágenes Planet (NO incluidas; bajo licencia Planet)
#   ./03_figures_&_results/<proyecto>/        -> tablas derivadas y figuras (salidas)

import os
import glob
import numpy as np
import geopandas as gpd
import rasterio
from rasterio.plot import show
from rasterio.transform import xy
from shapely.geometry import box
from shapely.ops import unary_union
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# === CONFIGURACIÓN ===
# Usa SOLO UNA imagen de referencia real (asegúrate que sea la SR, no la UDM)
# REF_IMG = r"/path/to\planet_downloader\descargas\Corema_Album\images\nubes_20_harmonized\lote_20\d8eb24ed-27ed-43ed-8be9-b6048455b6e1\PSScene\20210504_111457_45_2412_3B_AnalyticMS_SR_8b_harmonized_clip.tif" 
REF_IMG = r".\01_data\02_avocado_mango\images\nubes_20_harmonized\lote_1_new\70bc6af2-b582-42d3-98f4-0dc42b75412f\PSScene\20251217_113322_48_2518_3B_AnalyticMS_SR_8b_harmonized_clip.tif" 
# ^^^ OJO: Pon aquí la ruta a un TIF real que sepas que se ve bien.

# SHP_PATH = r"/path/to\DATA_en bruto_Corema Album\Data\AOI\veg_AOI_1.shp"
SHP_PATH = r".\01_data\02_avocado_mango\AOI\avocado_group.shp"

UMBRAL = 70.0 # Tu criterio riguroso
PIXEL_SIZE = 3 # 3 metros

def validar_mascara():
    print(f"[👁️] Inspeccionando geometría sobre: {os.path.basename(REF_IMG)}")
    
    with rasterio.open(REF_IMG) as src:
        img_data = src.read([6, 5, 3]) # False Color (NIR, Red, Green) para resaltar vegetación
        transform = src.transform
        width, height = src.width, src.height
        profile = src.profile
        
    # Normalizar imagen para visualización (clip al 98 percentil para brillo)
    img_data = img_data.astype(float)
    for i in range(3):
        p98 = np.percentile(img_data[i], 98)
        img_data[i] = np.clip(img_data[i] / p98, 0, 1)
        
    # Cargar Shapefile
    gdf = gpd.read_file(SHP_PATH)
    if gdf.crs != profile['crs']:
        gdf = gdf.to_crs(profile['crs'])
    geom_union = unary_union(gdf.geometry)

    # Crear máscara de validación
    mask_check = np.zeros((height, width), dtype=np.uint8)
    
    count = 0
    for row in range(height):
        for col in range(width):
            x_min, y_max = xy(transform, row, col, offset='ul')
            x_max, y_min = xy(transform, row, col, offset='lr')
            pixel_geom = box(x_min, y_min, x_max, y_max)
            
            if pixel_geom.intersects(geom_union):
                inter = pixel_geom.intersection(geom_union)
                pct = (inter.area / (PIXEL_SIZE**2)) * 100
                if pct >= UMBRAL:
                    mask_check[row, col] = 1
                    count += 1
                    
    print(f"[✔] Píxeles seleccionados: {count}")

    # PLOT
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 1. Imagen de fondo (Falso Color)
    show(img_data, transform=transform, ax=ax)
    
    # 2. Overlay de la máscara (Píxeles seleccionados en ROJO semitransparente)
    # Crear colormap: 0=Transparente, 1=Rojo brillante
    cmap = ListedColormap(['none', 'red'])
    show(mask_check, transform=transform, ax=ax, cmap=cmap, alpha=0.6)
    
    # 3. Overlay del vector original (Borde Cyan)
    gdf.plot(ax=ax, facecolor='none', edgecolor='cyan', linewidth=1, label='Vector Original')
    
    plt.title(f"Validación de Selección de Píxeles (Umbral {UMBRAL}%)")
    plt.tight_layout()
    plt.savefig("Validacion_Visual_Pixeles.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    validar_mascara()