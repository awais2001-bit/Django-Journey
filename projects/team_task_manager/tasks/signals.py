from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.core.cache import cache
from tasks.models import Project,Task,Activity


@receiver([post_delete,post_save],sender=Project)
def clear_project(sender,instance,**kwargs):
    cache.delete('projects_list')
    print(f'cache cleared for project{instance.id}')
    
@receiver([post_save,post_delete],sender=Task)
def clear_task(sender,instance,**kwargs):
    cache.delete('tasks_list')
    print(f'cache deleted for task {instance.id}')
    

@receiver(post_save,sender=Task)
def log_task_activity(sender,instance,created,**kwargs):
    if created:
        message = f'task {instance.title} created by {instance.owner.username}'
    else:
        message = f'task {instance.title} updated'
        
    Activity.objects.create(task=instance,message=message)
    
@receiver(post_delete,sender=Task)
def log_task_deletion(sender,instance, **kwargs):
    message = f'task {instance.title} deleted'
    Activity.objects.create(task=instance, message=message)
    