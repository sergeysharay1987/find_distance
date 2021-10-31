from wtforms import Form, TextField, TextAreaField


class CalculateDistanceForm(Form):
    address = TextAreaField('Address')
    result = TextField('Result')


