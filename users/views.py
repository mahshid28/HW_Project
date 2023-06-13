from django.shortcuts import render


def wellcome(request):
    return render(request, 'users/user.html')