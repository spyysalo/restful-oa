#!/bin/bash

ROOT="http://127.0.0.1:5000"
BASE="$ROOT/annotations"
DOCS="$ROOT/documents"

# curl -X PUT -i \
#     -H 'Content-Type: application/json' \
#     -d '{'\
# '"@id": "1", '\
# '"hasBody": "http://example.org/foo",'\
# '"hasTarget": "http://example.org/doc.txt#char=0,10"'\
# '}' \
#     "$BASE/1"

curl -X GET "$DOCS/test.txt"

curl -X GET -i -H 'Accept: application/json' "$BASE/1"

curl -X GET -i -H 'Accept: application/ld+json' "$BASE/1"

curl -X GET -i -H 'Accept: application/rdf+xml' "$BASE/1"

# put example annotations
for d in examples/*; do
    for f in $d/*.jsonld; do
	python -c '
import json
doc=json.load(open("examples/craft/11532192.jsonld"))
print "\n".join([json.dumps(a) for a in doc["@graph"]])
' | while read a; do
	    # echo "INSERT: $a "
	    curl -X POST -i -H 'Content-Type: application/json' -d "$a" "$BASE/"
	done
    done
done
