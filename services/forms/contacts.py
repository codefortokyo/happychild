from django import forms


class ContactForm(forms.Form):
    fullname = forms.CharField(required=True,
                               max_length=30,
                               label='お名前',
                               widget=forms.TextInput(attrs={
                                   'placeholder': '山田太郎',
                                   'class': 'input-text'
                               }))
    email = forms.EmailField(required=True,
                             label='返信先メールアドレス',
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'example@gmail.com',
                                 'class': 'input-text'
                             }))
    title = forms.CharField(required=True,
                            max_length=255,
                            label='お問い合わせに関するタイトル',
                            widget=forms.TextInput(attrs={
                                'placeholder': '機能改善の要望',
                                'class': 'input-text'
                            }))
    description = forms.CharField(required=True,
                                  max_length=1000,
                                  label='お問い合わせ内容',
                                  widget=forms.Textarea(attrs={
                                      'class': 'input-text'
                                  }))
