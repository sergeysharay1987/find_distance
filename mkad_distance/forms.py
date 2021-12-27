from geopy import Location
from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from mkad_distance.logic import ya_geocoder


class CalculateDistanceForm(Form):
    """Create form for """
    address: str = TextAreaField('Адрес', validators=[
        DataRequired('Please enter the address')])
    full_address = TextAreaField('Полный адрес', render_kw={'readonly': True})
    distance = TextField('Расстояние', render_kw={'readonly': True})

    def validate_address(form, field):
        address: str = field.data
        location = ya_geocoder.geocode(address)
        if not isinstance(location, Location) or '_*^!~' in address:
            raise ValidationError('Поле адрес должно содержать по крайней мере '
                                  'название страны или название населённого '
                                  'пункта или и то и другое')

        if location.address == 'Москва, Россия':
            raise ValidationError('Уточните пожалуйста адрес. Добавьте название района, улицы, '
                                  'или и то и другое')

        return address
