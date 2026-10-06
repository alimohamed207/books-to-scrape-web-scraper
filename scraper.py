import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/catalogue/"
TOTAL_PAGES = 50

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}


def get_soup(url):
    """Send a request and return a BeautifulSoup object."""
    page = requests.get(url, timeout=20)
    page.raise_for_status()
    return BeautifulSoup(page.content, "html.parser")


def get_category(book):
    """Open a book detail page and extract its category."""
    book_link = book.find("h3").find("a").get("href")
    book_url = urljoin(BASE_URL, book_link)

    book_soup = get_soup(book_url)

    breadcrumb = book_soup.find("ul", class_="breadcrumb")
    category = breadcrumb.find_all("li")[2].get_text(strip=True)

    return category


def get_book_data(book):
    """Extract the required fields from one book card."""
    book_name = book.find("a", title=True).get("title")

    book_rating = book.find("p", class_="star-rating")
    rating = RATING_MAP[book_rating["class"][1]]

    book_info = book.find("div", class_="product_price")

    book_price = book_info.find(
        "p", class_="price_color"
    ).get_text(strip=True)

    book_price = float(book_price.replace("£", ""))

    availability = book_info.find(
        "p", class_="instock availability"
    ).get_text(strip=True)

    category = get_category(book)

    return {
        "Book Name": book_name,
        "Price": book_price,
        "Rating": rating,
        "Availability": availability,
        "Category": category,
    }


def get_books_from_page(page_number):
    """Scrape all book cards from one catalogue page."""
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    soup = get_soup(url)
    return soup.find_all("article", class_="product_pod")


def scrape_books(total_pages=TOTAL_PAGES):
    """Scrape all books across the requested number of pages."""
    data = []

    for page_number in range(1, total_pages + 1):
        print(f"Scraping page {page_number}/{total_pages}...")

        books = get_books_from_page(page_number)

        for book in books:
            data.append(get_book_data(book))

    return pd.DataFrame(data)


if __name__ == "__main__":
    books_df = scrape_books()
    books_df.to_excel("data/books.xlsx", index=False)

    print(f"\nDone! Scraped {len(books_df)} books.")
    print("Saved : data/books.xlsx")
