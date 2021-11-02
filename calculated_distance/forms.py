from wtforms import Form, TextField, TextAreaField
# from wtforms.validators import Required, DataRequired

# data_required = DataRequired('Enter the address')


class CalculateDistanceForm(Form):
    address = TextAreaField('Address')
    result = TextField('Result', render_kw={'readonly': True})
