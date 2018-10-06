import datetime
import json
from typing import Dict
from urllib.parse import urlparse

from django.db import models
from django.utils import timezone
from django.utils.lru_cache import lru_cache
from django_mysql.models import Bit1BooleanField

from infrastructure.query import get_near_stations

DEFAULT_THUMBNAIL_URL = ''


class Age(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    is_active = Bit1BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'ages'


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    is_active = Bit1BooleanField(default=True)
    home_url = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'cities'

    @classmethod
    @lru_cache()
    def city(cls, city_id: int):
        """ 既に収集済みかを確認し、なかったらsaveする
        """
        return cls.objects.get(pk=city_id)

    def __str__(self):
        return self.name


class Ward(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, models.PROTECT)
    name = models.CharField(max_length=255, null=False)
    home_url = models.URLField()
    nursery_info_url = models.URLField()
    nursery_free_num_info_url = models.URLField()
    is_active = Bit1BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'wards'

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return self.city.name + self.name

    @property
    def nursery_info_name(self):
        hostname = urlparse(self.nursery_info_url).hostname
        if hostname == 'linkdata.org':
            if self.city_id == 1:
                return 'LinkData' + ' ' + '「保育園（23区)」'
            else:
                return 'LinkData' + ' ' + '「横浜市の保育所等の施設情報」'
        elif hostname == 'opendata-catalogue.metro.tokyo.jp':
            return '東京都オープンデータカタログサイト'
        return 'リンク'

    @property
    def nursery_free_num_info(self):
        home_hostname = urlparse(self.home_url).hostname
        free_num_hostname = urlparse(self.nursery_free_num_info_url).hostname

        if home_hostname == free_num_hostname and self.city_id == 1:
            return self.name + '公式サイト'
        elif home_hostname == free_num_hostname and self.city_id == 2:
            return 'ヨコハマはぴねすぽっと'
        return 'リンク'

    @classmethod
    @lru_cache()
    def get_wards(cls, city_id: int) -> Dict[int, str]:
        wards = cls.objects.filter(city_id=city_id, is_active=True).values('id', 'name')
        return json.dumps(list(wards))


class License(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    is_active = Bit1BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'licenses'

    def __str__(self):
        return self.name


class SchoolType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    is_active = Bit1BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'school_types'

    def __str__(self):
        return self.name


class Nursery(models.Model):
    id = models.AutoField(primary_key=True)
    ward = models.ForeignKey(Ward, models.PROTECT)
    license = models.ForeignKey(License, models.PROTECT)
    school_type = models.ForeignKey(SchoolType, models.PROTECT)
    name = models.CharField(max_length=255, null=False)
    is_active = Bit1BooleanField(default=True)
    postcode = models.CharField(max_length=8)
    address = models.CharField(max_length=255, null=False)
    station_info = models.CharField(max_length=255, null=True)
    url = models.URLField()
    phone_number = models.CharField(max_length=15, null=False)
    fax_number = models.CharField(max_length=15)
    thumbnail_url = models.URLField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9, null=False)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, null=False)
    open_time_weekday = models.CharField(max_length=255)
    open_time_saturday = models.CharField(max_length=255)
    close_day = models.CharField(max_length=1000)
    accept_age = models.CharField(max_length=255)
    stable_food_info = models.CharField(max_length=1000)
    stable_food = Bit1BooleanField()
    temporary_childcare = Bit1BooleanField()
    overnight_childcare = Bit1BooleanField()
    allday_childcare = Bit1BooleanField()
    evaluation = Bit1BooleanField()
    eco = Bit1BooleanField()
    evaluation_url = models.URLField()
    organizer = models.CharField(max_length=255)
    event = models.CharField(max_length=1000)
    service = models.CharField(max_length=1000)
    policy = models.CharField(max_length=1000)
    promise = models.CharField(max_length=1000)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'nurseries'

    @property
    def thumbnail_search_word(self) -> str:
        """ 画像検索用の文字列を返す
        """
        name = self.name.split()[0]
        return "{} {}".format(self.ward.city.name, name)

    @property
    @lru_cache()
    def free_num_info_url(self) -> str:
        """ 空き情報掲載URLを返す
        """
        return Ward.objects.filter(id=self.ward_id).first().nursery_free_num_info_url

    @property
    def default_thumbnail_url(self) -> str:
        """ 保育園のサムネイル画像を返す。もし画像がなかった場合はデフォルトの画像を返す
        """
        if self.thumbnail_url:
            return self.thumbnail_url
        return DEFAULT_THUMBNAIL_URL

    @property
    def default_service(self) -> str:
        if self.service:
            return self.service
        return '詳しくは公式サイトをご覧下さい'

    @property
    def default_policy(self) -> str:
        if self.policy:
            return self.policy
        return '詳しくは公式サイトをご覧下さい'

    @property
    def default_event(self) -> str:
        if self.event:
            return self.event
        return '詳しくは公式サイトをご覧下さい'

    @property
    def default_open_time_weekday(self) -> str:
        if self.close_day:
            return self.close_day
        return '詳しくは公式サイトをご覧下さい'

    @property
    def default_open_time_saturday(self) -> str:
        if self.close_day:
            return self.close_day
        return '詳しくは公式サイトをご覧下さい'

    @property
    def default_close_day(self) -> str:
        if self.close_day:
            return self.close_day
        return '詳しくは公式サイトをご覧下さい'

    @property
    def free_nums(self):
        """ 空き情報
        :rtype: NurseryFreeNum
        """
        return NurseryFreeNum(self)

    @property
    def scores(self):
        """ 実績指数情報
        :rtype: NurseryScores
        """
        return NurseryScore(self)


