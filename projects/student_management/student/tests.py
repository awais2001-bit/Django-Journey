from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Student, User, Teacher, Course, Enrollment

class StudentTests(APITestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username="admin",
            password="adminpass",
            is_staff=True
        )

        # Authenticate client as admin
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        self.student_data = {
            "name": "Awais",
            "email": "awais@gmail.com",
            "roll_number": "f20b1"
        }

    def test_create_student(self):
        url = reverse('student-list')  
        response = self.client.post(url, self.student_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().name, "Awais")



class StudentCourseTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.admin_user = User.objects.create_user(
            username="admin",
            password="adminpass",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin_user)
        
        self.teacher = Teacher.objects.create(name="Ali", subject="Math", email="ali@example.com")
        self.course = Course.objects.create(title="Algebra", description="Math basics", teacher=self.teacher)
        self.student = Student.objects.create(name="Awais", email="awais@example.com", roll_number="123")
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course)
        
        
    def test_student_course(self):
        url = reverse('student-student-courses', args=[self.student.roll_number])
        response = self.client.get(url,format='json')
            
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # def setUp(self):
        # # Create a normal user
        # self.user = User.objects.create_user(
        #     username="awais",
        #     password="testpass123"
        # )

        # # Generate JWT token for this user
        # refresh = RefreshToken.for_user(self.user)
        # self.access_token = str(refresh.access_token)

        # # Attach token to client
        # self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")