from rasters import RasterGeolocation

from .read_latitude import read_latitude
from .read_longitude import read_longitude

def read_geometry(filename: str) -> RasterGeolocation:
    """
    Reads the geometry (latitude and longitude) from a VNP21IMG-NRT product NetCDF file.

    Parameters:
        filename (str): Path to the NetCDF file containing the VNP21IMG-NRT product.

    Returns:
        RasterGeometry: A RasterGeometry object containing latitude and longitude data.
    """
    latitude = read_latitude(filename)
    longitude = read_longitude(filename)

    # Create a RasterGeolocation object with the latitude and longitude data
    geometry = RasterGeolocation(x=longitude, y=latitude)

    return geometry