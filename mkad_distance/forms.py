from wtforms import Form, TextField, TextAreaField
from wtforms.validators import DataRequired, ValidationError


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
    address: str = TextAreaField('Адрес', validators=[
        DataRequired('Пожалуйста, введите адрес')])
    full_address = TextAreaField('Полный адрес', render_kw={'readonly': True})
    distance = TextField('Расстояние', render_kw={'readonly': True})

    def validate_address(form, field):
        address: str = field.data
        if not check_str(address):
            raise ValidationError('Поле адрес содержит недопустимый символ(ы)')

    def __str__(self):
        return f'address: {self.address}, full_address: {self.full_address}, distance: {self.distance}'
