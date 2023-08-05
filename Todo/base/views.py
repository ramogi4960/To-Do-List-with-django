from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task


class Login(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list')


class List(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


class Detail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'


class Create(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'details', 'complete']
    success_url = reverse_lazy('list')
    template_name = 'create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(Create, self).form_valid(form)


class Update(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('list')
    template_name = 'create.html'


class Delete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('list')
    context_object_name = 'task'