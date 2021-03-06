from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from webapp.models import List, Projects
from webapp.forms import ListForm, SearchForm
from django.urls import reverse
from django.db.models import Q
from django.utils.http import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class IndexView(ListView):
    template_name = 'tasks/index.html'
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
                Q(description__icontains=self.search_data)
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


class TaskView(DetailView):
    template_name = 'tasks/view.html'
    model = List
    pk_url_kwarg = "id"


class TaskAddView(PermissionRequiredMixin, CreateView):
    model = Projects
    template_name = 'tasks/add.html'
    form_class = ListForm
    pk_url_kwarg = 'id'
    permission_required = 'webapp.add_list'

    def form_valid(self, form):
        project = get_object_or_404(Projects, id=self.kwargs.get('id'))
        list = form.save(commit=False)
        list.project = project
        list.save()
        form.save_m2m()
        return redirect('project', id=project.id)

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().user.all()


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'tasks/update.html'
    model = List
    form_class = ListForm
    context_object_name = 'list'
    pk_url_kwarg = 'id'
    permission_required = 'webapp.change_list'


    def get_success_url(self):
        return reverse('task', kwargs={'id': self.object.id})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.user.all()


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'tasks/delete.html'
    model = List
    context_object_name = 'list'
    pk_url_kwarg = 'id'
    permission_required = 'webapp.delete_list'

    def get_success_url(self):
        return reverse('project', kwargs={'id': self.object.project.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.user.all()