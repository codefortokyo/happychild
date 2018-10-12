from typing import Optional
from django import forms

from infrastructure.models import Age, City, License, SchoolType, Station, Ward
from infrastructure.query import get_near_stations


class SearchLocationForm(forms.Form):
    city = forms.ChoiceField(required=True,
                             choices=[(0, '市を選択')] + [(city.id, city.name) for city in
                                                      City.objects.filter(is_active=True)],
                             widget=forms.Select(attrs={
                                 'id': 'city',
                                 'class': 'selectpicker search-fields',
                                 'data-live-search': 'true',
                                 'data-live-search-placeholder': '市を検索'
                             }))
    ward = forms.ChoiceField(required=True,
                             choices=[('', '区を選択')],
                             widget=forms.Select(attrs={
                                 'id': 'ward',
                                 'class': 'selectpicker search-fields',
                                 'data-live-search': 'true',
                                 'data-live-search-placeholder': '区を検索',
                             }))
    station = forms.ChoiceField(required=False,
                                choices=[('', '駅を選択')],
                                widget=forms.Select(attrs={
                                    'id': 'station',
                                    'class': 'selectpicker search-fields',
                                    'data-live-search': 'true',
                                    'data-live-search-placeholder': '駅を検索',
                                }))
    latitude = forms.FloatField(required=False,
                                widget=forms.HiddenInput(attrs={
                                    'id': 'latitude'
                                }))
    longitude = forms.FloatField(required=False,
                                 widget=forms.HiddenInput(attrs={
                                     'id': 'longitude'
                                 }))

    def clean(self):
        ward_id = self.cleaned_data.get('ward')
        latitude = self.cleaned_data.get('latitude')
        longitude = self.cleaned_data.get('longitude')

        if not ward_id:
            if not latitude or not longitude:
                raise forms.ValidationError('検索対象の区または現在位置情報を設定してください')
        return self.cleaned_data

    def __init__(self, city_id: Optional[int] = None, ward_id: Optional[int] = None, latitude: Optional[float] = None,
                 longitude: Optional[float] = None, *args, **kwargs):
        super(SearchLocationForm, self).__init__(*args, **kwargs)
        if city_id:
            self.fields['ward'] = forms.ChoiceField(required=False,
                                                    choices=[(w.id, w.name) for w in
                                                             Ward.objects.filter(city_id=city_id)],
                                                    widget=forms.Select(attrs={
                                                        'id': 'ward',
                                                        'class': 'selectpicker search-fields',
                                                        'data-live-search': 'true',
                                                        'data-live-search-placeholder': '区を検索'
                                                    }))

        if latitude and longitude:
            self.fields['station'] = forms.ChoiceField(required=False,
                                                       choices=[('', '駅を選択')] + [(s['id'], s['name']) for s in
                                                                                 get_near_stations(latitude,
                                                                                                   longitude)],
                                                       widget=forms.Select(attrs={
                                                           'id': 'station',
                                                           'class': 'selectpicker search-fields',
                                                           'data-live-search': 'true',
                                                           'data-live-search-placeholder': '駅を検索'
                                                       }))
        elif ward_id:
            self.fields['station'] = forms.ChoiceField(required=False,
                                                       choices=[('', '駅を選択')] + [(s['id'], s['name']) for s in
                                                                                 Station.get_stations(ward_id)],
                                                       widget=forms.Select(attrs={
                                                           'id': 'station',
                                                           'class': 'selectpicker search-fields',
                                                           'data-live-search': 'true',
                                                           'data-live-search-placeholder': '駅を検索'
                                                       }))


class SearchTypeForm(forms.Form):
    age = forms.ChoiceField(required=False,
                            choices=[('', '年齢を選択')] + [(age.id, age.name) for age in
                                                       Age.objects.filter(is_active=True)],
                            widget=forms.Select(attrs={
                                'class': 'selectpicker search-fields',
                            }))
    license = forms.ChoiceField(required=False,
                                choices=[('', '保育園種別を選択')] + [(licence.id, licence.name) for licence in
                                                              License.objects.filter(is_active=True)],
                                widget=forms.Select(attrs={
                                    'class': 'selectpicker search-fields',
                                }))
    school_type = forms.ChoiceField(required=False,
                                    choices=[('', '保育園運営種別を選択')] + [(st.id, st.name) for st in
                                                                    SchoolType.objects.filter(is_active=True)],
                                    widget=forms.Select(attrs={
                                        'class': 'selectpicker search-fields',
                                    }))


class SearchFeatureForm(forms.Form):
    is_opening = forms.BooleanField(required=False,
                                    label='現在空きがある',
                                    label_suffix='',
                                    widget=forms.CheckboxInput(attrs={
                                        'type': 'checkbox'
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
