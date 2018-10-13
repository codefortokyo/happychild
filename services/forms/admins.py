from django import forms

from infrastructure.models import Nursery, Ward, License, SchoolType


class NurseryForm(forms.ModelForm):
    ward = forms.ModelChoiceField(required=True,
                                  label='区',
                                  queryset=Ward.objects.filter(is_active=True),
                                  widget=forms.Select(attrs={
                                      'class': 'selectpicker search-fields'
                                  }))
    license = forms.ModelChoiceField(required=True,
                                     label='保育園種類',
                                     queryset=License.objects.filter(is_active=True),
                                     widget=forms.Select(attrs={
                                         'class': 'selectpicker search-fields'
                                     }))
    school_type = forms.ModelChoiceField(required=True,
                                         label='保育園運営種',
                                         queryset=SchoolType.objects.filter(is_active=True),
                                         widget=forms.Select(attrs={
                                             'class': 'selectpicker search-fields'
                                         }))
    name = forms.CharField(required=True,
                           max_length=255,
                           label='保育園名',
                           widget=forms.TextInput(attrs={
                               'class': 'input-text'
                           }))
    postcode = forms.CharField(required=False,
                               max_length=8,
                               label='郵便番号',
                               widget=forms.TextInput(attrs={
                                   'class': 'input-text'
                               }))
    address = forms.CharField(required=False,
                              max_length=255,
                              label='住所',
                              widget=forms.TextInput(attrs={
                                  'class': 'input-text'
                              }))
    station_info = forms.CharField(required=True,
                                   label='最寄り駅情報',
                                   max_length=255,
                                   widget=forms.TextInput(attrs={
                                       'class': 'input-text'
                                   }))
    url = forms.CharField(required=False,
                          label='公式サイトURL',
                          max_length=255,
                          widget=forms.TextInput(attrs={
                              'class': 'input-text'
                          }))
    phone_number = forms.CharField(required=False,
                                   label='電話番号',
                                   max_length=255,
                                   widget=forms.TextInput(attrs={
                                       'class': 'input-text'
                                   }))
    fax_number = forms.CharField(required=False,
                                 label='FAX番号',
                                 max_length=255,
                                 widget=forms.TextInput(attrs={
                                     'class': 'input-text'
                                 }))
    thumbnail_url = forms.URLField(required=False,
                                   label='サムネイル画像URL',
                                   max_length=255,
                                   widget=forms.URLInput(attrs={
                                       'class': 'input-text'
                                   }))
    latitude = forms.DecimalField(required=False,
                                  label='緯度',
                                  decimal_places=9,
                                  max_digits=12,
                                  widget=forms.TextInput(attrs={
                                      'class': 'input-text'
                                  }))
    longitude = forms.DecimalField(required=False,
                                   label='経度',
                                   decimal_places=9,
                                   max_digits=12,
                                   widget=forms.TextInput(attrs={
                                       'class': 'input-text'
                                   }))
    open_time_weekday = forms.CharField(required=False,
                                        label='平日開所時間',
                                        max_length=255,
                                        widget=forms.TextInput(attrs={
                                            'class': 'input-text'
                                        }))
    open_time_saturday = forms.CharField(required=False,
                                         label='土曜日開所時間',
                                         max_length=255,
                                         widget=forms.TextInput(attrs={
                                             'class': 'input-text'
                                         }))
    close_day = forms.CharField(required=False,
                                label='閉館日',
                                max_length=255,
                                widget=forms.TextInput(attrs={
                                    'class': 'input-text'
                                }))
    accept_age = forms.CharField(required=False,
                                 label='入所可能年齢',
                                 max_length=255,
                                 widget=forms.TextInput(attrs={
                                     'class': 'input-text'
                                 }))
    stable_food = forms.BooleanField(required=False,
                                     label='主食あり',
                                     label_suffix='',
                                     widget=forms.CheckboxInput(attrs={
                                         'type': 'checkbox'
                                     }))
    temporary_childcare = forms.BooleanField(required=False,
                                             label='一時預け入れ可能',
                                             label_suffix='',
                                             widget=forms.CheckboxInput(attrs={
                                                 'type': 'checkbox'
                                             }))
    overnight_childcare = forms.BooleanField(required=False,
                                             label='夜間預け入れ可能',
                                             label_suffix='',
                                             widget=forms.CheckboxInput(attrs={
                                                 'type': 'checkbox'
                                             }))
    allday_childcare = forms.BooleanField(required=False,
                                          label='日中預け入れ可能',
                                          label_suffix='',
                                          widget=forms.CheckboxInput(attrs={
                                              'type': 'checkbox'
                                          }))
    evaluation = forms.BooleanField(required=False,
                                    label='第三者評価受審有',
                                    label_suffix='',
                                    widget=forms.CheckboxInput(attrs={
                                        'type': 'checkbox'
                                    }))
    evaluation_url = forms.URLField(required=False,
                                    label='受審URL',
                                    max_length=255,
                                    widget=forms.URLInput(attrs={
                                        'class': 'input-text'
                                    }))
    organizer = forms.CharField(required=False,
                                max_length=255,
                                label='運営者',
                                widget=forms.TextInput(attrs={
                                    'class': 'input-text'
                                }))
    event = forms.CharField(required=False,
                            max_length=1000,
                            label='イベント内容',
                            widget=forms.Textarea(attrs={
                                'class': 'input-text'
                            }))
    service = forms.CharField(required=False,
                              max_length=1000,
                              label='サービス内容',
                              widget=forms.Textarea(attrs={
                                  'class': 'input-text'
                              }))
    policy = forms.CharField(required=False,
                             max_length=1000,
                             label='ポリシー',
                             widget=forms.Textarea(attrs={
                                 'class': 'input-text'
                             }))
    promise = forms.CharField(required=False,
                              label='約束',
                              max_length=1000,
                              widget=forms.Textarea(attrs={
                                  'class': 'input-text'
                              }))

    class Meta:
        model = Nursery
        fields = (
            'ward', 'license', 'school_type', 'name', 'postcode', 'address', 'station_info', 'url', 'phone_number',
            'fax_number', 'thumbnail_url', 'latitude', 'longitude', 'open_time_weekday',
            'open_time_saturday', 'close_day', 'accept_age', 'stable_food', 'temporary_childcare',
            'overnight_childcare', 'allday_childcare', 'evaluation', 'evaluation_url',
            'organizer', 'event', 'service', 'policy', 'promise'
        )
