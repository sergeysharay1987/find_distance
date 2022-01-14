from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from .logic import ya_geocoder
from geopy import Location


def check_all_chars(string: str):
    """Функция возвращает True, если строка содержит допустимые символы, в противном случае возвращает False"""
    for char in string:
        # проверяем, что символ не буква или цифра
        if not char.isalnum():
            return False
        # если символ буква или цифра, то прерываем текущую итерацию
        continue
    # проверяем, что последний символ либо буква, либо запятая
    return True


def check_str(string: str):
    """Функция возвращает True, если строка содержит допустимые символы, в противном случае возвращает False"""
    splitted_str = string.split()
    for word in splitted_str:
        if check_all_chars(word):
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
        if not isinstance(self.location, Location) or not check_str(address):
            raise ValidationError('Поле адрес содержит недопустимый символ(ы)')
