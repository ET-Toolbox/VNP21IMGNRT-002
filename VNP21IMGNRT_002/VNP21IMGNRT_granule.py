from typing import Union, List
from os.path import expanduser
import numpy as np

import netCDF4

import rasters as rt
from rasters import Raster, RasterGeometry, RasterGeolocation

from VIIRS_swath_granules import VIIRSSwathGranule

from .constants import SWATH_NAME
from .read_latitude import read_latitude
from .read_longitude import read_longitude
from .read_geometry import read_geometry
from .read_QC import read_QC
from .read_DN import read_DN
from .read_layer import read_layer

class VNP21IMGNRTGranule(VIIRSSwathGranule):
    def __init__(self, filename: Union[str, VIIRSSwathGranule]):
        """
        Initialize the VNP21IMGNRTGranule object.

        :param filename: Path to the VIIRS granule file.
        """
        if isinstance(filename, VIIRSSwathGranule):
            filename = filename.filename
        elif isinstance(filename, str):
            filename = filename
        else:
            raise TypeError("filename must be a string or VIIRSSwathGranule object")
        
        super().__init__(filename)

        self._geometry = None
        self._QC = None

    @property
    def geometry(self) -> RasterGeolocation:
        """
        Return the geometry of the granule, which includes latitude and longitude.
        """
        if self._geometry is None:
            self._geometry = read_geometry(self.filename_absolute)

        return self._geometry
    
    @property
    def latitude(self) -> np.ndarray:
        """
        Return the latitude array of the granule.
        """
        if self._geometry is not None:
            return self._geometry.y
        else:
            return read_latitude(self.filename_absolute)

    lat = latitude

    @property
    def longitude(self) -> np.ndarray:
        """
        Return the longitude array of the granule.
        """
        if self._geometry is not None:
            return self._geometry.x
        else:
            return read_longitude(self.filename_absolute)

    lon = longitude

    @property
    def QC(self) -> Raster:
        """
        Return the Quality Control (QC) data as a Raster object.
        """
        if self._QC is None:
            self._QC = read_QC(self.filename_absolute, geometry=self.geometry)
        
        return self._QC
    
    @property
    def cloud(self) -> Raster:
        """
        Return the cloud mask as a Raster object.
        """
        return Raster(((np.array(self.QC) >> 4) & 3) > 0, geometry=self.geometry)
    
    @property
    def variables(self) -> List[str]:
        """
        Return the list of variables in a specific swath.

        :param swath: The swath name.
        """
        return super().variables(swath=SWATH_NAME)

    def DN(self, variable: str) -> Raster:
        """
        Read a specific variable as Digital Number (DN) from the granule.

        :param variable: The name of the variable to read.
        :return: A Raster object containing the DN data for the specified variable.
        """
        if variable not in self.variables:
            raise ValueError(f"Variable '{variable}' not found in granule {self.filename}")

        DN = read_DN(filename=self.filename_absolute, layer=variable, geometry=self.geometry)
        
        return DN
    
    def scale(self, variable: str):
        with netCDF4.Dataset(self.filename_absolute) as file:
            return file[f"{SWATH_NAME}/Data Fields/{variable}"].scale_factor

    def offset(self, variable: str):
        with netCDF4.Dataset(self.filename_absolute) as file:
            return file[f"{SWATH_NAME}/Data Fields/{variable}"].add_offset
        
    def fill(self, variable: str):
        with netCDF4.Dataset(self.filename_absolute) as file:
            return file[f"{SWATH_NAME}/Data Fields/{variable}"]._FillValue

    def read(
            self, 
            variable: str, 
            apply_cloud: bool = False,
            scale = None,
            offset = None,
            fill = None,
            upper = None,
            lower = None) -> Raster:
        """
        Read a specific variable from the granule.

        :param variable: The name of the variable to read.
        :return: A Raster object containing the data for the specified variable.
        """
        if variable not in self.variables:
            raise ValueError(f"Variable '{variable}' not found in granule {self.filename}")

        layer = read_layer(
            filename=self.filename_absolute, 
            layer=variable, 
            geometry=self.geometry,
            scale=scale,
            offset=offset,
            fill=fill,
            upper=upper,
            lower=lower
        )

        if apply_cloud:
            layer = rt.where(self.cloud, np.nan, layer)
        
        return layer
    
    @property
    def LST(self) -> Raster:
        """
        Return the Land Surface Temperature (LST) data as a Raster object.
        """
        return self.read("LST", scale=1, offset=0)

    ST_K = LST

    @property
    def ST_C(self) -> Raster:
        """
        Return the Land Surface Temperature in Celsius as a Raster object.
        """
        return self.read("LST", scale=1, offset=-273.15)

    @property
    def LST_err(self) -> Raster:
        """
        Return the Land Surface Temperature error data as a Raster object.
        """
        return self.read("LST_err", scale=1, offset=0)

    @property
    def Emis_I5(self) -> Raster:
        """
        Return the emissivity in band I5 as a Raster object.
        """
        return self.read("Emis_I5", scale=1, offset=0, upper=1)
    
    @property
    def Emis_I5_err(self) -> Raster:
        """
        Return the emissivity error in band I5 as a Raster object.
        """
        return self.read("Emis_I5_err", scale=1, offset=0)
    
    @property
    def View_angle(self) -> Raster:
        """
        Return the view angle data as a Raster object.
        """
        return self.read("View_angle", scale=1, offset=0)
