import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

class ScrapePage:
    def __init__(self, url, verifyText=None, cached=True):
        self._cached = cached
        self._url = url
        # these to be populated only if caching is off
        self._pagetext = None
        self._soup = None
        
        # only run requests when cached is off
        if not self._cached:
            self._pagetext = self._scrapepage()
            self._soup = BeautifulSoup(self._pagetext, 'html.parser')

    def _scrapepage(self):
        try:
            page = requests.get(self._url)
            pagetext = page.text
            return pagetext
        except:
            # log 
            print('Unable to scrape!')

    def scrape_table(self, identifier, saveas_csv, include_header=True, extract_links=False):
        # check if cached mode is on and file exists -> do not scrape then
        if self._cached and os.path.isfile(saveas_csv):
            return None
        # else cached is off -> scrape then
        # or cached is on file not exists though -> scrape then (but need to populate soup first, since constructor does not do it)
        else:
            if self._soup is None:
                self._pagetext = self._scrapepage()
                self._soup = BeautifulSoup(self._pagetext, 'html.parser')

            table = None
            if 'class' in identifier:
                table = self._soup.find("table", {"class": identifier['class']})
            elif 'id' in identifier:
                table = self._soup.find("table", {"id": identifier['id']})
            else:
                # log
                print('No valid identifier found')
                return None
            table_data = list()

            # extract headers
            headers = list()
            for table_head in table.find_all('thead'):
                for table_head_row in table_head.find_all('tr'):
                    for table_head_row_data in table_head_row.find_all('th'):
                        headers.append(table_head_row_data.get_text(strip=True))

            if include_header:
                table_data.append(headers)

            # extract data
            for table_body in table.find_all('tbody'):
                for table_row in table_body.find_all('tr'):
                    row_data = list()
                    anchors = list()
                    for table_row_data in table_row.find_all('td'):
                        row_data.append(table_row_data.get_text(strip=True))
                        # extract links if available in that cell
                        if extract_links:
                            for link in table_row_data.find_all('a'):
                                anchors.append(link['href'])
                    if extract_links:
                        row_data.append(anchors)
                    table_data.append(row_data)
            
            # write to csv
            # check if dir exists
            dir = os.path.dirname(saveas_csv)
            if not os.path.isdir(dir):
                os.mkdir(dir)

            with open(saveas_csv, 'w', newline="") as f:
                writer = csv.writer(f)
                for table_row in table_data:
                    writer.writerow(table_row)

# test stub
if __name__ == '__main__':
    sc = ScrapePage("https://www.worldometers.info/co2-emissions/co2-emissions-by-country/")
    sc.scrape_table({"id":"example2"}, saveas_csv='F:/work_learning/Chart Animation/utility/data/country-co2.csv', extract_links=True)

    sc_i = ScrapePage("https://www.worldometers.info/co2-emissions/india-co2-emissions/")
    sc_i.scrape_table({"class":"table table-striped table-bordered table-hover table-condensed table-list"}, saveas_csv='F:/work_learning/Chart Animation/utility/data/india-co2.csv')