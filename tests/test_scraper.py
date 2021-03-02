from bs4 import BeautifulSoup, element
from scraper.Scraper import Scraper

with open("tests/test_data/test_data.html") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

url = "https://domoplius.lt/skelbimai/butai?action_type=1&address_1=112&category_search=1&page_nr=2"

scraper = Scraper()
soup = scraper.get_page_soup(url)
listings = scraper.get_listings_from_page_soup(soup)
listing = listings[0]


def test_get_page_soup():

    assert isinstance(soup, BeautifulSoup)


def test_get_listings_from_page_soup():

    assert isinstance(listings, element.ResultSet)


def test_get_price():
   
    assert scraper.get_price(listing) == "\nKaina: 250 000 € (2 778 €/m²)\n\n"

def test_get_attribute_sq_meters():
    
    assert scraper.get_attribute(listing, "Buto plotas (kv. m)") == "90.00 m²"

def test_get_attribute_room_count():
    
    assert scraper.get_attribute(listing, "Kambarių skaičius") == "3 kamb."


def test_get_attribute_building_year():

    assert scraper.get_attribute(listing, "Statybos metai") == "2006 m."


def test_get_attribute_apartment_floor():

    assert scraper.get_attribute(listing, "Aukštas") == "7/9 a."


def test_get_listing_link():

    print(scraper.get_listing_link(listing))
    assert (
        scraper.get_listing_link(listing)
        == "https://domoplius.lt/skelbimai/parduodamas-3-kambariu-butas-klaipedoje-viteje-dariaus-ir-gireno-g-7212478.html"
    )