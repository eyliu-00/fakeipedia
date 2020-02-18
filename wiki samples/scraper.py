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
        if i % 2 == 0:
            continue
        item = objects['items'][i]
        item = item.replace(" ", "_").capitalize()
        url = "https://en.wikipedia.org/wiki/" + item
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            alltext = soup.find_all("div", class_="mw-parser-output")[0]
            blurb = ""
            for tag in alltext.find_all("p", recursive = False):
                blurb += tag.text
                if len(blurb) > 1000:
                    break
                # if not tag.has_attr("class"):
                #     text_len = len(tag.text)
                #     len_blurbs += text_len
                #     # if (text_len < 400 and text_len > 200) or n_blurbs == 0:
                #     blurb += tag.text
                #     print(blurb)
                #     n_blurbs += 1
                #     if (len_blurbs > 1400):
                #         break
            # print(blurb)
            if len(blurb) > 0:
                f.write(blurb)

            f.write("@@@\n")
        except:
            continue
    f.close()

if __name__ == '__main__':
    main()
