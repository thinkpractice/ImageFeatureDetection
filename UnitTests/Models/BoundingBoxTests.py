import unittest

from Src.Models.BoundingBox import BoundingBox


class BoundingBoxTests(unittest.TestCase):
    def testLeftSetCorrectly(self):
        self.assertEqual(1, BoundingBox([1, 6, 10, 20]).left)
        self.assertEqual(2, BoundingBox([2, 7, 11, 21]).left)
        self.assertEqual(3, BoundingBox([3, 8, 12, 22]).left)
        self.assertEqual(4, BoundingBox([4, 9, 13, 23]).left)
        self.assertEqual(5, BoundingBox([5, 10, 14, 24]).left)

    def testTopSetCorrectly(self):
        self.assertEqual(6, BoundingBox([1, 6, 10, 20]).top)
        self.assertEqual(7, BoundingBox([2, 7, 11, 21]).top)
        self.assertEqual(8, BoundingBox([3, 8, 12, 22]).top)
        self.assertEqual(9, BoundingBox([4, 9, 13, 23]).top)
        self.assertEqual(10, BoundingBox([5, 10, 14, 24]).top)

    def testRightCalculatedCorrectly(self):
        self.assertEqual(11, BoundingBox([1, 6, 10, 20]).right)
        self.assertEqual(13, BoundingBox([2, 7, 11, 21]).right)
        self.assertEqual(15, BoundingBox([3, 8, 12, 22]).right)
        self.assertEqual(17, BoundingBox([4, 9, 13, 23]).right)
        self.assertEqual(19, BoundingBox([5, 10, 14, 24]).right)

    def testBottomCalculatedCorrectly(self):
        self.assertEqual(26, BoundingBox([1, 6, 10, 20]).bottom)
        self.assertEqual(28, BoundingBox([2, 7, 11, 21]).bottom)
        self.assertEqual(30, BoundingBox([3, 8, 12, 22]).bottom)
        self.assertEqual(32, BoundingBox([4, 9, 13, 23]).bottom)
        self.assertEqual(34, BoundingBox([5, 10, 14, 24]).bottom

if __name__ == '__main__':
    unittest.main()
