from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views.generic import View, FormView
from account.forms import LoginForm, RegisterForm, CheckOtpForm, \
    ProfileForm, ForgetPasswordForm, ChangePasswordForm

from decouple import config
import ghasedakpack
from random import randint
from account.models import OTP, User
from django.utils.crypto import get_random_string, RANDOM_STRING_CHARS
from django.contrib.auth.hashers import check_password

SMS = ghasedakpack.Ghasedak(config('SMS_API'))


# Login & Logout Views
class LoginView(View):
    template_name = 'account/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('blog:home')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        messages = []
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('blog:home')
            messages += ['اطلاعات وارد شده نامعتبر است.']
        return render(request, self.template_name, context={'form': form, 'non_error': messages})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect(request.GET.get('next'))
        return redirect('blog:home')


# Register Views
class RegisterView(View):
    template_name = 'account/register.html'
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('blog:home')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        messages = []
        if form.is_valid():
            random_code = randint(1000, 9999)
            token = get_random_string(length=30)
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password1')
            if not User.objects.filter(phone_number=phone_number).exists():
                # SMS.verification({'receptor': phone_number, 'type': '1', 'template': 'mags', 'param1': random_code})
                print(random_code)
                OTP.objects.create(phone_number=phone_number, code=random_code, token=token, password=password)
                return redirect(reverse('check_otp') + f'?token={token}')
            messages += ['شماره تلفن وارد شده در سامانه وجود دارد، شماره دیگری وارد کنید.']
        return render(request, self.template_name, context={'form': form, 'messages': messages})


class CheckOtpView(View):
    template_name = 'account/check_otp.html'
    form_class = CheckOtpForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('blog:home')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if OTP.objects.filter(code=code, token=token).exists():
                otp = OTP.objects.get(token=token)
                user = User.objects.create_user(phone_number=otp.phone_number, username=otp.phone_number)
                user.set_password(otp.password)
                user.save()
                login(request, user)
                return redirect('blog:home')
            form.add_error('code', 'کد تایید وارد شده نامعتبر است.')

        return render(request, self.template_name, context={'form': form})


# Edit Profile Views
class EditProfileView(FormView):
    template_name = 'account/profile.html'
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated != True:
            return redirect('blog:home')
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:home')
        return render(request, self.template_name, context={'form': form})


# Forget Password Views
class ForgetPasswordView(View):
    # It receives the mobile number and if it is valid, sends a confirmation code to it.

    template_name = 'account/forget_password/forget_password.html'
    form_class = ForgetPasswordForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('blog:home')

        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        messages = []
        if form.is_valid():
            random_code = randint(1000, 9999)
            token = get_random_string(length=30)
            phone_number = form.cleaned_data.get('phone_number')
            if not User.objects.filter(phone_number=phone_number).exists():
                messages += ['شماره تلفن وارد شده در سامانه وجود ندارد، شماره دیگری وارد کنید.']
            else:
                # SMS.verification({'receptor': phone_number, 'type': '1', 'template': 'mags', 'param1': random_code})
                print(random_code)
                OTP.objects.create(phone_number=phone_number, code=random_code, token=token)
                return redirect(reverse('forget_pass_check') + f'?token={token}')
        return render(request, self.template_name, context={'form': form, 'messages': messages})


class ForgotPasswordCheckView(View):
    # The user enters the verification code sent and if it is correct, a new password is sent to that number.

    template_name = 'account/forget_password/forget_password_check.html'
    form_class = CheckOtpForm

    def get(self, request):
        form = self.form_class()
        if request.user.is_authenticated:
            return redirect('blog:home')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        token = request.GET.get('token')
        form = self.form_class(request.POST)
        messages = []
        if form.is_valid():
            code = form.cleaned_data.get('code')
            random_pass = get_random_string(length=9, allowed_chars=RANDOM_STRING_CHARS)
            if OTP.objects.filter(code=code, token=token).exists():
                otp = OTP.objects.get(token=token)
                # SMS.verification(
                #     {'receptor': otp.phone_number, 'type': '1', 'template': 'forgetpassword', 'param1': random_pass})
                print(random_pass)
                user = User.objects.get(phone_number=otp.phone_number)
                user.set_password(random_pass)
                user.save()
                return redirect('forget_pass_done')
            messages += ['کد تایید وارد شده نامعتبر است.']
        return render(request, self.template_name, context={'form': form, 'messages': messages})


class ForgetPasswordDoneView(View):
    # The operation is done successfully and now the user can log in with the new password.

    template_name = 'account/forget_password/forget_password_done.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('blog:home')
        return render(request, self.template_name)


# Change Password Views
class ChangePasswordView(View):
    template_name = 'account/change_password/change_password.html'
    form_class = ChangePasswordForm

    def get(self, request):
        form = self.form_class()
        if not request.user.is_authenticated:
            return redirect('blog:home')
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        messages = []
        if form.is_valid():
            match_check = check_password(form.cleaned_data['pre_password'], request.user.password)
            if match_check:
                user_login = authenticate(
                    username=request.user.phone_number,
                    password=form.cleaned_data['new_password'],
                )
                user = request.user
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                login(request, user_login)
                return redirect('change_pass_done')
            messages += ['رمز عبور قبلی شما نادرست است، لطفا تصحیح کنید.']
        return render(request, self.template_name, context={'form': form, 'messages': messages})


class ChangePasswordDoneView(View):
    template_name = 'account/change_password/change_password_done.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('blog:home')
        return render(request, self.template_name)
