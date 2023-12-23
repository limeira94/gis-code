from osgeo import gdal, ogr, osr
import rasterio
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape




def raster_to_shape_gdal(raster_file, vector_file):
    raster = gdal.Open(raster_file)
    band = raster.GetRasterBand(1)
    
    proj = raster.GetProjection()    
    shp_proj = osr.SpatialReference()
    shp_proj.ImportFromWkt(proj)
    
    call_drive =  ogr.GetDriverByName('ESRI Shapefile')
    create_shp = call_drive.CreateDataSource(vector_file)
    shp_layer = create_shp.CreateLayer('layername', srs = shp_proj)
    
    new_field = ogr.FieldDefn(str('ID'), ogr.OFTInteger)
    shp_layer.CreateField(new_field)
    
    gdal.Polygonize(band, None, shp_layer, 0, [], callback=None)
    
    create_shp.Destroy()
    raster = None
        
        
def raster_to_shape_rasterio(raster_file, vector_file):

    with rasterio.open(raster_file) as src:
        image = src.read(1)
        transform = src.transform
        results = shapes(image, transform=transform)
        
        geoms = []
        for geom, value in results:
            geoms.append({
                'geometry': shape(geom),
                'properties': {'ID': int(value)}
            })
        gdf = gpd.GeoDataFrame.from_features(geoms, crs=src.crs)  
        
    gdf.to_file(vector_file)

        
        
def main():    
    raster_file = 'data/rasterteste.tif'
    vector_file = 'results/rasterteste2.shp'
    raster_to_shape_rasterio(raster_file, vector_file)


if __name__ == '__main__':
    main()    
