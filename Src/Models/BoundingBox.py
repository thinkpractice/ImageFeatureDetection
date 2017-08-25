class BoundingBox(object):
    def __init__(self, boundingBoxArray):
        self.__topX = boundingBoxArray[0]
        self.__topY = boundingBoxArray[1]
        self.__width = boundingBoxArray[2]
        self.__height = boundingBoxArray[3]

    @property
    def topX(self):
        return self.__topX

    @property
    def topY(self):
        return self.__topY

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def maxX(self):
        return self.topX + self.width

    @property
    def maxY(self):
        return self.topY + self.height

    @property
    def xRange(self):
        return slice(self.topX, self.maxX+1)

    @property
    def yRange(self):
        return slice(self.topY, self.maxY + 1)

    def inBox(self, other):
        return False