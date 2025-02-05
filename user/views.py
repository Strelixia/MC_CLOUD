from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from  .models import User


def new_user(request):
    if request.method== 'POST':
        username = request.POST.get("name")
        mail= request.POST.get("mail")
        password = request.POST.get("password")
        User.objects.create(username = username, mail = mail, password = password)
        return redirect('dashboard')
    return render (request, 'new_user_login.html')

def existing_user(request):
    if request.method== 'POST':
        username = request.POST.get("name")
        mail= request.POST.get("mail")
        password = request.POST.get("password")
        user = authenticate(username =username, mail = mail, password = password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html')
    return render (request, 'login.html')