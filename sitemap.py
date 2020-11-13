from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests, time , datetime ,os

def ask_url():
  time.sleep(1)
  print('WRITE YOUR URL HERE')
  global url
  url = input()
  try:
    global response
    checking = url
    x = "www" in checking
    if x == True:  # HERE WE ARE CHECKING THAT USER URL CONTAINS WWW OR NOT
     url = "http://" + url +"/"
     response = requests.get(url) # HERE WE CHECKING THE URL EXIST ON INTERNET OR NOT
     start_crawling()
    else:
     print('Please valid url  Ex: www.abcd.xy')
     ask_url()
  except:
   print('Please enter valid url which exist on the internet Ex: www.abcd.xy')
   ask_url()

def start_crawling():
 print('Crawling for web pages')
 time.sleep(4)
 global checked_urls
 checked_urls = []
 checked_urls.append(url)
 crwaling_web_pages()


def crwaling_web_pages():
 global responses
 control = 0
 while control < 50001: # HERE WE FULL FILL THE CONDITION MAXIMUM NO. OF URL IN SITEMAP
  try:
   responses =requests.get(checked_urls[control])
   source_code =responses.text
   soup = BeautifulSoup(source_code,"html.parser")
   new_links = [w['href'] for w in soup.findAll('a',href=True)]
   counter = 0
   while counter < len(new_links):
    if "http" not in new_links[counter]:
     counter = counter + 1
     verify = new_links[counter][0]
     if verify == "/":
      new_links[counter] = url + new_links[counter]
      counter = counter + 1
     else:
      new_links[counter] = url + new_links[counter]
      counter = counter + 1
    else:
     counter = counter + 1
   else:
    counter2 = 0
    while counter2 < len(new_links):
     if "#" not in new_links[counter2] and "malito" not in new_links[counter2] and ".jpg" not in new_links[counter2] and new_links[counter2] not in checked_urls and url in new_links[counter2]:
      checked_urls.append(new_links[counter2])
      print(str(control)+"/"+str(len(checked_urls)))
      print('')
      print(str(control) + " web pages crawled and " + str(len(checked_urls)) + " web pages found ")
      print('')
      print(new_links[counter2])
      counter2 = counter2 + 1
     else:
      counter2 = counter2 + 1
    else:
     print(str(control)+"/"+str(len(checked_urls)))
     print('')
     print(str(control) + " web pages crawled and " + str(len(checked_urls)) + " web pages found ")
     print('')
     print(checked_urls[control])
     control = control + 1
  except:
   control = control + 1
 else:
  time.sleep(2)
  creating_sitemap()

def creating_sitemap():
 time.sleep(2)
 print('Creating Sitemap......')
 urlset = ET.Element("urlset",xmlns="https://www.sitemaps.org/schemas/sitemap/0.9")
 count = 0
 while count < len(checked_urls):
  today = datetime.datetime.today().strftime('%Y-%M-%D')
  urls = ET.SubElement(urlset,"url")
  ET.SubElement(urls,"loc",).text = str(checked_urls[count])
  ET.SubElement(urls,"lastmod",).text = str(today)
  ET.SubElement(urls,"priority",).text = "1.00"
  count = count + 1
 else:
  tree = ET.ElementTree(urlset)
  tree.write("sitemap.xml")
  sizi()

def sizi():# THIS FOR LIMITING SIZE OF FILE TO 50 Mb
   try:
    global size
    size = open('sitemap.xml')
    global si ,so
    si = os.path.abspath(os.getcwd())
    si = si + "\sitemap.xml"
    so = os.path.getsize(si)
    if so < 52428800 :
     print("sitemap is ready..!         ")
     print("Check a file 'sitemap.xml' in current directory ")
     print('thanks for using my code..')

    else:
     size.truncate(52428800)
     size.close()
     print("your sitemapfile exceed the limit of 50 Mb.")
     print("")
     print("Now the file is equal to 50 Mb")
     print("")
     print("sitemap is ready..!         ")
     print("Check a file 'sitemap.xml' in current directory ")
     print('thanks for using my code..')
   except:
    print("done")
   time.sleep(2)
ask_url()
