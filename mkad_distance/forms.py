from geopy import Location
from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from mkad_distance.logic import ya_geocoder


class CalculateDistanceForm(Form):
    """Форма для расчёта геодезического расстояния"""
    address: str = TextAreaField('Адрес', validators=[
        DataRequired('Пожалуйста, введите адрес')])
    full_address = TextAreaField('Полный адрес', render_kw={'readonly': True})
    distance = TextField('Расстояние', render_kw={'readonly': True})

    def validate_address(form, field):
        address: str = field.data
        if not isinstance(address, str):
            raise ValidationError('Поле адрес должно содержать по крайней мере '
                                  'название страны или название населённого'
                                  'пункта или и то и другое')
        # try:
        #     location: Location = ya_geocoder.geocode(address)
        #     if location.address == 'Москва, Россия':
        #         raise ValidationError('Уточните пожалуйста адрес. Добавьте название района, улицы, '
        #                               'или и то и другое')
        # except AttributeError:
        #     raise ValidationError('Поле адрес должно содержать по крайней мере '
        #                                'название страны или название населённого'
        #                                'пункта или и то и другое')

    def __str__(self):
        return f'address: {self.address}, full_address: {self.full_address}, distance: {self.distance}'
