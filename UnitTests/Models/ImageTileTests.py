import unittest
import numpy as np

from Src.Models.BoundingBox import BoundingBox
from Src.Models.ImageTile import ImageTile

class ImageTileTests(unittest.TestCase):
    def testInImageReturnsTrueWhenBoundingBoxInTile(self):
        self.assertTrue(self.imageTileWith(0, 0, 5, 5).inImage(BoundingBox([1, 1, 2, 2])))
        self.assertTrue(self.imageTileWith(1, 1, 10, 10).inImage(BoundingBox([2, 2, 3, 5])))
        self.assertTrue(self.imageTileWith(-2, -2, 3, 6).inImage(BoundingBox([0, 0, 1, 3])))
        self.assertTrue(self.imageTileWith(1, 3, 1,1).inImage(BoundingBox([0, 0, 1, 3])))
        self.assertTrue(self.imageTileWith(9, 9, 5, 5).inImage(BoundingBox([10, 10, 10, 30])))

    def testPartInImageReturnsSubsetOfImage(self):
        image1 = np.array([[0,0,0],
                           [0,1,1],
                           [0,1,1]])
        imageTile1 = self.imageTileWithImage(self.boundingBoxWith(0, 0, 3, 3), image1)
        subTile1 = imageTile1.partInImage(self.boundingBoxWith(1, 1, 2, 2))
        self.assertTrue(np.all(np.array([[1,1], [1,1]]) == subTile1))

        imageTile2 = self.imageTileWithImage(self.boundingBoxWith(3,3,3,3), image1)
        subTile2 = imageTile2.partInImage(self.boundingBoxWith(4, 4, 2, 2))
        self.assertTrue(np.all(np.array([[1, 1], [1, 1]]) == subTile2))

        imageTile3 = self.imageTileWithImage(self.boundingBoxWith(3,3,3,3), image1)
        subTile3 = imageTile3.partInImage(self.boundingBoxWith(5, 4, 2, 2))
        self.assertTrue(np.all(np.array([[1], [1]]) == subTile3))

        imageTile4 = self.imageTileWithImage(self.boundingBoxWith(3, 3, 3, 3), image1)
        subTile4 = imageTile4.partInImage(self.boundingBoxWith(4, 5, 2, 2))
        self.assertTrue(np.all(np.array([[1], [1]]) == subTile4))

    #Helper methods
    def boundingBoxWith(self, left, right, width, height):
        return BoundingBox([left, right, width, height])

    def imageTileWith(self, left, right, width, height):
        boundingBox = self.boundingBoxWith(left, right, width, height)
        image = np.zeros([height, width])
        return self.imageTileWithImage(boundingBox, image)

    def imageTileWithImage(self, boundingBox, image):
        return ImageTile(image, boundingBox)

if __name__ == '__main__':
    unittest.main()
