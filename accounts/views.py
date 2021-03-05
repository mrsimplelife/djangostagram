from accounts.forms import SignupForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'success!!!')
            # next_url = request.GET.get('next', '/')
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })
