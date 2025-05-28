from os.path import expanduser
import netCDF4
import numpy as np

from rasters import Raster, RasterGeolocation

from .constants import *
from .read_geometry import read_geometry

def read_DN(
        filename: str, 
        layer: str, 
        geometry: RasterGeolocation = None) -> Raster:
    if geometry is None:
        geometry = read_geometry(filename)

    with netCDF4.Dataset(expanduser(filename)) as file:
        dataset = file[f"{SWATH_NAME}/Data Fields/{layer}"]
        layer = np.array(dataset)

    layer = Raster(layer, geometry=geometry)

    return layer
