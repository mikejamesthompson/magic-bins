import sys, os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config')
db = SQLAlchemy(app)

if not app.debug:
	import logging

	log_directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..', 'logs'))

	from logging.handlers import RotatingFileHandler
	handler = RotatingFileHandler(log_directory+'/app.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.addHandler(handler)
	app.logger.setLevel(logging.INFO)

from app import views, models
