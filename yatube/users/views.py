from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm, ChangeForm, ResetForm
from django import forms


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class LogoutView(CreateView):
    form_class = CreationForm
    template_name = 'users/logged_out.html'


class PasswordChangeView(forms.Form):
    form_class = ChangeForm
    template_name = 'users/passw_change_form.html'


class PasswordChangeDoneView(forms.Form):
    form_class = ChangeForm
    template_name = 'users/passw_change_done.html'


class PasswordResetDoneView(forms.Form):
    form_class = ResetForm
    template_name = 'users/passw_reset_done.html'


class PasswordResetView(forms.Form):
    form_class = ResetForm
    template_name = 'users/passw_reset_form.html'


class PasswordResetConfirmView(forms.Form):
    form_class = ResetForm
    template_name = 'users/passw_reset_confirm.html'


class PasswordResetCompleteView(forms.Form):
    form_class = ResetForm
    template_name = 'users/passw_reset_complete.html'
