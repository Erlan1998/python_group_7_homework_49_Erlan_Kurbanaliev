from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from webapp.models import List
# Create your views here.


class IndexView(View):

    def get(self, request, *args, **kwargs):
        list = List.objects.all()
        return render(request, 'index.html', context={'lists': list})

class TaskView(View):
    def get(self, request, id):
        list = get_object_or_404(List, id=id)
        return render(request, 'task_view.html', context={'list': list})