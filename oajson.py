#!/usr/bin/env python

"""Open Annotation JSON-LD support.

This is primarily a thin wrapper around PyLD and the Open Annotation
recommended context.

See:

* http://www.openannotation.org/
* http://json-ld.org/
* https://github.com/digitalbazaar/pyld
* http://www.openannotation.org/spec/core/publishing.html#Serialization
"""

from pyld import jsonld

# Context description that is recommended for use in systems that
# implement the Open Annotation data model, copied Jan 2015 from
# http://www.openannotation.org/spec/core/publishing.html

oa_recommended_context = {
  "@context": {
    "oa": "http://www.w3.org/ns/oa#",
    "cnt": "http://www.w3.org/2011/content#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "dctypes": "http://purl.org/dc/dcmitype/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "prov": "http://www.w3.org/ns/prov#",
    "trig": "http://www.w3.org/2004/03/trix/rdfg-1/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",

    "hasBody" :         {"@type":"@id", "@id" : "oa:hasBody"},
    "hasTarget" :       {"@type":"@id", "@id" : "oa:hasTarget"},
    "hasSource" :       {"@type":"@id", "@id" : "oa:hasSource"},
    "hasSelector" :     {"@type":"@id", "@id" : "oa:hasSelector"},
    "hasState" :        {"@type":"@id", "@id" : "oa:hasState"},
    "hasScope" :        {"@type":"@id", "@id" : "oa:hasScope"},
    "annotatedBy" :  {"@type":"@id", "@id" : "oa:annotatedBy"},
    "serializedBy" : {"@type":"@id", "@id" : "oa:serializedBy"},
    "motivatedBy" :  {"@type":"@id", "@id" : "oa:motivatedBy"},
    "equivalentTo" : {"@type":"@id", "@id" : "oa:equivalentTo"},
    "styledBy" :     {"@type":"@id", "@id" : "oa:styledBy"},
    "cachedSource" : {"@type":"@id", "@id" : "oa:cachedSource"},
    "conformsTo" :   {"@type":"@id", "@id" : "dcterms:conformsTo"},
    "default" :      {"@type":"@id", "@id" : "oa:default"},
    "item" :         {"@type":"@id", "@id" : "oa:item"},
    "first":         {"@type":"@id", "@id" : "rdf:first"},
    "rest":          {"@type":"@id", "@id" : "rdf:rest", "@container" : "@list"},

    "annotatedAt" :  { "@type": "xsd:dateTimeStamp", "@id": "oa:annotatedAt" },
    "end" :          { "@type": "xsd:nonNegativeInteger", "@id": "oa:end" },
    "exact" :        "oa:exact",
    "prefix" :       "oa:prefix",
    "serializedAt" : { "@type": "xsd:dateTimeStamp", "@id": "oa:serializedAt" },
    "start" :        { "@type": "xsd:nonNegativeInteger", "@id": "oa:start" },
    "styleClass" :   "oa:styleClass",
    "suffix" :       "oa:suffix",
    "when" :         { "@type": "xsd:dateTimeStamp", "@id": "oa:when" },

    "chars" :        "cnt:chars",
    "bytes" :        "cnt:bytes",
    "format" :       "dc:format",
    "language" :     "dc:language",
    "value" :        "rdf:value",
    "label" :        "rdfs:label",
    "name" :         "foaf:name",
    "mbox" :         "foaf:mbox"

  }
}

class ValidationError(Exception):
    pass

def default_context():
    return oa_recommended_context

def default_base():
    return None

def _make_options(context, base):
    """Return pyld options for given context and base."""
    options = {}
    if context is None:
        context = default_context()
    options['expandContext'] = context
    if base is not None:
        options['base'] = base
    return options

def expand(document, context=None, base=None):
    """Expand OA JSON-LD, removing context."""
    # See http://www.w3.org/TR/json-ld-api/#expansion
    return jsonld.expand(document, _make_options(context, base))

def compact(document, context=None, base=None, remove_context=False):
    """Compact OA JSON-LD, shortening forms according to context."""

    # See http://www.w3.org/TR/json-ld-api/#compaction

    if context is None:
        context = default_context()
    if base is None:
        base = default_base()

    options = {}
    if base is not None:
        options['base'] = base

    compacted = jsonld.compact(document, context, options)

    if remove_context:
        try:
            del compacted['@context']
        except KeyError:
            pass

    return compacted

def flatten(document):
    """Flatten OA JSON-LD."""

    # See http://www.w3.org/TR/json-ld-api/#flattening

    return jsonld.flatten(document)

def to_rdf(document, context=None, base=None):
    """Deserialize OA JSON-LD to RDF, return N-Quads as string."""

    # From http://www.w3.org/TR/json-ld/#h3_serializing-deserializing-rdf:
    # 
    #     The procedure to deserialize a JSON-LD document to RDF
    #     involves the following steps:
    #
    #     1. Expand the JSON-LD document, removing any context; this
    #     ensures that properties, types, and values are given their
    #     full representation as IRIs and expanded values. [...]
    # 
    #     2. Flatten the document, which turns the document into an
    #     array of node objects. [...]
    #
    #     3. Turn each node object into a series of RDF triples.
    #
    # See also: http://www.w3.org/TR/2014/REC-json-ld-api-20140116/#rdf-serialization-deserialization-algorithms

    if context is None:
        context = default_context()
    if base is None:
        base = default_base()

    expanded = expand(document, context, base)
    print 'baz', expanded
    flattened = flatten(expanded)
    print 'quux', flattened
    return jsonld.to_rdf(expanded, {'format': 'application/nquads'})

def from_rdf(rdf, context=None, base=None, remove_context=False):
    """Serialize RDF as OA JSON-LD, return compacted JSON-LD."""

    # From http://www.w3.org/TR/json-ld/#h3_serializing-deserializing-rdf:
    #
    #    Deserializing [expanded and flattened JSON-LD] to RDF now is
    #    a straightforward process of turning each node object into
    #    one or more RDF triples. [...] The process of serializing RDF
    #    as JSON-LD can be thought of as the inverse of this last
    #    step, creating an expanded JSON-LD document closely matching
    #    the triples from RDF, using a single node object for all
    #    triples having a common subject, and a single property for
    #    those triples also having a common predicate.
    #
    # See also: http://www.w3.org/TR/2014/REC-json-ld-api-20140116/#rdf-serialization-deserialization-algorithms

    if context is None:
        context = default_context()
    if base is None:
        base = default_base()

    document = jsonld.from_rdf(rdf, {'format': 'application/nquads'})
    return compact(document, context, base, remove_context)
