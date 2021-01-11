﻿import requests
from bs4 import BeautifulSoup
from scrape_book import scrape_book
import argparse
import os
import csv


def scrape_category(url, name):
    r = requests.get(url)
    url = url.replace('index.html', '')             # replace l'index.html
    soup = BeautifulSoup(r.content, 'lxml')
    string_sup = '!/:,"*?'               # Creation d'une variable string pour supprimer les caractère spéciaux
    num = 0
    with open(os.path.join('C:/OpenClassroom/P2_Boulahrouf_Ryad/data', name + '.csv', ), 'w', newline="",
              encoding="utf-8") as f:
        fieldnames = ["product_page_url", "universal_product_code", "title", "price_including_tax",
                      "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                      "image_url"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        while True:
            all_book = soup.findAll('div', {'class': 'image_container'})  # recuperation de tout les book
            for book in all_book:
                end_book = book.find('a')['href'].replace('../', '')
                all_book = 'https://books.toscrape.com/catalogue/' + end_book
                data = scrape_book(all_book)
                print(data["image_url"])
                r = requests.get(data["image_url"])
                for char in string_sup:         # suppression des caractère spéciau
                    data['title'] = data['title'].replace(char, '')
                i = ""
                if data["image_url"] == "https://books.toscrape.com/media/cache/ac/1a/ac1a0546d9cdf6cd82ab7712a6c418df.jpg":
                    i = "(1)"
                with open(os.path.join('C:/OpenClassroom/P2_Boulahrouf_Ryad/img', data['title'] + i + '.png'), "wb") \
                        as file:
                    file.write(r.content)
                    file.close()
                    num += 1

                    writer.writerow({"product_page_url": data["product_page_url"],
                                     "universal_product_code": data["universal_product_code"], "title": data["title"],
                                     "price_including_tax": data["price_including_tax"],
                                     "price_excluding_tax": data["price_excluding_tax"],
                                     "number_available": data["number_available"],
                                     "product_description": data["product_description"],
                                     "category": data["category"],
                                     "review_rating": data["review_rating"],
                                     "image_url": "img/" + data["title"] + i + ".png"})

            if soup.find('li', {'class': 'next'}):      # Si le bouton next est là
                end_link = soup.find('li', {'class': 'next'}).find('a')['href']
                page_next = url + end_link
                r = requests.get(page_next)
                soup = BeautifulSoup(r.content, 'lxml')
            elif not soup.find('li', {'class': 'next'}):        # Si le bouton next est pas là fin du programme
                break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    parser.add_argument('--name')
    args = parser.parse_args()
    print(scrape_category(args.url, args.name))


if __name__ == '__main__':
    main()
