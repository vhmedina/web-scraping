# Web Scraping La Tercera
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.latercera.com/resultadoBusqueda.html?q=educacion');
time.sleep(10) # Let's see something before scraping

# Save the links in the following array
links=[]
i=0
while True:
    try:
        # find all url from the actual page
        search_box = driver.find_elements_by_css_selector('h2>a')
        # append the url to links
        for link in search_box:
            links.append(link.get_attribute('href'))
            i=i+1
        # Print the page number
        print(i)
        # Lets go to the next page
        driver.find_element_by_link_text(">").click()
        # Wait a bit
        time.sleep(5)
    except NoSuchElementException:
        print("over")
driver.quit()

# Save links
import csv
csvFile=open("test2.csv",'w+')
writer=csv.writer(csvFile)
writer.writerow(('number','link'))
for i in range(len(links)):
    writer.writerow((i+1,links[i]))
csvFile.close()

# Function to verify if the link is broke or not
def verifica_html(lala):
    from urllib.request import urlopen
    from urllib.request import HTTPError, URLError
    try:
        html=urlopen(lala)
        return True
    except:
        return False

# Extract content from links
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

with open('test2.csv') as csvfile:
    reader=csv.reader(csvfile,delimiter=';')
    i=0
    fecha=[]
    titulo=[]
    contenido=[]
    for row in reader:
        link=row[1]
        if verifica_html(link):
            html=urlopen(link) 
            bsObj=BeautifulSoup(html,"lxml")
            parse0=bsObj.find("i")
            if parse0 is None:
                parse0=bsObj.find("em")
            fecha.append(parse0.text)
            titulo.append(bsObj.find("h1").text)
            frase=""
            parse=bsObj.find("div",{"class":"articleContent"})
            if parse is None:
                parse=bsObj.find("div",{"class":"article-center-text"})
            texto=parse.findAll("p")
            for linea in texto:
                frase=frase+linea.text
            contenido.append(frase)
        i+=1
        if i%100==0:
            print(i)

# Save the content 
import unicodedata
import unicodecsv as csv2
import io

archivo=open("data_latercera.csv",'wb')
writer=csv2.writer(archivo)
writer.writerow(('number','fecha','titulo','contenido'))
for i in range(len(contenido)):
    writer.writerow((i+1,unicodedata.normalize("NFKD", fecha[i]),
    unicodedata.normalize("NFKD", titulo[i]),unicodedata.normalize("NFKD", contenido[i])))
archivo.close()

