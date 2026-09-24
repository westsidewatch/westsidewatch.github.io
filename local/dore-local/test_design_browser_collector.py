import unittest
import design_browser_collector as c
class BrowserCollectorContractTests(unittest.TestCase):
 def test_https_public_allowed(self):self.assertTrue(c._allowed('https://example.com/x'))
 def test_http_denied(self):self.assertFalse(c._allowed('http://example.com'))
 def test_wikisource_permanently_denied(self):self.assertFalse(c._allowed('https://zh.wikisource.org/wiki/X'))
 def test_viewports(self):
  self.assertEqual(c._viewport('desktop'),{'width':1440,'height':1000});self.assertEqual(c._viewport('mobile'),{'width':390,'height':844})
if __name__=='__main__':unittest.main()
