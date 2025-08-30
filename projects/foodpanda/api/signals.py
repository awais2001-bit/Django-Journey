from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import User,Restaurant
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Restaurant)
def Restaurant_saved(self, instance, created, **kwargs):
    if created:
        logger.info(f'Restauranr {instance.name} created!')
        
    else:
        logger.info(f'Restauranr {instance.name} updated!')
        
@receiver(post_delete, sender=Restaurant)
def Restaurant_deleted(self, instance, **kwargs):
    logger.info(f'restaurant {instance.name} does not exist anymore!')
    