class NurseryFreeNum:
    def __init__(self, nursery):
        self.nursery = nursery
        self._status = None
        self._latest_modified_date = None

    @property
    def latest_modified_date(self) -> datetime or str:
        if not self._latest_modified_date:
            self._latest_modified_date = NurseryStatus.latest_modified_date(self.nursery.id)
        return self._latest_modified_date or ''

    @property
    def status(self) -> Dict[int, int]:
        """ 指定された保育園の最新の空き情報を返す
        :rtype: Dict[age_id, free_num]
        """
        if not self._status:
            if not self.latest_modified_date:
                self._status = {}
                return self._status
            self._status = NurseryStatus.latest_nursery_free_nums(nursery_id=self.nursery.id,
                                                                  modified_date=self.latest_modified_date)
        return self._status

    @property
    def free_num_not_one(self) -> int:
        """ 0歳の空き情報を返す
        """
        return int(self.status.get(1, 0))

    @property
    def free_num_one_year_old(self) -> int:
        """ 1歳の空き情報を返す
        """
        return int(self.status.get(2, 0))

    @property
    def free_num_two_year_old(self) -> int:
        """ 2歳の空き情報を返す
        """
        return int(self.status.get(3, 0))

    @property
    def free_num_three_year_old(self) -> int:
        """ 3歳の空き情報を返す
        """
        return int(self.status.get(4, 0))

    @property
    def free_num_four_year_old(self) -> int:
        """ 4歳の空き情報を返す
        """
        return int(self.status.get(5, 0))

    @property
    def free_num_extent(self) -> int:
        """ 延長の空き情報を返す
        """
        return int(self.status.get(6, 0))

    @property
    def free_num_other(self) -> int:
        """ その他の空き情報を返す
        """
        return int(self.status.get(7, 0))

    @property
    def sum_free_num(self) -> int:
        return sum(self.status.values())

    def is_opening(self) -> bool:
        """ 指定された年齢の空きがあるかを返す
        """
        if self.sum_free_num > 0:
            return True
        return False

    def is_opening_by_age(self, age_id) -> bool:
        """ 指定された年齢の空きがあるかを返す
        """
        free_num = self.status.get(int(age_id), 0)
        if free_num > 0:
            return True
        return False


class NurseryScore:
    def __init__(self, nursery):
        self.nursery = nursery
        self._score = None
        self._latest_updated_year = None

    @property
    def latest_updated_year(self) -> int or None:
        if not self._latest_updated_year:
            self._latest_updated_year = NurseryScores.latest_updated_year(self.nursery.id)
        return self._latest_updated_year

    @property
    def score(self) -> Dict[int, int]:
        if not self._score:
            if not self.latest_updated_year:
                self._score = {}
                return self._score
            self._score = NurseryScores.latest_nursery_scores(self.nursery.id, self.latest_updated_year)
        return self._score

    @property
    def score_not_one(self) -> str:
        """ 0歳の実績入所指数を返す
        """
        return str(self.score.get(1, '-') or '-')

    @property
    def score_one_year_old(self) -> str:
        """ 1歳の実績入所指数を返す
        """
        return str(self.score.get(2, '-') or '-')

    @property
    def score_two_year_old(self) -> str:
        """ 2歳の実績入所指数を返す
        """
        return str(self.score.get(3, '-') or '-')

    @property
    def score_three_year_old(self) -> str:
        """ 3歳の実績入所指数を返す
        """
        return str(self.score.get(4, '-') or '-')

    @property
    def score_four_year_old(self) -> str:
        """ 4歳の実績入所指数を返す
        """
        return str(self.score.get(5, '-') or '-')

    @property
    def score_extent(self) -> str:
        """ 延長の実績入所指数を返す
        """
        return str(self.score.get(6, '-') or '-')


