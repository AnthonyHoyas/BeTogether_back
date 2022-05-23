from django.urls import resolve
from django.test import TestCase
from polls.apiviews import PollViewSet  

# class HomePageTest(TestCase):

#     def test_root_url_resolves_to_home_page_view(self):
#         found = resolve('/')  
#         self.assertEqual(found.view_name, PollViewSet)