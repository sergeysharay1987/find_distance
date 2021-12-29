from flask import Blueprint, render_template
from geopy import Location
from mkad_distance.forms import CalculateDistanceForm
from flask import request
from .logic import ya_geocoder, find_distance, write_in_log, Point

blprt_name: str = 'mkad_distance'  # название blueprint'а и название папки расположения blueprint'а
mkad_distance: Blueprint = Blueprint(blprt_name, __name__, template_folder='templates')


@mkad_distance.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        form = CalculateDistanceForm()
        return render_template(f'{blprt_name}/index.html', form=form)

    if request.method == 'POST':
        address = request.form['address']
        bound_form = CalculateDistanceForm(data={'address': address})
        if bound_form.validate():
            address = bound_form.data['address']
            loc_address: Location = ya_geocoder.geocode(address)
            coords_address: Point = Point(loc_address._tuple[1])
            full_address = loc_address.address
            bound_form = CalculateDistanceForm(data={'address': address,
                                                     'full_address': full_address,
                                                     'distance': find_distance(coords_address)})
            write_in_log(full_address, bound_form.data['distance'])
            return render_template(f'{blprt_name}/index.html', form=bound_form)
        elif not bound_form.validate():
            return render_template(f'{blprt_name}/index.html', form=bound_form)
