import pandas as pd
import numpy as np
import requests
import urllib.request
import sys
from tqdm import tqdm

from bs4 import BeautifulSoup

def main():
    f = open("fikipedia1.txt","w")
    objects = pd.read_csv("Daily Objects.csv")
    for i in tqdm(range(len(objects['items']))):
        item = objects['items'][i]
        item = item.replace(" ", "_").capitalize()
        url = "https://en.wikipedia.org/wiki/" + item
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            alltext = soup.find_all("div", class_="mw-parser-output")[0]
            for tag in alltext.find_all("p", recursive = False):
                if not tag.has_attr("class"):
                    f.write(tag.text + "@@@\n")
                    break
        except:
            continue
    f.close()

if __name__ == '__main__':
    main()
