import unittest
from bucketapp.bucketapp import app, get_id_for_email


class TestBucketListApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def register(self, name, email, password):
        # client = app.test_client(self)
        with self.client:
            return self.client.post(
                '/register',
                data=dict(inputName=name, inputEmail=email, inputPassword=password, inputPasswordAgain="test"),
                follow_redirects=True
            )

    def login(self, email, password):
        with self.client:
            return self.client.post(
                '/login',
                data=dict(inputEmail=email, inputPassword=password),
                follow_redirects=True
            )

    def logout(self):
        # client = app.test_client(self)
        with self.client:
            return self.client.get(
                '/logout', follow_redirects=True)

    def test_urls(self):
        welcome = self.client.get('/', content_type='html/text')
        self.assertEqual(welcome.status_code, 200)
        self.assertIn(b'Bucket List', welcome.data)

        login = self.client.get('/login', content_type='html/text')
        self.assertEqual(login.status_code, 200)
        self.assertIn(b'Please sign in', login.data)

    def test_protected_urls(self):
        bucketlist = self.client.get('/bucketlist', content_type='html/text', follow_redirects=True)
        self.assertIn(b'You need to login first', bucketlist.data)

        add_bucketlist = self.client.get('/add_bucketlist', content_type='html/text', follow_redirects=True)
        self.assertIn(b'You need to login first', add_bucketlist.data)

    def test_register(self):
        response = self.register('test', 'test@test.com', 'test')
        self.assertIn(b'You are registered and logged in', response.data)
        response = self.register('test', 'test@test.com', 'test')
        self.assertIn(b'Your email has been used.', response.data)
        self.assertIn("test@test.com", app.registered_emails)
        self.assertTrue(get_id_for_email('test@test.com'))

    def test_logout(self):
        response = self.logout()
        self.assertIn(b'you are logged out.', response.data)

    def test_correct_login(self):
        self.register('test', 'test2@test.com', 'test')
        self.logout()

        response = self.login('test2@test.com', 'test')
        self.assertIn(b'You are logged in', response.data)

    def test_incorrect_login(self):
        response = self.login('test@te.com', 'test')
        self.assertIn(b'You do not have an account, please register.', response.data)

if __name__ == '__main__':
    unittest.main()
