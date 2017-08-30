import os
import shapefile
import csv

class GenerateTrainingData(object):
    def __init__(self, imageFolder, addressShapeFile, addressPositives):
        self.__imageFolder = imageFolder
        self.__addressShapeFile = addressShapeFile
        self.__addressPositives = addressPositives

    @property
    def imageFolder(self):
        return self.__imageFolder

    @property
    def addressShapeFile(self):
        return self.__addressShapeFile

    @property
    def addressPositives(self):
        return self.__addressPositives

    def generateTrainingSet(self):
        addressShapes = shapefile.Reader(self.addressShapeFile)
        addressLookup = self.generatePositivesLookup(self.addressPositives)
        positivesPath = os.path.join(self.imageFolder, "Positives")
        os.mkdir(positivesPath)
        negativesPath = os.path.join(self.imageFolder, "Negatives")
        os.mkdir(negativesPath)
        for addressRecord in addressShapes.iterRecords():
            address, buildingNumber = self.getRecordInfo(addressRecord)
            imagePath = self.filePathFor(buildingNumber)
            if not os.path.exists(imagePath):
                continue

            imageFilename = self.imageNameFor(buildingNumber)
            if address in addressLookup:
                os.rename(imagePath, os.path.join(positivesPath, imageFilename))
            else:
                os.rename(imagePath, os.path.join(negativesPath, imageFilename))

    def generatePositivesLookup(self, filename):
        lookup = set()
        with open(filename, "r") as positivesFile:
            csvReader = csv.DictReader(positivesFile, delimiter=",")
            for row in csvReader:
                keyTuple = self.getAddressFromLookup(row)
                lookup.add(keyTuple)
        return lookup

    def filePathFor(self, buildingNumber):
        filename = self.imageNameFor(buildingNumber)
        path = os.path.join(self.imageFolder, filename)
        return path

    def imageNameFor(self, buildingNumber):
        return "{}.png".format(buildingNumber)

    def getAddressFromLookup(self, row):
        return (row["pc6"],row["huisnr"])

    def getRecordInfo(self, addressRecord):
        pass