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

    

def mapsUrlToHref(url, addressString):
    retval = "<a href=\"" + url + ", San Jose, CA\">" + addressString + "</a>"
    return retval


def rowGenerator(cells):
    row = '<tr>'
    for cell in cells:
        row = row + '<td>%s</td>'%(cell)
    row = row + '</tr>'
    return row

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: csvToTable.py csv_file html_file"
        exit(1)
   
    print sys.argv
    

    # Open the housing dataset CSV file for reading
    reader = csv.reader(open(sys.argv[1]))

    # Create the HTML file for output

    htmlfile = open(sys.argv[2], "w")

    # initialize rownum variable
    rownum = 0
    
    #loadHTMLHeader(htmlfile)
 
    addressList = []
    housingTable = ''

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
        hashTagMatch = re.search(r'#', columnTest)
        if hashTagMatch:
            columnList.append('Code Violations')
        if numMatch:
            columnNum = 0
            for column in columnList:
                if column == '':
                    columnList[columnNum] = 'Not applicable'
                columnNum+=1
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
            columnList.append(("<a href=javascript:loadDoc(\'%s\',\'%s\',\'%s\')>Link</a>" %(streetNum, street, streetType)).encode('utf-8').strip()) 

        columnList = list(filter(lambda x: x!= '', columnList))
        housingTable = housingTable + rowGenerator(columnList)
        
        # increment row count 
        rownum += 1

  
    loadHTMLFile = open('housing_script.txt')
    fileTemplate = Template(loadHTMLFile.read())
    htmlfile.write(fileTemplate.substitute(housingDataTable=housingTable))
       

    exit(0)
    
    
    
