import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient("localhost",27017)

db = client.examples
collection = db.myWebsites
website={}
website["Link"] = "www.gamw"
website["Source Link"] = "www.gamw"
website["is Crawled"] = "www.gamw"
website["Last Crawl Dt"] = "www.gamw"
website["Response Status"] = "www.gamw"
website["Content Type"] = "www.gamw"
website["Content Length"] = "www.gamw"
website["File Path"] = "www.gamw"
website["Created at"] = "www.gamw"
collection.insert_one(website)

internal_urls = set()
external_urls = set()

res = requests.get('https://flinkhub.com/')

soup = BeautifulSoup(res.text)
# print(soup.prettify())
a_tags = soup.find_all('a')
for link in a_tags:
    print(link.get('href'))
# print(a_tags)
# print(collection)
for item in collection.find():
    print(item)