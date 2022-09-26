from django.shortcuts import render
from random import choice as c
import string

# Домашняя страница
def home(request):
    return render(request, 'index.html')

# Страница FAQ
def faq(request):
    return render(request, 'faq.html')

# Страница сгенерированного пароля
def password(request):
    # Переменные, которые будут использованы
    users_password, word = '', ''
    length = int(request.GET.get('length', 12))
    combination = list('abcdefghijklmnopqrstuvwxyz')
    # Получение параметров пароля и дополнение списка символами
    if request.GET.get('uppercase'):
        combination.extend(list(('abcdefghijklmnopqrstuvwxyz').upper()))
    if request.GET.get('numbers'):
        combination.extend(list('0123456789'))
    if request.GET.get('special'):
        combination.extend(list('!#$%&()*+,-./:;<=>?@[\]^_{|}~'))
    if request.GET.get('word'):
        word = request.GET.get('word')
        first_part, second_part = '', ''
    # Если пользователь запросил использовать в пароле его слово, сработает условие, которое добавит это слово.
    if word:
        for i in range(int((length - len(word))/2)):
            first_part += c(combination)
            second_part += c(combination)
        users_password = first_part + word + second_part
    # Иначе сгенерируется пароль из рандомного списка символов.
    else:
        # Цикл, генерирующий пароль
        for i in range(length):
            users_password += c(combination)
    # Передача пароля в словарь для html
    context = {
        'password': users_password
    }
    return render(request, 'generated_password.html', context)

# Страница проверки пароля пользователя
def check(request):
    # Получение пароля, введенного пользователем, а также вычисление его длины
    password = request.POST.get('password')
    length = len(password)
    # Условие проверяющее длину пароля
    if length < 8:
        # Рекомендация
        output = f'Увеличьте длину пароля, минимум на {12 - length} символов'
        # 100 бальная оценка надежности пароля
        points = 0
    else:
        # Проверка пароля на наличие заглавных букв, цифр и спец. символов
        lower = any([1 if i in string.ascii_lowercase else 0 for i in password])
        upper = any([1 if i in string.ascii_uppercase else 0 for i in password])
        special = any([1 if i in string.punctuation else 0 for i in password])
        number = any([1 if i in string.digits else 0 for i in password])
        # Передача полученных значений в список
        list = [lower, upper, special, number]
        # Если все пункты совпали, то выводится текст
        if all(list):
            output = 'Ваш пароль надёжный'
            # 100 бальная оценка надежности пароля
            points = 100
        # Если же хоть один не совпал, то выводится рекомендация
        else:
            # Рекомендация
            output = ('Рекомендую добавить один или более символов из ' +
                      'букв нижнего регистра, '*(list[0] is False) +
                      'букв верхнего регистра, '*(list[1] is False) +
                      'специальных (!&? и т.д.), '*(list[2] is False) +
                      'цифр от 0 до 9, '*(list[3] is False) +
                      'и затем попробуйте снова!'
                      )
            # 100 бальная оценка надежности пароля
            points = (sum(list) + 1) * 20
    # Передача рекомендации и % в словарь для html
    context = {
        'output': output,
        'points': points,
    }
    return render(request, 'check.html', context)
