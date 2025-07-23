""" script to get the products table and turn it in a pandas DataFrame """

# products	ID product, name, price, category, summary, review

# import modules

from bs4 import BeautifulSoup
import requests
import pandas as pd


url_list = [
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    "https://books.toscrape.com/catalogue/soumission_998/index.html",
    "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
    "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html",
    "https://books.toscrape.com/catalogue/the-requiem-red_995/index.html",
    "https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html",
    "https://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html",
    "https://books.toscrape.com/catalogue/the-boys-in-the-boat-nine-americans-and-their-epic-quest-for-gold-at-the-1936-berlin-olympics_992/index.html",
    "https://books.toscrape.com/catalogue/the-black-maria_991/index.html",
    "https://books.toscrape.com/catalogue/starving-hearts-triangular-trade-trilogy-1_990/index.html",
    "https://books.toscrape.com/catalogue/shakespeares-sonnets_989/index.html",
    "https://books.toscrape.com/catalogue/set-me-free_988/index.html",
    "https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html",
    "https://books.toscrape.com/catalogue/rip-it-up-and-start-again_986/index.html"
    ]

book_id_list = []
name_list = []
price_list = []
genre_list = []
summary_list = []
rating_list = []


for x in url_list:
    
    url = x
    page = requests.get(url)

    if page.status_code != 200:
        continue

    soup = BeautifulSoup(page.text, "html.parser")

    # extracting the BOOK ID

    table = soup.find("table", class_='table table-striped')
    tr_upc = table.find_all("tr")
    upc = tr_upc[0].find("td").text

    book_id_list.append(upc)

    # extracting the name

    h1 = soup.find("h1")
    title = h1.text

    name_list.append(title)

    # extracting the price

    table = soup.find("table", class_="table table-striped")
    tr_price = table.find_all("tr")
    price = tr_price[3].find("td").text.replace("Â£","")

    price_list.append(price)

    # extracting the genre

    ul_genre = soup.find("ul", class_= "breadcrumb")
    li_genre = soup.find_all("li")
    genre = li_genre[2].find("a").text

    genre_list.append(genre)

    # extracting the summary

    title_desc = soup.find("div", class_="sub-header")
    description = title_desc.find_next_sibling("p").text

    summary_list.append(description)

    # extracting the rating

    div_rating = soup.find("div", class_="col-sm-6 product_main")
    p_rating = div_rating.find_all("p")
    stars = p_rating[2].get("class")[1]

    rating_list.append(stars)


products = pd.DataFrame({
    "book ID":book_id_list,
    "name":name_list,
    "price": price_list,
    "category": genre_list,
    "summary": summary_list,
    "rating": rating_list
})

products.to_csv("Desktop/product_table.csv", index=False)

