import requests
from bs4 import BeautifulSoup, element
from requests.api import request
import pandas as pd
import numpy as np
import time


class Scraper:
    """This class scrapes https://domoplius.lt/ website for apartments that are for sale in Klaipeda.

    The Scraper loops through these steps for every page number until it reaches the page_limit, which
     can be specified when creating a new object based on Scraper class:
    1. Gets BeautifulSoup from a page if it contains apartment listings.
    2. Gets attributes each apartment listing on that page.
    3. Appends scraped data to a dictionary which is then converted to a dataframe.
    """

    def __init__(
        self,
        headers: dict = {
            "User_Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15"
        },
        page_limit: float = 1,
    ):
        """Initialization method.

        :param headers: a dictionary of HTTP headers to send to the specified url, defaults to {"User_Agent": UserAgent().random}
        :type headers: dict, optional
        :param page_limit: tells how many pages to scrape(one page is 30 listings), defaults to 1
        :type page_limit: float, optional
        """
        self.headers = headers
        self.page_limit = page_limit

    def get_page_soup(self, URL: str) -> BeautifulSoup:
        """Gets BeautifulSoup from a passed in URL or a page.

        :param URL: a link to the domoplius.lt page which is scraped
        :type URL: str
        :return: BeautifulSoup for one page
        :rtype: BeautifulSoup
        """

        page = requests.get(URL, headers=self.headers)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    def get_listings_from_page_soup(self, soup: BeautifulSoup) -> element.ResultSet:
        """Apartment listing data is stored in "li" elements which are stored in a
        "ul" element (a.k.a unordered list).This function returns a whole unordered
        list for each page scraped. Each unordered list stores around 30 "li" elements.
        Lastly, every "li" element contains data for one apartment listing.

        :param soup: BeautifulSoup for one page
        :type soup: BeautifulSoup
        :return: unordered list of listings
        :rtype: element.ResultSet
        """
        unordered_list = soup.find("ul", class_="auto-list")
        listings = unordered_list.find_all("li", class_="not-viewed")
        return listings

    def get_title(self, listing: element.ResultSet) -> str:
        """Gets a title of a listing from a "li" element passed in
        by finding the first "h2" element.

        :param listing: "li" element for one apartment
        :type listing: element.ResultSet
        :return: title of an apartment's listing
        :rtype: str
        """
        title = listing.find("h2", class_="title-list").text
        return title

    def get_price(self, listing: element.ResultSet) -> str:
        """Gets a price of an apartment from a "li" element passed in
        by finding the first "div" element.

        :param listing: "li" element for one apartment
        :type listing: element.ResultSet
        :return: price of an apartment
        :rtype: str
        """
        price = listing.find("div", class_="price").text
        return price

    def get_attribute(self, listing: element.ResultSet, attribute_name: str) -> str:
        """ "Gets table row value by searching for corresponding keys which are
        passsed in as an attribute_name.

        :param listing: "li" element for one apartment
        :type listing: element.ResultSet
        :param attribute_name: a keyword to search for in a li element
        :type attribute_name: str
        :return: value that corresponds to a keyword
        :rtype: str
        """

        sq_meters = listing.find("span", title=attribute_name).text
        return sq_meters

    def get_listing_link(self, listing: element.ResultSet) -> str:
        """Gets a link of a listing from a "li" element passed in
        by finding the first "a" element.

        :param listing: "li" element for one apartment
        :type listing: element.ResultSet
        :return: a link to a listing
        :rtype: str
        """
        listing_link = listing.find("a")["href"]
        return listing_link

    def scrape_website(self) -> pd.DataFrame:
        """This is the main scraping method which returns scraped data in the form of a dictionary of lists.
        It first initialized a list which is going to store a dictionary of scraped data. Then, it loops
        through pages of domoplius.lt until page_limit is reached. For each page that is scraped
        get_page_soup method gets BeautifulSoup, finds an unordered list that stores apartment listings,
        and then calls methods on each apartment listing to get attributes of an apartment. Dictionary with
        scraped data is converted to a pd.DataFrame.

        :return: creates a pd.DataFrame with all the scraped data
        :rtype: pd.DataFrame
        """

        pages = np.arange(1, self.page_limit + 1, 1)

        self.list = []

        for page in pages:

            time.sleep(1)

            URL = f"https://domoplius.lt/skelbimai/butai?action_type=1&address_1=112&category_search=1&page_nr={page}"

            soup = self.get_page_soup(URL)
            listings = self.get_listings_from_page_soup(soup)

            if len(listings) >= 1 and soup != None:

                for listing in listings:

                    self.list.append(
                        {
                            "title": self.get_title(listing),
                            "price": self.get_price(listing),
                            "room_count": self.get_attribute(
                                listing, "Kambarių skaičius"
                            ),
                            "sq_meters": self.get_attribute(
                                listing, "Buto plotas (kv. m)"
                            ),
                            "apartment_floor": self.get_attribute(listing, "Aukštas"),
                            "year_built": self.get_attribute(listing, "Statybos metai"),
                            "link": self.get_listing_link(listing),
                        }
                    )
            else:
                break

        return pd.DataFrame(self.list)

    def to_csv(self) -> None:
        """Calls scrape_website method and converts the returned dataframe
        to a .csv file in the working directory.

        :return: .csv file with scraped data
        :rtype: None
        """
        dataframe = self.scrape_website()
        column_names = dataframe.columns
        return dataframe.to_csv(
            "scraped_data.csv", sep=",", header=column_names, index=None
        )