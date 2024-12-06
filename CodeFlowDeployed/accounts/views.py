from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from CodeFlowDeployed.accounts.forms import CustomAuthenticationForm, CustomUserEditForm
from CodeFlowDeployed.accounts.forms import CustomUserCreationForm, ProfileEditForm
from CodeFlowDeployed.accounts.models import Profile

UserModel = get_user_model()


class CustomUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    form_class = CustomAuthenticationForm

class CustomUserRegisterView(CreateView):
    model = UserModel
    form_class = CustomUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)

        return response



class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user



class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_questions_count'] = self.object.question_set.count()
        context['total_lectures_count'] = self.object.lecture_set.count()

        return context


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return self.request.user == profile.user

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk,
            }
        )

class CustomUserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserModel
    form_class = CustomUserEditForm
    template_name = "accounts/edit-user-credentials.html"
    success_url = reverse_lazy("profile-details")

    def test_func(self):
        user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return UserModel.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        user = form.save(commit=False)

        new_password = form.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)

        user.save()

        if new_password:
            update_session_auth_hash(self.request, user)


        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.object.pk,
            }
        )