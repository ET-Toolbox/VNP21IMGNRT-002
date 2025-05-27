import os
from os.path import join, abspath, expanduser, splitext
import posixpath
import earthaccess

import VIIRS_swath_granules

from .constants import *
from .VNP21IMGNRT_granule import VNP21IMGNRTGranule

def retrieve_granule(
        remote_granule: earthaccess.results.DataGranule, 
        download_directory: str = DOWNLOAD_DIRECTORY,
        parent_directory: str = None) -> VNP21IMGNRTGranule:
    """
    Retrieve and download a VIIRS granule from a remote source.

    Args:
        remote_granule (earthaccess.results.DataGranule): The remote granule to be downloaded.
        download_directory (str): The directory where the granule will be downloaded.

    Returns:
        VNP21IMGNRTGranule: The downloaded and processed VIIRS tiled granule.
    """
    return VNP21IMGNRTGranule(VIIRS_swath_granules.retrieve_granule(
        remote_granule=remote_granule,
        download_directory=download_directory,
        parent_directory=parent_directory
    ))
