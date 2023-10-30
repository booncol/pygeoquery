"""
PyGeoQuery is a Python library for querying Firestore documents by geographic location.
"""

__version__ = "0.1.6"
__author__ = "Lukasz Majda"

from .geo_document_snapshot import GeoPointFromCallback
from .geo_collection_reference import GeoCollectionReference, QueryBuilderCallback
from .geo_async_collection_reference import GeoAsyncCollectionReference, AsyncQueryBuilderCallback

__all__ = [
    "GeoCollectionReference",
    "GeoAsyncCollectionReference",
    "QueryBuilderCallback",
    "AsyncQueryBuilderCallback",
    "GeoPointFromCallback",
]
