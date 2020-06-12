from django.test import TestCase

from measurement.measures import Distance
from blog.models import Post


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title='Malyo', distance=Distance(km=10), elevation=Distance(m=1000),
                            description='tescription', lat=42.698334, lon=23.319941)

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_distance_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('distance').verbose_name
        self.assertEquals(field_label, 'distance')

    def test_elevation_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('elevation').verbose_name
        self.assertEquals(field_label, 'elevation')

    def test_description_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_in_range_func_in_range(self):
        malyo = Post.objects.get(title='Malyo')
        self.assertTrue(malyo.in_range((42.136097, 24.742168), 300))

    def test_in_range_func_out_of_range(self):
        malyo = Post.objects.get(title='Malyo')
        self.assertFalse(malyo.in_range((42.136097, 24.742168), 50))

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/blog/1/')