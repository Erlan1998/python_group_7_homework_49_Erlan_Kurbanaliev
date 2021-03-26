from webapp.forms import ProjectsForm
from django.views.generic import CreateView
from django.shortcuts import reverse, get_object_or_404
from webapp.models import Porjects, List


class ListProjectCreate(CreateView):
    template_name = 'projects/create.html'
    form_class = ProjectsForm
    model = Porjects

    def get_success_url(self):
        return reverse(
            'task',
            kwargs={'pk': self.kwargs.get('pk')}
        )

    def form_valid(self, form):
        list = get_object_or_404(List, id=self.kwargs.get('pk'))
        form.instance.list = list
        return super().form_valid(form)