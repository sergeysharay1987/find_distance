from flask import Blueprint, render_template
from calculated_distance.forms import CalculateDistanceForm
from flask import request, flash
from loguru import logger
# import requests
from calculated_distance.logic import *

calculated_distance = Blueprint('calculated_distance', __name__, template_folder='templates')


# @calculated_distance.route('/', methods=['POST', 'GET'])
# def index():
#     form = CalculateDistanceForm()
#
#     if request.method == 'GET':
#         form = CalculateDistanceForm()
#         return render_template('calculated_distance/index.html', form=form)
#
#     if request.method == 'POST':
#         address = request.form['address']
#         bound_form = CalculateDistanceForm(data={'address': address})
#         print(f'os.getcwd(): {os.getcwd()}')
#         if bound_form.validate():
#             print(f'bound_form.data["address"]: {bound_form.data["address"]}')
#             coords_of_address = geocode_address(bound_form.data['address'])
#             poly_mkad = get_polygon(shape_file)
#             print(f'coords_of_address: {coords_of_address}')
#             if poly_mkad.contains(coords_of_address):
#                 distance = 0
#             else:
#                 p1, nearest_pt = nearest_points(coords_of_address, poly_mkad)
#                 distance = geodesic((nearest_pt.x, nearest_pt.y), (coords_of_address.x, coords_of_address.y))
#             print(f'distance: {distance}')
#             bound_form = CalculateDistanceForm(data={'address': address, 'distance': distance})
#             write_in_log(address, distance)
#             return render_template('calculated_distance/index.html', form=bound_form)
#         elif not bound_form.validate():
#             print(f'bound_form.errors still have error {bound_form.errors}')
#             print(f'{form} is not pass validation')
#             # bound_form = CalculateDistanceForm(address=address)
#             print(f'There are errors {bound_form.address.errors}')
#             return render_template('calculated_distance/index.html', form=bound_form)


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
            loc_address = geocode_address(bound_form.data['address'])
            coords_address = Point(loc_address.latitude, loc_address.longitude)
            full_address = loc_address.address
            distance = find_distance(coords_address)
            bound_form = CalculateDistanceForm(data={'address': address,
                                                     'full_address': full_address,
                                                     'distance': distance})
            return render_template('calculated_distance/index.html', form=bound_form)
        elif not bound_form.validate():
            print(f'bound_form.errors still have error {bound_form.errors}')
            print(f'{form} is not pass validation')
            # bound_form = CalculateDistanceForm(address=address)
            print(f'There are errors {bound_form.address.errors}')
            return render_template('calculated_distance/index.html', form=bound_form)
