from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from apps.accounts.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
import logging
logger = logging.getLogger(__name__)



# ! Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

  def form_valid(self, form):
    logger.info('✅ Login successful for user: %s', form.get_user().username)
    return super().form_valid(form)
    
    
  def get_success_url(self):
    return reverse_lazy('profile')  # Cambia 'home' por el nombre de tu vista de inicio

# ! Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Set default values or process extra logic si hace falta
            user.user_type = 'cliente'  # o como corresponda

            user.save()

            logger.info('✅ User registered successfully: %s', user.email)
            return redirect('login')  # usa el name del path si es posible
        else:
            print("❌ Register failed! Errors:", form.errors)
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
  
  
def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm
  
  
#  ! Profile view and update
class ProfileView(LoginRequiredMixin, TemplateView):
  template_name = 'accounts/profile.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['user'] = self.request.user  # Añade el usuario al contexto
    return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/update_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user  # Asegura que solo el usuario autenticado pueda actualizar su perfil

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info('✅ User profile updated: %s', self.object.email)
        return response