from django.test import TestCase

from base.models import CustomUser, Topic, Articles, Messages


class CustomUserTestCase(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(
            email= 'easport@sport.eu',
            username= 'easport',
        )
        user.set_password('NissanGTR3')
        user.save()

    def test_user(self):
        single_user = CustomUser.objects.all().count()
        self.assertEqual(single_user,1)

class TopicTestCase(TestCase):

    def setUp(self):
        Topic.objects.create(name='Texnalogiya')
    
    def test_topic_exists(self):
        count = Topic.objects.all().count()
        self.assertEqual(count,1)

class ArticleTestCase(TestCase):

    def setUp(self):
        host = CustomUser.objects.create(email='cfe@gmail.com', username='cfe')
        topic = Topic.objects.create(name='Texnalogiya')
        Articles.objects.create(host=host, topic=topic, title='Ada', description='lorem ipsum')
    
    def test_article(self):
        article = Articles.objects.all().count()
        self.assertEqual(article,1)

class MessagesTestCase(TestCase):

    def setUp(self):
        host = CustomUser.objects.create(email='cfe@gmail.com', username='cfe')
        user = CustomUser.objects.create(email= 'easport@sport.eu', username= 'easport')
        topic = Topic.objects.create(name='Texnalogiya')
        article = Articles.objects.create(host=host, topic=topic, title='Ada', description='lorem ipsum')
        body = 'Hello 2'
        message = Messages.objects.create(
            user=user,
            article=article,
            body=body,
            parent=None,
        )

    def test_message(self):
        message_count = Messages.objects.all().count()
        self.assertEqual(message_count,1)