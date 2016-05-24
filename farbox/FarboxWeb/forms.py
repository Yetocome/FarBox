from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    """
    用户登录表单
    """
    remember_me = forms.BooleanField(label='下次自动登录', initial=False, required=False)


class RegistrationForm(UserCreationForm):
    """
    新用户注册表单
    """

    email = forms.EmailField(help_text='用户账号认证和密码重置')

    def clean_email(self):
        """
        确保注册邮箱的唯一性
        """
        value = self.cleaned_data['email']
        qs = User.objects.filter(email__iexact=value)
        if not qs.exists():
            return value
        raise forms.ValidationError('邮箱已被注册,请更换邮箱')


class UploadForm(forms.Form):
    """
    上传文件表单
    """
    file = forms.FileField(label='文件名', max_length=200)
    path_name = forms.CharField(label='路径名', max_length=200)