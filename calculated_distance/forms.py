from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import TextInput

from .logic import geocode_address


class CalculateDistanceForm(Form):
    """Create form for """
    address: str = TextAreaField('Address', validators=[
        DataRequired('Please enter the address')])
    distance = TextField('Distance', render_kw={'readonly': True})

    def validate_address(form, field):
        address: str = field.data
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
