import geopandas as gpd
import rasterio
from rasterio.mask import mask
from osgeo import gdal, ogr


def clip_img_tiff_raterio(shp_path, tiff_path, output_path):
    shp = gpd.read_file(shp_path)
    print(shp)
    polygon = shp.geometry
    
    with rasterio.open(tiff_path) as src:
        out_img, out_transform = mask(src, polygon, crop=True)
        out_meta = src.meta
    
    out_meta.update({
        "driver": "Gtiff",
        "height": out_img.shape[1],
        "width": out_img.shape[2],
        "transform": out_transform,
        "nodata": 0
    })
    
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(out_img)


def clip_img_tiff_gdal(shp_path, tiff_path, output_path):
    """
        Used when you need to cut based on a specific field 'cutlineWhere'.
    """
    tiff = gdal.Open(tiff_path)

    opts = gdal.WarpOptions(cutlineDSName=shp_path, cropToCutline=True,
                            # cutlineWhere="Field = 'Value'",
                            dstNodata=0)

    clip_img = gdal.Warp(output_path, tiff, options=opts)
    
    clip_img = None
    tiff = None


if __name__ == '__main__':
    shp_path = "../data/area_mask.shp"
    tiff_path = "../data/rasterteste.tif"
    output_path = "../results/raster_clip4.tif"
    
    clip_img_tiff_gdal(shp_path, tiff_path,  output_path)