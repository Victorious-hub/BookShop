from unittest import TestCase

from accounts.models import SimpleUser, UserAccount, HyperLinks


class ModelTest(TestCase):
    def setUp(self):
        self.simpleuser, created = SimpleUser.objects.get_or_create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
        )
        self.hyperlinks = HyperLinks.objects.create(
            user_linkedin='https://www.linkedin.com/in/johndoe',
            user_github='https://github.com/johndoe',
            user=self.simpleuser
        )

    def test_str(self):
        self.assertEqual(str(self.hyperlinks), str(self.simpleuser))

    def test_user_linkedin_max_length(self):
        max_length = self.hyperlinks._meta.get_field('user_linkedin').max_length
        self.assertEqual(max_length, 200)

    def test_user_github_max_length(self):
        max_length = self.hyperlinks._meta.get_field('user_github').max_length
        self.assertEqual(max_length, 200)

    def test_user_foreign_key(self):
        self.assertEqual(self.hyperlinks.user, self.simpleuser)

    def test_slug(self):
        self.assertEqual(self.simpleuser.slug,'john')

    def test_save(self):
        self.assertIsNotNone(self.simpleuser.slug)

    def test_has_perm(self):
        perm = "is_active"
        self.assertFalse(self.simpleuser.has_perm(perm))

    def test_has_module_perms(self):
        app_label = "some_app"
        self.assertTrue(self.simpleuser.has_module_perms(app_label))