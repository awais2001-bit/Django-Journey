from rest_framework import serializers
from .models import Student, Attendance, Grade
import re
from django.utils import timezone


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'class_name')
        
    def validate_name(self, value):
        
        if not re.match(r'^[A-Za-z\s]+$', value):
            raise serializers.ValidationError("Name must contain only alphabets and spaces.")
        return value
    


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('id', 'student', 'date', 'status')
        
    def validate_date(self, value):
        
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value
    
    def validate(self, data):
        """Prevent duplicate attendance entries per student per date"""
        student = data.get("student")
        date = data.get("date", timezone.now().date())

        qs = Attendance.objects.filter(student=student, date=date)
        if self.instance:  # when updating, exclude self
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Attendance for this student on this date already exists.")
        return data
    


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'student', 'subject', 'marks')  
    
    def validate(self, data):
        """Prevent duplicate subject entry per student"""
        student = data.get("student")
        subject = data.get("subject")

        qs = Grade.objects.filter(student=student, subject=subject)
        if self.instance:  # exclude self when updating
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("Grade for this student in this subject already exists.")
        return data

    def validate_marks(self, value):
        
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Marks must be between 0 and 100.")
        return value
