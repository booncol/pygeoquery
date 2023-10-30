import asyncio

from google.cloud import firestore
from google.cloud.firestore_v1 import GeoPoint

from pygeoquery import GeoAsyncCollectionReference


async def main():
    db = firestore.AsyncClient()

    collection_ref = GeoAsyncCollectionReference(db.collection("cities"))

    # Fetch documents within a radius of a GeoPoint
    center_point = GeoPoint(50.304328, 7.59378)

    # Fetch documents within a radius of 3km
    result = await collection_ref.fetch_within(
        pt=center_point,
        radius=3.0,
        geopoint_from=lambda data: data.get("coordinates"),
        strict=True
    )

    for document in result:
        print(document)

asyncio.run(main())
