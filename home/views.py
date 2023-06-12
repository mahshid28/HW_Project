from django.shortcuts import render


def wellcome(request):
    return render(request, 'home.html')
