# import logging
import logging
from logging.config import dictConfig
from flask import Flask
from config import Configuration
from calculated_distance.blueprint import calculated_distance

application = Flask(__name__)
application.config.from_object(Configuration)
application.register_blueprint(calculated_distance, url_prefix='/calculate_distance')

logger = application.logger

# logging.basicConfig()
# logging.basicConfig(filename='demo.log', level=logging.DEBUG)
