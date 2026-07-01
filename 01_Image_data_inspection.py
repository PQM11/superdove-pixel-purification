# Estructura esperada (relativa a la raíz del repo):
#   ./01_data/<proyecto>/AOI/                -> polígonos AOI (incluidos)
#   ./01_data/<proyecto>/images/             -> imágenes Planet (NO incluidas; bajo licencia Planet)
#   ./03_figures_&_results/<proyecto>/        -> tablas derivadas y figuras (salidas)

import rasterio
import glob
import os

# Ajusta esta ruta a donde tengas UNA imagen cualquiera de tus datos
# ruta_img_ejemplo = r"/path/to\planet_downloader\descargas\Corema_Album\images\nubes_20_harmonized\..." 
ruta_img_ejemplo = r".\01_data\02_avocado_mango\images\nubes_20_harmonized\..."
# (Busca un archivo .tif real dentro de tus carpetas y pega la ruta completa aquí)

# Si no quieres buscar la ruta, usa tu glob:
# search_path = r"/path/to\planet_downloader\descargas\Corema_Album\images\nubes_20_harmonized"
search_path = r".\01_data\02_avocado_mango\images\nubes_20_harmonized"
tif_files = glob.glob(os.path.join(search_path, "**", "*_clip.tif"), recursive=True)

if tif_files:
    with rasterio.open(tif_files[0]) as src:
        print(f"--- INSPECCIÓN DE IMAGEN: {os.path.basename(tif_files[0])} ---")
        print(f"Cantidad de Bandas: {src.count}")
        print(f"Driver: {src.driver}")
        print(f"Dimensiones: {src.width} x {src.height}")
        print(f"CRS: {src.crs}")
        print(f"Nodata value: {src.nodata}")
        print(f"Descriptions: {src.descriptions}") # A veces dice el nombre de la banda
else:
    print("No encontré imágenes para inspeccionar.")