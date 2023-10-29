from dataclasses import dataclass
from typing import Callable, Iterable, Optional

import geohashr as ghr
from geopy.distance import geodesic as gd
from google.cloud.firestore_v1 import CollectionReference, GeoPoint, DocumentSnapshot

# Constants
DETECTION_RANGE_BUFFER = 1.02

# Type aliases
QueryBuilderCallback = Callable[[CollectionReference], CollectionReference]
GeoPointFromCallback = Callable[[dict], GeoPoint]


def _geohash_digits_from_radius(radius: float) -> int:
    """
    Returns the number of digits of the geohash that are needed to cover the given radius.
    :param radius: Radius in km
    :return: Number of digits
    """
    if radius <= 0.00477:
        return 9
    elif radius <= 0.0382:
        return 8
    elif radius <= 0.153:
        return 7
    elif radius <= 1.22:
        return 6
    elif radius <= 4.89:
        return 5
    elif radius <= 39.1:
        return 4
    elif radius <= 156:
        return 3
    elif radius <= 1250:
        return 2
    else:
        return 1


def _geohashes_in_radius(pt: GeoPoint, radius: float) -> list[str]:
    """
    Returns a list of geohashes that cover the given radius.
    :param pt: Center point
    :param radius: Radius in km
    :return: List of geohashes
    """
    geohash = ghr.encode(pt.latitude, pt.longitude, 9)
    precision_digits = _geohash_digits_from_radius(radius)
    geohash = geohash[:precision_digits]
    return [*list(ghr.neighbors(geohash).values()), geohash]


@dataclass
class GeoDocumentSnapshot:
    """
    Represents a document snapshot with a distance to a given point.
    """
    snapshot: DocumentSnapshot
    distance: float


class GeoCollectionReference:
    """
    Represents a collection reference with geospatial queries.
    """
    _ref: CollectionReference
    _end_at_character: str

    def __init__(self, ref: CollectionReference, end_at_character: str = "{"):
        """
        Creates a new GeoCollectionReference.
        :param ref: Collection reference to wrap.
        :param end_at_character: Character to append to the end of the geohash range.
        """
        self._ref = ref
        self._end_at_character = end_at_character

    def fetch_within(self, pt: GeoPoint,
                     radius: float,
                     geopoint_from: GeoPointFromCallback,
                     query_builder: Optional[QueryBuilderCallback] = None,
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
        futures = self._futures(radius, pt, query_builder)
        merged = [snapshot for values in futures for snapshot in values]
        snapshots = [self._nullable_snapshot(snap, geopoint_from, pt) for snap in merged]
        filtered = [snapshot for snapshot in snapshots if
                    not strict or snapshot.distance <= radius * DETECTION_RANGE_BUFFER]
        filtered.sort(key=lambda x: x.distance)

        return [snap.snapshot.to_dict() for snap in filtered]

    def _geo_query(self, geohash: str, query_builder: Optional[QueryBuilderCallback] = None):
        """
        Returns a query for the given geohash.
        :param geohash: Geohash to query for.
        :param query_builder: Callback to build a query (optional).
        :return: Query for the given geohash.
        """
        query = self._ref
        if query_builder:
            query = query_builder(query)

        return query.order_by("geohash").start_at([geohash]).end_at([f"{geohash}{self._end_at_character}"])

    def _futures(self, radius: float, pt: GeoPoint, query_builder: Optional[QueryBuilderCallback] = None) -> \
            list[Iterable[DocumentSnapshot]]:
        """
        Returns a list of futures for the given radius and point.
        :param radius: Radius in km
        :param pt: Center point
        :param query_builder: Callback to build a query (optional).
        :return: List of futures for the given radius and point.
        """
        geohashes = _geohashes_in_radius(pt, radius * DETECTION_RANGE_BUFFER)
        return [self._geo_query(x, query_builder).get() for x in geohashes]

    @staticmethod
    def _nullable_snapshot(snapshot: DocumentSnapshot, geopoint_from: GeoPointFromCallback,
                           pt: GeoPoint) -> Optional[GeoDocumentSnapshot]:
        """
        Returns a GeoDocumentSnapshot from the given snapshot. If the snapshot does not exist, None is returned.
        :param snapshot: Document snapshot to convert.
        :param geopoint_from: Callback to get a GeoPoint from a document
        :param pt: Center point
        :return: GeoDocumentSnapshot or None if the snapshot does not exist.
        """
        if not snapshot.exists:
            return None

        fetched_data = snapshot.to_dict()
        fetched_geopoint = geopoint_from(fetched_data)
        distance = gd((pt.latitude, pt.longitude), (fetched_geopoint.latitude, fetched_geopoint.longitude)).km

        return GeoDocumentSnapshot(
            snapshot=snapshot,
            distance=distance,
        )
