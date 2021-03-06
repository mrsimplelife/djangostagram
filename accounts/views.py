from django.contrib import messages
from django.forms.models import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from accounts.forms import PasswordChangeForm, ProfileForm, SignupForm

User = get_user_model()


class MyPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change")
    template_name = "accounts/password_change_form.html"
    form_class = PasswordChangeForm

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, "password changed!!")
        return super().form_valid(form)


password_change = MyPasswordChangeView.as_view()

# class ProfileEditView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = ProfileForm
#     template_name = "accounts/profile_edit_form.html"
#     success_url = '/'

#     def get_success_url(self) -> str:
#         messages.success(self.request, 'profile edited!!!')
#         return super().get_success_url()

#     def get_object(self, queryset: Optional[QuerySet] = None) -> Model:
#         if queryset is None:
#             queryset = self.get_queryset()
#         queryset = queryset.filter(pk=self.request.user.pk)
#         try:
#             # Get the single item from the filtered queryset
#             obj = queryset.get()
#         except queryset.model.DoesNotExist as err:
#             raise Http404(_("No %(verbose_name)s found matching the query") %
#   {'verbose_name': queryset.model._meta.verbose_name}) from err
#         return obj


# profile_edit = ProfileEditView.as_view()


@login_required
def profile_edit(request: HttpRequest):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "profile edited!!")
            redirect("/")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html", {"form": form})


class MyLoginView(LoginView):
    template_name = "accounts/login_form.html"
    redirect_authenticated_user = True

    def form_valid(self, form) -> HttpResponse:
        messages.success(self.request, "login success!!")
        return super().form_valid(form)


login = MyLoginView.as_view()


@login_required
def logout(request):
    messages.success(request, "logout success!!")
    return logout_then_login(request)


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "success!!!")
            auth_login(request, user)
            subject = render_to_string("accounts/welcome_email_subject.txt")
            content = render_to_string(
                "accounts/welcome_email_content.txt", {"user": user}
            )
            user.email_user(subject, content, fail_silently=False)
            # next_url = request.GET.get('next', '/')
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, "accounts/signup_form.html", {"form": form})
