"""
datascraper.py scrapes data from .csv file from datatree.com. 
Scarped data is saved in a new .csv
"""
import sys
import os
import csv
from os import path
from datetime import date
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename


class DataScraper:
    def __init__(self, *args):
        if len(sys.argv) == 1:
            self.Parameters = args[0]
            self.Header = args[1]
            self.filename, self.newfilename = self.openScrapeGUI()
            self.scrapeCSV()
        else:
            self.filename, self.newfilename = None

    def openScrapeGUI(self) -> list:
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename(title='Select File To Scrape') # show an "Open" dialog box and return the path to the selected file
        parameters = path.splitext(filename)
        newfilename = parameters[0] + "_Scraped"+ parameters[1]
        return filename, newfilename
    
    def scrapeCSV(self):
        today_date = '{:%d-%b-%Y}'.format(date.today())
        f = open(self.newfilename, 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(self.Header)
        rows = []
        
        '''
        Note: .csv generated from Datatree.com have data in ALL CAPS format.
        '''
        with open(self.filename, 'r') as data:
            for dataAttributes in csv.DictReader(data):
                for parameter in self.Parameters:
                    # Keep data in ALL CAPS if it's state initials or legal description 
                    # TODO: Line 46 will be refactored to generalize any list for scraping
                    if parameter == 'MAIL STATE' or parameter == 'SITUS STATE' or parameter == 'LEGAL DESCRIPTION':
                        rows.append(dataAttributes[parameter])
                    else:
                        rows.append(dataAttributes[parameter].title()) # puts data in CamelCase format
                rows.append(today_date)
                writer.writerow(rows)
                rows.clear()
        f.close()
    
    #TODO: Will be developed to scrape multiple .csv files
    def scrapeMultipleCSV(self, *args):
        pass
        

if __name__ == "__main__":
    #TODO: Parameters and Header will be refactored at a future update
    # Columns to Scrape Data into a new .csv
    Parameters = ['APN - UNFORMATTED', 'OWNER MAILING NAME', 'MAILING STREET ADDRESS', 'MAIL CITY', 'MAIL STATE', 'MAIL ZIP/ZIP+4', 'COUNTY', 'SITUS STATE', 'LEGAL DESCRIPTION']
    # Columns for new .csv
    Header = ['apn', 'ao', 'address1', 'city', 'STATE', 'zip', 'cty', 'ctystate', 'legal description', 'DATE']
    scrape = DataScraper(Parameters,Header)   
