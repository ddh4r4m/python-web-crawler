import requests
from requests.compat import urlparse
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient("localhost",27017)

db = client.examples
collection = db.myWebsitesAA

def database_data(url, src_url):
    website={}
    r = requests.get(url)
    if(collection.count_documents()>10):
        print("Limit Exceed, Exiting ......")
        return
    else:
        print(collection.count())
    if r.status_code!=200:
        website["Link"] = url
        website["Source Link"] = src_url
        website["is Crawled"] = True
        website["Last Crawl Dt"] = datetime.datetime.utcnow()
        website["Response Status"] = r.status_code
        website["Content Type"] = r.headers['Content-Type']
        website["Content Length"] = r.headers['content-length']
        website["File Path"] = ""
        website["Created at"] = ""
        collection.insert_one(website)
    else:
        website["Link"] = url
        website["Source Link"] = src_url
        website["is Crawled"] = False
        website["Last Crawl Dt"] = None
        website["Response Status"] = r.status_code
        website["Content Type"] = r.headers['Content-Type']
        website["Content Length"] = 0
        website["File Path"] = ""
        website["Created at"] = ""
        collection.insert_one(website)
    # get_all_links(url)


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

def insert_into_db(links,src_url):
    for link in links:
        print(link)
        if collection.find_one({"Link":link}) is None:
            database_data(link,src_url)
        else:
            if collection.find_one({"Link":link})['is Crawled'] is False:
                get_all_links(link)



def get_all_links(url):
    if url.startswith('http'):
        base_url = get_base_url(url)
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
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
    insert_into_db(external_urls,url)
    print("NOW")
    insert_into_db(internal_urls,url)




my_url = input("Please Enter Your Address : ")
get_all_links(my_url)


# print(a_tags)
# # print(collection)
# for item in collection.find():
#     print(item)