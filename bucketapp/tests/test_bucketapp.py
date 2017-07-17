import unittest
from bucketapp.bucketapp import app


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
            # self.client.post(
            #     '/register',
            #     data=dict(inputName='test', inputEmail='test@test.com', inputPassword=password, inputPasswordAgain="test"),
            #     follow_redirects=True
            # )
            # self.client.get(
            #     '/logout', follow_redirects=True)
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
        # self.assertTrue(response.session['email'] == "test@test.com")
        # self.assertTrue(self.client.session['logged_in'])

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
        self.assertIn(b'Invalid email, please try again.', response.data)

    def test_adding_bucketlist(self):
        self.login('test@test.com', 'test')
        welcome = self.client.get('/add_bucketlist', content_type='html/text')
        self.assertEqual(welcome.status_code, 200)

        response = self.client.post('/add_bucketlist', data=dict(bucketlist='test bucketlis'), follow_redirects=True)
        self.assertIn(b'has been added successful.', response.data)

    # def test_session_created(self):
    #     self.assertFalse(self.client.session['logged_in'])


if __name__ == '__main__':
    unittest.main()
