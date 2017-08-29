from Src.Controllers.GeoMapTileController import GeoMapTileController
from Src.Models.GeoMap import GeoMap
from Src.Models.GeoTileCollection import GeoTileCollection
from Src.Models.GeoMapThumbnailer import GeoMapThumbnailer
from Src.Views.MapView import MapView


class App(object):
    def main(self):
        geoMap = GeoMap.open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Parkstad.tif")
        geoTileCollection = GeoTileCollection(geoMap)

        mapView = MapView()
        self.controller = GeoMapTileController(geoTileCollection, mapView)
        print("width={}, height={}".format(geoMap.widthInPixels, geoMap.heightInPixels))

        self.geoMapThumbnailer = GeoMapThumbnailer(geoMap)
        self.geoMapThumbnailer.createAllThumbnails()

        # coverageInM = (dataset.RasterXSize * abs(geotransform[1]) + dataset.RasterYSize * abs(geotransform[5]))
        # print(coverageInM)


if __name__ == '__main__':
    app = App()
    app.main()