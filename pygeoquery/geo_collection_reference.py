"""
Provides a wrapper for a collection reference with geospatial queries.
"""

from typing import Callable, Iterable, Optional

from google.cloud.firestore_v1 import CollectionReference, GeoPoint, DocumentSnapshot

from pygeoquery.geo_document_snapshot import GeoPointFromCallback
from pygeoquery.geo_math import geohashes_in_radius
from pygeoquery.geo_query import filtered_snapshots, geo_query

# Type aliases
QueryBuilderCallback = Callable[[CollectionReference], CollectionReference]


class GeoCollectionReference:
    """
    Represents a collection reference with geospatial queries.
    """
    _ref: CollectionReference

    def __init__(self, ref: CollectionReference):
        """
        Creates a new GeoCollectionReference.
        :param ref: Collection reference to wrap.
        """
        self._ref = ref

    def fetch_within(self,
                     center: GeoPoint,
                     radius: float,
                     geopoint_from: GeoPointFromCallback,
                     query_builder: Optional[QueryBuilderCallback] = None,
                     strict: bool = False) -> list:
        """
        Returns all documents within the given radius of the given point.
        :param center: Center point
        :param radius: Radius in km
        :param geopoint_from: Callback to get a GeoPoint from a document
        :param query_builder: Callback to build a query
        :param strict: If True, only documents within the given radius are returned.
        :return: List of documents within the given radius of the given point.
        """
        futures = self._futures(radius, center, query_builder)
        return filtered_snapshots(futures, center, radius, geopoint_from, strict)

    def _futures(self, radius: float, pt: GeoPoint, query_builder: Optional[QueryBuilderCallback] = None) -> \
            list[Iterable[DocumentSnapshot]]:
        """
        Returns a list of futures for the given radius and point.
        :param radius: Radius in km
        :param pt: Center point
        :param query_builder: Callback to build a query (optional).
        :return: List of futures for the given radius and point.
        """
        geohashes = geohashes_in_radius(pt, radius)
        return [geo_query(self._ref, x, query_builder).get() for x in geohashes]
