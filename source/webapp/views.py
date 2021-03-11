from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from webapp.models import List
from webapp.forms import ListForm
# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        kwargs['lists'] = List.objects.all()
        return super().get_context_data(**kwargs)


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        kwargs['list'] = get_object_or_404(List, id=kwargs.get('id'))
        return super().get_context_data(**kwargs)


class TaskAddView(TemplateView):
    template_name = 'add_view.html'

    def get_context_data(self, **kwargs):
        form = ListForm()
        kwargs['form'] = form
        return super().get_context_data(**kwargs)

    def post(self, request,  **kwargs):
        form = ListForm(data=request.POST)
        if form.is_valid():
            list = List.objects.create(
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description'),
                created_at=form.cleaned_data.get('created_at'),
                updated_at=form.cleaned_data.get('updated_at'),
                status=form.cleaned_data.get('status'),
                tip=form.cleaned_data.get('tip')
            )
            return redirect('task', id=list.id)
        return super().get_context_data(**kwargs)


class TaskUpdateView(TemplateView):
    template_name = 'update.html'

    def get_context_data(self, **kwargs):
        list = get_object_or_404(List, id=kwargs.get('id'))

        form = ListForm(initial={
            'summary': list.summary,
            'description': list.description,
            'status': list.status,
            'tip': list.tip
        })
        kwargs['form'] = form
        kwargs['list'] = list
        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs):
        list = get_object_or_404(List, id=kwargs.get('id'))
        form = ListForm(data=request.POST)
        if form.is_valid():
            list.summary = form.cleaned_data.get('summary')
            list.description = form.cleaned_data.get('description')
            list.status_id = form.cleaned_data.get('status')
            list.tip_id = form.cleaned_data.get('tip')
            list.save()
            return redirect('task', id=list.id)
        return super().get_context_data(**kwargs)


class TaskDeleteView(TemplateView):
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        kwargs['list'] = get_object_or_404(List, id=kwargs.get('id'))
        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs):
        list = get_object_or_404(List, id=kwargs.get('id'))
        list.delete()
        return redirect('index_tasks')
