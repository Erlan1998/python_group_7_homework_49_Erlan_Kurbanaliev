from django.contrib.auth import get_user_model, update_session_auth_hash, login
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView, UpdateView
from django.core.paginator import Paginator
from accounts.forms import UserRegisterForm
from django.shortcuts import render, redirect
from accounts.forms import UserUpdateForm, ProfileUpdateForm, UserChangePasswordForm
from webapp.forms import SearchForm


def register_view(request, *args, **kwargs):
    context = {}
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index_project')
    context['form'] = form
    return render(request, 'registration/registe.html', context=context)


class UserView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'index_users.html'
    context_object_name = 'user_object'
    pk_url_kwarg = 'id'
    paginate_related_by = 5
    paginate_related_orphans = 0
    permission_required = 'accounts.user_view'


    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(UserView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(username__icontains=self.search_data)
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


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    pk_url_kwarg = 'id'
    paginate_related_by = 5
    paginate_related_orphans = 1

    def get_context_data(self, **kwargs):
        projects = self.get_object().projects.all()
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_update.html'
    context_object_name = 'user_obj'
    form_class = UserUpdateForm
    profile_form_class = ProfileUpdateForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = self.get_profile_form()
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        return self.form_invalid(user_form, profile_form)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['profile_form'] = kwargs.get('profile_form')
        if context['profile_form'] is None:
            context['profile_form'] = self.get_profile_form()
        return context

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(
            form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)

    def form_valid(self, user_form, profile_form):
        response = super(UserUpdateView, self).form_valid(user_form)
        profile_form.save()
        return response

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return self.profile_form_class(**form_kwargs)

    def get_success_url(self):
        return reverse('all_accounts', kwargs={'id': self.object.id})


class UserChangePasswordView(LoginRequiredMixin, UpdateView):
    template_name = 'user_change_password.html'
    model = get_user_model()
    form_class = UserChangePasswordForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super(UserChangePasswordView, self).form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        return response

    def get_success_url(self):
        return  reverse('all_accounts', kwargs={'id': self.object.id})