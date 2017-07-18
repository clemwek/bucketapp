import unittest
from bucketapp.bucketapp import app, get_id_for_email, add_bucket_list, rm_bucket_list, edit_bucket_list


class TestBucketListApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def register(self, name, email, password):
        return self.client.post(
            '/register',
            data=dict(inputName=name, inputEmail=email, inputPassword=password, inputPasswordAgain="test"),
            follow_redirects=True
        )

    def login(self, email, password):
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
        # self.assertFalse(session['logged_in'])

    def test_login(self):
        self.register('test', 'test2@test.com', 'test')
        self.logout()
        response = self.login('test@te.com', 'test')
        self.assertIn(b'You do not have an account, please register.', response.data)
        response = self.login('test2@test.com', 'test')
        self.assertIn(b'You are logged in', response.data)

    def test_add_edit_delete_bucket_list(self):
        add_bucket_list('test', 'abdfhs')
        self.assertIn('abdfhs', app.bucketlist)
        self.assertTrue(len(app.bucketlist['abdfhs']) == 1)

        edit_bucket_list('test edit', 'abdfhs', list(app.bucketlist['abdfhs'].keys())[0])
        self.assertEqual('test edit', app.bucketlist['abdfhs'][list(app.bucketlist['abdfhs'].keys())[0]].name)

        add_bucket_list('test2', 'abdfhs')
        init_bucket_count = len(app.bucketlist['abdfhs'])
        rm_bucket_list(list(app.bucketlist['abdfhs'].keys())[0], 'abdfhs')
        self.assertEqual(init_bucket_count - len(app.bucketlist['abdfhs']), 1)

if __name__ == '__main__':
    unittest.main()
