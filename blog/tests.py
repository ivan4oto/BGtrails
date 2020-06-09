from django.test import TestCase

from measurement.measures import Distance
from blog.models import Post


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title='Malyo', distance=Distance(km=10), elevation=Distance(m=1000),
                            description='tescription', lat=42.698334, lon=23.319941)

    def test_in_range_func_in_range(self):
        malyo = Post.objects.get(title='Malyo')
        self.assertTrue(malyo.in_range((42.136097, 24.742168), 300))

    def test_in_range_func_out_of_range(self):
        malyo = Post.objects.get(title='Malyo')
        self.assertFalse(malyo.in_range((42.136097, 24.742168), 50))
