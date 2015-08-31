# Jeff Stern, dedicated to Cait Holman
# Scrapes http://apod.nasa.gov/apod/ and downloads all photos

from bs4 import BeautifulSoup

import urllib2
import os
import csv

def parse_html(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	content = response.read()
	return BeautifulSoup(content, "html.parser")

def get_url_list(url):
	soup = parse_html(url)
	urlList = []
	for link in soup.find_all('a'):
		href = link.get('href')
		if "ap" in href[:2]:
			urlList.append(href)
	return urlList

def download_photo(img_url, filename):
	# http://stackoverflow.com/questions/3042757/downloading-a-picture-via-urllib-and-python
	try:
	    image_on_web = urllib2.urlopen(img_url)
	    if image_on_web.headers.maintype == 'image':
	        buf = image_on_web.read()
	        path = os.getcwd() + "/"
	        file_path = "%s%s" % (path, filename)
	        downloaded_image = file(file_path, "wb")
	        downloaded_image.write(buf)
	        downloaded_image.close()
	        image_on_web.close()
	    else:
			return False    
	except:
		print("URL for "+ img_url + " not found")
		return False
	return True

# Gets full-res source if available
def get_image_src(img):
	if img.parent.name == 'a':
		return img.parent.get('href')
	else:
		return img.get('src')

# Gets the first image on the page and downloads it
def download_photos_from_html(urlList, url_prepend=""):
	for link in urlList:
		url = url_prepend + link
		soup = parse_html(url)
		src = get_image_src(soup.find('img'))
		savename = href[src.rfind("/")+1:]
		download_photo("http://apod.nasa.gov/apod/" + src, savename)

def get_metadata_from_html(urlList, url_prepend=""):
	allMetaData = []
	for link in urlList:
		link = url_prepend + link
		soup = parse_html(link)
		date = ""
		name = ""
		savename = ""
		try:
			title = soup.find('title').string
			date = title[7:title.find("-")-1]
			name = title[title.find("-")+2:].replace("\n","").strip()
			src = get_image_src(soup.find('img'))
			savename = src[src.rfind("/")+1:]
		except:
			print("couldn't get all metadata for " + link)
		allMetaData.append([date, name, savename, link])
		# print(linkMetaData)
	return allMetaData

def create_csv_from_list_of_lists(array, filename):
	f = open(filename, 'wb')
	writer = csv.writer(f)
	for r in array:
		writer.writerow([unicode(s).encode("utf-8") for s in r])


urlList = get_url_list("http://apod.nasa.gov/apod/archivepix.html")
directory = "http://apod.nasa.gov/apod/"

download_photos_from_html(urlList, directory)
allMetaData = get_metadata_from_html(urlList, "http://apod.nasa.gov/apod/")
create_csv_from_list_of_lists(allMetaData, "_astronomyphotos_metadata.csv")