from django.shortcuts import render
from library.models import Books,BorrowRecord,User
from library.serializers import BookDetailSerializer,BookSerializer,BorrowActionSerializer,BorrowRecordSerializer,UserSerializer,ReturnActionSerializer
from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.utils.timezone import now
from rest_framework import status
# Create your views here.


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Books.objects.all()
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.max_page_size = 10 
    pagination_class.page_size_query_param = 'size'
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.action == 'create':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action =='retreive':
            return BookDetailSerializer
        elif self.action == 'borrow':
            return BorrowActionSerializer
        elif self.action == 'return_book':
            return ReturnActionSerializer
        
        return BookSerializer
            
    @action(detail=True, methods=['post'])
    def borrow(self,request, pk=None):
        book = self.get_object()
        
        if not book.available:
            return Response('Book not available')
        
        
        BorrowRecord.objects.create(user=request.user, book=book)
        book.available = False
        book.save()
        
        
        serializer = BorrowActionSerializer(book.borrow_records.last())
        return Response(serializer.data)
        
        
    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        book = self.get_object()
        active_record = book.borrow_records.filter(returned_at__isnull=True, user=request.user).first()

        if not active_record:
            return Response({"detail": "You have not borrowed this book."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark as returned
        active_record.returned_at = now()
        active_record.save()

        # Mark book available again
        book.available = True
        book.save()

        serializer = ReturnActionSerializer(active_record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class BorrowViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all().select_related('user', 'book')
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def mine(self, request):
        queryset = BorrowRecord.objects.filter(user=request.user)
        serializer = BorrowRecordSerializer(queryset, many=True)
        return Response(serializer.data)
    
    