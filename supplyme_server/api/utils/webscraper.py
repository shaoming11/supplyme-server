import requests
from bs4 import BeautifulSoup
soup = BeautifulSoup("<p>Some<b>bad<i>HTML", "html.parser")
results = soup.find(id="ResultsContainer")
suppliers = results.find_all("div", class_="text-yeti-abominable-10 hover:underline fill-blue-700 font-bold text-sm")
# text-yeti-abominable-10 hover:underline fill-blue-700 font-bold text-sm