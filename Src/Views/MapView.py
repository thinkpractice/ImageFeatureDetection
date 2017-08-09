import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from Src.Models.GeoMap import GeoMap

class MapView(object):
    def update(self, geoTileCollection):
        numberOfRows = geoTileCollection.numberOfRows
        numberOfColumns = geoTileCollection.numberOfColumns

        f, axarr = plt.subplots(numberOfRows, numberOfColumns)
        for row in range(numberOfRows):
            y = row * geoTileCollection.tileHeight
            for column in range(numberOfColumns):
                x = column * geoTileCollection.tileWidth
                tileImage = geoTileCollection.getTileAt(x, y)
                axarr[row, column].imshow(tileImage, interpolation='nearest', vmin=0)

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bprev = Button(axprev, 'Previous')

        plt.show()

geoMap = GeoMap.open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Parkstad.tif")
print ("width={}, height={}".format(geoMap.widthInPixels, geoMap.heightInPixels))

#geotransform = dataset.GetGeoTransform()
#print (geotransform)
#coverageInM = (dataset.RasterXSize * abs(geotransform[1]) + dataset.RasterYSize * abs(geotransform[5]))
#print(coverageInM)






