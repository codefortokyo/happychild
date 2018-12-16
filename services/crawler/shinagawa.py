import re
import datetime
from typing import Optional

import tabula
import pandas as pd

from infrastructure.models import Age, Nursery, NurseryFreeNum, NurseryScore
from services.consts import AGE_LABELS, SHINAGAWA_OPEN_DATA, SHINAGAWA_WARD_ID
from happychild import logging

logger = logging.getLogger(__name__)

COLUMNS = ['name', 'year', 'min_age', 'max_age', 'capacity', 'free_num', 'score', 'hierarchy', 'note', 'code']


class ShinagawaNurseryCrawlerFromOpenData(object):
    def search_nursery(self, name: str, ward_id: int) -> Optional[Nursery]:
        nursery = self._search_nursery_directly(name, ward_id)
        return nursery

    @classmethod
    def _search_nursery_directly(cls, name: str, ward_id: int) -> Optional[Nursery]:
        try:
            return Nursery.objects.get(name=name, ward_id=ward_id)
        except Nursery.DoesNotExist:
            return None

    @classmethod
    def search_age(cls, age: str) -> Optional[Age]:
        for key, labels in AGE_LABELS.items():
            for label in labels:
                if label in age:
                    return Age.objects.get(pk=key)
        return None

    def run(self) -> None:
        try:
            nursery_df = pd.read_csv(SHINAGAWA_OPEN_DATA['url'], encoding='SHIFT-JIS', skipfooter=1)
            nursery_df.columns = COLUMNS
            nursery_df = nursery_df.where((pd.notnull(nursery_df)), None)

            nursery_df['min_age'] = nursery_df['min_age'].astype(str)
            nursery_df['max_age'] = nursery_df['max_age'].astype(str)

            indexes = nursery_df.index
            for i in indexes:
                target_df = nursery_df.iloc[i]
                nursery = self.search_nursery(name=target_df['name'], ward_id=SHINAGAWA_WARD_ID)
                if not nursery:
                    logger.warn('[WARN] nursery object is not found. {}'.format(target_df['name']))
                    continue
                for a in set([target_df['min_age'], target_df['max_age']]):
                    age = self.search_age(a)
                    if not age:
                        logger.warn('[WARN] age object is not found. {nursery}, {age}'.format(
                            nursery=target_df['name'], age=a))
                    # upsert of nursery free num
                    NurseryFreeNum.upsert(nursery, age, SHINAGAWA_OPEN_DATA['modified_date'], target_df['free_num'])
                    # upsert of nursery score
                    NurseryScore.upsert(nursery, age, target_df['year'], target_df['score'], target_df['hierarchy'])
        except Exception as e:
            logger.exception('[ERROR] failed to run shinagawa nursery crawler. %s', e)


shinagawa_crawler_from_opendata = ShinagawaNurseryCrawlerFromOpenData()

DOWNLOAD_LINK = {
    'url': 'http://www.city.shinagawa.tokyo.jp/ct/pdf/201811191366_1.pdf',
    'modified_date': datetime.date(2018, 11, 20),
    'page': 2,
}
COULUMN_KODOMO_HOIKUEN = ['night_hoiku', 'zero', 'name', 'infant', 'infant_', 'infant_sum', 'free_num_not_one',
                          'free_num_one_year_old', 'free_num_two_year_old', 'free_num_subtotal',
                          'free_num_three_year_old', 'free_num_four_year_old', 'free_num_extent', 'subtotal', 'sum',
                          'note']


class ShinagawaNurseryCrawlerFromKodomoHoikuen(ShinagawaNurseryCrawlerFromOpenData):
    def update_kodomo_hoikuen(self):
        for page in range(DOWNLOAD_LINK['page']):
            df = tabula.read_pdf(DOWNLOAD_LINK['url'], pages=str(page + 1))
            df.columns = COULUMN_KODOMO_HOIKUEN

            # delete header
            df = df.iloc[1:].reset_index(drop=True)
            # convert from None to nan
            df = df.where((pd.notnull(df)), None)

            nurseries = list(name for name in df['name'] if name)
            free_num_not_one = list(re.sub('歳', '', free) for free in df['free_num_not_one'] if free)[1:]
            free_num_one_year_old = list(re.sub('歳', '', free) for free in df['free_num_one_year_old'] if free)[1:]
            free_num_two_year_old = list(re.sub('歳', '', free) for free in df['free_num_two_year_old'] if free)[1:]
            free_num_three_year_old = list(re.sub('歳', '', free) for free in df['free_num_three_year_old'] if free)[1:]
            free_num_four_year_old = list(re.sub('歳', '', free) for free in df['free_num_four_year_old'] if free)[1:]
            free_num_extent = list(re.sub('歳', '', free) for free in df['free_num_extent'] if free)[1:]

            for i, name in enumerate(nurseries):
                if '保育園' in name:
                    name += '保育園'
                nursery = self.search_nursery(name=name, ward_id=SHINAGAWA_WARD_ID)
                if not nursery:
                    logger.warning('該当の保育園情報がありません: {}'.format(name))
                    continue

                for age_id in range(1, 6):
                    if age_id == 1:
                        free_num = free_num_not_one[i]
                    elif age_id == 2:
                        free_num = free_num_one_year_old[i]
                    elif age_id == 3:
                        free_num = free_num_two_year_old[i]
                    elif age_id == 4:
                        free_num = free_num_three_year_old[i]
                    elif age_id == 5:
                        free_num = free_num_four_year_old[i]
                    else:
                        free_num = free_num_extent[i]
                    if free_num.isdigit():
                        # upsert of nursery free num
                        age = Age.objects.get(pk=age_id)
                        NurseryFreeNum.upsert(nursery, age, DOWNLOAD_LINK['modified_date'], int(free_num))
