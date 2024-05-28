from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
# Create your views here.

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True,help_text="Enter Email Adress")
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SignUpView(CreateView):
    form_class = CreateUserForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

