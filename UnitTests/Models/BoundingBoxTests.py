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
        self.assertEqual(34, BoundingBox([5, 10, 14, 24]).bottom)

    def testXRangeReturnsCorrectSlice(self):
        self.assertEqual(slice(1, 12), BoundingBox([1, 6, 10, 20]).xRange)
        self.assertEqual(slice(2, 14), BoundingBox([2, 7, 11, 21]).xRange)
        self.assertEqual(slice(3, 16), BoundingBox([3, 8, 12, 22]).xRange)
        self.assertEqual(slice(4, 18), BoundingBox([4, 9, 13, 23]).xRange)
        self.assertEqual(slice(5, 20), BoundingBox([5, 10, 14, 24]).xRange)

    def testYRangeReturnsCorrectSlice(self):
        self.assertEqual(slice(6, 27), BoundingBox([1, 6, 10, 20]).yRange)
        self.assertEqual(slice(7, 29), BoundingBox([2, 7, 11, 21]).yRange)
        self.assertEqual(slice(8, 31), BoundingBox([3, 8, 12, 22]).yRange)
        self.assertEqual(slice(9, 33), BoundingBox([4, 9, 13, 23]).yRange)
        self.assertEqual(slice(10, 35), BoundingBox([5, 10, 14, 24]).yRange)

    def testInBoxReturnsFalseIfBoxOutsideOfOtherBox(self):
        self.assertFalse(BoundingBox([1, 1, 2, 2]).inBox(BoundingBox([4, 4, 2, 2])))
        self.assertFalse(BoundingBox([2, 2, 3, 5]).inBox(BoundingBox([2, 8, 3, 5])))
        self.assertFalse(BoundingBox([0, 0, 1, 3]).inBox(BoundingBox([-2, -2, 1, 1])))
        self.assertFalse(BoundingBox([0, 0, 1, 3]).inBox(BoundingBox([2, 0, 1, 1])))
        self.assertFalse(BoundingBox([10, 10, 10, 30]).inBox(BoundingBox([10, 0, 5, 5])))

    def testInBoxReturnsTrueIfBoxInsideOtherBox(self):
        self.assertTrue(BoundingBox([1, 1, 2, 2]).inBox(BoundingBox([0, 0, 4, 4])))
        self.assertTrue(BoundingBox([2, 2, 3, 5]).inBox(BoundingBox([1, 1, 10, 10])))
        self.assertTrue(BoundingBox([0, 0, 1, 3]).inBox(BoundingBox([-2, -2, 5, 6])))
        self.assertTrue(BoundingBox([0, 0, 1, 3]).inBox(BoundingBox([0, 0, 1, 3])))
        self.assertTrue(BoundingBox([10, 10, 10, 30]).inBox(BoundingBox([0, 0, 50, 50])))

    def testOverlapsWithReturnsFalseWhenNoOverlap(self):
        self.assertFalse(BoundingBox([1, 1, 2, 2]).overlapsWith(BoundingBox([4, 4, 2, 2])))
        self.assertFalse(BoundingBox([2, 2, 3, 5]).overlapsWith(BoundingBox([2, 8, 3, 5])))
        self.assertFalse(BoundingBox([0, 0, 1, 3]).overlapsWith(BoundingBox([-2, -2, 1, 1])))
        self.assertFalse(BoundingBox([0, 0, 1, 3]).overlapsWith(BoundingBox([2, 0, 1, 1])))
        self.assertFalse(BoundingBox([10, 10, 10, 30]).overlapsWith(BoundingBox([10, 0, 5, 5])))

    def testOverlapsWithReturnsTrueWithOverlap(self):
        self.assertTrue(BoundingBox([1, 1, 2, 2]).overlapsWith(BoundingBox([0, 0, 1, 1])))
        self.assertTrue(BoundingBox([2, 2, 3, 5]).overlapsWith(BoundingBox([1, 1, 10, 10])))
        self.assertTrue(BoundingBox([0, 0, 1, 3]).overlapsWith(BoundingBox([-2, -2, 3, 6])))
        self.assertTrue(BoundingBox([0, 0, 1, 3]).overlapsWith(BoundingBox([1, 3, 1, 1])))
        self.assertTrue(BoundingBox([10, 10, 10, 30]).overlapsWith(BoundingBox([9, 9, 5, 5])))

    def testOverlapReturnsBoundingBoxOfOverlap(self):
        self.assertEquals(BoundingBox([1,1,0,0]), BoundingBox([1, 1, 2, 2]).overlap(BoundingBox([0, 0, 1, 1])))
        self.assertEquals(BoundingBox([2, 2, 3, 5]), BoundingBox([2, 2, 3, 5]).overlap(BoundingBox([1, 1, 10, 10])))
        self.assertEquals(BoundingBox([0, 0, 1, 3]), BoundingBox([0, 0, 1, 3]).overlap(BoundingBox([-2, -2, 3, 6])))
        self.assertEquals(BoundingBox([1, 3, 0, 0]), BoundingBox([0, 0, 1, 3]).overlap(BoundingBox([1, 3, 1, 1])))
        self.assertEquals(BoundingBox([10, 10, 14, 14]), BoundingBox([10, 10, 10, 30]).overlap(BoundingBox([9, 9, 5, 5])))

if __name__ == '__main__':
    unittest.main()
