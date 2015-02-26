#!/usr/bin/env python

import sys

import flask

from render import render_resource, render_collection, map_exceptions
from error import NotFound
from config import DOCUMENT_PATH, DEBUG

from app import app

def get_store():
    if get_store._store is None:
        from sqlitestore import SQLiteStore
        get_store._store = SQLiteStore()
    return get_store._store
get_store._store = None

### annotation collection

@app.route('/annotations/', methods=['GET', 'POST'])
@map_exceptions
@render_collection
def annotation_collection():
    method = flask.request.method
    if method == 'GET':
        return get_annotation_collection()
    elif method == 'POST':
        return post_annotation_collection()
    else:
        assert False, 'unexpected method'

def get_annotation_collection():
    store = get_store()
    ids = store.ids()
#    return { 'data' : { 'ids': ids }, 'links' : {} }
    # TODO: get in bulk from DB
    annotations = [store.get(i) for i in ids]
    links = { i: '/annotations/%s' % str(i) for i in ids }
    for a in annotations:
        _expand_relative(a, 'http://127.0.0.1:5000/annotations/')
    return { 'data' : { '@graph' : annotations }, 'links' : links }

def post_annotation_collection():
    annotation = flask.request.get_json()
    inserted = get_store().insert(annotation)
    return { 'data' : {}, 'links': {} } # TODO

### annotation

def _is_relative(uri):
    # TODO: avoid ad-hoc impl, invoke JSON-LD expansion instead
    return not uri.startswith('http://')

def _expand_relative(obj, base):
    # TODO: avoid ad-hoc impl, invoke JSON-LD expansion instead
    if _is_relative(obj['@id']):
        obj['@id'] = base + obj['@id']

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

def get_annotation(id_, format=None):
    annotation = get_store().get(id_)
    _expand_relative(annotation, 'http://127.0.0.1:5000/annotations/')
    return { 'data' : annotation, 'links' : { 'self' : id_, } }

def put_annotation(id_):
    annotation = flask.request.get_json()
    get_store().put(annotation, id_)
    return { 'data' : annotation, 'links' : { 'self' : id_, } }

def delete_annotation(id_):
    get_store().delete(id_)
    return { 'data' : {}, 'links' : { 'self' : id_, } }

### static documents

@app.route('/documents/')
def document_collection():
    raise NotImplementedError('document listing TODO')

@app.route('/documents/<id_>')
def document(id_):
    return flask.send_from_directory(DOCUMENT_PATH, id_)

def main(argv):
    app.run(debug=DEBUG)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
