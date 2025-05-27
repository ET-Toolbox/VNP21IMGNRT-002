from typing import Union, List
from datetime import datetime, date
from dateutil import parser
import logging

import earthaccess

import colored_logging as cl
from rasters import Point, Polygon, RasterGeometry
from modland import generate_modland_grid

import VIIRS_swath_granules

from .constants import *

__author__ = "Gregory H. Halverson, Evan Davis"

logger = logging.getLogger(__name__)

def search_granules(
        date_UTC: Union[date, str] = None,
        start_date_UTC: Union[date, str] = None,
        end_date_UTC: Union[date, str] = None,
        geometry: Union[Point, Polygon, RasterGeometry] = None,
        tile: str = None,
        tile_size: int = None) -> List[earthaccess.search.DataGranule]:
    """
    Search for VIIRS granules within a specified date range and target geometry.

    Args:
        concept_ID (str): The concept ID for the granules.
        date_UTC (Union[date, str], optional): The specific date for the search.
        start_date_UTC (Union[date, str], optional): The start date for the search range.
        end_date_UTC (Union[date, str], optional): The end date for the search range.
        target_geometry (Union[Point, Polygon, RasterGeometry], optional): The target geometry for the search.
        tile (str, optional): The tile identifier for the granules.

    Returns:
        List[earthaccess.search.DataGranule]: A list of found granules.
    """
    return VIIRS_swath_granules.search_granules(
        concept_ID=VNP21IMGNRT_002_CONCEPT_ID,
        date_UTC=date_UTC,
        start_date_UTC=start_date_UTC,
        end_date_UTC=end_date_UTC,
        geometry=geometry,
        tile=tile,
        tile_size=tile_size
    )
