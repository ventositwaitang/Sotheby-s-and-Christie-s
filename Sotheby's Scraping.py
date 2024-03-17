import requests
import csv
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import os
import datetime as dt


auction = "Sotheby's"


names = open('Artist_name.txt').read().splitlines()
for name in names:


    artist_name = ' '.join(name.split()).lower()


    now = dt.datetime.now().strftime("%Y-%m-%d_%H.%M")
    try:
      f_ = open(f"Data Lake/{artist_name}/'{artist_name}'_{now}.csv", 'a+', newline='')
    except:
      os.makedirs(f"Data Lake/{artist_name}")
      f_ = open(f"Data Lake/{artist_name}/'{artist_name}'_{now}.csv", 'a+', newline='')
    writer = csv.DictWriter(f_, fieldnames=['', 'Artist name', 'Title of Artwork', 'Artwork type', 'Auction', 'Location', 'Closed date', 'Currency', 'low Estimate', 'high Estimate', 'Price realised', 'Details', 'Website link'])
    writer.writeheader()


    def filNone(self):
        try: return self
        except: return ['']

    def page(num=1):
        global auction, artist_name

        if auction=="Sotheby's":

            json_data = {"requests": [{"indexName": "bsp_dotcom_prod_en","params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&hitsPerPage=51&filters=type%3A%22Bid%22%20OR%20type%3A%22Buy%20Now%22%20OR%20type%3A%22Lot%22%20OR%20type%3A%22Private%20Sale%22%20OR%20type%3A%22Retail%22&query={artist_name}&maxValuesPerFacet=9999&page={num}&facets=%5B%22type%22%2C%22endDate%22%2C%22lowEstimate%22%2C%22highEstimate%22%2C%22artists%22%5D&tagFilters=&facetFilters=%5B%5B%22type%3ALot%22%5D%5D"},{"indexName": "bsp_dotcom_prod_en","params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=false&hitsPerPage=1&filters=type%3A%22Bid%22%20OR%20type%3A%22Buy%20Now%22%20OR%20type%3A%22Lot%22%20OR%20type%3A%22Private%20Sale%22%20OR%20type%3A%22Retail%22&query={artist_name}&maxValuesPerFacet=9999&page={num}&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&facets=type"}]}
            page = requests.post("https://o28sy4q7wu-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia for JavaScript (4.2.0); Browser (lite); react (16.13.1); react-instantsearch (6.7.0); JS Helper (3.2.2)&x-algolia-api-key=e732e65c70ebf8b51d4e2f922b536496&x-algolia-application-id=O28SY4Q7WU",json=json_data)
            return page.json()['results'][0]

        elif auction=="Christie's":

            page = requests.get(f"https://www.christies.com/api/discoverywebsite/search/lot-infos?keyword={artist_name}&page={num}&is_past_lots=true&language=en")
            return page.json()


    count = 1
    last_page_num = page(1)['nbPages']
    for num in range(1,last_page_num):
        for item in page(num)['hits']:


            if item['artistName'] and item['artistName'].lower().strip()==artist_name:
                try: writer.writerow({'':count,
                                    'Artist name': item["artists"][0].upper(),
                                    'Title of Artwork': item["title"],
                                    'Artwork type': item["departments"][0],
                                    'Auction': auction,
                                    'Location': filNone(item["locations"])[0],
                                    'Closed date': filNone(item["auctionDetails"]).split('|')[0],
                                    'Currency': item["estimateCurrency"],
                                    'low Estimate': item["lowEstimate"],
                                    'high Estimate': item["highEstimate"],
                                    'Price realised': item["salePrice"],
                                    'Details': filNone(item['fullText']),
                                    'Website link': item["url"]})


                    print('added ', count, ' item ')
                    count += 1


                except Exception as e: print(e)


        print('Page ',num,' done.')
    f_.close()




