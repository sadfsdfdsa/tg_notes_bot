import requests
from bs4 import BeautifulSoup


soup = BeautifulSoup(requests.get('http://spys.one/en/free-proxy-list/').text, features="html.parser")
list1 = soup.findAll('font', {'class': 'spy14'})
print(list1[1])
