#!/usr/bin/env python

from store import Store
from error import NotFound

class MemStore(Store):
    """In-memory id-based storage."""
    
    def __init__(self, id_key=None):
        super(MemStore, self).__init__(id_key)
        self.obj_by_id = {}
        self._next_id = 1

    def get(self, id_):
        try:
            return self.obj_by_id[id_]
        except KeyError:
            raise NotFound

    def put(self, obj, id_=None):
        if id_ is None:
            id_ = self.obj_id(obj)
        self.obj_by_id[id_] = obj

    def insert(self, obj):
        try:
            id_ = self.obj_id(obj)
        except KeyError:
            id_ = self._assign_id(obj)
        self.put(obj, id_)

    def delete(self, id_):
        del self.obj_by_id[id_]

    def ids(self):
        return self.obj_by_id.keys()

    def _assign_id(self, obj):
        while True:
            if self._next_id not in self.obj_by_id:
                break
            self._next_id += 1
        obj[self._id_key] = self._next_id
        self._next_id += 1
        return obj[self._id_key]
