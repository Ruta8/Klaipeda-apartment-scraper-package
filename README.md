# Klaipeda apartment scraping package

This project is a Python package that scrapes https://domoplius.lt/ website for apartments that are for sale in Klaipeda.
This website was chosen because it lists more apartments in Klaiped than other real estate websites. 
The package is intended to meet all expected Python package standards: clean code, tests, documentation.

The Scraper loops through these steps for every page number until it reaches the page_limit, which can be specified when creating a new object based on Scraper class:
1. Gets BeautifulSoup from a page if it contains apartment listings.
2. Gets attributes each apartment listing on that page.
3. Appends scraped data to a dictionary which is then converted to a dataframe.

## Install package through pip

`pip install git+https://github.com/Ruta8/Klaipeda-apartment-scraper-package.git`

## Import Scraper class
`from scraper.Scraper import Scraper`

## Use Scraper
One domoplius.lt page displays around 30 listings. Specify page_limit to scrape a certain number of pages. 
To create a new scraping object type:<br>

`scraper = Scraper(page_limit = 120)`<br>

To create a dataframe with scraped data type:<br>
`df = scraper.scrape_website()`<br>

To scrape the data straight into a .csv file type, and then check your working directory: <br>
`scraper.to_csv()`<br>

## License
Licensed under the [MIT License](./LICENSE).