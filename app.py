import csv
from utility.scrape_utility import ScrapePage

PARENT_CSV = 'F:/work_learning/Chart Animation/data/country-co2.csv'
sc = ScrapePage("https://www.worldometers.info/co2-emissions/co2-emissions-by-country/")
sc.scrape_table({"id":"example2"}, saveas_csv=PARENT_CSV, extract_links=True)

BASE_URL = 'https://www.worldometers.info'
# extract and dump country wise data to csvs 
with open(PARENT_CSV, 'r') as f:
    # Construct the csv reader object from the file object
    reader = csv.reader(f)
    # skip header
    next(reader)
    for row in reader:
        try:
            country = row[1]
            country_page_url = BASE_URL + eval(row[-1])[0]
            sc_c = ScrapePage(country_page_url)
            sc_c.scrape_table({"class":"table table-striped table-bordered table-hover table-condensed table-list"}, saveas_csv='F:/work_learning/Chart Animation/data/{}-co2.csv'.format(country.lower().replace(' ','_')))
        except IndexError:
            # log
            print('Error for: ' + row)
        except:
            # log
            print('Error for: ' + row)