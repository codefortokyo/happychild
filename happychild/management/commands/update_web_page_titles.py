import lxml.html
import requests
from django.core.management.base import BaseCommand

from infrastructure.models import Nursery
from happychild import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('[update_web_page_titles] start.')
        try:
            nurseries = Nursery.objects.filter(ward_id=9)
            for nursery in nurseries:
                web_page_title = self._update_web_page_title(nursery.url)
                nursery.web_page_title = web_page_title
                nursery.save()

            logger.info('[update_web_page_titles] finished.')
        except Exception as e:
            logger.exception('[update_web_page_titles] failed.'
                             'error_type: {}, error: {}'.format(type(e), e))

    @classmethod
    def _update_web_page_title(cls, url: str):
        try:
            response = requests.get(url, timeout=3)
            response.raise_for_status()

            if response.encoding.lower() not in ['utf-8', 'shift-jis', 'euc-jp']:
                response.encoding = response.apparent_encoding
        except:
            return ''

        try:
            tree = lxml.html.fromstring(response.text)
        except ValueError:
            tree = lxml.html.fromstring(response.content)
        return tree.findtext('.//title').strip()
