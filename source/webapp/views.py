from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, ListView
from webapp.models import List
from webapp.forms import ListForm, SearchForm
from django.urls import reverse
from django.db.models import Q
from django.utils.http import urlencode
# Create your views here.


class IndexView(ListView):
    template_name = 'index.html'
    model = List
    context_object_name = 'lists'
    ordering = ('-created_at', 'summary')
    paginate_by = 5
    paginate_orphans = 2

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(summary__icontains=self.search_data) |
                Q(status__status__icontains=self.search_data) |
                Q(tip__tip__icontains=self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['search_form'] = self.form

        if self.search_data:
            kwargs['query'] = urlencode({'search_value': self.search_data})

        return kwargs


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
            )
            list.tip.set(form.cleaned_data.get('tip'))
            return redirect('task', id=list.id)
        return render(request, 'add_view.html', context={'form': form})


class TaskUpdateView(TemplateView):
    template_name = 'update.html'

    def get_context_data(self, **kwargs):
        list = get_object_or_404(List, id=kwargs.get('id'))

        form = ListForm(initial={
            'summary': list.summary,
            'description': list.description,
            'status': list.status,
            'tip': list.tip.all()
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
            list.tip.set(form.cleaned_data.get('tip'))
            list.save()
            return redirect('task', id=list.id)
        return render(request, 'add_view.html', context={'form': form})


class TaskDeleteView(TemplateView):
    template_name = 'delete.html'

    def get_context_data(self, **kwargs):
        kwargs['list'] = get_object_or_404(List, id=kwargs.get('id'))
        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs):
        list = get_object_or_404(List, id=kwargs.get('id'))
        list.delete()
        return redirect('index_tasks')
