import os

import shapely.geometry
from flask import Blueprint, render_template, make_response, url_for
from werkzeug.utils import redirect
from calculated_distance.forms import CalculateDistanceForm
from flask import request, flash
from loguru import logger
import requests
from calculated_distance.logic import *





API_KEY = 'cbddbd2c-95ce-4aa1-ba5a-5d0416597c20'
calculated_distance = Blueprint('calculated_distance', __name__, template_folder='templates')
dir = os.getcwd()
def make_url(address):
    return f'https://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={address}&format=json'


def get_data_from_response(url):
    req = requests.get(url)
    data = req.json()
    return data


# logging.basicConfig(level=20, filename='my_log.log')


# @calculated_distance.route('/', methods=['POST', 'GET'])
# def index():
#     form = CalculateDistanceForm()
#     if request.method == 'POST':
#
#         address = request.form['address']
#         bound_form = CalculateDistanceForm(address=address)
#         # print(f'bound_form["address"]: {bound_form.address.data}')
#         if bound_form.validate():
#             url = make_url(address)
#             data = get_data_from_response(url)
#             print(type(data))
#             # print(response.is_json)
#             logger.add('info.log', format='{time} {message}', level='INFO')
#             logger.info(f'{address} {data}')
#             print('Helloo')
#             # response = make_response()
#             return redirect(make_url(address))
#         else:
#             form = CalculateDistanceForm(address=address)
#             print(form.address.errors)
#
#             return render_template('calculated_distance/index.html', form=form)
#     return render_template('calculated_distance/index.html', form=form)

@calculated_distance.route('/', methods=['POST', 'GET'])
def index():
    form = CalculateDistanceForm()

    if request.method == 'GET':
        form = CalculateDistanceForm()
        return render_template('calculated_distance/index.html', form=form)

    if request.method == 'POST':
        address = request.form['address']
        bound_form = CalculateDistanceForm(data={'address': address})
        if bound_form.validate():
            coords_of_address = geocode_address(bound_form.data['address'])
            distance = find_distance(coords_of_address)
            bound_form = CalculateDistanceForm(data={'address': address, 'distance': distance})
            logger.add('info.log', format='{time} {message}', level='INFO')
            logger.info(f'Растояние от МКАД до {address} равно {distance}')
            return render_template('calculated_distance/index.html', form=bound_form)
        elif not bound_form.validate():
            print(f'bound_form.errors still have error {bound_form.errors}')
            print(f'{form} is not pass validation')
            # bound_form = CalculateDistanceForm(address=address)
            print(f'There are errors {bound_form.address.errors}')
            return render_template('calculated_distance/index.html', form=bound_form)
