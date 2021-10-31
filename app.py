from flask import Flask
from config import Configuration
from calculated_distance.blueprint import calculated_distance


app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(calculated_distance, url_prefix='/calculate_distance')
