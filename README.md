# Books to Scrape — Web Scraping Project

A practical Python web scraping project that collects structured book data from **Books to Scrape** using `Requests`, `BeautifulSoup`, and `Pandas`.

The project demonstrates a complete beginner-friendly scraping workflow:

**Website → HTTP Request → HTML → BeautifulSoup → Data Extraction → Pandas DataFrame → Excel**

## Project Overview

This scraper is designed to collect book information from the Books to Scrape catalogue across its 50 catalogue pages.

For each book, the scraper extracts:

- Book Name
- Price
- Rating
- Availability
- Category

The category is collected from the individual book detail page because it is not directly available inside the catalogue card.

## Tech Stack

- Python
- Requests
- BeautifulSoup4
- Pandas
- OpenPyXL
- HTML / CSS selectors
- Web Scraping

## Project Structure

```text
books-to-scrape-web-scraper/
│
├── scraper.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── books_scraped.xlsx
```

## How It Works

### 1. Request the catalogue page

`Requests` downloads the HTML returned by the website.

```python
page = requests.get(url, timeout=20)
```

### 2. Parse the HTML

`BeautifulSoup` turns the raw HTML into a searchable structure.

```python
soup = BeautifulSoup(page.content, "html.parser")
```

### 3. Find all book cards

Each book is represented by:

```html
<article class="product_pod">
```

The scraper uses:

```python
books = soup.find_all("article", class_="product_pod")
```

### 4. Extract the book name

The full title is stored in the `title` attribute of the link:

```python
book_name = book.find("a", title=True).get("title")
```

### 5. Extract the rating

The website stores the rating inside the CSS class:

```html
<p class="star-rating Three">
```

The scraper maps the class name to a numeric rating:

```python
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}
```

### 6. Extract and clean the price

The raw value looks like:

```text
£51.77
```

It is converted to a numeric value:

```python
book_price = float(book_price.replace("£", ""))
```

This makes the column easier to analyze later with Pandas.

### 7. Extract availability

The scraper reads the availability text from:

```html
<p class="instock availability">
```

### 8. Extract category

The catalogue page does not contain the category directly inside the book card.

So the scraper:

1. Gets the book's relative URL.
2. Builds the full URL with `urljoin`.
3. Requests the book detail page.
4. Reads the category from the breadcrumb.

```python
book_link = book.find("h3").find("a").get("href")
book_url = urljoin(BASE_URL, book_link)
```

Then:

```python
breadcrumb = book_soup.find("ul", class_="breadcrumb")
category = breadcrumb.find_all("li")[2].get_text(strip=True)
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/books-to-scrape-web-scraper.git
cd books-to-scrape-web-scraper
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Scraper

Run:

```bash
python scraper.py
```

The script will scrape all 50 catalogue pages and save the result to:

```text
data/books_scraped.xlsx
```

The website contains 1,000 books across 50 pages, with up to 20 books per catalogue page.

## Output

The generated Excel file contains these columns:

| Column | Description |
|---|---|
| Book Name | Full title of the book |
| Price | Book price as a numeric value |
| Rating | Rating from 1 to 5 |
| Availability | Current stock status |
| Category | Book category |

## Example Output

| Book Name | Price | Rating | Availability | Category |
|---|---:|---:|---|---|
| A Light in the Attic | 51.77 | 3 | In stock | Poetry |
| Tipping the Velvet | 53.74 | 1 | In stock | Poetry |
| Soumission | 50.10 | 1 | In stock | Poetry |

## Important Scraping Lesson

One of the main lessons from this project is that the information you want is not always in the element you first expect.

For example, the book title may appear visually as:

```text
A Light in the ...
```

while the complete title is stored in:

```html
title="A Light in the Attic"
```

Similarly, the rating is not represented by the number of `<i>` elements. It is encoded in the CSS class:

```html
class="star-rating Three"
```

The category is located on another page entirely.

This is why a reliable scraping workflow starts with:

**Inspect HTML → Identify where the data actually lives → Choose the selector → Extract → Clean → Store**

## Notes

- This project is built for learning and portfolio demonstration.
- Books to Scrape is a sandbox website specifically intended for web scraping practice.
- Prices and ratings on the website are demonstration data and should not be treated as real commercial information.
- The scraper makes additional HTTP requests to individual book pages to collect categories, so scraping the full catalogue requires substantially more requests than scraping catalogue pages alone.

## Future Improvements

Possible next steps:

- Add request headers and retry handling.
- Add a small delay between requests.
- Store the raw HTML or scraped data as CSV/JSON.
- Add logging instead of `print`.
- Add error handling for missing HTML elements.
- Add a command-line argument for the number of pages.
- Add data validation before exporting.
- Load the cleaned data into PostgreSQL.
- Build an EDA dashboard using the resulting dataset.

## Skills Demonstrated

This project demonstrates practical experience with:

- Web scraping
- HTML inspection
- BeautifulSoup
- Requests
- CSS selectors
- Attribute extraction
- Pagination
- Relative vs. absolute URLs
- Data cleaning
- Pandas DataFrames
- Excel data export
- Basic data pipeline design

## Source

The project uses the public Books to Scrape sandbox:

https://books.toscrape.com/
