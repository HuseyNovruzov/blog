
from django.test import TestCase, Client

class URLTestCase(TestCase):
    client = Client()


    def test_urls(self):

        urls = {'home': '/', 
                'login': '/login/', 
                'register': '/register/', 
                'forgot-password': '/forgot-password/',
                }
        for url in urls.values():
            response = self.client.get(url)
            status_code = response.status_code
            self.assertEqual(status_code,200)

    def test_logout_url(self):
        logout_url = '/logout/'
        response = self.client.get(logout_url, follow=True)
        redirected_path = response.request['PATH_INFO']
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        self.assertEqual(redirected_path, '/')
    
    
    
    
    