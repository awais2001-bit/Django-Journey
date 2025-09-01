
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from event.models import User,OrderItem,Organizer

@receiver(post_save, sender=Organizer)
def User_saved(sender,instance,created,**kwargs):
    if created:
        Organizer.objects.create(
            name = f'Default Organizer for {instance.name}',
        )
    