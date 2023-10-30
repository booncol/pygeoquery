import geohashr as ghr
from google.cloud.firestore_v1 import GeoPoint

# Buffer for the detection range. This is needed because the geohash algorithm is not exact.
DETECTION_RANGE_BUFFER = 1.02


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


def geohashes_in_radius(center: GeoPoint, radius: float) -> list[str]:
    """
    Returns a list of geohashes that cover the given radius.
    :param center: Center point
    :param radius: Radius in km
    :return: List of geohashes
    """
    geohash = ghr.encode(center.latitude, center.longitude, 9)
    precision_digits = _geohash_digits_from_radius(radius * DETECTION_RANGE_BUFFER)
    geohash = geohash[:precision_digits]
    return [*list(ghr.neighbors(geohash).values()), geohash]
