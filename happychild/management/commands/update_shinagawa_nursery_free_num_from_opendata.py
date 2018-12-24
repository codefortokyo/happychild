from django.core.management.base import BaseCommand

from happychild import logging
from services.crawler.shinagawa import shinagawa_crawler_from_opendata

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('[update_shinagawa_nursery_free_num_from_opendata] start.')
        try:
            shinagawa_crawler_from_opendata.run()
            logger.info('[update_shinagawa_nursery_free_num_opendata] finished.')
        except Exception as e:
            logger.exception('[update_shinagawa_nursery_free_num_opendata] failed.'
                             'error_type: {}, error: {}'.format(type(e), e))
