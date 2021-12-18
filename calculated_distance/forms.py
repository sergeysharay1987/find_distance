from geopy import Location
from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from calculated_distance.logic import ya_geocoder


class CalculateDistanceForm(Form):
    """Create form for """
    address: str = TextAreaField('Address', validators=[
        DataRequired('Please enter the address')])
    full_address = TextAreaField('Full address', render_kw={'readonly': True})
    distance = TextField('Distance', render_kw={'readonly': True})

    def validate_address(form, field):
        address: str = field.data
        loc_address: Location = ya_geocoder.geocode(address)
        if loc_address.address == 'Москва, Россия':
            raise ValidationError('Need more information, try to add street or district')
        if address.isdigit():
            raise ValidationError('Incorrect data')
        try:
            ya_geocoder.geocode(address)
        except (AttributeError, TypeError):
            raise ValidationError(
                'The "address" field must contain at least name of the country or name of the locality or both.')
        return address
