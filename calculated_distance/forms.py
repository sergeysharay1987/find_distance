from geopy import Location
from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import TextInput
from .logic import geocode_address, ya_geocoder, get_toponims, make_dict

set_nessesary = {'country', 'locality', 'street'}
nessesary_info_1 = {'country', 'locality', 'house'}
nessesary_info_2 = {'country', 'locality', 'metro'}


class CalculateDistanceForm(Form):
    """Create form for """
    address: str = TextAreaField('Address', validators=[
        DataRequired('Please enter the address')])
    full_address = TextAreaField('Full address', render_kw={'readonly': True})
    distance = TextField('Distance', render_kw={'readonly': True})

    def validate_address(form, field):
        address: str = field.data
        # list_toponims = get_toponims(address)
        # dict_toponims = make_dict(list_toponims)
        # if 'country' and 'locality' in dict_toponims.keys():

        # if dict_toponims['locality'] != 'Москва':
        #     pass
        # elif not dict_toponims['locality']:
        #     raise ValidationError('')
        # elif dict_toponims['locality'] == 'Москва':
        #     raise ValidationError('Уточните адрес, укажите улицу(станцию метро), номер дома')
        # if len(location.address.split()) == len(address.split()):
        #     raise ValidationError('Need more information about address')
        if len(address.split()) == 1 and 'Russia' in address:
            raise ValidationError('Add name of locality (city, town etc.)')
        # if len(field.data) <= 1:
        #     raise ValidationError('Name must be less than 50 characters')
        if address.isdigit():
            raise ValidationError('Incorrect data')
        try:
            geocode_address(address)
            print(address)
        except (AttributeError, TypeError):
            raise ValidationError(
                'The "address" field must contain at least name of the country or name of the locality or both.')
        return address
