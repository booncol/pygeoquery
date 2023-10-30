from dataclasses import dataclass

from geopy.distance import geodesic as gd
from google.cloud.firestore_v1 import DocumentSnapshot, GeoPoint

from pygeoquery import GeoPointFromCallback


@dataclass(frozen=True)
class GeoDocumentSnapshot:
    """
    Represents a document snapshot with a distance to a given point.
    """
    snapshot: DocumentSnapshot
    distance: float

    @classmethod
    def nullable(cls, snapshot: DocumentSnapshot, geopoint_from: GeoPointFromCallback, center: GeoPoint):
        """
        Returns a GeoDocumentSnapshot from the given snapshot. If the snapshot does not exist, None is returned.
        :param snapshot: Document snapshot to convert.
        :param geopoint_from: Callback to get a GeoPoint from a document
        :param center: Center point
        :return: GeoDocumentSnapshot or None if the snapshot does not exist.
        """
        if not snapshot.exists:
            return None

        data = snapshot.to_dict()
        geopoint = geopoint_from(data)
        distance = gd((center.latitude, center.longitude), (geopoint.latitude, geopoint.longitude)).km

        return GeoDocumentSnapshot(snapshot=snapshot, distance=distance)
