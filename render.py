import json

from mimerender import FlaskMimeRender

render = FlaskMimeRender()

from flask import render_template
from mimerender import FlaskMimeRender

from config import DEBUG
from error import NotFound

# Following https://github.com/martinblech/mimerender
render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message

def render_default(f):
    return render(default='html', 
                  html=render_html, 
                  xml=render_xml,
                  json=render_json,
                  txt=render_txt)(f)

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
        default = 'html',
        html=render_html_exception,
        xml=render_xml_exception,
        json=render_json_exception,
        txt=render_txt_exception)(f)

# RESTish
def render_resource_html(data, links):
    return render_template('resource.html', data=data, links=links)

def render_resource_xml(data, links):
    return render_template('resource.xml', data=data, links=links)

def render_resource_json(data, links):
    return json.dumps({ 'data' : data, '_links' : links })
    
def render_resource(f):
    return render(default='xml', 
                  html=render_resource_html,
                  xml=render_resource_xml,
                  json=render_resource_json)(f)
