#!/usr/bin/env python3
""" Inserts a document in a collection based on kwargs """


def insert_school(mongo_collection, **kwargs):
    """ Insert into a collection """
    return mongo_collection.insert_one(kwargs)
