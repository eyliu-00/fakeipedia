import pandas as pd
import numpy as np
import requests
import urllib.request
import sys
from tqdm import tqdm

from bs4 import BeautifulSoup

def main():
    f = open("city_blurbs.txt","w")
    objects = pd.read_csv("cal_cities.csv")
    for i in tqdm(range(len(objects['Name']))):
        item = objects['Name'][i]
        item = item.replace(" ", "_").capitalize()
        url = "https://en.wikipedia.org/wiki/" + item + ",_California"
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
