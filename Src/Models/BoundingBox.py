class BoundingBox(object):
    def __init__(self, boundingBoxArray):
        self.__left = boundingBoxArray[0]
        self.__top = boundingBoxArray[1]
        self.__width = boundingBoxArray[2]
        self.__height = boundingBoxArray[3]

    @property
    def left(self):
        return self.__left

    @property
    def top(self):
        return self.__top

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def xRange(self):
        return slice(self.left, self.right + 1)

    @property
    def yRange(self):
        return slice(self.top, self.bottom + 1)

    def inBox(self, other):
        #todo check!!
        return (other.left >= self.left or other.right <= self.right) and \
               (other.top >= self.top or other.bottom <= self.bottom)