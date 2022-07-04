from django.test import TestCase, Client

from base.models import CustomUser, Articles, Topic, Messages
import json

class UserTestCase(TestCase):

    client = Client()

    def setUp(self):
        user_a_pw = 'Bmwe39528i'
        user_email = 'cfe@gmail.com'
        user_a = CustomUser.objects.create(email='cfe@gmail.com', username='cfe')
        user_a.set_password(user_a_pw)
        user_a.is_active = True
        self.user_a_pw = user_a_pw
        self.user_a = user_a
        self.user_email = user_email
        user_a.save()

    def login_user(self):
        login_url = '/login/'
        data = {'email': self.user_email,  'password': self.user_a_pw}
        return self.client.post(login_url, data, follow=True)

    def test_user_exists(self):
        user_count = CustomUser.objects.all().count()
        self.assertEqual(user_count,1)


    def test_login(self):
        response = self.login_user()
        status_code = response.status_code
        redirected_path = response.request.get('PATH_INFO')

        self.assertEqual(redirected_path, '/')
        self.assertEqual(status_code,200)

    def test_register(self):
        register_url = '/register/'
        data = {'username': 'huseyn', 'email': 'cklub11@gmail.com', 'password1': 'VolvoCX80', 'password2': 'VolvoCX80'}
        response = self.client.post(register_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code,200)


    def test_reset_password(self):
        # go to forgot password page
        url = '/forgot-password/'
        data = {'email': self.user_email }
        response = self.client.post(url, data, follow=True)
        # go to reset password page
        reset_password_url = f'/reset_password/{response.context["uid"]}/{response.context["token"]}'
        reset_password_data = {'new_password1': 'NissanGTR22', 'new_password2': 'NissanGTR22'}
        reset_password_response = self.client.post(reset_password_url, reset_password_data, follow=True)
        status_code = reset_password_response.status_code
        
        self.assertEqual(status_code, 200)
        self.assertEqual(reset_password_response.context['reseted'], True)


        

    def test_comment(self):
        topic = Topic.objects.create(name='Texnalogiya')
        article = Articles.objects.create(id=1,host=self.user_a, topic=topic, title='Ada', 
        description='lorem ipsum')

        # login
        data = {'email': self.user_email, 'password': self.user_a_pw}
        self.client.post('/login/', data)
        
        # add comment
        article_url = '/article/Ada/'
        comment_response = self.client.post(article_url, {'body': 'Hello'})
        add_status_code = comment_response.status_code
        
        # delete comment
        c = Messages.objects.all()
        id = c[0].id
        delete_comment_response = self.client.post('/delete/', {'deletedcomment': id})
        delete_status = delete_comment_response.status_code

        self.assertEqual(add_status_code,200)
        self.assertEqual(delete_status,200)
    

    def test_like(self):
        topic = Topic.objects.create(name='Texnalogiya')
        article = Articles.objects.create(id=1,host=self.user_a, topic=topic, title='Ada', 
        description='lorem ipsum')
        # login
        data = {'email': self.user_email, 'password': self.user_a_pw}
        self.client.post('/login/', data)
        # like
        like_url = '/like/'
        data = {'post_id' :1}
        like_response = self.client.post(like_url, data)
        status_code = like_response.status_code
        self.assertEqual(status_code, 200)
    
    def test_user_profile(self):
        profile_url = f'/user_profile/{self.user_a.id}/'
        response = self.client.get(profile_url)
        status_code = response.status_code
        self.assertEqual(status_code,200)
        
    def test_user_settings(self):

        self.login_user()
        settings_url = '/settings/'
        data = {'username': 'ccc'}
        response = self.client.post(settings_url, data, follow=True)
        redirected_path = response.request['PATH_INFO']
        status_code = response.status_code
        self.assertEqual(status_code,200)
        self.assertEqual(redirected_path,'/')

    def test_update_password(self):

        self.login_user()
        update_passsword_url = '/update-password/'
        data = {'password1': 'Felicita2014', 'password2': 'Felicita2014'}

        response = self.client.post(update_passsword_url, data, follow=True)
        redirected_path = response.request['PATH_INFO']
        status_code = response.status_code
        self.assertEqual(redirected_path, '/login/')
        self.assertEqual(status_code, 200)
    


        




    
    
        


