#!/usr/bin/env python

import sys

import flask

from render import render_resource, map_exceptions
from error import NotFound
from config import DEBUG

from app import app

def get_store():
    if get_store._store is None:
        from memstore import MemStore
        get_store._store = MemStore()
    return get_store._store
get_store._store = None

### annotation collection

@app.route('/annotations/', methods=['GET', 'POST'])
@map_exceptions
@render_resource
def annotation_collection():
    method = flask.request.method
    if method == 'GET':
        return get_annotation_collection()
    elif method == 'POST':
        raise NotImplementedError
    else:
        assert False, 'unexpected method'

def get_annotation_collection():
    ids = get_store().ids()
    return { 'data' : { 'ids': ids }, 'links' : {} }

### annotation

@app.route('/annotations/<id_>', methods=['GET', 'PUT', 'DELETE'])
@map_exceptions
@render_resource
def annotation(id_):
    method = flask.request.method
    if method == 'GET':
        return get_annotation(id_)
    elif method == 'PUT':
        return put_annotation(id_)
    elif method == 'DELETE':
        return delete_annotation(id_)
    else:
        assert False, 'unexpected method'

def get_annotation(id_):
    annotation = get_store().get(id_)
    return { 'data' : annotation, 'links' : { 'self' : id_, } }

def put_annotation(id_):
    annotation = flask.request.get_json()
    get_store().put(annotation, id_)
    return { 'data' : annotation, 'links' : { 'self' : id_, } }

def delete_annotation(id_):
    get_store().delete(id_)
    return { 'data' : {}, 'links' : { 'self' : id_, } }

def main(argv):
    app.run(debug=DEBUG)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
