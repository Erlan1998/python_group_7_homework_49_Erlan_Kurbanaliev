from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from webapp.forms import ProjectsForm, SearchForm, ProjectsUpdateForm, UserUpdateForm
from django.views.generic import CreateView, ListView,  UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from webapp.models import Projects, List
from django.db.models import Q
from django.utils.http import urlencode


class IndexViewProject(ListView):
    template_name = 'projects/index_project.html'
    model = Projects
    context_object_name = 'projects'
    ordering = ('-created_date', 'name')
    paginate_by = 5
    paginate_orphans = 1

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexViewProject, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(name__icontains=self.search_data) |
                Q(description__icontains=self.search_data) |
                Q(update_date__icontains=self.search_data)
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


class ProjectView(DetailView):
    template_name = 'projects/view_project.html'
    model = Projects
    pk_url_kwarg = 'id'
    context_object_name = 'project'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = List.objects.filter(project=self.get_object())
        paginator = Paginator(object_list, self.paginate_by, )
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if page_obj.paginator.num_pages == 1:
            context['is_paginated'] = False
        else:
            context['is_paginated'] = True
        context['page_obj'] = page_obj
        context['lists'] = page_obj.object_list
        return context


class ProjectCreate(PermissionRequiredMixin, CreateView):
    template_name = 'projects/create.html'
    form_class = ProjectsForm
    model = Projects
    permission_required = 'webapp.add_projects'

    def get_success_url(self):
        return reverse('project', kwargs={'id': self.object.id})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'projects/update_project.html'
    model = Projects
    form_class = ProjectsUpdateForm
    context_object_name = 'project'
    pk_url_kwarg = 'id'
    permission_required = 'webapp.change_projects'

    def get_success_url(self):
        return reverse('project', kwargs={'id': self.object.id})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'projects/delete.html'
    model = Projects
    context_object_name = 'project'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('index_project')
    permission_required = 'webapp.delete_projects'


class UserUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'users/create.html'
    form_class = UserUpdateForm
    model = Projects
    pk_url_kwarg = 'id'
    permission_required = 'webapp.user_project_add'

    def get_success_url(self):
        return reverse('project', kwargs={'id': self.object.id})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().user.all()