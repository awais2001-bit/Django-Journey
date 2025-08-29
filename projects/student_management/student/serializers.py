from rest_framework import serializers
from student.models import Student,Course,Teacher,Enrollment


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('name','email','roll_number')
        
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('name','subject','email')
        
class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(write_only=True)
    teacher_details = TeacherSerializer(source='teacher', read_only=True)
    class Meta:
        model = Course
        fields = ('title','description','teacher','teacher_details')
        
        

class EnrollmentSerializer(serializers.ModelSerializer):
    student_roll_number = serializers.CharField(write_only=True)
    course_name = serializers.CharField(write_only=True)
    student_details = StudentSerializer(source='student', read_only=True)
    course_details = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Enrollment
        fields = ('student_roll_number', 'course_name', 'date_enrolled', 'student_details', 'course_details')

    def validate_student_roll_number(self, value):
        try:
            Student.objects.get(roll_number=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError(f"Student with roll_number '{value}' does not exist.")
        return value

    def validate_course_name(self, value):
        try:
            Course.objects.get(title=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError(f"Course with title '{value}' does not exist.")
        return value

    def validate(self, attrs):
        student_roll_number = attrs.get('student_roll_number')
        course_name = attrs.get('course_name')
        student = Student.objects.get(roll_number=student_roll_number)
        course = Course.objects.get(title=course_name)
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Student is already enrolled in this course.")
        return attrs

    def create(self, validated_data):
        student = Student.objects.get(roll_number=validated_data.pop('student_roll_number'))
        course = Course.objects.get(title=validated_data.pop('course_name'))
        validated_data['student'] = student
        validated_data['course'] = course
        return super().create(validated_data)