#Треба реалізувати:
#1) функцію generator_numbers: 
#аналізувати текст, ідентифікувати всі дійсні числа, 
#що вважаються частинами доходів - записані без помилок, і 
#повертати їх як генератор;
#2) функцію sum_profit:
#використовувати generator_numbers для підсумовування цих чисел,
#розрахунку загального прибутку.


import re
from typing import Callable, Iterator

#генератор для вилучення дійсних чисед із текста

def generator_numbers(text: str) -> Iterator[float]:

    pattern = r'[ ](\d+\.\d+)[ ]' #дійсні числа без помилок, відокремлені " "
#   pattern = r'(?<=\s)\d+\.\d+(?=\s)' ''' lookbehind і lookahead'''

    for number_str in re.findall(pattern, text):
        number = float(number_str)

        yield number

#на льоту рахуємо сумму

def sum_profit(text: str, func: Callable, Iterator[float]) -> float:

return sum(func(text))