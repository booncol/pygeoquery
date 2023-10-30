# pygeoquery

[![PyPI package](https://img.shields.io/badge/pip%20install-pygeoquery-brightgreen)](https://pypi.org/project/pygeoquery/)
[![Version](https://img.shields.io/pypi/v/pygeoquery)](https://pypi.org/project/pygeoquery/)
[![License](https://img.shields.io/github/license/booncol/pygeoquery)](https://github.com/booncol/pygeoquery/blob/main/LICENSE)

Perform geospatial queries on a Firestore database with ease.

pygeoquery allows you to retrieve documents within a certain radius of a given geographic point. It utilizes geohashes for efficient querying.

## Features
- query Firestore collections by geographic proximity.
- efficiently filter and retrieve documents within a specified radius.
- flexible and customizable query building.
- utilizes geohashes for high-performance geospatial queries.
- supports both synchronous and asynchronous Firestore clients.

## Installation
You can install the library using pip:

```bash
pip install pygeoquery
```

## Prerequisites

Before using this library, ensure that each document in the searched Firestore collection includes a field called **"geohash"** containing a geohash value generated from the geographical coordinates. This geohash field is essential for the library to perform accurate geospatial queries.

![Document preview](https://github.com/booncol/pygeoquery/blob/main/document_preview.png?raw=true)  

To generate geohashes, you can use Python libraries such as:

- [pygeohash](https://pypi.org/project/pygeohash/): Provides functions for decoding and encoding geohashes.
- [geohashr](https://pypi.org/project/geohashr/): Just another Python geohashing library.


## Usage

1) Initialize Firebase

    ```python
    from firebase_admin import initialize_app, credentials
    from google.cloud import firestore
    
    
    # Initialize Firebase
    cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
    initialize_app(cred, {"projectId": "your-project-id"})
    ```

2) Create Firestore client

    ```python
   # Synchronous client
    db = firestore.Client()
    ```
    or    

    ```python
   # Asynchronous client
    db = firestore.AsyncClient()
    ```

3) Define callback functions

    ```python
    # Define a GeoPointFromCallback
    def geopoint_from_callback(data):
        return data.get("location")  # Replace with your data structure
    
    # Define query builder callback function (optional). This function allows you to customize your query.
    def query_builder_callback(query):
        return query.where("property", "==", "value")  # Customize your query
    ```

4) Create a GeoCollectionReference or GeoAsyncCollectionReference

    ```python
    # Create a GeoCollectionReference
    geocollection = GeoCollectionReference(db.collection("your_collection"))
   ```
   
    or

    ```python
    # Create a GeoAsyncCollectionReference (asynchronous client only)
    geocollection = GeoAsyncCollectionReference(db.collection("your_collection"))
   ```

5) Fetch documents within a radius of a GeoPoint

    ```python
    # Fetch documents within a radius of a GeoPoint
    center_point = GeoPoint(latitude, longitude)
    radius_km = 10.0
    
    result = geocollection.fetch_within(
        center_point,
        radius_km,
        geopoint_from_callback,
        query_builder_callback
    )
    
    # Process the retrieved documents
    for document in result:
        print(document)
    ```

    If you are using the asynchronous client, use the `await` keyword to wait for the result.

    ```python
    result = await geocollection.fetch_within(
        center_point,
        radius_km,
        geopoint_from_callback,
        query_builder_callback
    )
    ```   

## Acknowledgments
This project is inspired by the [geoflutterfire_plus](https://github.com/KosukeSaigusa/geoflutterfire_plus) Flutter module by [Kosuke Saigusa](https://github.com/kosukesaigusa), which provides similar geospatial querying functionality for Firestore databases in the Flutter framework.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/booncol/pygeoquery/blob/main/LICENSE) file for details.

## Contributing
Please read [CONTRIBUTING.md](https://github.com/booncol/pygeoquery/blob/main/CONTRIBUTING.md) for details on my code of conduct, and the process for submitting pull requests to me.

## Contact
If you have questions or need assistance, feel free to contact me.

**Happy querying!**