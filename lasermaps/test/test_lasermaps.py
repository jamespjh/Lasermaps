import lasermaps
import unittest

class TestLaserMap(unittest.TestCase):

    def setUp(self):
        self.lasermap=lasermaps.Lasermap("London",size=8)

    def test_create(self):
        self.assertIsNotNone(self.lasermap)
        
    def test_requesturi(self):
        self.assertRegexpMatches(self.lasermap.requesturl(),
        "http://maps.googleapis.com/maps/api/staticmap\?")
        
    def test_getimage(self):
        self.assertRegexpMatches(self.lasermap.getimage().read(),"PNG")
    