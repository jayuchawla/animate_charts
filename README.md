# animate_charts
This project scrapes CO-2 emission data and presents an animated visualization of the data over time.

## Data Scraping
-   #### Data: https://www.worldometers.info/co2-emissions/co2-emissions-by-country/
-   Scraping tables:
    -   Parent table (country wise recent data) and writing to csv file
    -   Extract links from each cell and append to end of csv row
    -   Enabled caching by introducing a class parameter (cached -> enabled by default)

## Data Merging
-   Required Data format:
    -   Each row is a year
    -   Each column is a country
    -   Each cell is yearly value for that specific country