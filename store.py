#!/usr/bin/env python

DEFAULT_ID_KEY='@id'

class Store(object):
    """Abstract base for id-based storage."""
    
    def __init__(self, id_key=None):
        if id_key is None:
            id_key = DEFAULT_ID_KEY
        self._id_key = id_key

    def obj_id(self, obj):
        return obj[self._id_key]

    def get(self, id_):
        raise NotImplementedError

    def put(self, obj, id_=None):
        raise NotImplementedError

    def insert(self, obj):
        raise NotImplementedError

    def delete(self, id_):
        raise NotImplementedError

    def ids(self):
        raise NotImplementedError
