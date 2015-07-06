<<<<<<< HEAD
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("opened init")

from flask import Flask


logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

logging.debug("doing something")

from app import views

logging.debug("Opened app!")

>>>>>>> 22be319d053eab3e4a616a27ccd848e32c120553
