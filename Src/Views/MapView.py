import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class MapView(object):
    def update(self, geoTileCollection):
        tileImage = geoTileCollection.getCurrentTile()
        plt.imshow(tileImage, interpolation='nearest', vmin=0)

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bprev = Button(axprev, 'Previous')

        plt.show()







