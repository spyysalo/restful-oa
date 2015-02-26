#!/bin/bash

ROOT="http://127.0.0.1:5000"
BASE="$ROOT/annotations"
DOCS="$ROOT/documents"

curl -X PUT -i \
    -H 'Content-Type: application/json' \
    -d '{'\
'"@id": "1", '\
'"hasBody": "http://example.org/foo",'\
'"hasTarget": "http://example.org/doc.txt#char=0,10"'\
'}' \
    "$BASE/1"

curl -X GET "$DOCS/test.txt"

curl -X GET -i -H 'Accept: application/json' "$BASE/1"

curl -X GET -i -H 'Accept: application/ld+json' "$BASE/1"

curl -X GET -i -H 'Accept: application/rdf+xml' "$BASE/1"
