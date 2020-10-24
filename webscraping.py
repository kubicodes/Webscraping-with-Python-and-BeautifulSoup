from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

wrapped_url = "https://www.newegg.com/p/pl?d=GTX&N=-1&IsNodeId=1&bop=And&Page=1&PageSize=36&order=BESTMATCH"
ssl._create_default_https_context = ssl._create_unverified_context

response_url = urlopen(wrapped_url)
html_page_of_url = response_url.read()
parsed_html = BeautifulSoup(html_page_of_url, "html.parser")
response_url.close()

all_products = parsed_html.findAll("div", {"class": "item-container"})

#header definition for CSV file
header_names = "brand,product_name,rating \n"

f = open("web_scraper.csv", "w")
f.write(header_names)

for product in all_products:
    #select the a tag where all information is stored we need
    link_tags = product.div.select("a")

    #collect row information for CSV
    brand = link_tags[0].img["title"].title()
    product_name = link_tags[2].text
    rating = link_tags[1]["title"].replace("Rating", "")

    #write collected information to CSV file
    f.write(brand + ", " + product_name.replace(",", "|") + ", " + rating + "\n")

#close the file
f.close()
