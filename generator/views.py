from django.shortcuts import render
import random

def home(request):
    return render(request, 'index.html')

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
