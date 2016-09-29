from botrest import app
import unittest


class BotrestTestClass(unittest.TestCase):

    def test_one(self):
        tester = app.test_client(self)
        resp = tester.get('/',content_type='html/text')
        #print resp
        self.assertEqual(resp.status_code,200)

    def test_atleastOneBotUser(self):
        tester = app.test_client(self)
        resp = tester.get('/userslist')
        self.assertNotEquals(resp.data.rstrip(),'[]','No Bot users found.') 


if __name__ == '__main__':
    unittest.main()