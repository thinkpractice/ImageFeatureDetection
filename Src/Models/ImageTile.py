class ImageTile(object):
    def __init__(self, image, boundingBox):
        self.__image = image
        self.__boundingBox = boundingBox

    @property
    def image(self):
        return self.__image

    @property
    def boundingBox(self):
        return self.__boundingBox

    def inImage(self, otherBoundingBox):
        return otherBoundingBox.overlapsWith(self.boundingBox)

    def partInImage(self, otherBoundingBox):
        if not self.inImage(otherBoundingBox):
            return None
        boundingBoxForOverlap = otherBoundingBox.overlap(self.boundingBox)
        boundingBoxForOverlap.left -= self.boundingBox.left
        boundingBoxForOverlap.top -= self.boundingBox.top
        return self.image[boundingBoxForOverlap.yRange, boundingBoxForOverlap.xRange]