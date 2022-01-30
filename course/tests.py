import django
from django.test import TestCase, Client
from course.models import Course
from django.contrib.auth.models import User

class YourTestClass(TestCase):

    def setUp(self) -> None:
        n=10
        self.user=User.objects.create(username="mega_login",password="mega_password", is_staff=True)
        
        Course.objects.create(teacher=self.user,name="Название курса")     

    def tearDown(self) -> None:
        n=10
        User.objects.filter(username="mega_login").delete()
        Course.objects.get(id=1).delete()

    def test_getting_the_right_user(self) -> bool:
        client=Client()
        client.force_login(self.user)
        resp = client.get('/course/1/settings')
        print(resp.content)
        self.assertEqual(resp.status_code, 200)