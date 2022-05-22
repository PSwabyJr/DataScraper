"""
datascraper.py scrapes data from .csv file from datatree.com. 
Scarped data is saved in a new .csv
"""
import sys
import os
import csv
import shutil
from os import path
from datetime import date
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename


class DataScraper:
    def __init__(self, *args):
        self.Parameters = args[0]
        self.Header = args[1]
        
        if len(sys.argv) == 1:
            self.filename, self.newfilename = self.openScrapeGUI()
            self.scrapeCSV()
        else:
            self.filename = None 
            self.newfilename = None
            self.scrapeMultipleCSV()

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
    
    def scrapeMultipleCSV(self):
        dir = sys.argv[1]

        if os.path.isdir(dir):
            dir_files_folders = os.listdir(dir)
        
            for item in dir_files_folders:
                if '.csv' in item:
                    self.filename = dir + "\\" + item
                    self.newfilename = dir + "\\"  + item.split('.')[0] + '_Scraped.csv'   #item.split pulls the filename minus the .csv extension
                    self.scrapeCSV()
            self.moveFiles()
        else:
            current_dir = os.getcwd() + "\\"
            print(current_dir)
            f = open(current_dir+'error.log', 'a', newline="\n")
            f.write(f'The directory {sys.argv[1]} does not exist. Check entered directory in autoScrape.bat for possible typos\n')
            f.close()


    def moveFiles(self):
        current_dir = sys.argv[1]
        current_dir_files_folders = os.listdir(current_dir)

        scraped_files_dir = current_dir + "\\" + "Scarped Files"
        raw_files_dir = current_dir + "\\" + "Raw Files"

        if not os.path.isdir(scraped_files_dir):
            os.makedirs(scraped_files_dir)  #make directory if it doesn't exist
        
        if not os.path.isdir(raw_files_dir):
            os.makedirs(raw_files_dir)  #make directory if it doesn't exist

        for item in current_dir_files_folders:
            if '.csv' in item:
                if '_Scraped' in item:
                    shutil.move(current_dir + "\\" + item, scraped_files_dir + "\\" + item)
                else:
                    shutil.move(current_dir + "\\" + item, raw_files_dir + "\\" + item)
             
if __name__ == "__main__":
    #TODO: Parameters and Header will be refactored at a future update
    # Columns to Scrape Data into a new .csv
    Parameters = ['APN - UNFORMATTED', 'OWNER MAILING NAME', 'MAILING STREET ADDRESS', 'MAIL CITY', 'MAIL STATE', 'MAIL ZIP/ZIP+4', 'COUNTY', 'SITUS STATE', 'LEGAL DESCRIPTION']
    # Columns for new .csv
    Header = ['apn', 'ao', 'address1', 'city', 'STATE', 'zip', 'cty', 'ctystate', 'legal description', 'DATE']
    scrape = DataScraper(Parameters,Header)   
