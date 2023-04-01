from django.shortcuts import render

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            return redirect('visitor_view')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
