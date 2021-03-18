from django.core.validators import BaseValidator, ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Value "%(value)s" has length of %(show_value)d! It should be at least %(limit_value)d symbols long!'
    code = 'too_short'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x)


def CapitalLetter(a):
    if not a[0].isupper():
        raise ValidationError('Введите название задачи с заглавной буквы!')


def OnlyLetters(a):
    for i in a:
        try:
            int(i)
            raise ValidationError('Не вводите цифры!')
        except ValidationError as e:
            raise e
        except ValueError:
            pass