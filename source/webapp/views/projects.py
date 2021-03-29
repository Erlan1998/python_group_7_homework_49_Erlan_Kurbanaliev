from webapp.forms import ProjectsForm, SearchForm, ProjectsUpdateForm
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DetailView
from django.shortcuts import reverse, get_object_or_404, redirect, render
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


class ProjectCreate(CreateView):
    template_name = 'projects/create.html'
    form_class = ProjectsForm
    model = Projects

    def get_success_url(self):
        return reverse('project', kwargs={'id': self.object.id})


class ProjectUpdateView(TemplateView):
    template_name = 'projects/update_project.html'

    def get_context_data(self, **kwargs):
        project = get_object_or_404(Projects, id=kwargs.get('id'))

        form = ProjectsUpdateForm(initial={
            'name': project.name,
            'description': project.description,
            'update_date': project.update_date
        })
        kwargs['form'] = form
        kwargs['project'] = project
        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs):
        project = get_object_or_404(Projects, id=kwargs.get('id'))
        form = ProjectsUpdateForm(data=request.POST)

        if form.is_valid():
            project.name = form.cleaned_data.get('name')
            project.description = form.cleaned_data.get('description')
            project.update_date = form.cleaned_data.get('update_date')
            project.save()
            return redirect('project', id=project.id)
        return render(request, 'projects/update_project.html', context={'form': form})


class ProjectDeleteView(TemplateView):
    template_name = 'projects/delete.html'


    def get_context_data(self, **kwargs):
        kwargs['project'] = get_object_or_404(Projects, id=kwargs.get('id'))
        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs):
        project = get_object_or_404(Projects, id=kwargs.get('id'))
        project.delete()
        return redirect('index_project')




