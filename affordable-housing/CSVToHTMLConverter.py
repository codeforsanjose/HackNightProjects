import sys
import csv
import re
import usaddress

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
    retval = "<a href=\"" + url + " San Jose, CA\">" + addressString + "</a>"
    return retval

def javaScriptWriter():
    retval = "<script>\r\nfunction loadDoc(streetName, street, streetType) {\r\n  var xhttp = new XMLHttpRequest();\r\n  \r\n\r\nvar settings = {\r\n  \"async\": true,\r\n  \"crossDomain\": true,\r\n  \"url\": \"http://www3.sanjoseca.gov/codeEnforcement/cets/New_ces_Results.asp\",\r\n  \"method\": \"POST\",\r\n  \"headers\": {\r\n    \"accept-language\": \"en-us\",\r\n    \"content-type\": \"application/x-www-form-urlencoded; Charset=UTF-8\",\r\n    \"Access-Control-Allow-Origin\" : \"http://localhost\"\r\n  },\r\n  \"data\": \"PropHouse=\" + streetName + \"&PropStreet=\" + street + \"&PropStreetType=\" + streetType\r\n}\r\n\r\n$.ajax(settings).done(function (response) {\r\n  console.log(response);\r\n\r\n});\r\n\r\n}\r\n</script>"
    return retval
    

if len(sys.argv) < 3:
    print "Usage: csvToTable.py csv_file html_file"
    exit(1)

print sys.argv

# Open the CSV file for reading

reader = csv.reader(open(sys.argv[1]))

# Create the HTML file for output

htmlfile = open(sys.argv[2], "w")

# initialize rownum variable
rownum = 0

htmlfile.write("<!DOCTYPE html>\r\n<script type=\"text/javascript\" src=\"http://code.jquery.com/jquery-1.7.1.min.js\"></script>\r\n<html>\r\n<body>\r\n\r\n<h2>AFFORDABLE PROPERTIES IN SAN JOSE</h2>")
htmlfile.write(javaScriptWriter())

htmlfile.write("""<style>
    td, th {
                border: 1px solid #999;
                    padding: 0.5rem;
                    }
    </style>""")


# write <table> tag
htmlfile.write("<body>")
htmlfile.write('<table>')

# generate table contents
for row in reader:  # Read a single row from the CSV file
# write header row. assumes first row in csv contains header
    if rownum == 0:
        htmlfile.write('<tr>')  # write <tr> tag
        for column in row:
            htmlfile.write('<th>' + column + '</th>')
        htmlfile.write('</tr>')
# write all other rows 
    else:
        htmlfile.write('<tr>')
        columnNum = 1
        for column in row:
            if columnNum == 1:
                numTest = column
            numMatch = re.search(r'\d+', numTest)
            if numMatch:
                if columnNum == 3:
                    addressString = column
                    mapsUrl = "http://maps.google.com/?q=" + addressString
                    addressDict = usaddress.parse(addressString)
                    streetNum = (addressDict[0])[0]
                    street = (addressDict[1])[0]
                    if len(addressDict) >= 3:
                        streetType = stTypeToAbbrev((addressDict[2])[0])
                    else:
                        streetType = ''
                    htmlfile.write('<td>' + mapsUrlToHref(mapsUrl, addressString) + '</td>\n')
                elif columnNum == 4:
                    siteTest = column
                    noSiteMatch = re.search(r'No website', siteTest)
                    if not noSiteMatch:
                        htmlfile.write('<td><a href=\"' + siteTest + '\">Link</a></td>\n')
                    else:
                        htmlfile.write('<td>' + column + '</td>')
                else:
                    htmlfile.write('<td>' + column + '</td>')
            else:
                htmlfile.write('<td>' + column + '</td>')
            columnNum += 1
        if rownum == 1:
            htmlfile.write('<td>' + 'Code Violations' + '</td>')
        if numMatch:
            htmlfile.write("<td><A HREF=javascript:loadDoc(\'" + streetNum + "\',\'" + street + "\',\'" + streetType + "\')>Link</A></td>\n")
        htmlfile.write('</tr>\n')

    # increment row count 
    rownum += 1

# write </table> tag
htmlfile.write('</table>')
htmlfile.write("</body>")
htmlfile.write("</html>")

# print results to shell
print "Created " + str(rownum) + " row table."
exit(0)


