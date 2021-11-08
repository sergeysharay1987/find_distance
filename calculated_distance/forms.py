from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, ValidationError


class CalculateDistanceForm(Form):
    """Create form for """
    address = TextAreaField('Address', validators=[
        DataRequired('Please enter the address'),
    ])
    distance = TextField('Distance', render_kw={'readonly': True})

    # def validate_address(self):
    #     # address = '0'
    #     if self.address == '0':
    #         raise ValidationError('address should not be the 0')