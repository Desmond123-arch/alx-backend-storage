#!/usr/bin/env python3
"""
Lists all top students soreted by average score
"""


def top_students(mongo_collection):
    """ students by average score """
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])