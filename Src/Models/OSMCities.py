import overpy

class OSMCities(object):
    def __init__(self, country="Nederland"):
        self.__country = country
        self.__cities = []
        self.__cityNames = []

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

    def performCityQuery(self, countryName):
        overApi = overpy.Overpass()
        query = 'area[name="{}"];(node[place~"^(city|town)$"](area););out;'
        return overApi.query(query.format(countryName))
