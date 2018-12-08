from django import forms

from infrastructure.models import NurseryReservation


class NurseryReservationForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           label='お名前',
                           widget=forms.TextInput(attrs={
                               'class': 'input-text'
                           }))
    email = forms.EmailField(required=True,
                             label='連絡先メールアドレス',
                             widget=forms.TextInput(attrs={
                                 'class': 'input-text'
                             }))
    address = forms.CharField(required=True,
                              label='住所',
                              max_length=255,
                              widget=forms.TextInput(attrs={
                                  'class': 'input-text'
                              }))
    phone_number = forms.CharField(required=True,
                                   label='電話番号',
                                   max_length=255,
                                   widget=forms.TextInput(attrs={
                                       'class': 'input-text'
                                   }))
    note = forms.CharField(required=False,
                           max_length=255,
                           label='ご要望や連絡事項',
                           widget=forms.TextInput(attrs={
                               'class': 'input-text'
                           }))

    class Meta:
        model = NurseryReservation
        fields = ('name', 'email', 'address', 'phone_number', 'note')
