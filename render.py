import json

from mimerender import FlaskMimeRender, register_mime, MimeRenderException

render = FlaskMimeRender()
try:
    register_mime('jsonld', ('application/ld+json', ))
except MimeRenderException:
    # assume already registered
    pass

from flask import render_template
from mimerender import FlaskMimeRender

from config import DEBUG
from error import NotFound

# Following http://stackoverflow.com/q/13480675
render_xml_exception = lambda exception: '<exception>%s</exception>'%exception
render_json_exception = lambda exception: json.dumps({ 'exception' : '; '.join(exception.args)})
render_html_exception = lambda exception: '<html><body>%s</body></html>'%exception
render_txt_exception = lambda exception: exception

def map_exceptions(f):
    mapping = [(NotFound, '404 Not Found')]  # always mapped
    if not DEBUG:
        # only mapped when w/o Werkzeug
        mapping.append([
                (ValueError, '500 Internal Server Error'),
                (NameError, '500 Internal Server Error'),
                ])
    return render.map_exceptions(
        mapping=mapping,
        default = 'json',
        html=render_html_exception,
        xml=render_xml_exception,
        json=render_json_exception,
        txt=render_txt_exception)(f)

### render individual resource

def render_resource_html(data, links):
    return render_template('resource.html', data=data, links=links)

def render_resource_xml(data, links):
    return render_template('resource.xml', data=data, links=links)

def render_resource_json(data, links):
    return json.dumps({ 'data' : data, '_links' : links }, sort_keys=True, indent=2, separators=(',', ': '))+'\n'

def render_resource_jsonld(data, links):
    # Assume Open Annotation, fill in recommended JSON-LD context
    # (see http://www.openannotation.org/spec/core/publishing.html)
    data = data.copy()
    if '@context' not in data:
        data['@context'] =  'http://www.w3.org/ns/oa-context-20130208.json'
    return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))+'\n'
    
def render_resource_rdf(data, links):
    import oajson
    rdf = oajson.to_rdf(data, base='http://127.0.0.1:5000/')
    return rdf

### render collection resource

def render_collection_html(data, links):
    if isinstance(data, dict) and '@graph' in data:
        data = data['@graph']
    if not(isinstance(data, list)):
        data = [data]
    return render_template('collection.html', data=data, links=links)

### decorators

def render_resource(f):
    return render(default='jsonld',
                  html=render_resource_html,
                  xml=render_resource_xml,
                  json=render_resource_json,
                  jsonld=render_resource_jsonld,
                  rdf=render_resource_rdf,
                  override_input_key = 'format')(f)

def render_collection(f):
    return render(default='json',
                  html=render_collection_html,
                  xml=render_resource_xml,
                  json=render_resource_json,
                  jsonld=render_resource_jsonld,
                  rdf=render_resource_rdf)(f)
