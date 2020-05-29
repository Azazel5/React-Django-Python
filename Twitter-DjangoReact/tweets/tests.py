from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .models import Tweet

User = get_user_model()

""" Each function you write is one single test. Need to use
test_ for it to run as a test. The test methods don't care 
what you put inside and will delete the database. Anything you
want to be persisted needs to be in the setUp function.
"""

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe-2', password='somepassword')

        Tweet.objects.create(content='my_first_tweet', user=self.user)
        Tweet.objects.create(content='my_first_tweet', user=self.user)
        Tweet.objects.create(content='my_first_tweet', user=self.userb)
        self.current_count = Tweet.objects.all().count()
    
    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content='my_second_tweet', user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user) 

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client
 
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
    
    def test_tweets_related_name(self):
        user = self.user 
        self.assertEqual(user.tweets.count(), 2)

    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 1, 'action': 'like'})
        like_count = response.json().get('likes')
        user = self.user 
        my_like_instances = user.tweetlike_set.count()
        my_related_likes = user.tweet_user.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(like_count, 1)
        self.assertEqual(my_like_instances, 1)
        self.assertEqual(my_like_instances, my_related_likes)
    
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'like'})
        self.assertEqual(response.status_code, 200)
            
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'unlike'})
        self.assertEqual(response.status_code, 200)

        like_count = response.json().get('likes')
        self.assertEqual(like_count, 0)

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'retweet'})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        self.assertNotEqual(new_tweet_id, 2)
        self.assertEqual(self.current_count + 1, new_tweet_id)

    def test_tweet_create_api_view(self):
        request_data = {'content': 'test tweet'}
        client = self.get_client()
        response = client.post('/api/tweets/create/', request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get('id')        
        self.assertEqual(self.current_count + 1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        id_ = data.get('id')
        self.assertEqual(id_, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 200)
 
        client = self.get_client()
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 404)

        response_incorrect_owner = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response_incorrect_owner.status_code, 401)