from django.core.management.base import BaseCommand

from services.normalizer import normalizer
from infrastructure.models import Nursery
from happychild import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('[update_normalized_nursery_names] start.')
        try:
            nurseries = Nursery.objects.filter(is_active=True)
            for nursery in nurseries:
                normalized_name = normalizer.run(nursery.clean_name)
                if not normalized_name:
                    continue
                Nursery.update_normalized_nursery_name(nursery_id=nursery.id, normalized_name=normalized_name)
            logger.info('[update_normalized_nursery_names] finished.')
        except Exception as e:
            logger.exception('[update_normalized_nursery_names] failed.'
                             'error_type: {}, error: {}'.format(type(e), e))
