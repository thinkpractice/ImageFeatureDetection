import matplotlib.pyplot as plt
from Src.GeoMap import GeoMap

geoMap = GeoMap.open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Parkstad.tif")
print ("width={}, height={}".format(geoMap.widthInPixels, geoMap.heightInPixels))

#geotransform = dataset.GetGeoTransform()
#print (geotransform)
#coverageInM = (dataset.RasterXSize * abs(geotransform[1]) + dataset.RasterYSize * abs(geotransform[5]))
#print(coverageInM)

tileWidth = 300
numRows = 2
numColumns = 2
f,axarr = plt.subplots(numRows, numColumns)
for row in range(numRows):
    y = row * tileWidth
    for column in range(numColumns):
        x = column * tileWidth
        stacked = geoMap.readTile(x, y, 300, 300)
        axarr[row, column].imshow(stacked, interpolation='nearest', vmin=0)
plt.show()
