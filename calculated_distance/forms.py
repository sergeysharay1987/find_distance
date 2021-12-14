from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from .logic import ya_geocoder

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
        if address.isdigit():
            raise ValidationError('Incorrect data')
        try:
            ya_geocoder.geocode(address)
        except (AttributeError, TypeError):
            raise ValidationError(
                'The "address" field must contain at least name of the country or name of the locality or both.')
        return address
