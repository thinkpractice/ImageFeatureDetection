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

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.top == other.top and self.bottom == other.bottom

    def __str__(self):
        return "bbox({},{},{},{})".format(self.left, self.top, self.width, self.height)

    def __repr__(self):
        return self.__str__()

    def inBox(self, other):
        #todo check!!
        return (self.left >= other.left and self.right <= other.right) and \
               (self.top  >= other.top and self.bottom <= other.bottom)

    def overlapsWith(self, other):
        return self.overlap(other) is not None

    def overlap(self, other):
        left = max(self.left, other.left)
        right = min(self.right, other.right)
        top = max(self.top, other.top)
        bottom = min(self.bottom, other.bottom)
        width = right-left
        height = bottom-top
        if width < 0 or height < 0:
            return None
        return BoundingBox([left, top, width, height])