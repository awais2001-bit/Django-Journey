from library.models import Books,BorrowRecord,User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')
        
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ('id','title','author','genre','published_date','available')
        
        
class BookDetailSerializer(serializers.ModelSerializer):
    current_borrower = serializers.SerializerMethodField()
    class Meta:
        model = Books
        fields = ('id','title','author','genre','published_date','available','current_borrower')
        
    def get_current_borrower(self, obj):
        borrow_record = BorrowRecord.objects.filter(book=obj, returned_at__isnull=True).first()
        if borrow_record:
            return borrow_record.user.username
        return None
        
class BorrowRecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    
    class Meta:
        model = BorrowRecord
        fields = ('id','user','book','borrowed_at','returned_at')
        
        
class BorrowActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ('book','borrowed_at')
    
    
class ReturnActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ('book','returned_at')
        