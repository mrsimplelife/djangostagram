from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth import login as auth_login
from accounts.forms import SignupForm


class MyLoginView(LoginView):
    template_name = 'accounts/login_form.html'
    redirect_authenticated_user = True

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, 'login success!!')
        return super().form_valid(form)


login = MyLoginView.as_view()


def logout(request):
    messages.success(request, 'logout success!!')
    return logout_then_login(request)


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'success!!!')
            auth_login(request, user)
            subject = render_to_string("accounts/welcome_email_subject.txt")
            content = render_to_string("accounts/welcome_email_content.txt",
                                       {'user': user})
            user.email_user(subject, content, fail_silently=False)
            # next_url = request.GET.get('next', '/')
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form
    })
