from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import profileUpdateForm
from .forms import userUpdateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to log in.')
            form.save()
            return redirect('login')
    else: 
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'users/logout.html')
    else:
        return render(request, 'users/logout.html')
    
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = userUpdateForm(request.POST, instance=request.user)
        p_form = profileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account details has beem updated !')
            return redirect('profile')

    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

        context = {
            'u_form' : u_form,
            'p_form': p_form 
        }

        return render(request, 'users/profile.html', context)
