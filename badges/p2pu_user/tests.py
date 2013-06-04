from django.test import TestCase

from p2pu_user import models as user_api

class UserTest(TestCase):

    def test_save_user(self):
        user = user_api.save_user('testuser', 'http://placehold.it/40x40', 'user@email.com')
        self.assertIn('username', user)
        self.assertIn('uri', user)
        self.assertIn('image_url', user)

        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(user['uri'], '/uri/user/testuser')
        self.assertEqual(user['image_url'], 'http://placehold.it/40x40')

    def test_get_user(self):
        user = user_api.save_user('testuser', '/media/images/test.png', 'user@email.com')
        user2 = user_api.get_user(user['uri'])
        self.assertEqual(user, user2)

    def test_get_users(self):
        user = user_api.save_user('testuser1', 'http://placehold.it/40x40', 'user@email.com')
        user = user_api.save_user('testuser2', 'http://placehold.it/20x20', 'user@email.com')
        user = user_api.save_user('testuser1', 'http://placehold.it/40x40', 'user@email.com')

        user_list = user_api.get_users()
        self.assertEqual(len(user_list), 2)

    def test_create_partner_without_user(self):
        user = user_api.save_user('testuser', 'http://placehold.it/40x40', 'user@email.com')
        partner = user_api.create_partner('testparnter')
        self.assertIn('name', partner)
        self.assertEquals('testparnter', partner['name'])
        self.assertEquals([], partner['user'])

    def test_create_partner_with_user(self):
        user = user_api.save_user('testuser', 'http://placehold.it/40x40', 'user@email.com')
        partner = user_api.create_partner('testparnter', user_uri=user['uri'])
        self.assertIn('name', partner)
        self.assertEquals('testparnter', partner['name'])
        self.assertEquals(1, len(partner['user']))
        self.assertEquals(user['username'], partner['user'][0]['username'])
