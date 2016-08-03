import sys
import csv
import re
import usaddress
import urllib2
import xml.dom.minidom
import json
from string import Template

# @author: ashwin

def stTypeToAbbrev(streetType):
    if streetType == 'Avenue':
        return 'AV'
    elif streetType == 'Boulevard':
        return 'BL'
    elif streetType == 'Circle':
        return 'CL'
    elif streetType == 'Court':
        return 'CT'
    elif streetType == 'Drive':
        return 'DR'
    elif streetType == 'Expressway':
        return 'EX'
    elif streetType == 'Freeway':
        return 'FY'
    elif streetType == 'Highway':
        return 'HY'
    elif streetType == 'Lane':
        return 'LN'
    elif streetType == 'Loop':
        return 'LP'
    elif streetType == 'Place':
        return 'PL'
    elif streetType == 'Parkway':
        return 'PY'
    elif streetType == 'Road':
        return 'RD'
    elif streetType == 'Square':
        return 'SQ'
    elif streetType == 'Street':
        return 'ST'
    elif streetType == 'Terrace':
        return 'TR'
    elif streetType == 'Walkway':
        return 'WW'
    elif streetType == 'Way':
        return 'WY'
    else:
        return streetType
    
def geocode(address, sensor=False):    
  mapsUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
  url = ''.join([mapsUrl, urllib2.quote(address), '&sensor=', str(sensor).lower()])
  jsonOutput = str(urllib2.urlopen(url).read ())  # get the response 
  jsonOutput = jsonOutput.replace ("\\n", "")
  result = json.loads(jsonOutput)  # converts jsonOutput into a dictionary 
  if result['status'] != "OK": 
    return ""
  coordinates = result['results'][0]['geometry']['location']  # extract the geometry 
  return str(coordinates['lng']) + ',' + str(coordinates['lat'])    
    

def mapsUrlToHref(url, addressString):
    retval = "<a href=\"" + url + ", San Jose, CA\">" + addressString + "</a>"
    return retval


def templateGenerator(cells):
    row = '<tr>'
    for cell in cells:
        s = Template('<td>$column</td>')
        row = row + (s.substitute(column = cell))
    row = row + '</tr>'
    return row

def codeEnforcerLinkGenerator(streetNum, street, streetType):
    s = Template("<a href=javascript:loadDoc(\'$num\',\'$name\',\'$type\')>Link</a>")
    return s.substitute(num = streetNum, name = street, type = streetType)

def loadHTMLHeader(htmlfile):
    htmlHeaderFile = open('housing_script_header.txt')
    for line in htmlHeaderFile:
            htmlfile.write(line) 
    
def loadHTMLFooter(htmlfile):
    htmlFooterFile = open('housing_script_footer.txt')
    for line in htmlFooterFile:
            htmlfile.write(line) 

if __name__ == "__main__":
    if len(sys.argv) < 4:
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

    # Create the HTML file for output

    htmlfile = open(sys.argv[2], "w")

    # initialize rownum variable
    rownum = 0
    
    loadHTMLHeader(htmlfile)
 
    addressList = []

    # generate table contents
    for row in reader:  # Read a single row from the CSV file
        # write header row. assumes first row in csv contains header
        columnList = []
        columnNum = 1
        for column in row:
            if column != '':
                columnList.append(column)
            if columnNum == 1:
                columnTest = column
        numMatch = re.search(r'\d+', columnTest)
        hashTagMatch = re.search(r'#', columnTest)
        if hashTagMatch:
            columnList.append('Code Violations')
        if numMatch:
            addressString = columnList[2]
            mapsUrl = "http://maps.google.com/?q=" + addressString
            addressDict = usaddress.parse(addressString)
            streetNum = (addressDict[0])[0]
            street = (addressDict[1])[0]
            if len(addressDict) >= 3:
                streetType = stTypeToAbbrev((addressDict[2])[0])
            else:
                streetType = ''
            columnList[2] = mapsUrlToHref(mapsUrl, addressString)
            siteTest = columnList[3]
            noSiteMatch = re.search(r'No website', siteTest)
            if not noSiteMatch:
                columnList[3] = '<a href=\"' + siteTest + '\">Link</a>'
            if len(columnList) < 6:
                columnList.append('N/A')
            columnList.append((codeEnforcerLinkGenerator(streetNum, street, streetType)).encode('utf-8').strip()) 
            placemarkElement = kmlDoc.createElement('Placemark')
            nameElement = kmlDoc.createElement('name')
            nameText = kmlDoc.createTextNode(columnList[1])
            nameElement.appendChild(nameText)
            placemarkElement.appendChild(nameElement)
            descriptionElement = kmlDoc.createElement('description')
            descriptionText = kmlDoc.createTextNode(addressString + "<br/>" + columnList[3] + "<br/>" + columnList[4] + "<br/>" + columnList[5])
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
            
        templateRow = templateGenerator(columnList)
        htmlfile.write(templateRow)
         # increment row count 
        rownum += 1

  
    loadHTMLFooter(htmlfile)
    
    # This writes the KML Document to a file.
    kmlFile = open(sys.argv[3], 'w')
    kmlFile.write(kmlDoc.toprettyxml(' '))  
    kmlFile.close()
       

    exit(0)
    
    
    
