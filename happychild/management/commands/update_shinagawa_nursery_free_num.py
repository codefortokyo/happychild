from django.core.management.base import BaseCommand

from happychild import logging
from services.crawler.shinagawa import shinagawa_crawler

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('[update_shinagawa_nursery_free_num] start.')
        try:
            shinagawa_crawler.run()
            logger.info('[update_shinagawa_nursery_free_num] finished.')
        except Exception as e:
            logger.exception('[update_shinagawa_nursery_free_num] failed.'
                             'error_type: {}, error: {}'.format(type(e), e))
