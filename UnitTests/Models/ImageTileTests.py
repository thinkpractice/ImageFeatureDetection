import unittest
import numpy as np

from Src.Models.BoundingBox import BoundingBox
from Src.Models.ImageTile import ImageTile

class ImageTileTests(unittest.TestCase):
    def testInImageReturnsWhetherBoundingBoxInTile(self):
        self.assertTrue(self.imageTileWith(0, 0, 5, 5).inImage(BoundingBox([1, 1, 2, 2])))
        self.assertTrue(self.imageTileWith(1,1, 10, 10).inImage(BoundingBox([2, 2, 3, 5])))
        self.assertTrue(self.imageTileWith(-2, -2, 3, 6).inImage(BoundingBox([0, 0, 1, 3])))
        self.assertTrue(self.imageTileWith(1, 3, 1,1).inImage(BoundingBox([0, 0, 1, 3])))
        self.assertTrue(self.imageTileWith(9, 9, 5, 5).inImage(BoundingBox([10, 10, 10, 30])))

    #Helper methods
    def imageTileWith(self, left, right, width, height):
        boundingBox = BoundingBox([left, right, width, height])
        image = np.zeros([height, width])
        return ImageTile(image, boundingBox)

if __name__ == '__main__':
    unittest.main()
