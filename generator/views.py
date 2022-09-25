from django.shortcuts import render
import random
import string


def home(request):
    return render(request, 'index.html')


def faq(request):
    return render(request, 'faq.html')


def password(request):
    users_password = ''
    length = int(request.GET.get('length', 12))
    combination = list('abcdefghijklmnopqrstuvwxyz')

    if request.GET.get('uppercase'):
        combination.extend(list(('abcdefghijklmnopqrstuvwxyz').upper()))
    if request.GET.get('numbers'):
        combination.extend(list('0123456789'))
    if request.GET.get('special'):
        combination.extend(list('!#$%&()*+,-./:;<=>?@[\]^_{|}~'))

    for i in range(length):
        users_password += random.choice(combination)
    context = {
        'password': users_password
    }

    return render(request, 'generated_password.html', context)


def check(request):
    password = request.POST.get('password')
    length = len(password)

    if length <= 8:
        output = f'Увеличьте длину пароля, минимум на {12 - length} символов'
    else:
        lower = any(
            [1 if i in string.ascii_lowercase else 0 for i in password])
        upper = any(
            [1 if i in string.ascii_uppercase else 0 for i in password])
        special = any([1 if i in string.punctuation else 0 for i in password])
        number = any([1 if i in string.digits else 0 for i in password])
        list = [lower, upper, special, number]

        if all(list):
            output = 'Ваш пароль надёжный'
        else:
            output = ('Рекомендую добавить один или более символов из ' +
                      'букв нижнего регистра, '*(list[0] is False) +
                      'букв верхнего регистра, '*(list[1] is False) +
                      'специальных (!&? и т.д.), '*(list[2] is False) +
                      'цифр от 0 до 9, '*(list[3] is False) +
                      'и затем попробуйте снова!'
                      )
    context = {
        'output': output,
    }

    return render(request, 'check.html', context)
