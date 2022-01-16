from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from .logic import ya_geocoder


def check_str(string: str):
    """Функция возвращает True, если строка содержит допустимые символы, в противном случае возвращает False"""
    splitted_str = string.split()
    for word in splitted_str:
        if word.isalnum() or word[-1] == ',' or word[-1] == ' ':
            return True
        return False


class CalculateDistanceForm(Form):
    """Форма для расчёта геодезического расстояния"""
    address = TextAreaField('Адрес', validators=[
        DataRequired('Пожалуйста, введите адрес')])
    full_address = TextAreaField('Полный адрес', render_kw={'readonly': True})
    distance = TextField('Расстояние', render_kw={'readonly': True})

    @property
    def location(self):
        address = self.address.data
        location = ya_geocoder.geocode(address)
        return location

    def validate_address(self, field):
        address: str = field.data
        if not check_str(address):
            raise ValidationError('Поле адрес содержит недопустимый символ(ы)')