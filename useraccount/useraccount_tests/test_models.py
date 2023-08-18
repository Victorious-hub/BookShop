from unittest import TestCase

from useraccount.models import SimpleUser, UserAccount


class UserAccountTest(TestCase):
    simpleuser1 = SimpleUser.objects.create(
        first_name='Vitya',
        last_name='Shyster',
        email='vitya@gmail.com',
        user_linkedin='https://education.github.com/globalcampus/exchange',
        user_github='https://education.github.com/globalcampus/exchange'
    )

    simpleuser2 = SimpleUser.objects.create(
        first_name='John',
        last_name='Doe',
        email='john@gmail.com',
        user_linkedin='https://education.github.com/globalcampus/exchange',
        user_github='https://education.github.com/globalcampus/exchange'
    )
    def setUp(self):
        self.user = UserAccount.objects.create(
            first_name='John',
            last_name='Doe',
            user_linkedin='https://education.github.com/globalcampus/exchange',
            user_github='https://education.github.com/globalcampus/exchange'
        )

    def test_slug(self):
        self.assertEquals(self.user.slug, 'john')

