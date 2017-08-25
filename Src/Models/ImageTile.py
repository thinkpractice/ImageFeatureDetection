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
        return otherBoundingBox.inBox(self.boundingBox)

    def partInImage(self, otherBoundingBox):
        if not self.inImage(otherBoundingBox):
            return None
        return self.image[otherBoundingBox.yRange, otherBoundingBox.xRange]