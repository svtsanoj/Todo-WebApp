from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterationForm, loginForm

from django.contrib import messages

# Create your views here.
def register(request):
    form = RegisterationForm()
    if(request.method == 'POST'):
        form = RegisterationForm(request.POST)
        if(form.is_valid()):
            form.save()
            
            first_name = form.cleaned_data.get('first_name')
            messages.success(request, 'Hi '+first_name)

            return redirect('login')

    contents = {'form': form}
    return render(request, 'register.html', contents)


def loginPage(request):
	if request.user.is_authenticated:
		return redirect('todo')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('todo')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)

def logoutLink(request):
	logout(request)
	return redirect('login')