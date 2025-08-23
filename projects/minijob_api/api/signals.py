
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from api.models import User,JobApplication,Company,Job

@receiver(post_save, sender=User)
def User_saved(sender,instance,created,**kwargs):
    if created:
        Company.objects.create(
            name = f'Default Company for {instance.username}',
            created_by = instance
        )
    