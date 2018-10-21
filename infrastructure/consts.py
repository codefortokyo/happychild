import enum

NURSERY_FREE_NUM_FMT = 'nursery_id:{}age_id:{}'

NOT_ONE_AGE_ID = 1
ONE_YEAR_OLD_AGE_ID = 2
TWO_YEAR_OLD_AGE_ID = 3
THREE_YEAR_OLD_AGE_ID = 4
FOUR_YEAR_OLD_AGE_ID = 5
EXTENT_AGE_ID = 6
OTHER_AGE_ID = 7

AGE_IDS = [NOT_ONE_AGE_ID, ONE_YEAR_OLD_AGE_ID, TWO_YEAR_OLD_AGE_ID, THREE_YEAR_OLD_AGE_ID, FOUR_YEAR_OLD_AGE_ID,
           EXTENT_AGE_ID]


NURSERY_INFO = 'basic'
NURSERY_FREE_NUM = 'free_num'
NURSERY_SCORE = 'score'


class DayOfWeek(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def get_default_held_days(cls):
        return [cls.TUESDAY.value, cls.FRIDAY.value]
