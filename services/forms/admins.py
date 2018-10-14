from django import forms

from infrastructure.models import (
    Nursery,
    Ward,
    License,
    SchoolType,
    NurseryDefaultTourSetting,
)


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


class NurseryFreeNumForm(forms.Form):
    free_num_not_one = forms.IntegerField(required=True,
                                          label='0歳',
                                          widget=forms.TextInput(attrs={
                                              'class': 'input-text'
                                          }))
    free_num_one_year_old = forms.IntegerField(required=True,
                                               label='1歳',
                                               widget=forms.TextInput(attrs={
                                                   'class': 'input-text'
                                               }))
    free_num_two_year_old = forms.IntegerField(required=True,
                                               label='2歳',
                                               widget=forms.TextInput(attrs={
                                                   'class': 'input-text'
                                               }))
    free_num_three_year_old = forms.IntegerField(required=True,
                                                 label='3歳',
                                                 widget=forms.TextInput(attrs={
                                                     'class': 'input-text'
                                                 }))
    free_num_four_year_old = forms.IntegerField(required=True,
                                                label='4歳',
                                                widget=forms.TextInput(attrs={
                                                    'class': 'input-text'
                                                }))
    free_num_extent = forms.IntegerField(required=True,
                                         label='延長',
                                         widget=forms.TextInput(attrs={
                                             'class': 'input-text'
                                         }))


class NurseryScoreForm(forms.Form):
    year = forms.IntegerField(required=True,
                              label='年度',
                              widget=forms.TextInput(attrs={
                                  'class': 'input-text'
                              }))
    score_not_one = forms.IntegerField(required=False,
                                       label='0歳 指数',
                                       widget=forms.TextInput(attrs={
                                           'class': 'input-text'
                                       }))
    hierarchy_not_one = forms.CharField(required=False,
                                        max_length=255,
                                        label='0歳 階層',
                                        widget=forms.TextInput(attrs={
                                            'class': 'input-text'
                                        }))
    score_one_year_old = forms.IntegerField(required=False,
                                            label='1歳 指数',
                                            widget=forms.TextInput(attrs={
                                                'class': 'input-text'
                                            }))
    hierarchy_one_year_old = forms.CharField(required=False,
                                             max_length=255,
                                             label='1歳 階層',
                                             widget=forms.TextInput(attrs={
                                                 'class': 'input-text'
                                             }))
    score_two_year_old = forms.IntegerField(required=False,
                                            label='2歳 指数',
                                            widget=forms.TextInput(attrs={
                                                'class': 'input-text'
                                            }))
    hierarchy_two_year_old = forms.CharField(required=False,
                                             max_length=255,
                                             label='2歳 階層',
                                             widget=forms.TextInput(attrs={
                                                 'class': 'input-text'
                                             }))
    score_three_year_old = forms.IntegerField(required=False,
                                              label='3歳 指数',
                                              widget=forms.TextInput(attrs={
                                                  'class': 'input-text'
                                              }))
    hierarchy_three_year_old = forms.CharField(required=False,
                                               max_length=255,
                                               label='3歳 階層',
                                               widget=forms.TextInput(attrs={
                                                   'class': 'input-text'
                                               }))
    score_four_year_old = forms.IntegerField(required=False,
                                             label='4歳 指数',
                                             widget=forms.TextInput(attrs={
                                                 'class': 'input-text'
                                             }))
    hierarchy_four_year_old = forms.CharField(required=False,
                                              max_length=255,
                                              label='4歳 階層',
                                              widget=forms.TextInput(attrs={
                                                  'class': 'input-text'
                                              }))
    score_extent = forms.IntegerField(required=False,
                                      label='延長 指数',
                                      widget=forms.TextInput(attrs={
                                          'class': 'input-text'
                                      }))
    hierarchy_extent = forms.CharField(required=False,
                                       max_length=255,
                                       label='延長 階層',
                                       widget=forms.TextInput(attrs={
                                           'class': 'input-text'
                                       }))


class NurseryDefaultTourForm(forms.ModelForm):
    start_time = forms.TimeField(required=True,
                                 label='見学会開始予定時間',
                                 widget=forms.TimeInput(attrs={
                                     'class': 'input-text timepicker',
                                 }))
    end_time = forms.TimeField(required=True,
                               label='見学会終了予定時間',
                               widget=forms.TimeInput(attrs={
                                   'class': 'input-text timepicker',
                               }))
    capacity = forms.IntegerField(required=True,
                                  label='見学会上限人数',
                                  widget=forms.TextInput(attrs={
                                      'class': 'input-text'
                                  }))
    note = forms.CharField(required=False,
                           label='見学会の内容',
                           widget=forms.Textarea(attrs={
                               'class': 'input-text'
                           }))

    class Meta:
        model = NurseryDefaultTourSetting
        fields = ('start_time', 'end_time', 'capacity', 'note')
