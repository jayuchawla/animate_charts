import os
import csv
from utility.scrape_utility import ScrapePage
from utility.data_utility import csv_merger

# put in config
BASE_DATA_DIR = 'F:/work_learning/Chart Animation/data'
PARENT_CSV = BASE_DATA_DIR + '/country-co2.csv'

sc = ScrapePage("https://www.worldometers.info/co2-emissions/co2-emissions-by-country/")
sc.scrape_table({"id":"example2"}, saveas_csv=PARENT_CSV, extract_links=True)

BASE_URL = 'https://www.worldometers.info'

# ------ extract and dump country wise data to csvs ------ #
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


# ------ merge scraped csvs ------ #
MERGED_CSV = BASE_DATA_DIR + '/' + 'merged.csv'

CSV_FILE_PATHS = None
CSV_FILE_NAMES = None
for root, dir, files in os.walk(BASE_DATA_DIR):
    # put filenames as complete path
    CSV_FILE_PATHS = [root + '/' + file for file in files]
    CSV_FILE_NAMES = files

# removing PARENT_CSV -> not required for merging
CSV_FILE_PATHS.remove(PARENT_CSV)
CSV_FILE_NAMES.remove(os.path.basename(PARENT_CSV))
# removing MERGED_CSV from list if it exists in directory -> not required for merging
CSV_FILE_PATHS.remove(MERGED_CSV) if MERGED_CSV in CSV_FILE_PATHS else None 
CSV_FILE_NAMES.remove(os.path.basename(MERGED_CSV)) if MERGED_CSV in CSV_FILE_PATHS else None

# get country name from file name
prefixes = [country.split('-co2')[0].replace('_',' ').title() for country in CSV_FILE_NAMES]
csv_merger('Year', 'Fossil CO2Emissions(tons)', prefixes, MERGED_CSV, *tuple(CSV_FILE_PATHS), cached=True)