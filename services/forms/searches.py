from typing import Optional
from django import forms

from infrastructure.models import Age, City, License, SchoolType, Station, Ward
from infrastructure.repository.query import get_near_stations
from services.converter import convert_address_to_geocode


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
                                                             Ward.objects.filter(city_id=city_id, is_active=True)],
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


class SearchAddressForm(forms.Form):
    address = forms.CharField(required=False,
                              label='住所から検索',
                              max_length=255,
                              widget=forms.TextInput(attrs={
                                  'class': 'form-control input-text search-fields',
                                  'placeholder': '住所から検索',
                              }))

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            return address
        try:
            convert_address_to_geocode(address)
            return address
        except ValueError:
            raise forms.ValidationError('住所が正しくありません')


class SearchTypeForm(forms.Form):
    age = forms.ChoiceField(required=True,
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


class SearchScoreForm(forms.Form):
    FATHER_CHOICES = [
        (0, '選択してください'),
        (20, '月20日以上勤務し、日中8時間以上の就労が常態'),
        (19, '月20日以上勤務し、日中7時間以上の就労が常態'),
        (19, '月18日以上勤務し、日中8時間以上の就労が常態'),
        (18, '月20日以上勤務し、日中6時間以上の就労が常態'),
        (18, '月18日以上勤務し、日中7時間以上の就労が常態'),
        (18, '月16日以上勤務し、日中8時間以上の就労が常態'),
        (16, '月16日以上勤務し、日中6時間以上の就労が常態'),
        (16, '月12日以上勤務し、日中8時間以上の就労が常態'),
        (14, '月20日以上勤務し、日中4時間以上の就労が常態'),
        (14, '月16日以上勤務し、日中5時間以上の就労が常態'),
        (12, '月16日以上勤務し、日中4時間以上の就労が常態'),
        (12, '月14日以上勤務し、日中5時間以上の就労が常態'),
        (12, '月12日以上勤務し、日中6時間以上の就労が常態'),
        (10, '月12日以上勤務し、日中4時間以上の就労が常態'),
        (8, '上記のほか、勤務の態様から保育できないと認められる場合'),
        (12, '月16日以上、日中5時間以上月収25000円以上の就労が常態'),
        (10, '月12日以上、日中4時間以上月収25000円未満の就労が常態'),
        (8, '上記のほか、勤務の態様から保育できないと認められる場合'),
        (8, '出産前後の休養のため保育にあたることができない場合'),
        (20, 'おおむね3カ月程度の入院もしくは入院を決定された場合'),
        (20, '常時病臥、重度の精神性疾患に罹患し定期的に通院'),
        (18, '安静を要する状態(自分の身の回りのことができない場合'),
        (14, '負傷や疾病のため、保育にあたることができないと認められる場合'),
        (14, '一般療養で定期的に通院を要し、家事困難'),
        (14, '一般療養で定期的に通院を要するが、家事は可能'),
        (20, '身障手帳1から2級、愛の手帳1から3度'),
        (16, '身障手帳3級、愛の手帳4度'),
        (12, '身障手帳4級'),
        (8, '身障手帳5級以下'),
        (16, '月16日以上、1日6時間以上の通所の付添'),
        (16, '月12日以上、1日4時間以上の通所の付添'),
        (16, '上記以外の付添'),
        (17, '日中1人での常時観察・全面的身体介護をしている場合'),
        (17, '上記以外の常時観察・全面的身体介護をしている場合'),
        (17, '病人や心身に障害のある方を常時看護、介護している場合'),
        (17, '日常生活動作の一部介助が必要'),
        (17, '上記以外の介護・看護'),
        (20, '災害による家屋の損傷、その災害復旧のため、保育に当たることができない場合'),
        (12, '月20日以上勤務し、日中8時間以上の常勤の就労が内定している場合'),
        (8, '上記以外の就労が内定している場合 （起業準備を含む）'),
        (4, '求職活動中のため'),
        (20, '就学・技能習得のため保育にあたることができない場合'),
        (20, '死別、離別、行方不明、拘禁'),
        (20, '前各号に掲げるもののほか、明らかに保育に当たることができないと認められる場合（児童虐待、配偶者からの暴力を含む）')
    ]
    MOTHER_CHOICE = [
        (0, '選択してください'),
        (20, '月20日以上勤務し、日中8時間以上の就労が常態'),
        (19, '月20日以上勤務し、日中7時間以上の就労が常態'),
        (19, '月18日以上勤務し、日中8時間以上の就労が常態'),
        (18, '月20日以上勤務し、日中6時間以上の就労が常態'),
        (18, '月18日以上勤務し、日中7時間以上の就労が常態'),
        (18, '月16日以上勤務し、日中8時間以上の就労が常態'),
        (16, '月16日以上勤務し、日中6時間以上の就労が常態'),
        (16, '月12日以上勤務し、日中8時間以上の就労が常態'),
        (14, '月20日以上勤務し、日中4時間以上の就労が常態'),
        (14, '月16日以上勤務し、日中5時間以上の就労が常態'),
        (12, '月16日以上勤務し、日中4時間以上の就労が常態'),
        (12, '月14日以上勤務し、日中5時間以上の就労が常態'),
        (12, '月12日以上勤務し、日中6時間以上の就労が常態'),
        (10, '月12日以上勤務し、日中4時間以上の就労が常態'),
        (8, '上記のほか、勤務の態様から保育できないと認められる場合'),
        (12, '月16日以上、日中5時間以上月収25000円以上の就労が常態'),
        (10, '月12日以上、日中4時間以上月収25000円未満の就労が常態'),
        (8, '上記のほか、勤務の態様から保育できないと認められる場合'),
        (8, '出産前後の休養のため保育にあたることができない場合'),
        (20, 'おおむね3カ月程度の入院もしくは入院を決定された場合'),
        (20, '常時病臥、重度の精神性疾患に罹患し定期的に通院'),
        (18, '安静を要する状態(自分の身の回りのことができない場合）'),
        (14, '負傷や疾病のため、保育にあたることができないと認められる場合'),
        (14, '一般療養で定期的に通院を要し、家事困難'),
        (14, '一般療養で定期的に通院を要するが、家事は可能'),
        (20, '身障手帳1から2級、愛の手帳1から3度'),
        (16, '身障手帳3級、愛の手帳4度'),
        (12, '身障手帳4級'),
        (8, '身障手帳5級以下'),
        (16, '月16日以上、1日6時間以上の通所の付添'),
        (16, '月12日以上、1日4時間以上の通所の付添'),
        (16, '上記以外の付添'),
        (17, '日中1人での常時観察・全面的身体介護をしている場合'),
        (17, '上記以外の常時観察・全面的身体介護をしている場合'),
        (17, '病人や心身に障害のある方を常時看護、介護している場合'),
        (17, '日常生活動作の一部介助が必要'),
        (17, '上記以外の介護・看護'),
        (20, '災害による家屋の損傷、その災害復旧のため、保育に当たることができない場合'),
        (12, '月20日以上勤務し、日中8時間以上の常勤の就労が内定している場合'),
        (8, '上記以外の就労が内定している場合 （起業準備を含む）'),
        (4, '求職活動中のため'),
        (20, '就学・技能習得のため保育にあたることができない場合'),
        (20, '死別、離別、行方不明、拘禁'),
        (20, '前各号に掲げるもののほか、明らかに保育に当たることができないと認められる場合（児童虐待、配偶者からの暴力を含む）')
    ]
    ADJUST_SCORE = [
        (0, '選択してください'),
        (4, '生活保護受給世帯'),
        (6, 'ひとり親世帯'),
        (4, 'ひとり親に準ずる世帯'),
        (6, '世帯の生計中心者が失業、倒産等により、生計維持のため就労を要するとき'),
        (1, '区内在住の兄弟姉妹で異なる区内認可保育園に在園しており、第一希望で同一区内認可保育園に転園申請する場合'),
        (3, '兄弟姉妹が区内認可保育園に在園している区内在住児童が、区内認可保育園・家庭的保育事業・小規模保育事業に入園申請する場合'),
        (4, '世帯の生計中心者が失業、倒産等により、生計維持のため就労を要するとき'),
        (2, '集団保育を必要とする障害児等で、特別支援保育審査会で認められた場合'),
        (2, '申込児が障害を有するために、通所施設(品川児童学園等)に通所、または病院に定期的に通院している場合'),
        (1, '入所を希望する児童を品川区の保育料助成制度の対象となる認可外保育施設等(都道府県に届出がある施設のうち認証保育所を除く）に月額20,000円以上で預けている場合'),
        (3, '入所を希望する児童を品川区の保育料助成制度の対象となる認可外保育施設等(都道府県に届出がある施設のうち認証保育所を除く）に月額20,000円未満で預けている場合'),
        (1, '入所を希望する児童を品川区の保育料助成制度の対象とならない認可外保育施設等(都道府県に届出がある施設のうち認証保育所を除く）に月額20,000円以上で設けている場合'),
        (2, '入所を希望する児童を品川区の保育料助成制度の対象とならない認可外保育施設等(都道府県に届出がある施設のうち認証保育所を除く）に月額20,000円未満で預けている場合'),
        (2, '入所を希望する児童を認証保育所に預けている場合'),
        (2, '入所を希望する児童を家庭的保育事業・小規模保育事業に預けている場合'),
        (2, '年齢上上限のある区内認可保育園（日本音楽学校保育園、短時間保育室）を卒園する場合'),
        (1, '保護者が単身赴任をしている場合'),
        (1, '求職中で求職活動を証明できる公的な書類の提出がある場合 （ハローワークカードなど）'),
        (1, '兄弟姉妹で同時に区内認可保育園・家庭的保育事業・小規模保育事業に入園申請する場合'),
        (4, '育児休業法等に基づく育休取得（1年以上）により、育休取得前に品川区認可保育園を退園し、育児休業明けに再'),
        (4, '入園する場合（育児休業取得対象児童も加点対象）'),
        (-1, '勤務先（仕事場）に児童を同伴している場合※ただし、職場が危険業種の場合は対象外とする'),
        (-1, '同一世帯に未申請児（介護を要する児童を除く）がいる場合'),
        (-1, '申込締切日時点で給与明細等で確認できる勤務実績が3カ月に満たない場合（1カ月以内の転職等を除く）'),
        (-2, '申込締切日時点で育休取得中であり、利用開始月までには復職するが利用開始後3カ月以内に出産予定で、かつ産休取得後に育休取得予定の場合'),
        (-10, '正当な理由もなく、保育料（区立幼稚園・区立認定こども園含む）を滞納している場合')
    ]
    HIERARCHY = [
        (0, '選択してください'),
        ('A', '生活保護世帯'),
        ('B', '当年度分区市町村民税　非課税世帯'),
        ('C1', '当年度分区市町村民税　均等割のみの世帯'),
        ('C2', '当年度分区市町村民税　所得割5,000円未満'),
        ('C3', '当年度分区市町村民税　所得割5,000円以上48,700円未満'),
        ('D1', '当年度分区市町村民税　所得割48,700円以上50,500円未満'),
        ('D2', '当年度分区市町村民税　所得割50,500円以上59,800円未満'),
        ('D3', '当年度分区市町村民税　所得割59,800円以上68,500円未満'),
        ('D4', '当年度分区市町村民税　所得割68,500円以上88,600円未満'),
        ('D5', '当年度分区市町村民税　所得割88,600円以上108,600円未満'),
        ('D6', '当年度分区市町村民税　所得割108,600円以上128,500円未満'),
        ('D7', '当年度分区市町村民税　所得割128,500円以上148,600円未満'),
        ('D8', '当年度分区市町村民税　所得割148,600円以上171,600円未満'),
        ('D9', '当年度分区市町村民税　所得割171,600円以上204,900円未満'),
        ('D10', '当年度分区市町村民税　所得割204,900円以上228,800円未満'),
        ('D11', '当年度分区市町村民税　所得割228,800円以上252,900円未満'),
        ('D12', '当年度分区市町村民税　所得割252,900円以上276,800円未満'),
        ('D13', '当年度分区市町村民税　所得割276,800円以上300,800円未満'),
        ('D14', '当年度分区市町村民税　所得割300,800円以上322,000円未満'),
        ('D15', '当年度分区市町村民税　所得割322,000円以上338,000円未満'),
        ('D16', '当年度分区市町村民税　所得割338,000円以上354,000円未満'),
        ('D17', '当年度分区市町村民税　所得割354,000円以上370,000円未満'),
        ('D18', '当年度分区市町村民税　所得割370,000円以上440,200円未満'),
        ('D19', '当年度分区市町村民税　所得割440,200円以上500,200円未満'),
        ('D20', '当年度分区市町村民税　所得割500,200円以上560,200円未満'),
        ('D21', '当年度分区市町村民税　所得割560,200円以上665,000円未満'),
        ('D22', '当年度分区市町村民税　所得割665,000円以上772,600円未満'),
        ('D23', '当年度分区市町村民税　所得割887,500円以上1,031,300円未満'),
        ('D24', '当年度分区市町村民税　所得割1,031,300円以上'),
        ('D25', '当年度分区市町村民税　所得割322,000円以上338,000円未満')
    ]
    father_score = forms.ChoiceField(required=True,
                                     label='父の基本指数',
                                     choices=FATHER_CHOICES,
                                     widget=forms.Select(attrs={
                                         'class': 'selectpicker search-fields',
                                         'onChange': 'calc(this.form)',
                                     }))
    mother_score = forms.ChoiceField(required=True,
                                     label='母の基本指数',
                                     choices=MOTHER_CHOICE,
                                     widget=forms.Select(attrs={
                                         'class': 'selectpicker search-fields',
                                         'onChange': 'calc(this.form)',
                                     }))
    adjust_score = forms.ChoiceField(required=True,
                                     label='調整指数',
                                     choices=ADJUST_SCORE,
                                     widget=forms.Select(attrs={
                                         'class': 'selectpicker search-fields',
                                         'onChange': 'calc(this.form)',
                                     }))
    hierarchy_score = forms.ChoiceField(required=True,
                                        label='階層',
                                        choices=HIERARCHY,
                                        widget=forms.Select(attrs={
                                            'class': 'selectpicker search-fields',
                                            'onChange': 'judge(this.form)',
                                        }))
