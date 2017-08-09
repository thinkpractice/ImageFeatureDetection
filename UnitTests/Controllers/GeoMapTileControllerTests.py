import unittest
from unittest.mock import MagicMock
from Src.Controllers.GeoMapTileController import GeoMapTileController

class GeoMapTileControllerTests(unittest.TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.view = MagicMock()
        self.tileController = GeoMapTileController(self.model, self.view)

    def testNextMethodCallsNextOnModel(self):
        self.tileController.next()
        self.assertTrue(self.model.next.called)

    def testNextMethodCallsViewUpdate(self):
        type(self.model).next = MagicMock(return_value="testobject")
        self.tileController.next()
        self.view.update.assert_called_with("testobject")

    def testPreviousMethodCallsPreviousOnModel(self):
        self.tileController.previous()
        self.assertTrue(self.model.previous.called)

    def testPreviousMethodCallsViewUpdate(self):
        type(self.model).previous = MagicMock(return_value="testobject")
        self.tileController.previous()
        self.view.update.assert_called_with("testobject")

if __name__ == '__main__':
    unittest.main()
