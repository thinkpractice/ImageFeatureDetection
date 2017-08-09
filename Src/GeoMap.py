class GeoMap(object):
    def __init__(self, dataset):
        """Constructor

        :param gdal dataset: the gdal dataset for a GeoTiff file
        """
        self.__dataset = dataset

    @property
    def dataset(self):
        return self.__dataset

    @property
    def widthInPixels(self):
        return self.dataset.RasterXSize

    @property
    def heightInPixels(self):
        return self.dataset.RasterYSize