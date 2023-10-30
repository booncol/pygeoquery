"""
Provides a wrapper for a collection reference with geospatial queries (async version).
"""

import asyncio
from typing import Callable, Optional

from google.cloud.firestore_v1 import AsyncCollectionReference, GeoPoint

from pygeoquery import GeoPointFromCallback
from pygeoquery.geo_math import geohashes_in_radius
from pygeoquery.geo_query import filtered_snapshots, geo_query

# Type aliases
AsyncQueryBuilderCallback = Callable[[AsyncCollectionReference], AsyncCollectionReference]


class GeoAsyncCollectionReference:
    """
    Represents a collection reference with geospatial queries (async version).
    """
    _ref: AsyncCollectionReference

    def __init__(self, ref: AsyncCollectionReference):
        """
        Creates a new GeoCollectionReference.
        :param ref: Collection reference to wrap.
        """
        self._ref = ref

    async def fetch_within(self, pt: GeoPoint,
                           radius: float,
                           geopoint_from: GeoPointFromCallback,
                           query_builder: Optional[AsyncQueryBuilderCallback] = None,
                           strict: bool = False) -> list:
        """
        Returns all documents within the given radius of the given point.
        :param pt: Center point
        :param radius: Radius in km
        :param geopoint_from: Callback to get a GeoPoint from a document
        :param query_builder: Callback to build a query
        :param strict: If True, only documents within the given radius are returned.
        :return: List of documents within the given radius of the given point.
        """
        futures = await self._futures(radius, pt, query_builder)
        return filtered_snapshots(futures, pt, radius, geopoint_from, strict)

    async def _futures(self, radius: float, pt: GeoPoint, query_builder: Optional[AsyncQueryBuilderCallback] = None):
        """
        Returns a list of futures for the given radius and point.
        :param radius: Radius in km
        :param pt: Center point
        :param query_builder: Callback to build a query (optional).
        :return: List of futures for the given radius and point.
        """
        geohashes = geohashes_in_radius(pt, radius)
        coroutines = [geo_query(self._ref, x, query_builder).get() for x in geohashes]

        return list(await asyncio.gather(*coroutines))
