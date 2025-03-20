from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

class CustomLoginView(LoginView):
    """
    Custom login view that uses email instead of username.
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        messages.success(self.request, "Login successful!")
        return redirect(self.get_success_url())

class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view.
    """
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def form_valid(self, form):
        messages.info(self.request, "Password reset email has been sent.")
        return super().form_valid(form)
