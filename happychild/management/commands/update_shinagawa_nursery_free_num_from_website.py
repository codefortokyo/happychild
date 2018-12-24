from django.core.management.base import BaseCommand

from happychild import logging
from services.crawler.shinagawa import shinagawa_crawler_from_website

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('[update_shinagawa_nursery_free_num_from_website] start.')
        try:
            shinagawa_crawler_from_website.run_website()
            logger.info('[update_shinagawa_nursery_free_num_website] finished.')
        except Exception as e:
            logger.exception('[update_shinagawa_nursery_free_num_website] failed.'
                             'error_type: {}, error: {}'.format(type(e), e))
