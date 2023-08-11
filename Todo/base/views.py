from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Task

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# test for base template
# def base(request):
#     return render(request, 'base.html')


class Login(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list')


class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('list')
        return super(Register, self).get(*args, **kwargs)


class List(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input

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
