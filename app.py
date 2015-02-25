#!/usr/bin/env python

import flask

from config import TEMPLATE_PATH, STATIC_PATH, TRIM_BLOCKS

app = flask.Flask(__name__, 
                  template_folder=TEMPLATE_PATH,
                  static_folder=STATIC_PATH)

app.jinja_env.trim_blocks = TRIM_BLOCKS
