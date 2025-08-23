from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from catalog.models import User,Category,Cart,CartItem,Order,OrderItem,Product


@receiver(post_save, sender=Product)
def product_saved(sender,instance,created,**kwargs):
    if created:
       print(f' {instance.name} is created successfully!!')
    else:
        print( f' {instance.name} is updated successfully!!')
    
@receiver(post_delete, sender=Product)
def product_deleted(sender,instance,**kwargs):
    return print(f' {instance.name} is deleted successfully!!')