import os, unittest, requests
from kanban import app, db

TEST_DB = 'unit_test.db'

class UnitTests(unittest.TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['DEBUG'] = False

        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass

    def test_init(self):
        res = self.app.get('/kanban', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_login(self):
        res = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(res.url, 'http://127.0.0.1:5000/login')

    def test_register_and_login(self):
        cred = {'username':'Hello', 'password':'helloworld', 'confirm_pass':'helloworld'}
        res = requests.post('http://127.0.0.1:5000/register', data = cred)
        res = requests.post('http://127.0.0.1:5000/login', data = cred)

        self.assertEqual(res.url, 'http://127.0.0.1:5000/kanban')   

    def test_login_before_creation(self):
        cred = {'username':'IDONTEXIST', 'password':'IDONTEXIST!'}
        res = requests.post('http://127.0.0.1:5000/login', data = cred)

        self.assertEqual(res.url, 'http://127.0.0.1:5000/login')

if __name__ == "__main__":
    unittest.main()
