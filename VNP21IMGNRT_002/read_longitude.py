import warnings
from os.path import expanduser
import numpy as np
import netCDF4
import rasters as rt

from .constants import *

def read_longitude(filename: str) -> np.ndarray:
    """
    Reads the longitude array from a VNP21IMG-NRT product NetCDF file.

    Parameters:
        filename (str): Path to the NetCDF file containing the VNP21IMG-NRT product.

    Returns:
        np.ndarray: 2D array of longitude values, with fill values replaced by np.nan.

    Notes:
        - The function accesses the 'VIIRS_I5_LST/Geolocation Fields/Longitude' dataset.
        - Fill values in the dataset are replaced with np.nan for easier downstream processing.
        - Warnings from the netCDF4 library are suppressed during array extraction.
    """
    # Open the NetCDF file, expanding user (~) in the path if present
    with netCDF4.Dataset(expanduser(filename)) as file:
        # Access the longitude dataset within the file
        dataset = file[f"{SWATH_NAME}/Geolocation Fields/Longitude"]
        fill_value = dataset._FillValue

        # Suppress warnings that may arise from reading the dataset
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            array = np.array(dataset)
            
        # Replace fill values with np.nan for easier handling of missing data
        array = np.where(array == fill_value, np.nan, array)
        
        return array