import overpy

class OSMCities(object):
    def __init__(self, country="Nederland"):
        self.__overApi = None
        self.__country = country
        self.__cities = []
        self.__cityNames = []

    @property
    def overApi(self):
        if not self.__overApi:
            self.__overApi = overpy.Overpass()
        return self.__overApi

    @property
    def country(self):
        return self.__country

    @property
    def cities(self):
        if not self.__cities:
            self.__cities = self.performCityQuery(self.country)
        return self.__cities

    @property
    def cityNames(self):
        if not self.__cityNames:
            self.__cityNames = sorted([node.tags["name"] for node in self.cities.nodes])
        return self.__cityNames

    def getNodeForCity(self, cityName):
        for node in self.cities:
            if node.tags["name"] == cityName:
                return node
        return None

    def getBoundingBoxForCity(self, cityName):
        query = '(rel[name="{}"];>;);out;'.format(cityName)
        result = self.overApi.query(query)
        latitudes = [float(node.lat) for node in result.nodes]
        longitudes = [float(node.lon) for node in result.nodes]
        return (min(latitudes), min(longitudes), max(latitudes), max(longitudes))

    def performCityQuery(self, countryName):
        query = 'area[name="{}"];(node[place~"^(city|town)$"](area););out;'
        return self.overApi.query(query.format(countryName))
