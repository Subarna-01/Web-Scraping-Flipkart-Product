# import essential modules.
from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook

# I have made an excel sheet named flipkart_product_data.xlsx to store the data.
work_book = load_workbook("flipkart_product_data.xlsx")
work_sheet = work_book.active

# I have used this url to scrap the data about mobiles.
# This url is valid for only page 1.To get more pages just change the value of page=1 to 2,3... or whatever you want in the url end.
URL = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"

# Use your own user agent here.This is my user agent.Just head to google chrome and type my user agent to get yours.
# The "User-Agent" will remain the same key just replace the value of this key with the string that you got.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
response = requests.get(URL, HEADERS)

html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

products = soup.find_all("div", class_="_13oc-S")

# Filtering functions.


def filter_price_string(string):
    cleaned_string = ""

    for i in range(len(string)):

        if string[i].isdigit():
            cleaned_string += string[i]

    return int(cleaned_string)


def filter_off_on_price_string(string):
    cleaned_string = ""
    for i in range(len(string)):

        if not string[i].isdigit():
            return int(cleaned_string)

        cleaned_string += string[i]


# I have defined three columns in flipkart_product_data.xlsx namely product_name,price and off to store the data as per requirements.
for product in products:
    product_name_ = product.find("div", class_="_4rR01T")
    product_price_ = product.find("div", class_="_30jeq3 _1_WHN1")
    product_off_ = product.find("div", class_="_3Ay6Sb")

    if product_off_ == None:
        work_sheet.append([product_name_.string, product_price_.string, 0])
    else:
        work_sheet.append(
            [
                product_name_.string,
                filter_price_string(product_price_.string),
                filter_off_on_price_string(product_off_.span.string),
            ]
        )

# I have saved the data in same excel file so the name of the excel sheet here remains the same.
# If you want to save the data in another excel sheet then replace the name of this sheet with your desired on.
work_book.save("flipkart_product_data.xlsx")
