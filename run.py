#!/usr/bin/env python

# Init standard python logging:
# - With debug=True, flask prints our exceptions and returns them in the html
# - With debug=False, flask doesn't print our exceptions
# - Init logging so that flask prints our exceptions when debug=False


from app import app
import logging
logging.basicConfig(level=logging.DEBUG)
app.run(debug = False)