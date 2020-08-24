import requests
from requests.compat import urlparse
from bs4 import BeautifulSoup
from pymongo import MongoClient

# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient("localhost",27017)

db = client.examples
collection = db.myWebsites
website={}
website["Link"] = ""
website["Source Link"] = ""
website["is Crawled"] = False
website["Last Crawl Dt"] = "www.gamw"
website["Response Status"] = "r = requests.get('https://httpbin.org/get')  r.status_code"
website["Content Type"] = "r.headers['Content-Type']"
website["Content Length"] = 0
website["File Path"] = "www.gamw"
website["Created at"] = "www.gamw"
collection.insert_one(website)

internal_urls = set()
external_urls = set()

def is_valid(url):
    try:
        requests.get(url)
        return True
    except:
        return False

def get_base_url(url):
    return urlparse(url)[0]+"://"+urlparse(url)[1]


def get_all_links(url):
    if url.startswith('http'):
        base_url = get_base_url(url)
    res = requests.get(url).content
    soup = BeautifulSoup(res, "html.parser")
    # print(soup.prettify())
    a_tags = soup.find_all('a')

    for link in a_tags:
        href = link.get('href')
        # print(href)
        if href=="" or href is None:
            continue
        if href.startswith('/'):
            local_link = base_url + href
            internal_urls.add(local_link)
        elif not href.startswith('http'):
            pass
            # local_link = path + href
            # internal_urls.add(local_link)
        else:
            external_urls.add(href)
    for link in external_urls:
        print(link)
    print("NOW")
    for link in internal_urls:
        print(link)
    # print("NOW")
    # print(internal_urls)


my_url = input("Please Enter Your Address : ")
get_all_links(my_url)


# print(a_tags)
# # print(collection)
# for item in collection.find():
#     print(item)