import sys
import csv
import re
import urllib2
import xml.dom.minidom
import json
import time

# @author: ashwin

def geocode(address, sensor=False):    
 # This function queries the Google Maps API geocoder with an
 # address. It gets back a csv file, which it then parses and
 # returns a string with the longitude and latitude of the address.

 # This isn't an actual maps key, you'll have to get one yourself.
 # Sign up for one here: https://code.google.com/apis/console/
  mapsUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
     
 # This joins the parts of the URL together into one string.
  url = ''.join([mapsUrl, urllib2.quote(address), '&sensor=', str(sensor).lower()])
  jsonOutput = str(urllib2.urlopen(url).read ())  # get the response 
  # fix the output so that the json.loads function will handle it correctly
  jsonOutput = jsonOutput.replace ("\\n", "")
  result = json.loads(jsonOutput)  # converts jsonOutput into a dictionary 
  # check status is ok i.e. we have results (don't want to get exceptions)
  if result['status'] != "OK": 
    return ""
  coordinates = result['results'][0]['geometry']['location']  # extract the geometry 
  return str(coordinates['lng']) + ',' + str(coordinates['lat'])
  time.sleep(0.5)   


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: csvToTable.py csv_file html_file kml_file"
        exit(1)
   
    print sys.argv
    
    kmlDoc = xml.dom.minidom.Document()
  
    kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')

    kmlElement = kmlDoc.appendChild(kmlElement)

    documentElement = kmlDoc.createElement('Document')
    documentElement = kmlElement.appendChild(documentElement)

    # Open the housing dataset CSV file for reading
    reader = csv.reader(open(sys.argv[1]))

    # initialize rownum variable
    rownum = 0

    # generate table contents
    for row in reader:  # Read a single row from the CSV file
         # write header row. assumes first row in csv contains header
        columnList = []
        columnNum = 1
        for column in row:
            columnList.append(column)
            if columnNum == 1:
                columnTest = column
            columnNum+=1
        numMatch = re.search(r'\d+', columnTest)
        if numMatch:
            columnNum = 0
            for column in columnList:
                if column == '':
                    columnList[columnNum] = 'Not applicable'
                columnNum+=1
            addressString = columnList[2] + ", San Jose, CA"
            siteTest = columnList[3]
            noSiteMatch = re.search(r'No website', siteTest)
            if not noSiteMatch:
                columnList[3] = '<a href=\"' + siteTest + '\">Link</a>' 
            placemarkElement = kmlDoc.createElement('Placemark')
            nameElement = kmlDoc.createElement('name')
            nameText = kmlDoc.createTextNode(columnList[1])
            nameElement.appendChild(nameText)
            placemarkElement.appendChild(nameElement)
            descriptionElement = kmlDoc.createElement('description')
            descriptionText = kmlDoc.createTextNode(addressString + "<br/>" + "Property Website: " + columnList[3] + "<br/>" + "Management Company: " + columnList[4] + "<br/>" + "Phone Number: " + columnList[5])
            descriptionElement.appendChild(descriptionText)
            placemarkElement.appendChild(descriptionElement)
            pointElement = kmlDoc.createElement('Point')
            placemarkElement.appendChild(pointElement)
            coorElement = kmlDoc.createElement('coordinates')

            # This geocodes the address and adds it to a  element.
            address = addressString.encode('utf-8').strip()
            coordinates = geocode(address)
            coorElement.appendChild(kmlDoc.createTextNode(coordinates))
            pointElement.appendChild(coorElement)

            documentElement.appendChild(placemarkElement)
        
        # increment row count 
        rownum += 1
    
    # This writes the KML Document to a file.
    kmlFile = open(sys.argv[2], 'w')
    kmlFile.write(kmlDoc.toprettyxml(' '))  
    kmlFile.close()
       

    exit(0)
    
    
    