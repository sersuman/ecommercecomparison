from bs4 import BeautifulSoup
import requests
import csv

# acquires html file from the website in source variable
source = requests.get('https://www.sastodeal.com/mens-fashion/accessories/watches.html').text



soup = BeautifulSoup(source, 'lxml')

# prettify does indentation to html file
# print(soup.prettify())

for article in soup.findAll("strong", {"class": "product name product-item-name"}):
    title = article.a.text
    print(title)
