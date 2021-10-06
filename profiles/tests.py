from django.test import TestCase,Client
from django.contrib.auth.models import User

class YourTestClass(TestCase):
    def setUp(self) -> None:
        self.user=User.objects.create(username="mega_login",password="mega_password")
    
    def tearDown(self) -> None:
        User.objects.get(username="mega_login").delete()

    def test_getting_the_right_user(self) -> bool:
        client=Client()
        client.force_login(self.user)
        resp = client.get('/user/'+str(self.user.id))
        self.assertEqual(resp.status_code,200)
        self.assertTrue(b'mega_login' in resp.content)
