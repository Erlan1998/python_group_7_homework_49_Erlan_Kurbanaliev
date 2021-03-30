from webapp.forms import ProjectsForm, SearchForm, ProjectsUpdateForm
from django.views.generic import CreateView, ListView,  UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy
from webapp.models import Projects
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


class ProjectCreate(CreateView):
    template_name = 'projects/create.html'
    form_class = ProjectsForm
    model = Projects

    def get_success_url(self):
        return reverse('project', kwargs={'id': self.object.id})


class ProjectUpdateView(UpdateView):
    template_name = 'projects/update_project.html'
    model = Projects
    form_class = ProjectsUpdateForm
    context_object_name = 'project'
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return reverse('project', kwargs={'id': self.object.id})


class ProjectDeleteView(DeleteView):
    template_name = 'projects/delete.html'
    model = Projects
    context_object_name = 'project'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('index_project')

