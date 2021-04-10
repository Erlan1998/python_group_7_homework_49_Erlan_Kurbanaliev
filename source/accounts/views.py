from accounts.forms import UserRegisterForm
from django.shortcuts import render, redirect



def register_view(request, *args, **kwargs):
    context = {}
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_project')
    context['form'] = form
    return render(request, 'registration/registe.html', context=context)