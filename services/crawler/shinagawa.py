from typing import Optional

import pandas as pd

from infrastructure.models import Age, Nursery, NurseryFreeNum, NurseryScore
from services.consts import AGE_LABELS, SHINAGAWA_OPEN_DATA, SHINAGAWA_WARD_ID
from happy_child import logging

logger = logging.getLogger(__name__)

COLUMNS = ['name', 'year', 'min_age', 'max_age', 'capacity', 'free_num', 'score', 'hierarchy', 'note', 'code']


class ShinagawaNurseryrawler(object):
    def search_nursery(self, name: str, ward_id: int) -> Optional[Nursery]:
        # TODO: Search nursery word by Google Search API if cannot search the nursery
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


shinagawa_crawler = ShinagawaNurseryrawler()
