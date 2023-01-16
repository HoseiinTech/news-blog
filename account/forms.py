from django import forms
from django.core.exceptions import ValidationError
from account.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

captcha_default_errors = {
    'required': 'اعتبار سنجی کپچا را کامل کنید.',
    'invalid': 'اعتبار سنجی کپچا با خطا مواجه گردید.'
}


# Login Form
class LoginForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        label='شماره تلفن',
        widget=forms.TextInput(attrs={'class': 'form-control text-left'}),
    )
    password = forms.CharField(
        max_length=60,
        widget=forms.PasswordInput(attrs={'class': 'form-control text-left',
                                          'style': 'padding-left: 60px;'}),
        label='رمز عبور'
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), error_messages=captcha_default_errors)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 11:
            raise ValidationError(
                'شماره تلفن "%(value)s" نامعتبر است.',
                code='invalid_phone_number',
                params={'value': f'{phone_number}'}
            )
        return phone_number


# Register Forms
class RegisterForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label='شماره تلفن',
        widget=forms.TextInput(attrs={'class': 'form-control text-left'}),
    )
    password1 = forms.CharField(
        max_length=60,
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control text-left',
                                          'style': 'padding-left: 60px;'})
    )
    password2 = forms.CharField(
        max_length=60,
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control text-left',
                                          'style': 'padding-left: 60px;'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), error_messages=captcha_default_errors)

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        min_length = 8
        if len(password1) < min_length:
            raise ValidationError('رمز عبور باید حداقل هشت قسمت باشد.',
                                  code='min_length_error')
        if not any(char.isdigit() for char in password1):
            raise ValidationError('رمز عبور باید حداقل شامل یک رقم باشد.',
                                  code='check_digit_error')
        if not any(char.isalpha() for char in password1):
            raise ValidationError('رمز عبور باید حداقل شامل یک حرف باشد.',
                                  code='check_letter_error')

        if password1 != password2:
            raise ValidationError(
                'رمز عبور ها شباهت ندارند، لطفا تصحیح کنید.',
                code='password_do_not_match'
            )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 11:
            raise ValidationError(
                'شماره تلفن "%(value)s" نامعتبر است.',
                code='invalid_phone_number',
                params={'value': f'{phone_number}'}
            )
        return phone_number


class CheckOtpForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        label='کد تایید',
        widget=forms.TextInput(attrs={'class': 'form-control text-left'}),
    )


# Forget Password Form
class ForgetPasswordForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        label='شماره تلفن',
        widget=forms.TextInput(attrs={'class': 'form-control text-left'}),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 11:
            raise ValidationError(
                'شماره تلفن "%(value)s" نامعتبر است.',
                code='invalid_phone_number',
                params={'value': f'{phone_number}'}
            )
        return phone_number


# Change Password Form
class ChangePasswordForm(forms.Form):
    pre_password = forms.CharField(
        max_length=60,
        label='رمز عبور قبلی',
        widget=forms.PasswordInput(attrs={'class': 'form-control text-left',
                                          'style': 'padding-left: 60px;'})
    )
    new_password = forms.CharField(
        max_length=60,
        label='رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control text-left',
                                          'style': 'padding-left: 60px;'})
    )
    new_password_conf = forms.CharField(
        max_length=60,
        label='تکرار رمز عبور جدید',
        widget=forms.PasswordInput(attrs={'class': 'form-control text-left',
                                          'style': 'padding-left: 60px;'})
    )

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_conf = self.cleaned_data.get('new_password_conf')

        min_length = 8
        if len(new_password) < min_length:
            raise ValidationError('رمز عبور باید حداقل هشت قسمت باشد.',
                                  code='min_length_error')
        if not any(char.isdigit() for char in new_password):
            raise ValidationError('رمز عبور باید حداقل شامل یک رقم باشد.',
                                  code='check_digit_error')
        if not any(char.isalpha() for char in new_password):
            raise ValidationError('رمز عبور باید حداقل شامل یک حرف باشد.',
                                  code='check_letter_error')

        if new_password != new_password_conf:
            raise ValidationError(
                'رمز عبور ها شباهت ندارند، لطفا تصحیح کنید.',
                code='password_do_not_match'
            )


# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'phone_number', 'profile_photo', 'about_me')
