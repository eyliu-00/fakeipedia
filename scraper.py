import pandas as pd
import numpy as np
import urllib
import sys
from tqdm import tqdm

from bs4 import BeautifulSoup

def main():
	file1 = open("fikipedia.txt","w")
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	objects = pd.read_csv("Daily Objects.csv")
	for i in tqdm(range(len(objects['items']))):
		item = objects['items'][i]
		# print(item)
		item = item.replace(" ", "_").capitalize()
		url = "https://en.wikipedia.org/wiki/" + item
		# print(url)
		html = urllib.urlopen(url).read()
		soup = BeautifulSoup(html)
		try:
			alltext = soup.find_all("div", class_="mw-parser-output")[0]
			try: 
				tag2 = alltext.find_all("p", recursive = False)[1]
				file1.write(tag2.text + "@@@\n")

			except IndexError:
				continue
		except:
			continue


	file1.close()


	
if __name__ == '__main__':
	main()