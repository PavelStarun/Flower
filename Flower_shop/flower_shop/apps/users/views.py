from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Регистрация прошла успешно! Войдите в аккаунт.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме.")
        return self.render_to_response(self.get_context_data(form=form))



class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('shop-index')


@login_required
def profile_view(request):
    if request.method == 'POST':
        # Обновление профиля
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Обновляем поля из формы в профиле пользователя
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            profile.telegram_nickname = form.cleaned_data['telegram_nickname']
            profile.birth_date = form.cleaned_data['birth_date']

            # Сохраняем изменения
            request.user.save()  # Сохраняем данные в модели User
            profile.save()  # Сохраняем данные в модели Profile

            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        # Инициализация формы для отображения текущих данных пользователя
        form = UserProfileForm(
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'telegram_nickname': request.user.profile.telegram_nickname,
                'birth_date': request.user.profile.birth_date,
                'email': request.user.email
            }
        )

    context = {
        'form': form,
        'is_editing': request.GET.get('edit') == 'true',
    }
    return render(request, 'users/profile.html', context)
