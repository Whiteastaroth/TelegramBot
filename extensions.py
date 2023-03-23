import requests
import json

from confic import exchanges


class APIException(Exception):
    """ Общий класс исключений. """
    pass


class Convertor:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        """ Статический метод который будет конвертировать наши валюты.
        Принимает три аргумента и возвращающий нужную сумму в требуемой валюте.
        Подымаем исключения при ошибочном вводе данных, пользователем."""
        if quote == base:
            raise APIException(f'{base}, не переводится в {base}.')

        try:
            sym_ticker = exchanges[quote]
        except KeyError:
            raise APIException(f'Валюта {quote}, указана не верно.')

        try:
            base_ticker = exchanges[base]
        except KeyError:
            raise APIException(f'Валюта {base}, указана не верно.')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Количество валюты, {amount}, не допустимо.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={sym_ticker}&tsyms={base_ticker}')

        # Выполняем запрос, передав - (fsym) - какую валюту хотим купить. (tsyms) - за какую валюту мы будем покупать
        total_base = json.loads(r.content)[exchanges[base]] * amount

        return round(total_base, 2)
