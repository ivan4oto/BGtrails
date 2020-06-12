from django.test import TestCase

from blog.forms import CreateUserForm


class CreateUserFormTest(TestCase):
    def test_valid_user_form(self):
        form = CreateUserForm(data={'username': 'piron4oto', 'email': 'piron4oto@gmail.com',
                                    'password1': 'Password!1234', 'password2': 'Password!1234'})
        self.assertTrue(form.is_valid())

    def test_too_short_password(self):
        form = CreateUserForm(data={'username': 'piron4oto', 'email': 'piron4oto@gmail.com',
                                    'password1': 'asd', 'password2': 'asd'})
        self.assertFalse(form.is_valid())

    def test_passwords_not_matching(self):
        form = CreateUserForm(data={'username': 'piron4oto', 'email': 'piron4oto@gmail.com',
                                    'password1': 'Password!1234', 'password2': 'Password!4321'})
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        form = CreateUserForm(data={'username': 'piron4oto', 'email': 'ThisMailIsFake',
                                    'password1': 'Password!1234', 'password2': 'Password!1234'})
        self.assertFalse(form.is_valid())