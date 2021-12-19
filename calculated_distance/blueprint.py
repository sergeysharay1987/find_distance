from flask import Blueprint, render_template
from distance_MKAD.forms import CalculateDistanceForm
from flask import request
from distance_MKAD.logic import *

distance_MKAD = Blueprint('distance_MKAD', __name__, template_folder='templates')
distance_MKAD.root_path


@distance_MKAD.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        form = CalculateDistanceForm()
        print(f'blueprint_root: {blueprint}')
        return render_template('calculated_distance/index.html', form=form)

    if request.method == 'POST':
        address = request.form['address']
        bound_form = CalculateDistanceForm(data={'address': address})
        if bound_form.validate():
            loc_address = ya_geocoder.geocode(bound_form.data['address'])
            coords_address = Point(loc_address.latitude, loc_address.longitude)
            full_address = loc_address.address
            distance = find_distance(coords_address)
            bound_form = CalculateDistanceForm(data={'address': address,
                                                     'full_address': full_address,
                                                     'distance': distance})
            return render_template('calculated_distance/index.html', form=bound_form)
        elif not bound_form.validate():
            return render_template('calculated_distance/index.html', form=bound_form)
