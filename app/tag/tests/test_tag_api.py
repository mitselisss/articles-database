"""
Test for tag api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from tag.serializers import TagSerializer


TAG_LIST_URL = reverse('tag:tag-list')


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicTagApiTests(TestCase):
    """Test the unauthorized user tag api."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required_for_create(self):
        """Test authorization required for tag creation."""
        payload = {'name': 'sample_tag'}
        res = self.client.post(TAG_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tags(self):
        """Test that anyone can list tags."""
        Tag.objects.create(name='test1')
        Tag.objects.create(name='test2')

        res =  self.client.get(TAG_LIST_URL)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)


class PrivateTagApiTests(TestCase):
    """Test the authorized user tag api."""
    def setUp(self):
        self.user = create_user(
            username='user1',
            email='u1@example.com',
            password='pass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_tag_successful(self):
        """Test creating a tag returns succesful"""
        payload = {'name': 'sample_tag'}
        res = self.client.post(TAG_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tag.objects.filter(name=payload['name']).exists())

    def test_create_tag_invalid(self):
        """Test creating a tag with empty name returns error."""
        res = self.client.post(TAG_LIST_URL, {'name': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
