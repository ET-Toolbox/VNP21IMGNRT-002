from os.path import expanduser
import netCDF4
import numpy as np

from rasters import Raster, RasterGeolocation

from .constants import *
from .read_geometry import read_geometry

def read_layer(
        filename: str, 
        layer: str, 
        geometry: RasterGeolocation = None,
        scale = None,
        offset = None,
        fill = None,
        upper = None,
        lower = None) -> Raster:
    if geometry is None:
        geometry = read_geometry(filename)

    with netCDF4.Dataset(expanduser(filename)) as file:
        dataset = file[f"{SWATH_NAME}/Data Fields/{layer}"]
        
        if scale is None:
            scale = dataset.scale_factor

        if offset is None:
            offset = dataset.add_offset
        
        if fill is None:
            fill = dataset._FillValue

        layer = np.array(dataset) * scale + offset
        layer = np.where(layer == fill, np.nan, layer)

    if upper is not None:
        layer = np.clip(layer, None, upper)

    if lower is not None:
        layer = np.clip(layer, lower, None)

    layer = Raster(layer, geometry=geometry)

    return layer
