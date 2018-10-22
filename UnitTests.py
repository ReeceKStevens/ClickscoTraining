import unittest
import xml.etree.ElementTree as ET
from Server1 import chooseAd
from Server2 import apply_strategy

class TestAdSelection(unittest.TestCase):

    def test_input1_valid(self):
        keywords='food'
        self.assertEqual(chooseAd(keywords), 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/220px-Good_Food_Display_-_NCI_Visuals_Online.jpg')

    def test_imput1_invalid(self):
        keywords='leg'
        self.assertEqual(chooseAd(keywords), '')

    def test_input2_valid(self):
        keywords='sweets mango'
        self.assertEqual(chooseAd(keywords), 'https://cdn2.bigcommerce.com/server5100/4030hufb/products/1295/images/2407/Sweets_Sept_17_0020__52696.1507070952.500.750.jpg?c=2')

    def test_input2_validinvalid(self):
        keywords ='mango keyhole'
        self.assertEqual(chooseAd(keywords), 'https://i5.walmartimages.ca/images/Large/188/9_r/6000191271889_R.jpg')

    def testinput2_invalid(self):
        keywords = 'pool skateboard'
        self.assertEqual(chooseAd(keywords), '')

    def test_noinput(self):
        keywords = ''
        self.assertEqual(chooseAd(keywords), '')

class TestServerTwo(unittest.TestCase):

    def test_Half(self):
        configdata = ET.parse('data/ServerB.config')
        root = configdata.getroot()
        self.assertEqual(apply_strategy(root, 50), 25)

    def test_five(self):
        configdata = ET.parse('data/ServerC.config')
        root = configdata.getroot()
        self.assertEqual(apply_strategy(root, 50), 5)

    def test_ten(self):
        configdata = ET.parse('data/ServerD.config')
        root = configdata.getroot()
        self.assertEqual(apply_strategy(root, 50), 10)

if __name__=='__main__':
    unittest.main()
