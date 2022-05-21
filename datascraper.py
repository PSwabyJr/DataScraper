"""
datascraper.py scrapes data from .csv file from datatree.com. 
Scarped data is saved in a new .csv
"""

import csv
from os import path
from datetime import date
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename



def openScrapeGUI() -> list:
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(title='Select File To Scrape') # show an "Open" dialog box and return the path to the selected file
    parameters = path.splitext(filename)
    newfilename = parameters[0] + "_Scraped"+ parameters[1]
    return filename, newfilename


# Columns to Scrape Data into a new .csv
Parameters = ['APN - UNFORMATTED', 'OWNER MAILING NAME', 'MAILING STREET ADDRESS', 'MAIL CITY', 'MAIL STATE', 'MAIL ZIP/ZIP+4', 'COUNTY', 'SITUS STATE', 'LEGAL DESCRIPTION']
# Columns for new .csv
Header = ['apn', 'ao', 'address1', 'city', 'STATE', 'zip', 'cty', 'ctystate', 'legal description', 'DATE']

if __name__ == "__main__":
    filename, newfilename = openScrapeGUI()
    
    today_date = '{:%d-%b-%Y}'.format(date.today())
    f = open(newfilename, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(Header)
    rows = []
    
    '''
    Note: .csv generated from Datatree.com have data in ALL CAPS format.
    '''
    with open(filename, 'r') as data:
        for dataAttributes in csv.DictReader(data):
            for parameter in Parameters:
                # Keep data in ALL CAPS if it's state initials or legal description
                if parameter == 'MAIL STATE' or parameter == 'SITUS STATE' or parameter == 'LEGAL DESCRIPTION':
                    rows.append(dataAttributes[parameter])
                else:
                    rows.append(dataAttributes[parameter].title()) # puts data in CamelCase format
            rows.append(today_date)
            writer.writerow(rows)
            rows.clear()
    f.close()    
