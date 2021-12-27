from flask import Flask
from config import Configuration
from mkad_distance.blueprint import mkad_distance

application = Flask(__name__)
application.config.from_object(Configuration)
application.register_blueprint(mkad_distance, url_prefix='/calculate_distance')
