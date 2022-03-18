import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

class ScrapePage:
    def __init__(self, url, verifyText=None):
        self._url = url
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

    def scrape_table(self, table_id, saveas_csv=None, include_header=True, extract_links=False):
        table = self._soup.find("table", {"id": table_id})
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
        if saveas_csv is not None:
            # check if dir exists
            dir = os.path.dirname(saveas_csv)
            if not os.path.isdir(dir):
                os.mkdir(dir)

            with open(saveas_csv, 'w', newline="") as f:
                writer = csv.writer(f)
                for table_row in table_data:
                    writer.writerow(table_row)
        else:
            return table_data

# test stub
if __name__ == '__main__':
    sc = ScrapePage("https://www.worldometers.info/co2-emissions/co2-emissions-by-country/")
    print(sc.scrape_table("example2", saveas_csv='F:/work_learning/Chart Animation/data/country-co2.csv', extract_links=True))