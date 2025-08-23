from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from events.models import User,EventAttendee,Events

@receiver(post_save, sender=Events)
def event_saved(sender,instance,created,**kwargs):
    if created:
        print('Event created successfully!!')
    else:
        print('Event updated successfully!!')
        
@receiver(post_delete, sender=Events)
def event_deleted(sender,instance,created,**kwargs):
    print('Event Deleted successfully!!')