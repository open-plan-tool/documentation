from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, CustomUserChangeForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
@require_http_methods(["GET", "POST"])
def user_info(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User info successfully updated!')
            return redirect('user_info')
        else:
            messages.error(request, 'Please check errors and resubmit!')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/user_info.html', {
        'form': form
    })


@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please check errors and resubmit!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })
