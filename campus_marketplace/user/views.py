from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Respect `next` parameter if provided
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'user:profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # respect `next` if present (POST or GET)
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'user:profile')
    else:
        # pass request so the form has access to it (important for some auth flows)
        form = CustomUserLoginForm(request=request)

    return render(request, 'user/login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'user/profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('main:product_list')