class NurseryStatus(models.Model):
    id = models.AutoField(primary_key=True)
    age = models.ForeignKey(Age, models.PROTECT)
    nursery = models.ForeignKey(Nursery, models.PROTECT)
    free_num = models.IntegerField()
    is_active = Bit1BooleanField(default=True)
    modified_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'nursery_status'

    @classmethod
    @lru_cache()
    def latest_modified_date(cls, nursery_id: int) -> datetime or None:
        try:
            latest_modified_date = cls.objects.filter(
                nursery_id=nursery_id).latest('modified_date').modified_date
            return latest_modified_date
        except NurseryStatus.DoesNotExist:
            return None

    @classmethod
    @lru_cache()
    def latest_nursery_free_nums(cls, nursery_id: int, modified_date: datetime) -> Dict[int, int]:
        return {ns.age.id: ns.free_num for ns in cls.objects.select_related('age').filter(
            nursery_id=nursery_id, modified_date=modified_date, is_active=True)}


class NurseryScores(models.Model):
    id = models.AutoField(primary_key=True)
    nursery = models.ForeignKey(Nursery, models.PROTECT)
    age = models.ForeignKey(Age, models.PROTECT)
    year = models.CharField(max_length=10)
    score = models.IntegerField(default=None)
    hierarchy = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    is_active = Bit1BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'nursery_scores'

    @classmethod
    @lru_cache()
    def latest_updated_year(cls, nursery_id: int) -> int or None:
        try:
            latest_updated_year = cls.objects.filter(
                nursery_id=nursery_id).latest('year').year
            return latest_updated_year
        except NurseryScores.DoesNotExist:
            return None

    @classmethod
    @lru_cache()
    def latest_nursery_scores(cls, nursery_id: int, year: int) -> Dict[int, int]:
        return {ns.age.id: ns.score for ns in cls.objects.select_related('age').filter(
            nursery_id=nursery_id, year=year, is_active=True)}


class CrawledGuid(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'crawled_guid'

    @classmethod
    @lru_cache()
    def is_crawled(cls, guid: str) -> bool:
        """ 既に収集済みかを確認し、なかったらsaveする
        """
        return True if not cls.objects.get_or_create(guid=guid)[1] else False


class Line(models.Model):
    id = models.AutoField(primary_key=True)
    api_id = models.IntegerField(null=False)
    city = models.ForeignKey(City, models.PROTECT)
    name = models.CharField(max_length=255, null=False)
    is_active = Bit1BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'lines'

    @classmethod
    @lru_cache()
    def line(cls, api_line_id: int):
        return cls.objects.get(api_id=api_line_id)


class Station(models.Model):
    id = models.AutoField(primary_key=True)
    api_id = models.IntegerField(null=False)
    line = models.ForeignKey(Line, models.PROTECT)
    name = models.CharField(max_length=255, null=False)
    is_active = Bit1BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'stations'

    @classmethod
    @lru_cache()
    def get_stations(cls, ward_id: int):
        ward = cls.objects.filter(id=ward_id).first()
        return get_near_stations(ward.latitude, ward.longitude)

    @classmethod
    @lru_cache()
    def get_stations_api(cls, ward_id: int) -> Dict[int, str]:
        ward = cls.objects.filter(id=ward_id).first()
        stations = []
        for i, station in enumerate(get_near_stations(ward.latitude, ward.longitude)):
            stations.append({
                'id': station['id'],
                'name': station['name']
            })
        stations.insert(0, {'id': "", 'name': '駅を選択'})
        stations = json.dumps(stations)
        return stations


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    text = models.CharField(max_length=1000, null=False)
    mail = models.EmailField(null=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'contacts'
