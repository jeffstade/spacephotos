# spacephotos
Astronomy Photo of the Day Web Scraper

Requires BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)

Will download all of the full-res photos (>5GB of data, as of 8-31-15) from http://apod.nasa.gov/apod/archivepix.html and generate a CSV with metadata.

Relies on a couple of assumptions:
- Astronomy photo is always the first image on the page
- If there's an <a> tag surrounding the image, that's the link to the full-resolution image

Roughly 1 out of 7 of days do not have an image, but instead a video/SVG/Java Applet/etc. These will not download.
