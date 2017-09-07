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

        self.createDir(positivesPath)
        negativesPath = os.path.join(self.imageFolder, "Negatives")
        self.createDir(negativesPath)
        for addressRecord in addressShapes.iterRecords():
            address, buildingNumber = self.getRecordInfo(addressRecord)
            imagePath = self.filePathFor(buildingNumber)
            if not os.path.exists(imagePath):
                print("Not available {}, address={}".format(imagePath, address))
                continue

            imageFilename = self.imageNameFor(buildingNumber)
            if address in addressLookup:
                os.rename(imagePath, os.path.join(positivesPath, imageFilename))
            else:
                os.rename(imagePath, os.path.join(negativesPath, imageFilename))

    def generatePositivesLookup(self, filename):
        lookup = set()
        with open(filename, "r") as positivesFile:
            csvReader = csv.reader(positivesFile, delimiter=",")
            for row in csvReader:
                #TODO filter out rows after 2016 (as our image is from summer 2016)
                keyTuple = self.getAddressFromLookup(row)
                lookup.add(keyTuple)
        return lookup

    def filePathFor(self, buildingNumber):
        filename = self.imageNameFor(buildingNumber)
        path = os.path.join(self.imageFolder, filename)
        return path

    def createDir(self, path):
        if os.path.exists(path):
            return
        os.mkdir(path)

    def imageNameFor(self, buildingNumber):
        return "{}.png".format(buildingNumber)

    def getAddressFromLookup(self, row):
        address = (row[0].lower(), row[1])
        return address

    def getRecordInfo(self, addressRecord):
        #TODO houdt nog geen rekening met huisnummer letter of toevoegingen
        recordInfo = (addressRecord[-9].lower(), str(addressRecord[6])), addressRecord[-3]
        return recordInfo

def main():
    generateTrainingData = GenerateTrainingData(r'/home/tjadejong/Documents/CBS/ZonnePanelen/Images', r'/home/tjadejong/Documents/CBS/ZonnePanelen/Shapes/num_parkstad_wgs84', r'/home/tjadejong/Documents/CBS/ZonnePanelen/addresses_solar_panels.csv')
    generateTrainingData.generateTrainingSet()

if __name__ == "__main__":
    main()