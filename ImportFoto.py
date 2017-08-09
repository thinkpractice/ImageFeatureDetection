import gdal
from gdalconst import *
import numpy
import matplotlib
import matplotlib.pyplot as plt

def readGeoImage(dataset, startX, startY, width, height):
    R = dataset.GetRasterBand(1)
    G = dataset.GetRasterBand(2)
    B = dataset.GetRasterBand(3)

    redArray = R.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)
    greenArray = G.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)
    blueArray = B.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)

    redArray = numpy.expand_dims(redArray, axis=2)
    greenArray = numpy.expand_dims(greenArray, axis=2)
    blueArray = numpy.expand_dims(blueArray, axis=2)

    stacked = numpy.append(redArray, greenArray, axis=2)
    return numpy.append(stacked, blueArray, axis=2)


dataset = gdal.Open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Parkstad.tif", GA_ReadOnly)

if dataset is None:
    print("Could not read dataset")

geotransform = dataset.GetGeoTransform()
coverageInM = (dataset.RasterXSize * abs(geotransform[1]) + dataset.RasterYSize * abs(geotransform[5]))
print(coverageInM)

tileWidth = 300
numRows = 2
numColumns = 2
f,axarr = plt.subplots(numRows, numColumns)
for row in range(numRows):
    y = row * tileWidth
    for column in range(numColumns):
        x = column * tileWidth
        stacked = readGeoImage(dataset, x, y, 300, 300)
        axarr[row, column].imshow(stacked, interpolation='nearest', vmin=0)
plt.show()
