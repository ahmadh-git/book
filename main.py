# Step 1: Import the package
import csv
import urllib.request
from bs4 import BeautifulSoup

# Step 2: Assign the URL to variable
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
 
# Step 3: First open, then read the the HTML
text = urllib.request.urlopen(url).read().decode("utf-8")
soup = BeautifulSoup(text, "html.parser")
paragraphs = soup.find_all('p')

#Step 4: Print the HTML code
table_elements = soup.find("table").find_all("tr")

base_path = "https://books.toscrape.com/"
upc = table_elements[0].find("td").get_text()
price_inc_tax = table_elements[3].find("td").get_text()
price_exc_tax = table_elements[2].find("td").get_text()
availability = table_elements[5].find("td").get_text()
imageurl = base_path + soup.img["src"][6:len(soup.img["src"])]

book_title = soup.find("ul").find_all("li")[3].get_text()
book_category = soup.find("ul").find_all("li")[2].get_text()
review = paragraphs[2]["class"][1]
product_desc = paragraphs[3]

print(book_title, book_category, imageurl, review, product_desc)

#Create a Dictionary

dictionary = {
        "product_page_url": imageurl, 
        "universal_product_code (upc)": upc,
        "book_title": book_title,
        "price_including_tax": price_inc_tax,
        "price_excluding_tax": price_exc_tax,
        "quantity_available": availability,
        "product_description": product_desc,
        "category": book_category,
        "review_rating": review,
        "image_url": imageurl
    }

# use dictionary
temp = [dictionary]
fields = temp[0].keys()
filename = "bookScrape_" + book_title.replace(" ", "_") + ".csv"
with open(filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(temp)

#Define Categories
categories = soup.find_all("ul")
print(categories)