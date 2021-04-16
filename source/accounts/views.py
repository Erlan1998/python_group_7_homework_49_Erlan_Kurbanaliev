from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
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



class UserView(ListView):
    model = get_user_model()
    template_name = 'index_users.html'
    context_object_name = 'user_object'
    pk_url_kwarg = 'id'
    paginate_related_by = 5
    paginate_related_orphans = 0


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    pk_url_kwarg = 'id'
    paginate_related_by = 5
    paginate_related_orphans = 1

    def get_context_data(self, **kwargs):
        projects = self.get_object().projects.all()
        print(projects)
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        print(page_number)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)