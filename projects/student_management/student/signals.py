import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Student,Teacher

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Student)
def student_saved(sender, instance, created, **kwargs):
    if created:
        logger.info(f"✅ Student with roll no {instance.roll_number} created successfully.")
    else:
        logger.info(f"✏️ Student with roll no {instance.roll_number} updated successfully.")

@receiver(post_delete, sender=Student)
def student_deleted(sender, instance, **kwargs):
    logger.info(f"🗑️ Student with roll no {instance.roll_number} deleted successfully.")


@receiver(post_save, sender=Teacher)
def student_saved(sender, instance, created, **kwargs):
    if created:
        logger.info(f"✅ Teacher {instance.name} created successfully.")
    else:
        logger.info(f"✏️ Teacher {instance.name} updated successfully.")

@receiver(post_delete, sender=Student)
def student_deleted(sender, instance, **kwargs):
    logger.info(f"🗑️ Teacher  {instance.name} deleted successfully.")