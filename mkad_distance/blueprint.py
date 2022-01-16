from flask import Blueprint, render_template
from mkad_distance.forms import CalculateDistanceForm
from flask import request
from shapely.geometry import Point
from .logic import shape_file, check_file, get_polygon, find_distance, write_in_log
from flask import flash

blprt_name: str = 'mkad_distance'  # название blueprint'а и название папки расположения blueprint'а
mkad_distance: Blueprint = Blueprint(blprt_name, __name__, template_folder='templates')
blpt_root = mkad_distance.root_path
data_dir = f'{blpt_root}/data'
poly_mkad = get_polygon(shape_file, data_dir)


@mkad_distance.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':

        form = CalculateDistanceForm()
        return render_template(f'{blprt_name}/index.html', form=form)

    if request.method == 'POST':

        data = request.form.copy()
        bound_form = CalculateDistanceForm(data=data)
        if bound_form.validate():

            check_file(data_dir)
            address = bound_form.data['address']
            if not bound_form.location:

                flash('Такого адреса не существует.', category='warning')
                bound_form.distance.data = ''
                bound_form.full_address.data = ''
            else:
                full_address = bound_form.location.address
                coords_address = Point(bound_form.location._tuple[-1])
                if full_address == 'Москва, Россия':

                    flash('Уточните пожалуйста адрес. Добавьте например название населённого пункта или улицы, '
                          'номер дома', category='warning')
                    distance = ''
                elif poly_mkad.contains(coords_address):

                    flash('Адрес находится внутри МКАД', category='info')
                    distance = ''
                else:
                    distance = f'{find_distance(coords_address, poly_mkad)} km'
                bound_form = CalculateDistanceForm(data={'address': address,
                                                         'full_address': full_address,
                                                         'distance': distance})
                if distance:

                    write_in_log(full_address, distance, blpt_root)
            return render_template(f'{blprt_name}/index.html', form=bound_form)
        elif not bound_form.validate():
            bound_form.full_address.data = ''
            bound_form.distance.data = ''
            return render_template(f'{blprt_name}/index.html', form=bound_form)
