from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from accounts.forms import SignupForm


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = render_to_string("accounts/welcome_email_subject.txt")
            content = render_to_string("accounts/welcome_email_content.txt",
                                       {'user': user})
            user.email_user(subject, content, fail_silently=False)
            messages.success(request, 'success!!!')
            # next_url = request.GET.get('next', '/')
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })
