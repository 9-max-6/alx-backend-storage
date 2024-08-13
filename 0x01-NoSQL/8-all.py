#!/usr/bin/env python3
"""
module: function: list_all()
"""


def list_all(mongo_collection):
    """"returns all the documents in a collection.
    """
    return [docx for docx in mongo_collection.find()]
