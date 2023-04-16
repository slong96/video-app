from django.test import TestCase
from django.urls import reverse # convert name of url into the actual path
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Video

class TestHomePageMessage(TestCase):
    
    def test_app_title_message_shown_on_home_page(self):
      url = reverse('home')
      response = self.client.get(url) # get the home url page
      self.assertContains(response, 'Music Videos')



class TestAddVideos(TestCase):
   
   def test_add_video(self):
      valid_video = {
          'name': 'bobby',
          'url': 'https://www.youtube.com/watch?v=ZDWzXDTxI4Q',
          'notes': 'Nice!'
      }

      url = reverse('add_video')
      response = self.client.post(url, data=valid_video, follow=True) # post request, if request is redirected, follow=True will follow the redirect

      self.assertTemplateUsed('video_collection/video_list.html')

      # does the video list show the new video?
      self.assertContains(response, 'bobby')
      self.assertContains(response, 'https://www.youtube.com/watch?v=ZDWzXDTxI4Q')
      self.assertContains(response, 'Nice!')

      # check if video in the database
      video_count = Video.objects.count()
      self.assertEqual(1, video_count) # expect 1 video in the database (bobby music video)

      # check if the video valid_video list is the same in the database attributes
      video = Video.objects.first() # return the first result
      self.assertEqual('bobby', video.name)
      self.assertEqual('https://www.youtube.com/watch?v=ZDWzXDTxI4Q', video.url)
      self.assertEqual('Nice!', video.notes)
      self.assertEqual('ZDWzXDTxI4Q', video.video_id)


   def test_add_video_invalid_url_not_added(self):
      invalid_video_urls = [
          'https://www.youtube.com/watch',
          'https://www.youtube.com/watch?',
          'https://www.youtube.com/watch?abc=123',
          'https://www.youtube.com/watch?v=',
          'https://www.github.com',
          'https://www.minneapolis.edu',
          'https://www.minneapolis.edu?v=123454'
      ]

      for invalid_video_url in invalid_video_urls:
          
          new_video = {
            'name': 'example',
            'url': invalid_video_url,
            'notes': 'example notes'
          }

          url = reverse('add_video')
          response = self.client.post(url, new_video)

          self.assertTemplateNotUsed('video_collection/add.html')

          messages = response.context['messages']
          messages_text = [ message.message for message in messages ]

          self.assertIn('Invalid Youtube URL', messages_text)
          self.assertIn('Please check the data entered.', messages_text)

          video_count = Video.objects.count()

          self.assertEqual(0, video_count) # should expect 0 because those links aren't valid, so it shouldn't be added



class TestVideoList(TestCase):
   
   def test_all_videos_displayed_in_correct_order(self):
      v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
      v2 = Video.objects.create(name='abc', notes='example', url='https://www.youtube.com/watch?v=124')
      v3 = Video.objects.create(name='AAA', notes='example', url='https://www.youtube.com/watch?v=125')
      v4 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=126')

      expected_video_order = [ v3, v2, v4, v1 ] # sorted by name, case sensitive way

      url = reverse('video_list')
      response = self.client.get(url)
      videos_in_template = list(response.context['videos'])

      self.assertEqual(videos_in_template, expected_video_order)
   
   
   def test_no_video_message(self):
      url = reverse('video_list')
      response = self.client.get(url)

      self.assertContains(response, 'No videos')
      self.assertEqual(0, len(response.context['videos']))

  
   def test_video_number_message_one_video(self):
      v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
      url = reverse('video_list')
      response = self.client.get(url)

      self.assertContains(response, '1 video')
      self.assertNotContains(response, '1 videos')


   def test_video_number_message_two_video(self):
      v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
      v2 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=124')

      url = reverse('video_list')
      response = self.client.get(url)

      self.assertContains(response, '2 videos')
      



class TestVideoSearch(TestCase):
   pass




class TestVideoModel(TestCase):
   
   def test_invalid_url_raises_validation_error(self):
      invalid_video_urls = [
          'https://www.youtube.com/watch/something',
          'https://www.youtube.com/watch/somethingelse?v=1234565',
          'https://www.youtube.com/watch',
          'https://www.youtube.com/watch?',
          'https://www.youtube.com/watch?abc=123',
          'https://www.youtube.com/watch?v=',
          'https://www.github.com',
          '123456788',
          'hhhhhhhhttps://www.youtube.com/watch',
          'http://www.youtube.com/watch/somethingelse?v=1234565'
          'https://www.minneapolis.edu',
          'https://www.minneapolis.edu?v=123454'
      ]

      for invalid_video_url in invalid_video_urls:
         with self.assertRaises(ValidationError):
            Video.objects.create(name='example', url=invalid_video_url, notes='example note')
      
      self.assertEqual(0, Video.objects.count())


   def test_duplicate_video_raises_integrity_error(self):
      v1 = Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')
      with self.assertRaises(IntegrityError):
         Video.objects.create(name='ZXY', notes='example', url='https://www.youtube.com/watch?v=123')