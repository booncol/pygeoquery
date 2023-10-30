from typing import Iterable

from google.cloud.firestore_v1 import GeoPoint

from pygeoquery import GeoPointFromCallback, GeoDocumentSnapshot
from pygeoquery.geo_math import DETECTION_RANGE_BUFFER


def geo_query(collection_ref, geohash, query_builder):
    """
    Returns a query for the given geohash.
    :param collection_ref: Collection reference to query.
    :param geohash: Geohash to query for.
    :param query_builder: Callback to build a query (optional).
    :return: Query for the given geohash.
    """
    if query_builder:
        collection_ref = query_builder(collection_ref)

    return collection_ref.order_by("geohash").start_at([geohash]).end_at([f"{geohash}\uf8ff"])


def filtered_snapshots(futures: list[Iterable],
                       center: GeoPoint,
                       radius: float,
                       geopoint_from: GeoPointFromCallback,
                       strict: bool) -> list:
    """
    Returns a list of snapshots from the given futures.
    :param futures: List of futures to get snapshots from.
    :param center: Center point.
    :param radius: Radius in km.
    :param geopoint_from: Callback to get a GeoPoint from a document.
    :param strict: If True, only documents within the given radius are returned.
    :return: List of snapshots from the given futures.
    """
    merged = [snapshot for values in futures for snapshot in values]
    snapshots = [GeoDocumentSnapshot.nullable(snap, geopoint_from, center) for snap in merged]
    filtered = [snapshot for snapshot in snapshots if
                not strict or snapshot.distance <= radius * DETECTION_RANGE_BUFFER]
    filtered.sort(key=lambda x: x.distance)

    return [snap.snapshot.to_dict() for snap in filtered]
