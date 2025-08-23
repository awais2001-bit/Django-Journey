from django.db.models.signals import post_delete,post_save
from library.models import User,Books,BorrowRecord
from django.dispatch import receiver


@receiver(post_save, sender=Books)
def book_saved(sender,instance,created,**kwargs):
    if created:
        print('Book created successfully!!')
        
    else:
        print('Book updated successfully!!')

@receiver(post_delete, sender=Books)
def book_deleted(sender,instance,created,**kwargs):
        print('Book deleted successfully!!')
        
@receiver(post_save, sender=BorrowRecord)
def borrow_record_saved(sender,instance,created,**kwargs):
    if created:
        print("Borrow records added!")
    else:
        print('Borrow records updated successfully')
        
@receiver(post_delete, sender=BorrowRecord)
def borrow_record_deleted(sender,instance,created,**kwargs):
        print('Borrow records deleted successfully!!')     
        
        
@receiver(post_save, sender=User)
def user_saved(sender,instance,created,**kwargs):
    if created:
        print('User added successfully!!')
    else:
        print("User updated successfully!!")
    
@receiver(post_delete, sender=User)
def user_deleted(sender,instance,created,**kwargs):
    print('User deleted successfully!!')