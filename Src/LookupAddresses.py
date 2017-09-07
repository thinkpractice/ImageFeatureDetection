import csv
import requests
import time

def query(queryString):
    response = requests.get(queryString)
    if response.status_code == 200:
        return response.json()
    print("error = {}".format(response.status_code))
    return []

def queryPostalCode(city, postalcode, country):
    postalCodeQuery = "http://nominatim.openstreetmap.org/search?format=json&q={}+{}+{}&addressdetails=1&namedetails=1"
    queryString = postalCodeQuery.format(city, postalcode, country)
    json = query(queryString)
    if len(json) > 1:
        print("Multiple postal codes found")
    if len(json) > 0:
        json = json[0]
        return json["lat"], json["lon"]
    return None

def queryAddress(lat, lon):
    addressQuery = "http://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}"
    json = query(addressQuery.format(lat, lon))
    if not json:
        return ""
    return json["address"].get("road", "")


with open(r"/home/tjadejong/Downloads/Adressen_zonnepanelen_zonder_finr.csv", "r") as csvFile:
    csvReader = csv.reader(csvFile, delimiter=";")
    with open(r"/home/tjadejong/Downloads/address_lookup.csv", "w") as csvOut:
        csvWriter = csv.writer(csvOut, delimiter=";")
        for index, line in enumerate(csvReader):
            if index == 0:
                line.append("address lookup")
                csvWriter.writerow(line)
                continue

            gpsCoordinates = queryPostalCode(line[1], line[2], line[3])
            if not gpsCoordinates:
                address = ""
            else:
                lat, lon = gpsCoordinates
                address = queryAddress(lat, lon)
            line.append(address)
            csvWriter.writerow(line)
            time.sleep(2)