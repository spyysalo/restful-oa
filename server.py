#!/usr/bin/env python

import sys

import flask

app = flask.Flask(__name__)

def get_store():
    if get_store._store is None:
        from memstore import MemStore
        get_store._store = MemStore()
    return get_store._store
get_store._store = None

### annotation collection

@app.route('/annotations/', methods=['GET', 'POST'])
def annotation_collection():
    method = flask.request.method
    if method == 'GET':
        return get_annotation_collection()
    elif method == 'POST':
        raise NotImplementedError
    else:
        assert False, 'unexpected method'

def render_ids_html(ids):
    return str(ids)

def get_annotation_collection():
    return render_ids_html(get_store().ids())

### annotation

@app.route('/annotations/<id_>', methods=['GET', 'PUT', 'DELETE'])
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

def render_annotation_html(annotation):
    return str(annotation)

def get_annotation(id_):
    return render_annotation_html(get_store().get(id_))

def put_annotation(id_):
    annotation = flask.request.get_json()
    get_store().put(annotation, id_)
    return 'OK'

def delete_annotation(id_):
    get_store().delete(id_)
    return 'OK'

def main(argv):
    app.run(debug=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
