from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index_project')
        context['has_error'] = True
    return render(request, 'registration/login.html', context=context)


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('index_project')