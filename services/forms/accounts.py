from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from infrastructure.models import CustomUser as User
from infrastructure.models import Age


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=20,
                               required=True,
                               error_messages={
                                   'required': 'そのユーザ名は既に使用されています'
                               },
                               widget=forms.TextInput(attrs={
                                   'class': 'input-text',
                                   'placeholder': 'ユーザー名'
                               }))
    email = forms.EmailField(required=True,
                             error_messages={
                                 'required': 'そのメールアドレスは既に使用されています'
                             },
                             widget=forms.TextInput(attrs={
                                 'class': 'input-text',
                                 'placeholder': 'メールアドレス'
                             }))
    password1 = forms.CharField(required=True,
                                max_length=255,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'input-text',
                                    'placeholder': 'パスワード'
                                }))
    password2 = forms.CharField(required=True,
                                max_length=255,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'input-text',
                                    'placeholder': '確認用パスワード'
                                }))

    class Meta:
        model = User
        fields = (
            "username", "email", "password1", "password2",
        )


class LoginForm(forms.Form):
    error_messages = {
        'invalid_username': "指定のメールアドレスは登録されていません",
        'password_incorrect': "パスワードが正しくありません",
    }
    username = forms.CharField(max_length=255,
                               required=True,
                               widget=forms.EmailInput(attrs={
                                   'class': 'input-text',
                                   'placeholder': '登録メールアドレス'
                               }))
    password = forms.CharField(max_length=255,
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'input-text',
                                   'placeholder': 'パスワード'
                               }))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username, password=password):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect', )
        return self.cleaned_data


class EmailChangeForm(forms.Form):
    error_messages = {
        'email_mismatch': "パスワードが一致していません",
        'email_inuse': "指定のメールアドレスは既に別のアカウントで使用されています",
        'password_incorrect': "パスワードが正しくありません",
    }

    current_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True
    )

    new_email1 = forms.EmailField(
        max_length=254,
        required=True
    )

    new_email2 = forms.EmailField(
        max_length=254,
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        """
        Validates that the password field is correct.
        """
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect', )
        return current_password

    def clean_new_email1(self):
        """
        Prevents an e-mail address that is already registered from being registered by a different user.
        """
        email1 = self.cleaned_data.get('new_email1')
        if User.objects.filter(email=email1).count() > 0:
            raise forms.ValidationError(self.error_messages['email_inuse'], code='email_inuse', )
        return email1

    def clean_new_email2(self):
        """
        Validates that the confirm e-mail address's match.
        """
        email1 = self.cleaned_data.get('new_email1')
        email2 = self.cleaned_data.get('new_email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError(self.error_messages['email_mismatch'], code='email_mismatch', )
        return email2

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email1']
        if commit:
            self.user.save()
        return self.user


class ProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=255,
                              required=False,
                              label='住所',
                              widget=forms.TextInput(attrs={
                                  'class': 'input-text',
                                  'placeholder': '住所を登録できます(見学会予約時などに入力を省略できます)'
                              }))
    phone_number = forms.CharField(max_length=255,
                                   required=False,
                                   label='電話番号',
                                   widget=forms.TextInput(attrs={
                                       'class': 'input-text',
                                       'placeholder': '電話番号'
                                   }))
    child_age = forms.ModelChoiceField(required=False,
                                       label='お子様の年齢',
                                       queryset=Age.objects.filter(is_active=True),
                                       widget=forms.Select(attrs={
                                           'class': 'selectpicker search-fields'
                                       }))

    class Meta:
        model = User
        fields = (
            "address", "phone_number", "child_age",
        )
