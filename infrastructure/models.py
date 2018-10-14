import json
from typing import Dict, List
from urllib.parse import urlparse
from itertools import groupby

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.lru_cache import lru_cache
from django_mysql.models import Bit1BooleanField
from django.db.models.aggregates import Max

from infrastructure.consts import NURSERY_FREE_NUM_FMT
from infrastructure.managers import MyUserManager
from infrastructure.query import get_near_stations


class Age(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    is_active = Bit1BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = False
        db_table = 'ages'

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        max_length=20,
        unique=True
    )
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    child_age = models.ForeignKey(Age, models.PROTECT, null=True)
    is_active = Bit1BooleanField(default=True)
    is_admin = Bit1BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        managed = True
        db_table = 'users'

    @classmethod
    def is_exist_username(cls, username):
        try:
            cls.objects.get(email=username)
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_user(cls, user_id: int):
        return cls.objects.get(pk=user_id)


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
    def default_thumbnail_url(self) -> str:
        return self.thumbnail_url or 'http://placehold.it/555x370'

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

    @classmethod
    def get_nursery(cls, nursery_id: int):
        try:
            return cls.objects.select_related('license', 'school_type').filter(id=nursery_id).first()
        except cls.DoesNotExist:
            return None


class NurseryFreeNum(models.Model):
    age = models.ForeignKey(Age, models.PROTECT)
    nursery = models.ForeignKey(Nursery, models.PROTECT)
    free_num = models.IntegerField(null=False)
    is_active = Bit1BooleanField(default=True)
    modified_date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'nursery_free_nums'
        managed = False

    @classmethod
    def get_free_nums(cls, nursery_ids: List[int]) -> dict:
        free_nums = cls.objects.filter(nursery__id__in=nursery_ids)

        ret = dict()
        for k, g in groupby(sorted(free_nums, key=lambda x: (x.nursery_id, x.age_id)),
                            key=lambda x: (x.nursery_id, x.age_id)):
            free_num = sorted(list(g), key=lambda x: x.modified_date, reverse=True)[0]
            ret[NURSERY_FREE_NUM_FMT.format(free_num.nursery_id, free_num.age_id)] = free_num.free_num
        return ret

    @classmethod
    def get_last_updated_date(cls, nursery_ids: List[int]) -> dict:
        dates = cls.objects.filter(nursery__id__in=nursery_ids).values('nursery_id').annotate(
            last_updated_date=Max('modified_date'))

        ret = dict()
        for d in dates:
            ret[d['nursery_id']] = d['last_updated_date']
        return ret

    @classmethod
    def bulk_insert(cls, entities):
        cls.objects.bulk_create([cls(age=entity.age, nursery=entity.nursery, free_num=entity.free_num,
                                     modified_date=entity.modified_date) for entity in entities])


class NurseryScore(models.Model):
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
    def upsert(cls, entities):
        for entity in entities:
            cls.objects.update_or_create(nursery=entity.nursery, age=entity.age, year=entity.year,
                                         defaults={'score': entity.score, 'hierarchy': entity.hierarchy})


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


class UserNurseryMapping(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, models.PROTECT)
    nursery = models.ForeignKey(Nursery, models.PROTECT)
    is_active = Bit1BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'user_nursery_mappings'


class NurseryBookmarks(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, models.PROTECT)
    nursery = models.ForeignKey(Nursery, models.PROTECT)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'nursery_bookmarks'
