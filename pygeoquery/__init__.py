"""
PyGeoQuery is a Python library for querying Firestore documents by geographic location.
"""

__version__ = "0.1.4"
__author__ = "Lukasz Majda"

from typing import Callable

from google.cloud.firestore_v1 import GeoPoint
from .geo_document_snapshot import GeoDocumentSnapshot
from .geo_collection_reference import GeoCollectionReference, QueryBuilderCallback
from .geo_async_collection_reference import GeoAsyncCollectionReference, AsyncQueryBuilderCallback

GeoPointFromCallback = Callable[[dict], GeoPoint]

__all__ = [
    "GeoCollectionReference",
    "GeoAsyncCollectionReference",
    "QueryBuilderCallback",
    "AsyncQueryBuilderCallback",
    "GeoPointFromCallback",
    "GeoDocumentSnapshot",
]
