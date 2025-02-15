#!/usr/bin/env python3
""" Inserts a document in a collection based on kwargs """


def insert_school(mongo_collection, **kwargs):
    """ Insert into a collection """
    result  = mongo_collection.insert_one(kwargs)
    return result.inserted_id