from bs4 import BeautifulSoup
import urllib
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import urlretrieve
from os import makedirs
import os.path, time, re
import codecs
import html2text

test_files = {}

def enum_links(html, base):
   soup = BeautifulSoup(html, "html.parser")
   links = soup.select("link[rel='stylesheet']")
   links += soup.select("a[href]")
   result = []

   for a in links:
      href = a.attrs['href']
      url = urljoin(base, href)
      result.append(url)
   return result

def download_file(url):
   o = urlparse(url)
   savepath = "./" + o.netloc + o.path
   if re.search(r"/$", savepath):
      savepath += "index.html"
   savedir = os.path.dirname(savepath)
   #print(savepath)
   if os.path.exists(savepath): return savepath

   if not os.path.exists(savedir):
      print("mkdir=", savedir)
      makedirs(savedir)

   try:
      print("download=", url)
      urlretrieve(url, savepath)
      html2text.convert(url)
      time.sleep(1)
      return savepath
   except:
      print("ダウンロード失敗:", url)
      return None

def analize_html(url, root_url):
   savepath = download_file(url)

   if savepath is None: return
   if savepath in test_files: return
   test_files[savepath] = True
   print("analize_html=", url)

   html = codecs.open(savepath, "r", 'utf-8', 'ignore').read()
   links = enum_links(html, url)
   print(links)
   for link_url in links:
      if link_url.find(root_url) != 0:
         if not re.search(r".css$", link_url): continue

      if re.search(r".(html|htm)$", link_url):
         analize_html(link_url, root_url)
         continue

      download_file(link_url)

if __name__ == "__main__":
   url = "http://growhack.velvet.jp/danshari/"
   analize_html(url, url)