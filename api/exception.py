from rest_framework.exceptions import APIException


class CurrencyIncorrect(APIException):
    status_code = 400
    default_detail = 'Bad request Currency Incorrect'
    default_code = 'currency_incorrect'
