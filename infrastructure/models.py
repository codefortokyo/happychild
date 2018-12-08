import datetime
import json
from typing import Dict, List, Optional
from urllib.parse import urlparse
from itertools import groupby

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.lru_cache import lru_cache
from django_mysql.models import Bit1BooleanField
from django.db.models.aggregates import Max

from infrastructure.consts import NURSERY_FREE_NUM_FMT
from infrastructure.repository.managers import MyUserManager
from infrastructure.repository.query import get_near_stations


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

    @property
    def is_organizer(self):
        try:
            UserNurseryMapping.objects.get(user_id=self.id)
            return True
        except self.DoesNotExist:
            return False


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
    url = models.URLField(max_length=1000)
    phone_number = models.CharField(max_length=15, null=False)
    fax_number = models.CharField(max_length=15)
    thumbnail_url = models.URLField(max_length=1000)
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
    evaluation_url = models.URLField(max_length=1000)
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
    free_num = models.IntegerField(null=True)
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
    def upsert(cls, nursery: Nursery, age: Age, modified_date: datetime.date, free_num: Optional[int]):
        NurseryFreeNum.objects.update_or_create(
            nursery=nursery,
            age=age,
            modified_date=modified_date,
            defaults={
                'free_num': free_num,
                'updated_at': timezone.now()
            }
        )

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
    def upsert(cls, nursery: Nursery, age: Age, year: str, score: int, hierarchy: str):
        cls.objects.update_or_create(
            nursery=nursery, age=age, year=year,
            defaults={
                'score': score,
                'hierarchy': hierarchy,
                'updated_at': timezone.now()
            }
        )

    @classmethod
    def get_last_year_score(cls, nursery_id: int, age_id: int, year='2018'):
        return cls.objects.filter(year=year, nursery_id=nursery_id, age_id=age_id).first()


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
        ward = Ward.objects.filter(id=ward_id).first()
        return get_near_stations(ward.latitude, ward.longitude)

    @classmethod
    @lru_cache()
    def get_stations_api(cls, ward_id: int) -> Dict[int, str]:
        ward = Ward.objects.filter(id=ward_id).first()
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


class NurseryBookmark(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, models.PROTECT)
    nursery = models.ForeignKey(Nursery, models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'nursery_bookmarks'

    @classmethod
    def register_bookmark(cls, user_id: int, nursery_id: int) -> None:
        if cls.objects.filter(user_id=user_id, nursery_id=nursery_id).exists():
            return
        cls.objects.create(user=CustomUser.objects.get(pk=user_id), nursery=Nursery.objects.get(pk=nursery_id))

    @classmethod
    def get_bookmarked(cls, user_id: int) -> List[Nursery]:
        return [n.nursery for n in cls.objects.filter(user_id=user_id)]

    @classmethod
    def is_bookmarked(cls, user_id: int, nursery_id: int) -> bool:
        return cls.objects.filter(user_id=user_id, nursery_id=nursery_id).exists()


class NurseryDefaultTourSetting(models.Model):
    id = models.AutoField(primary_key=True)
    nursery = models.OneToOneField(Nursery, models.PROTECT)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    capacity = models.IntegerField(null=False)
    description = models.CharField(max_length=255, null=False)
    note = models.CharField(max_length=255, default=None)
    is_active = Bit1BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'nursery_default_tour_settings'

    @classmethod
    def get_settings(cls, nursery_id):
        try:
            return cls.objects.get(nursery_id=nursery_id)
        except cls.DoesNotExist:
            return None


class NurseryTours(models.Model):
    id = models.AutoField(primary_key=True)
    nursery = models.ForeignKey(Nursery, models.PROTECT)
    nursery_default_tour_setting = models.ForeignKey(NurseryDefaultTourSetting, models.PROTECT, null=True)
    date = models.DateField(null=False)
    special_start_time = models.TimeField(default=None)
    special_end_time = models.TimeField(default=None)
    special_capacity = models.TimeField(default=None)
    special_note = models.CharField(max_length=255, default=None)
    is_active = Bit1BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'nursery_tours'

    @classmethod
    def create_tour_schedules_in_a_month(cls, nursery_id: int, held_days: List[int],
                                         default_setting_is_changed: bool = False):
        today = timezone.now().date()
        last_date = cls.objects.values('nursery_id').filter(nursery_id=nursery_id).annotate(
            last_date=Max('date')).first()

        dates = [today + datetime.timedelta(days=i) for i in range(1, 30)]

        if default_setting_is_changed:
            scheduled = cls.objects.filter(nursery_id=nursery_id, date__gte=today)
            if scheduled:
                scheduled.delete()
            target_dates = [d for d in dates if d.weekday() in held_days]
        elif last_date:
            target_dates = [d for d in dates if d.weekday() in held_days and d > last_date]
        else:
            target_dates = [d for d in dates if d.weekday() in held_days]

        default_settings = NurseryDefaultTourSetting.objects.filter(nursery_id=nursery_id)
        if not default_settings:
            return
        nursery = Nursery.objects.get(pk=nursery_id)
        schedules = []
        for target_date in target_dates:
            for default_setting in default_settings:
                schedules.append(cls(
                    nursery=nursery,
                    nursery_default_tour_setting=default_setting,
                    date=target_date
                ))
        cls.objects.bulk_create(schedules)

    @property
    def start_time(self):
        if self.special_start_time:
            return self.special_start_time
        return self.nursery_default_tour_setting.start_time

    @property
    def end_time(self):
        if self.special_end_time:
            return self.special_end_time
        return self.nursery_default_tour_setting.end_time

    @property
    def capacity(self):
        if self.special_capacity:
            return self.special_capacity
        return self.nursery_default_tour_setting.capacity

    @property
    def note(self):
        if self.special_note:
            return self.special_note
        return self.nursery_default_tour_setting.note

    @property
    def applied_count(self):
        return NurseryReservation.objects.filter(nursery_tour_id=self.id, is_active=True).count()

    @classmethod
    def get_nursery_tours(cls, nursery_id: int, limit: int = 5):
        return cls.objects.filter(
            nursery_id=nursery_id, is_active=True, date__gte=timezone.now().date()).order_by('date')[:limit]


class NurseryReservation(models.Model):
    id = models.AutoField(primary_key=True)
    nursery_tour = models.ForeignKey(NurseryTours, models.PROTECT)
    user = models.ForeignKey(CustomUser, models.PROTECT)
    note = models.CharField(max_length=255, null=True)
    is_active = Bit1BooleanField(default=True)
    status = models.IntegerField(default=0, null=False)
    reservation_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'nursery_reservations'
