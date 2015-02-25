#!/usr/bin/env python

class Store(object):
    """Abstract base for id-based storage."""
    
    def __init__(self):
        raise NotImplementedError

    def get(self, id_):
        raise NotImplementedError

    def put(self, obj):
        raise NotImplementedError

    def insert(self, obj):
        raise NotImplementedError

    def delete(self, id_):
        raise NotImplementedError

    def ids(self):
        raise NotImplementedError
