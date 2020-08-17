from django.test import TestCase, Client
from django.urls import reverse

from blog.views import PostCreateView
from blog.models import Post
from measurement.measures import Distance
import tempfile


class TestViews(TestCase):

    def setUp(self):
        file = tempfile.NamedTemporaryFile(suffix=".gpx").name
        client = Client()       
        Post.objects.create(
            title='Malyo',
            distance=Distance(km=20),
            elevation=Distance(m=1000),
            file=file
        )
       
    def test_home_GET(self):
        response = self.client.get(reverse('blog-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_detail_GET(self):
        response = self.client.get(reverse('detail', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')

    def test_update_post(self):
        p = Post.objects.get(pk=1)

        response = self.client.post(
            reverse('update', kwargs={'post_id': 1}),
            {'title': 'usala', 'distance': '', 'elevation': '', 'lat': '', 'lon': '', 'description': '',
                'date_posted': '', 'want_go': '', 'been_there': '', 'author': '', 'file': '', 'image': ''})

        self.assertEqual(response.status_code, 302)

        p.refresh_from_db()
        self.assertEqual(p.title, '123')