# affordable-housing-sanjose
A python converter to visualize affordable housing data for San Jose on an html page.

# Dev Setup #

Python
Eclipse For Python

# Dependencies #

Install the usaddress python library to parse address strings - pip install usaddress

usaddress(https://pypi.python.org/pypi/usaddress)

# Resources #

San Jose affordable-housing datasets - PublishAffordableExcelCSV.csv

Code Enforcer link - http://www3.sanjoseca.gov/codeEnforcement/cets/form_index.asp

# How to run this app #
python CSVToHTMLConverter.py PublishAffordableExcelCSV.csv <name of the html output file>

Example :
python CSVToHTMLConverter.py PublishAffordableExcelCSV.csv housing.html

The resulting html file will contain an html table with the property listings.

#Open issues#

All the addresses do not conform to the US address conventions. Their format differs so we are unable to identify the Street Direction accurately.

Cannot access the code enforcer url via javascript because of CORS issues.

CURL posts to the code enforcer url work fine.







