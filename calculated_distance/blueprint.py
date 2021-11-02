from flask import Blueprint, render_template
from calculated_distance.forms import CalculateDistanceForm
import logging
from flask import request
import app
from flask.logging import default_handler
from loguru import logger


API_KEY = 'cbddbd2c-95ce-4aa1-ba5a-5d0416597c20'
calculated_distance = Blueprint('calculated_distance', __name__, template_folder='templates')


logger.add('info.log', format = '{time} {message}')


def make_url(address):
    return f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode=Т{address}'


# logging.basicConfig(level=20, filename='my_log.log')

@calculated_distance.route('/', methods=['POST', 'GET'])
def index():
    form = CalculateDistanceForm()
    if request.method == 'POST':
        address = request.form['address']
        result = request.form['result']
        bound_form = CalculateDistanceForm(address=address, result=result)
        if bound_form.validate():

            # app.logger.removeHandler(default_handler)
            # file_handler = logging.FileHandler("summary.log")
            # file_handler.setLevel('INFO')
            # app.logger.addHandler(file_handler)
            # #logging.basicConfig(level=20, filename='find_distance/my_log.log')
            # print('_____________________')
            logger.info(f'Расстояние от МКАД  {address} равно {result}')
    return render_template('calculated_distance/index.html', form=form)
