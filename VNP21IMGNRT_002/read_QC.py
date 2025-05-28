from os.path import expanduser
import warnings
import numpy as np
import netCDF4
from rasters import Raster, RasterGeometry, RasterGeolocation
import h5py
import logging
import colored_logging as cl

from .constants import *
from .read_geometry import read_geometry

logger = logging.getLogger(__name__)    

def read_QC(filename: str, geometry: RasterGeolocation = None) -> np.ndarray:
    """
    Reads the Quality Control (QC) flag layer from a VNP21IMG-NRT product file.

    Parameters
    ----------
    filename : str
        Path to the VNP21IMG-NRT product file (NetCDF format).
    geometry : RasterGeolocation, optional
        Geolocation information for the raster. If not provided, it will be read from the file.

    Returns
    -------
    QC : Raster
        A Raster object containing the QC flag layer data and associated geolocation.

    Notes
    -----
    The QC flag layer is typically used to assess the quality of the science data in the product.
    This function suppresses warnings that may arise during data reading.
    """
    if geometry is None:
        # If no geometry is provided, read it from the file
        geometry = read_geometry(filename)

    # Open the NetCDF file and read the QC flag layer
    with netCDF4.Dataset(expanduser(filename)) as file:
        dataset = file[f"{SWATH_NAME}/Data Fields/QC"]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            QC = np.array(dataset).astype(np.uint16)

    # Wrap the QC data in a Raster object with geolocation
    QC = Raster(QC, geometry=geometry)
        
    return QC