#!/usr/bin/env python3
"""module: function insert_school()
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in an existing collection.
    """
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
