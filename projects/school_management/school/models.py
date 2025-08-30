from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} ({self.class_name})"
    
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        LATE = "late", "Late"
    
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, related_name="attendances", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"], name="unique_student_attendance"
            )
        ]
    
class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, related_name="grades", on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'subject'], name='unique_student_subject')
        ]
        
    def __str__(self):
        return f"{self.student.name} - {self.subject}: {self.marks}"