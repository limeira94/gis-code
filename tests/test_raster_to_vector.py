import os
import geopandas as gpd
import pytest

from tools.raster_to_vector import raster_to_shape_rasterio, raster_to_shape_gdal


@pytest.fixture
def sample_raster():
    return 'data/rasterteste.tif'


@pytest.fixture
def output_shapefile(tmp_path):
    return os.path.join(tmp_path, 'output.shp')


@pytest.mark.parametrize("raster_function", [raster_to_shape_rasterio, raster_to_shape_gdal])
def test_raster_to_shape_rasterio_gpd(raster_function, sample_raster, output_shapefile):
    raster_function(sample_raster, output_shapefile)
    
    output_gdf = gpd.read_file(output_shapefile)
    
    assert not output_gdf.empty
    assert output_gdf['ID'].dtype == 'int64'
