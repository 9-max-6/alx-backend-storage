#!/usr/bin/env python3
"""module: function: update_topics()
"""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of a collection's document according to the name.
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )