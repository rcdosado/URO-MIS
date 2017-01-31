from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import FormView, CreateView
from . import forms


# Create your views here.
def dashboard(request):
    return render(request, 'users/dashboard.html')


class LogoutView(LoginRequiredMixin, FormView):
    form_class = forms.LogoutForm
    template_name = 'users/logout.html'

    def form_valid(self, form):
        logout(self.request)
        return HttpResponseRedirect(reverse('home'))


class SignupView(CreateView):
    form_class = UserCreationForm 
    template_name = 'users/signup.html'
