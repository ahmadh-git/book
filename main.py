import csv
import math
import os
import urllib.request
import pathlib
import re

from bs4 import BeautifulSoup
from funcs import single_book, clean_tags, get_html_string

# Function to sanitize filenames by replacing invalid characters
def sanitize_filename(filename):
    # Replace any characters that are not valid in file names with an underscore
    return re.sub(r'[<>:"/\\|?*#]', '_', filename)

def main():
    html_string = get_html_string("https://books.toscrape.com/catalogue/category/books_1/index.html")
    cat_path = "https://books.toscrape.com/catalogue/category/books/"
    book_path = "https://books.toscrape.com/catalogue"
    soup = BeautifulSoup(html_string, "html.parser")
    categories = soup.find("div", {"class": "side_categories"}).find_all("a")
    category_strings = []
    
    for x in categories:
        category_strings.append(clean_tags(str(x).strip()).strip())

    category_strings = category_strings[1:len(category_strings)]  # Skipping the first 'Books' category
    catInt = 2
    category_title = ""

    for y in category_strings:
        url = cat_path + y.lower().replace(" ", "-") + "_" + str(catInt) + "/index.html"
        html_string = get_html_string(url)
        soup = BeautifulSoup(html_string, "html.parser")
        result_num = clean_tags(str(soup.find_all("strong")[1]))
        product_page_tags = soup.find_all("div", {"class": "image_container"})
        page_paths = []
        category_title = clean_tags(str(soup.find("h1")))

        for x in product_page_tags:
            curr = str(x.find("a").get("href"))
            page_paths.append(curr[8:len(curr)])

        # Handling multiple pages of products
        if int(result_num) > 20:
            number_of_pages = math.ceil(int(result_num) / 20)
            current_page = 2
            while current_page <= number_of_pages:
                url2 = cat_path + y.lower().replace(" ", "-") + "_" + str(catInt) + "/page-" + str(current_page) + ".html"
                html_string2 = get_html_string(url2)
                soup2 = BeautifulSoup(html_string2, "html.parser")
                product_page_tags2 = soup2.find_all("div", {"class": "image_container"})
                for z in product_page_tags2:
                    curr = str(z.find("a").get("href"))
                    page_paths.append(curr[8:len(curr)])
                current_page += 1
        
        cat_data = []
        for b in page_paths:
            cat_data.append(single_book(False, book_path + b))

        path = str(pathlib.Path().resolve())
        
        # Create directories if they don't exist
        if not os.path.exists(path + "/data"):
            os.mkdir(path + "/data")
        if not os.path.exists(path + "/data/img"):
            os.mkdir(path + "/data/img")

        # Save images with sanitized filenames
        for c in cat_data:
            sanitized_category_title = sanitize_filename(category_title.replace(" ", "_"))
            sanitized_book_title = sanitize_filename(c["book_title"].replace(" ", "_"))
            image_path = path + f"/data/img/{sanitized_category_title}_{sanitized_book_title}_img.png"
            
            # Download image and handle invalid characters in URLs
            urllib.request.urlretrieve(c["image_url"], image_path)

        # Save data to CSV
        fields = cat_data[0].keys()
        filename = "categoryScrape_" + sanitize_filename(category_title.replace(" ", "_")) + ".csv"
        with open(path + "/data/" + filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(cat_data)

        catInt += 1

main()
