from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.db import IntegrityError



# Регистрация
class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user.save()
            messages.success(self.request, 'Регистрация прошла успешно. Вы можете войти.')
            return redirect('profile')
        except IntegrityError:
            form.add_error(None, 'Пользователь с таким именем уже существует. Попробуйте другое имя.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Исправьте ошибки в форме.')
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

# Профиль
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль был обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(
            instance=request.user.profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        )

    is_editing = request.GET.get('edit') == 'true'

    context = {
        'form': form,
        'is_editing': is_editing,
    }
    return render(request, 'users/profile.html', context)

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('shop-index')