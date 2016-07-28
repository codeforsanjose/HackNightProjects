'''
Created on Jul 26, 2016

@author: ashwin
'''

import sys
import csv
import re
import urllib2
import xml.dom.minidom
import json
from bs4 import BeautifulSoup
# @author: ashwin


def getAddresses(url):
    response = urllib2.urlopen(url)
    soup = BeautifulSoup(response.read(), 'html.parser')
    addressList = []
    for link in soup.find_all('a'):
        linkMatch = re.search(r'blobdload.aspx', str(link.get('href')))
        if linkMatch:
            # addressLink = 'http://www.mountainview.gov/' + link.get('href')
            addressString = link.next_element
            addressList.append(addressString.encode('utf-8').strip())
    return addressList

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
    
def createKML(filename):
    # This function creates an XML document and adds the necessary
 # KML elements.

  kmlDoc = xml.dom.minidom.Document()
  
  kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')

  kmlElement = kmlDoc.appendChild(kmlElement)

  documentElement = kmlDoc.createElement('Document')
  documentElement = kmlElement.appendChild(documentElement)
  addresses = getAddresses('http://www.mountainview.gov/depts/cs/parks/parks/dog.asp')
  for address in addresses:
      placemarkElement = kmlDoc.createElement('Placemark')
      nameElement = kmlDoc.createElement('name')
      nameText = kmlDoc.createTextNode('Off-Leash Park')
      nameElement.appendChild(nameText)
      placemarkElement.appendChild(nameElement)
      descriptionElement = kmlDoc.createElement('description')
      descriptionText = kmlDoc.createTextNode(address)
      descriptionElement.appendChild(descriptionText)
      placemarkElement.appendChild(descriptionElement)
      pointElement = kmlDoc.createElement('Point')
      placemarkElement.appendChild(pointElement)
      coorElement = kmlDoc.createElement('coordinates')

      # This geocodes the address and adds it to a  element.
      coordinates = geocode(address)
      coorElement.appendChild(kmlDoc.createTextNode(coordinates))
      pointElement.appendChild(coorElement)

      documentElement.appendChild(placemarkElement)
      

  

  # This writes the KML Document to a file.
  kmlFile = open(filename, 'w')
  kmlFile.write(kmlDoc.toprettyxml(' '))  
  kmlFile.close()
  
  

createKML('dogs.kml')


exit(0)





